"""Check shared instructions/skills and evaluate their Home Manager wiring.

No activation, downloads of skills, or reads of live agent state. Nix may need
its pinned flake inputs if they are not already in the local store.
"""

import json
import os
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
ALIASES = {".pi/agent/AGENTS.md", ".codex/AGENTS.md"}


class AgentConfigTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.skills = sorted(path for path in SKILLS.iterdir() if path.is_dir())
        host = os.environ.get("DOTFILES_HOST", "dev-laptop")
        result = subprocess.run(
            [
                "nix",
                "eval",
                "--json",
                "--no-write-lock-file",
                f"path:{ROOT}#nixosConfigurations.{host}.config.home-manager.users.gabe",
                "--apply",
                """config: {
                  files = builtins.mapAttrs (_: file: {
                    source = toString file.source;
                    inherit (file) target recursive force;
                  }) (builtins.removeAttrs config.home.file
                    (builtins.filter (name:
                      !(builtins.any (prefix:
                        builtins.substring 0 (builtins.stringLength prefix) name == prefix
                      ) [ ".agents" ".pi" ".codex" ])
                    ) (builtins.attrNames config.home.file)));
                  failures = map (item: item.message)
                    (builtins.filter (item: !item.assertion) config.assertions);
                }""",
            ],
            check=True,
            capture_output=True,
            text=True,
        )
        cls.config = json.loads(result.stdout)
        cls.files = cls.config["files"]

    def test_home_manager_assertions(self):
        self.assertEqual(self.config["failures"], [])

    def test_only_explicit_agent_files_are_managed(self):
        expected = (
            {".agents/AGENTS.md"}
            | ALIASES
            | {f".agents/skills/{path.name}" for path in self.skills}
        )
        self.assertEqual(set(self.files), expected)
        for name, file in self.files.items():
            with self.subTest(name=name):
                self.assertEqual(file["target"], name)
                self.assertFalse(file["recursive"])
                self.assertFalse(file["force"])

    def test_instruction_aliases_share_a_single_source(self):
        sources = {self.files[name]["source"] for name in ALIASES}
        self.assertEqual(len(sources), 1)
        # The aliases use a symlink derivation, not another installed copy.
        self.assertNotIn(self.files[".agents/AGENTS.md"]["source"], sources)
        self.assertTrue((ROOT / ".agents/AGENTS.md").read_text().strip())

    def test_skills_have_portable_metadata_and_are_installed(self):
        self.assertTrue(self.skills)
        for skill in self.skills:
            with self.subTest(skill=skill.name):
                self.assertRegex(skill.name, r"^[a-z0-9]+(-[a-z0-9]+)*$")
                self.assertLessEqual(len(skill.name), 64)
                text = (skill / "SKILL.md").read_text()
                self.assertTrue(text.startswith("---\n"))
                frontmatter, body = text[4:].split("\n---\n", 1)
                name = re.search(r"^name: (.+)$", frontmatter, re.MULTILINE)
                description = re.search(
                    r"^description: (.+)$", frontmatter, re.MULTILINE
                )
                self.assertIsNotNone(name)
                self.assertIsNotNone(description)
                self.assertEqual(name.group(1), skill.name)
                self.assertTrue(description.group(1).strip())
                self.assertLessEqual(len(description.group(1)), 1024)
                self.assertTrue(body.strip())
                source = self.files[f".agents/skills/{skill.name}"]["source"]
                self.assertTrue(source.endswith(f"/.agents/skills/{skill.name}"))

    def test_vendored_skills_do_not_reference_external_symlinks(self):
        for path in SKILLS.rglob("*"):
            if path.is_symlink():
                with self.subTest(path=path):
                    self.assertTrue(path.resolve().is_relative_to(SKILLS.resolve()))
                    self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
