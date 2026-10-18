"""Check shared instructions/skills and evaluate their Home Manager wiring.

No activation, downloads of skills, or reads of live agent state. Nix may need
its pinned flake inputs if they are not already in the local store.
"""

import json
import os
import re
import subprocess
import tempfile
import unittest
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SKILLS = ROOT / ".agents/skills"
ALIASES = {".pi/agent/AGENTS.md", ".codex/AGENTS.md"}


def metadata_field(text, key):
    """Read the scalar and folded fields used by this collection's metadata."""
    match = re.search(rf"^ *{re.escape(key)}: *(.*)$", text, re.MULTILINE)
    if not match:
        return None
    value = match.group(1).strip()
    if value in {">", ">-", "|", "|-"}:
        lines = []
        for line in text[match.end() :].splitlines()[1:]:
            if not line.startswith(" "):
                break
            lines.append(line.strip())
        return " ".join(lines)
    return value.strip("\"'")


def local_link_problems(root):
    """Validate local inline Markdown links, excluding fenced examples and URLs."""
    problems = []
    for path in root.rglob("*.md"):
        text = re.sub(r"```.*?```|~~~.*?~~~", "", path.read_text(), flags=re.DOTALL)
        for target in re.findall(r"\[[^\]\n]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", text):
            parsed = urlsplit(target)
            if parsed.scheme == "file":
                problems.append(f"{path.relative_to(root)}: nonportable {target}")
                continue
            if parsed.scheme or parsed.netloc or not parsed.path:
                continue
            relative = Path(unquote(parsed.path))
            local = path.parent / relative
            if relative.is_absolute() or not local.resolve().is_relative_to(
                root.resolve()
            ):
                problems.append(f"{path.relative_to(root)}: nonportable {target}")
            elif not local.exists():
                problems.append(f"{path.relative_to(root)}: missing {target}")
    return problems


def unsupported_tool_assumptions(root):
    patterns = (
        r"\bTask tool\b",
        r"\bSkill tool\b",
        r"\bsubagent_type\s*[:=]",
        r"\brun_in_background\s*[:=]",
        r"\.cursor/",
        r"pstack-models\.mdc",
        r"\bclaude-opus-\d",
        r"\bgrok-\d",
    )
    problems = []
    for path in root.rglob("*.md"):
        for number, line in enumerate(path.read_text().splitlines(), 1):
            if any(re.search(pattern, line) for pattern in patterns):
                problems.append(f"{path.relative_to(root)}:{number}: {line.strip()}")
    return problems


