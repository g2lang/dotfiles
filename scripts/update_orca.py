"""Update only the Orca package pin; never build, activate, or run the AppImage."""

import argparse
import base64
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.request import Request, urlopen

REPO = "https://github.com/stablyai/orca"
API = "https://api.github.com/repos/stablyai/orca/releases"
PACKAGE = Path(__file__).resolve().parents[1] / "pkgs/orca-ide.nix"
VERSION = re.compile(r'^  version = "(\d+\.\d+\.\d+)";$', re.MULTILINE)
HASH = re.compile(r'^    sha256 = "([0-9a-f]{64})";$', re.MULTILINE)


def fetch_release(selector):
    if selector == "latest":
        endpoint = "latest"
    else:
        version = selector.removeprefix("v")
        if not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("Use 'latest' or a stable version such as 1.4.229")
        endpoint = f"tags/v{version}"
    request = Request(
        f"{API}/{endpoint}",
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "dotfiles-update-orca",
        },
    )
    with urlopen(request, timeout=30) as response:
        return json.load(response)


def release_asset(release, selector):
    tag = release.get("tag_name", "")
    if (
        release.get("draft")
        or release.get("prerelease")
        or not re.fullmatch(r"v\d+\.\d+\.\d+", tag)
    ):
        raise ValueError("Expected a published stable Orca release")
    version = tag[1:]
    if selector != "latest" and selector.removeprefix("v") != version:
        raise ValueError("GitHub returned a different release than requested")
    assets = [
        asset
        for asset in release.get("assets", [])
        if asset.get("name") == "orca-linux.AppImage"
    ]
    if len(assets) != 1:
        raise ValueError("Expected exactly one x86-64 orca-linux.AppImage asset")
    asset = assets[0]
    url = f"{REPO}/releases/download/{tag}/orca-linux.AppImage"
    if asset.get("browser_download_url") != url:
        raise ValueError("Unexpected AppImage download URL")
    digest = asset.get("digest") or ""
    if not re.fullmatch(r"sha256:[0-9a-f]{64}", digest):
        raise ValueError("Release asset is missing a valid published SHA-256 digest")
    return version, url, digest.removeprefix("sha256:")


def prefetch(url):
    result = subprocess.run(
        ["nix", "store", "prefetch-file", "--hash-type", "sha256", "--json", url],
        check=True,
        capture_output=True,
        text=True,
    )
    sri = json.loads(result.stdout)["hash"]
    if not sri.startswith("sha256-"):
        raise ValueError("Nix returned an unexpected hash type")
    digest = base64.b64decode(sri.removeprefix("sha256-"), validate=True)
    if len(digest) != 32:
        raise ValueError("Nix returned an invalid SHA-256 hash")
    return digest.hex()


def update(package, selector):
    original = package.read_text()
    versions, hashes = VERSION.findall(original), HASH.findall(original)
    if len(versions) != 1 or len(hashes) != 1:
        raise ValueError("Package must contain exactly one version and SHA-256 pin")
    version, url, published_hash = release_asset(fetch_release(selector), selector)
    if version == versions[0] and published_hash == hashes[0]:
        print(f"Orca is already pinned to {version}; no changes.")
        return

    print(f"Fetching Orca {version} to verify its checksum…", flush=True)
    digest = prefetch(url)
    if digest != published_hash:
        raise ValueError("Downloaded AppImage does not match GitHub's published digest")
    updated = VERSION.sub(f'  version = "{version}";', original)
    updated = HASH.sub(f'    sha256 = "{digest}";', updated)
    if package.read_text() != original:
        raise ValueError("Package changed during download; refusing to overwrite it")

    # Replace atomically only after all network and checksum checks have succeeded.
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", dir=package.parent, delete=False
        ) as f:
            temporary = Path(f.name)
            f.write(updated)
        temporary.chmod(package.stat().st_mode & 0o777)
        temporary.replace(package)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)
    print(f"Updated {package}: {versions[0]} -> {version}")
    print(
        "Review the package diff. No build, activation, or flake.lock update was run."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("version", nargs="?", default="latest")
    args = parser.parse_args()
    try:
        update(PACKAGE, args.version)
    except (
        OSError,
        ValueError,
        KeyError,
        TypeError,
        subprocess.CalledProcessError,
    ) as error:
        print(f"Orca update failed: {error}", file=sys.stderr)
        if isinstance(error, subprocess.CalledProcessError) and error.stderr:
            print(error.stderr, file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
