"""Offline updater regression tests; no real network, Nix calls, or package edits."""

import base64
import copy
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from scripts import update_orca as updater


class UpdateOrcaTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.package = Path(temporary.name) / "orca-ide.nix"
        self.original = updater.PACKAGE.read_text()
        self.package.write_text(self.original)
        self.version = "99.0.1"
        self.digest = "ab" * 32
        self.url = (
            f"{updater.REPO}/releases/download/v{self.version}/orca-linux.AppImage"
        )
        self.release = {
            "tag_name": f"v{self.version}",
            "draft": False,
            "prerelease": False,
            "assets": [
                {
                    "name": "orca-linux.AppImage",
                    "browser_download_url": self.url,
                    "digest": f"sha256:{self.digest}",
                }
            ],
        }

    def run_update(self, digest=None, selector="latest"):
        with (
            patch.object(updater, "fetch_release", return_value=self.release),
            patch.object(
                updater, "prefetch", return_value=digest or self.digest
            ) as fetch,
        ):
            updater.update(self.package, selector)
        return fetch

    def test_update_changes_only_version_and_hash(self):
        fetch = self.run_update(selector=self.version)
        expected = updater.VERSION.sub(f'  version = "{self.version}";', self.original)
        expected = updater.HASH.sub(f'    sha256 = "{self.digest}";', expected)
        self.assertEqual(self.package.read_text(), expected)
        fetch.assert_called_once_with(self.url)
        self.assertEqual(list(self.package.parent.iterdir()), [self.package])

    def test_same_pin_does_not_download_or_write(self):
        self.release["tag_name"] = "v" + updater.VERSION.findall(self.original)[0]
        self.release["assets"][0].update(
            browser_download_url=(
                f"{updater.REPO}/releases/download/{self.release['tag_name']}/orca-linux.AppImage"
            ),
            digest="sha256:" + updater.HASH.findall(self.original)[0],
        )
        before = self.package.stat().st_mtime_ns
        self.run_update().assert_not_called()
        self.assertEqual(self.package.stat().st_mtime_ns, before)

    def test_checksum_mismatch_preserves_package(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            self.run_update(digest="cd" * 32)
        self.assertEqual(self.package.read_text(), self.original)

    def test_network_and_prefetch_failures_preserve_package(self):
        for operation in ("fetch_release", "prefetch"):
            with self.subTest(operation=operation):
                with (
                    patch.object(updater, "fetch_release", return_value=self.release),
                    patch.object(updater, operation, side_effect=OSError("offline")),
                    self.assertRaises(OSError),
                ):
                    updater.update(self.package, "latest")
                self.assertEqual(self.package.read_text(), self.original)

    def test_rejects_bad_release_metadata(self):
        cases = []
        for key in ("draft", "prerelease"):
            release = copy.deepcopy(self.release)
            release[key] = True
            cases.append(release)
        for key, value in (
            ("name", "orca-linux-arm64.AppImage"),
            ("digest", None),
            ("browser_download_url", "https://example.com/other.AppImage"),
        ):
            release = copy.deepcopy(self.release)
            release["assets"][0][key] = value
            cases.append(release)
        for release in cases:
            with self.subTest(release=release), self.assertRaises(ValueError):
                updater.release_asset(release, "latest")
        with self.assertRaisesRegex(ValueError, "different release"):
            updater.release_asset(self.release, "1.0.0")

    def test_unexpected_package_format_fails_before_network(self):
        self.package.write_text(self.original + '\n  version = "1.0.0";\n')
        with (
            patch.object(updater, "fetch_release") as fetch,
            self.assertRaisesRegex(ValueError, "exactly one"),
        ):
            updater.update(self.package, "latest")
        fetch.assert_not_called()

    def test_concurrent_edit_is_preserved(self):
        def concurrent_edit(url):
            self.package.write_text(self.original + "# user edit\n")
            return self.digest

        with (
            patch.object(updater, "fetch_release", return_value=self.release),
            patch.object(updater, "prefetch", side_effect=concurrent_edit),
            self.assertRaisesRegex(ValueError, "changed during download"),
        ):
            updater.update(self.package, "latest")
        self.assertEqual(self.package.read_text(), self.original + "# user edit\n")

    def test_prefetch_parses_sri_and_passes_url_as_argument(self):
        sri = "sha256-" + base64.b64encode(bytes.fromhex(self.digest)).decode()
        result = subprocess.CompletedProcess([], 0, json.dumps({"hash": sri}), "")
        with patch.object(updater.subprocess, "run", return_value=result) as run:
            self.assertEqual(updater.prefetch(self.url), self.digest)
        self.assertEqual(
            run.call_args.args[0],
            [
                "nix",
                "store",
                "prefetch-file",
                "--hash-type",
                "sha256",
                "--json",
                self.url,
            ],
        )

    def test_invalid_version_does_not_contact_github(self):
        with patch.object(updater, "urlopen") as request, self.assertRaises(ValueError):
            updater.fetch_release("../../bad")
        request.assert_not_called()


if __name__ == "__main__":
    unittest.main()