class SkillContractTests(unittest.TestCase):
    def test_local_references_resolve(self):
        self.assertEqual(local_link_problems(ROOT / ".agents"), [])

    def test_no_unsupported_tool_assumptions(self):
        self.assertEqual(unsupported_tool_assumptions(SKILLS), [])

    def test_link_checker_catches_missing_dependency(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text("Read [dependency](missing/SKILL.md).\n")
            self.assertEqual(len(local_link_problems(root)), 1)
            (root / "missing").mkdir()
            (root / "missing/SKILL.md").write_text("# Reference\n")
            self.assertEqual(local_link_problems(root), [])

    def test_link_checker_handles_anchors_urls_and_examples(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "SKILL.md").write_text(
                "[self](#section) [web](https://example.com/missing.md)\n"
                "```md\n[example](not-a-real-path.md)\n```\n"
                "[reference](a%20reference.md#heading)\n"
            )
            (root / "a reference.md").write_text("# Heading\n")
            self.assertEqual(local_link_problems(root), [])

    def test_link_checker_rejects_nonportable_paths(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory) / "skills"
            root.mkdir()
            outside = Path(directory) / "outside.md"
            outside.write_text("# Exists locally, but is not installed\n")
            for target in ("../outside.md", str(outside), outside.as_uri()):
                with self.subTest(target=target):
                    (root / "SKILL.md").write_text(f"[dependency]({target})\n")
                    self.assertIn("nonportable", local_link_problems(root)[0])

    def test_tool_checker_rejects_each_retired_assumption(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            file = root / "SKILL.md"
            for instruction in (
                "Call the Task tool",
                "Call the Skill tool",
                "subagent_type: generalPurpose",
                "run_in_background: true",
                "Write .cursor/skills/check/SKILL.md",
                "Read pstack-models.mdc",
                "model: claude-opus-5-5-xhigh",
                "model: grok-4.7-xhigh-fast",
            ):
                with self.subTest(instruction=instruction):
                    file.write_text(instruction)
                    self.assertEqual(len(unsupported_tool_assumptions(root)), 1)
            file.write_text(
                "Read the installed Orca guide and use configured defaults."
            )
            self.assertEqual(unsupported_tool_assumptions(root), [])

    def test_metadata_reader_handles_folded_descriptions(self):
        self.assertEqual(
            metadata_field(
                "description: >-\n  First line\n  second line\nname: x\n", "description"
            ),
            "First line second line",
        )
        self.assertEqual(metadata_field('name: "example"\n', "name"), "example")
        self.assertIsNone(metadata_field("name: x\n", "missing"))

    def test_invocation_policies_agree(self):
        for skill in sorted(SKILLS.iterdir()):
            if not skill.is_dir():
                continue
            with self.subTest(skill=skill.name):
                text = (skill / "SKILL.md").read_text()
                frontmatter = text[4:].split("\n---\n", 1)[0]
                flag = metadata_field(frontmatter, "disable-model-invocation")
                self.assertIn(flag, (None, "true", "false"))
                disabled = flag == "true"
                policy = skill / "agents/openai.yaml"
                if disabled:
                    self.assertTrue(
                        policy.is_file(), "Explicit commands need matching Codex policy"
                    )
                if policy.is_file():
                    implicit = metadata_field(
                        policy.read_text(), "allow_implicit_invocation"
                    )
                    self.assertIn(implicit, (None, "true", "false"))
                    self.assertEqual(implicit != "false", not disabled)
                if (
                    skill.name.startswith("principle-")
                    or skill.name == "benchmark-checklist"
                ):
                    self.assertFalse(
                        disabled,
                        "Engineering references must be automatically selectable",
                    )

    def test_procedures_remain_explicit(self):
        for name in (
            "architect",
            "interrogate",
            "implement-spec",
            "correct",
            "create-verification-skill",
            "to-spec",
            "to-tickets",
            "grill-me",
            "grill-with-docs",
            "handoff-note",
            "blast-radius",
        ):
            with self.subTest(skill=name):
                text = (SKILLS / name / "SKILL.md").read_text()
                self.assertEqual(
                    metadata_field(
                        text.split("\n---\n", 1)[0], "disable-model-invocation"
                    ),
                    "true",
                )
        self.assertFalse((SKILLS / "handoff").exists())


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
                name = metadata_field(frontmatter, "name")
                description = metadata_field(frontmatter, "description")
                self.assertEqual(name, skill.name)
                self.assertTrue(description)
                self.assertLessEqual(len(description), 1024)
                self.assertTrue(body.strip())
                source = self.files[f".agents/skills/{skill.name}"]["source"]
                self.assertTrue(source.endswith(f"/.agents/skills/{skill.name}"))

    def test_references_resolve_in_the_nix_store_source(self):
        source = Path(self.files[".agents/skills/orchestration"]["source"])
        installed_agents = source.parent.parent
        self.assertEqual(local_link_problems(installed_agents), [])
        self.assertTrue((source / "references/workflow-policy.md").is_file())

    def test_vendored_skills_do_not_reference_external_symlinks(self):
        for path in SKILLS.rglob("*"):
            if path.is_symlink():
                with self.subTest(path=path):
                    self.assertTrue(path.resolve().is_relative_to(SKILLS.resolve()))
                    self.assertTrue(path.exists())


if __name__ == "__main__":
    unittest.main()
