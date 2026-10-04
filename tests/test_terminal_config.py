"""Exercise terminal configuration without touching live sessions or personal files.

Run: python3 tests/test_terminal_config.py
Requires zsh, tmux, ghostty, starship, fzf, and direnv in PATH. Zsh plugins must
be installed by Home Manager, or provided before activation with
CXF_TEST_AUTOSUGGESTIONS_FILE and CXF_TEST_HIGHLIGHTING_DIR (Nix store paths).
All runtime files and the tmux socket are isolated in a temporary directory.
"""

import os
import pty
import re
import select
import shlex
import shutil
import signal
import subprocess
import tempfile
import termios
import time
import unittest
from contextlib import ExitStack
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
DOTFILES = REPO
USER_CONFIG = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))


class TerminalConfigTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="cxf-terminal-")
        self.addCleanup(temporary.cleanup)
        self.home = Path(temporary.name)
        self.config = self.home / ".config"
        self.config.mkdir()
        self.work = self.home / "work tree's [test]"
        self.work.mkdir()
        # Git fixture commands must never inherit a caller's worktree/index paths.
        self.env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        for name in (
            "TMUX",
            "TMUX_PANE",
            "ZDOTDIR",
            "VIRTUAL_ENV",
            "CONDA_DEFAULT_ENV",
            "SSH_CONNECTION",
            "SSH_CLIENT",
            "SSH_TTY",
            "GHOSTTY_SHELL_INTEGRATION",
        ):
            self.env.pop(name, None)
        self.env.update(
            HOME=str(self.home),
            ZDOTDIR=str(self.home),
            XDG_CONFIG_HOME=str(self.config),
            XDG_CACHE_HOME=str(self.home / ".cache"),
            XDG_STATE_HOME=str(self.home / ".local/state"),
            XDG_DATA_HOME=str(self.home / ".local/share"),
            STARSHIP_CONFIG=str(DOTFILES / ".config/starship.toml"),
            STARSHIP_CACHE=str(self.home / ".cache/starship"),
            GIT_CONFIG_GLOBAL="/dev/null",
            GIT_CONFIG_NOSYSTEM="1",
            TERM="xterm-256color",
            PWD=str(self.work),
            STARSHIP_SHELL="zsh",
            SHELL=shutil.which("zsh") or "/bin/sh",
        )

    def command(self, *args, env=None, expected=0):
        with ExitStack() as stack:
            stdin = None
            if args[0] == "zsh" and "-i" in args:
                # ZLE requires terminal input even for an interactive -c command.
                master, stdin = pty.openpty()
                stack.callback(os.close, master)
                stack.callback(os.close, stdin)
            result = subprocess.run(
                args,
                cwd=self.work,
                env=env or self.env,
                text=True,
                stdin=stdin,
                capture_output=True,
                check=False,
                timeout=30,
            )
        self.assertEqual(
            result.returncode, expected, f"{args}\n{result.stdout}\n{result.stderr}"
        )
        return result

    def prepare_zsh(self):
        shutil.copyfile(DOTFILES / ".zshrc", self.home / ".zshrc")
        plugins = self.config / "zsh/plugins"
        plugins.mkdir(parents=True)
        suggestions = Path(
            os.environ.get(
                "CXF_TEST_AUTOSUGGESTIONS_FILE",
                str(USER_CONFIG / "zsh/plugins/zsh-autosuggestions.zsh"),
            )
        )
        highlighting = Path(
            os.environ.get(
                "CXF_TEST_HIGHLIGHTING_DIR",
                str(USER_CONFIG / "zsh/plugins/zsh-syntax-highlighting"),
            )
        )
        self.assertTrue(suggestions.is_file(), f"Missing plugin: {suggestions}")
        self.assertTrue(
            (highlighting / "zsh-syntax-highlighting.zsh").is_file(),
            f"Missing plugin: {highlighting}",
        )
        (plugins / "zsh-autosuggestions.zsh").symlink_to(suggestions)
        (plugins / "zsh-syntax-highlighting").symlink_to(highlighting)

    def test_zsh_noninteractive_source_is_inert(self):
        self.command("zsh", "-n", str(DOTFILES / ".zshrc"))
        result = self.command(
            "zsh",
            "-d",
            "-f",
            "-c",
            """
            EDITOR=untouched
            source "$1" || exit 1
            [[ $EDITOR == untouched ]] || exit 2
            (( ! $+functions[mkcd] )) || exit 3
            print NONINTERACTIVE_OK
        """,
            "zsh",
            str(DOTFILES / ".zshrc"),
        )
        self.assertIn("NONINTERACTIVE_OK", result.stdout)
        self.assertFalse((self.home / ".cache").exists())

    def test_zsh_integrations_and_local_override(self):
        self.prepare_zsh()
        (self.home / ".zshrc.local").write_text("export CXF_LOCAL_LOADED=yes\n")
        result = self.command(
            "zsh",
            "-d",
            "-i",
            "-c",
            """
            [[ $CXF_LOCAL_LOADED == yes && $EDITOR == nvim ]] || exit 1
            [[ $HISTFILE == $HOME/.zsh_history && $SAVEHIST == 100000 ]] || exit 2
            [[ -o sharehistory && -o histignorespace ]] || exit 3
            (( $+functions[compdef] && $+functions[_direnv_hook] )) || exit 4
            (( $+functions[_zsh_autosuggest_start] && $+functions[_zsh_highlight] )) || exit 5
            (( $+functions[starship_zle-keymap-select] )) || exit 6
            [[ $(bindkey -M viins '^R') == *fzf-history-widget* ]] || exit 7
            [[ $(bindkey -M viins '^@') == *autosuggest-accept* ]] || exit 8
            [[ $(bindkey -M viins '^X^E') == *edit-command-line* ]] || exit 9
            mkcd "directory with spaces" || exit 10
            [[ $PWD == */'directory with spaces' ]] || exit 11
            mkcd >/dev/null 2>&1 && exit 12
            print INTERACTIVE_OK
        """,
        )
        self.assertIn("INTERACTIVE_OK", result.stdout)
        self.assertEqual(result.stderr, "")

    def test_croot_handles_worktrees_and_failure(self):
        self.prepare_zsh()
        self.command("git", "init", "--quiet")
        result = self.command(
            "zsh",
            "-d",
            "-i",
            "-c",
            """
            root=$PWD
            mkcd nested/deeper || exit 1
            croot || exit 2
            [[ $PWD == $root ]] || exit 3
            cd "$HOME"
            croot >/dev/null 2>&1 && exit 4
            [[ $PWD == $HOME ]] || exit 5
            print CROOT_OK
        """,
        )
        self.assertIn("CROOT_OK", result.stdout)
        self.assertEqual(result.stderr, "")

    def starship_text(self, *args, env=None, preserve_whitespace=False):
        result = self.command("starship", *args, env=env)
        self.assertEqual(result.stderr, "")
        plain = re.sub(r"\x1b\[[0-9;]*m", "", result.stdout)
        plain = plain.replace("%{", "").replace("%}", "")
        return plain.strip("\n") if preserve_whitespace else plain.strip()

    def prepare_git(self, *files):
        self.command("git", "init", "--quiet", "--initial-branch=main")
        self.command("git", "config", "user.name", "CXF test")
        self.command("git", "config", "user.email", "test@example.invalid")
        for name in files:
            (self.work / name).write_text(f"{name}\n")
        self.command("git", "add", "--", *files)
        self.command("git", "commit", "--quiet", "-m", "Fixture baseline")

    def test_starship_prompt_states(self):
        # Only exceptional context remains: no routine environment labels.
        env = self.env | {
            "IN_NIX_SHELL": "impure",
            "VIRTUAL_ENV": str(self.home / "venv"),
        }
        for keymap, symbol in (("viins", "❯"), ("vicmd", "❮")):
            plain = self.starship_text(
                "prompt",
                "--status",
                "1",
                "--keymap",
                keymap,
                "--cmd-duration",
                "12000",
                "--jobs",
                "2",
                env=env,
            )
            self.assertTrue(plain.endswith(symbol), plain)
            self.assertIn("12s", plain)
            self.assertIn("jobs:2", plain)
            for absent in ("nix:", "venv:", "took"):
                self.assertNotIn(absent, plain)
        short = self.starship_text("prompt", "--cmd-duration", "3000")
        self.assertNotIn("3s", short)
        self.assertNotIn("jobs:", short)

    def test_starship_clock_is_in_context_row_only(self):
        self.assertEqual(self.starship_text("prompt", "--right"), "")
        plain = self.starship_text("prompt", preserve_whitespace=True)
        context, prompt = plain.splitlines()
        self.assertRegex(context, r" (?:[01]\d|2[0-3]):[0-5]\d $")
        self.assertEqual(prompt, "❯ ")
        self.assertTrue(context.startswith(" ~/"))
        # Only the clock's inner boundary is rounded; the outer edges are flat.
        self.assertEqual(context.count(""), 1)
        self.assertNotIn("", context)
        self.assertNotIn("", context)
        self.assertNotIn("│", context)

    def test_zsh_renders_clock_above_input(self):
        self.prepare_zsh()
        self.prepare_git("modified")
        (self.work / "modified").write_text("changed\n")
        (self.work / "untracked").write_text("new\n")
        # Exercise the real Zsh prompt, including a terminal narrow enough to
        # wrap the context row. The clock must never reappear alongside input.
        for columns in (40, 60, 120):
            with self.subTest(columns=columns):
                pid, fd = pty.fork()
                if pid == 0:
                    termios.tcsetwinsize(0, (24, columns))
                    os.chdir(self.work)
                    os.execvpe("zsh", ["zsh", "-d", "-i"], self.env)
                output = b""
                try:
                    deadline = time.monotonic() + 15
                    while time.monotonic() < deadline:
                        if not select.select([fd], [], [], 0.2)[0]:
                            continue
                        output += os.read(fd, 65536)
                        if b"\x1b[?2004h" in output:  # ZLE is ready for input.
                            break
                    self.assertIn(b"\x1b[?2004h", output)
                    plain = re.sub(
                        r"\x1b\[[0-?]*[ -/]*[@-~]", "", output.decode()
                    ).replace("\r", "")
                    context, prompt = plain.splitlines()[-2:]
                    self.assertRegex(context, r" (?:[01]\d|2[0-3]):[0-5]\d $")
                    self.assertEqual(prompt, "❯ ")
                    if columns >= 60:
                        self.assertEqual(len(context), columns)
                    else:
                        self.assertGreater(len(context), columns)
                finally:
                    try:
                        os.kill(pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                    os.waitpid(pid, 0)
                    os.close(fd)

    def test_starship_directory_keeps_parent_and_nested_paths(self):
        self.work = self.home / "Projects/cxf"
        self.work.mkdir(parents=True)
        self.env["PWD"] = str(self.work)
        self.prepare_git("baseline")
        self.assertEqual(self.starship_text("module", "directory"), "~/Projects/cxf")
        nested = self.work / "foundry/python/src/foundry/math"
        nested.mkdir(parents=True)
        prompt = self.starship_text(
            "prompt", "--path", str(nested), "--logical-path", str(nested)
        )
        self.assertIn("~/Projects/cxf/foundry/python/src/foundry/math", prompt)
        # Outside HOME, show an absolute path rather than a misleading '~'.
        with tempfile.TemporaryDirectory(prefix="cxf-external-") as outside:
            prompt = self.starship_text(
                "prompt", "--path", outside, "--logical-path", outside
            )
            self.assertIn(outside, prompt)

    def test_starship_context_row_fills_width(self):
        for in_git in (False, True):
            if in_git:
                self.prepare_git("modified")
                (self.work / "modified").write_text("changed\n")
                (self.work / "untracked").write_text("new\n")
            for columns in (80, 120):
                with self.subTest(in_git=in_git, columns=columns):
                    args = ("prompt", "--terminal-width", str(columns))
                    plain = self.starship_text(*args, preserve_whitespace=True)
                    context, prompt = plain.splitlines()
                    # Fixture text and the Nerd Font separator are single-cell.
                    self.assertEqual(len(context), columns)
                    self.assertTrue(context.startswith(" ~/work tree's [test] "))
                    self.assertRegex(context, r" (?:[01]\d|2[0-3]):[0-5]\d $")
                    self.assertEqual(plain.count(""), 1)
                    self.assertNotIn("", plain)
                    self.assertEqual(prompt, "❯ ")
                    if in_git:
                        self.assertIn("│  main │ work ~1 │ new 1 ", context)
                    else:
                        self.assertNotIn("│", context)
                    for glyph in ("", "", "", "", "", "", "", "", ""):
                        self.assertNotIn(glyph, plain)
                    self.assert_context_background(
                        self.command("starship", *args).stdout
                    )

        # Include the conditional remote identity, duration, and job segments.
        result = self.command(
            "starship",
            "prompt",
            "--terminal-width",
            "160",
            "--cmd-duration",
            "12000",
            "--jobs",
            "2",
            env=self.env | {"SSH_CONNECTION": "127.0.0.1 1234 127.0.0.1 22"},
        )
        self.assertEqual(result.stderr, "")
        self.assertIn("12s", result.stdout)
        self.assertIn("jobs:2", result.stdout)
        self.assertIn("@", result.stdout)
        self.assert_context_background(result.stdout)

    def test_starship_context_row_wraps_without_losing_context(self):
        self.prepare_git("modified")
        (self.work / "modified").write_text("changed\n")
        (self.work / "untracked").write_text("new\n")
        previous = None
        for columns in (20, 40):
            args = ("prompt", "--terminal-width", str(columns))
            plain = self.starship_text(*args)
            context, prompt = plain.splitlines()
            self.assertGreater(len(context), columns)
            self.assertIn("~/work tree's [test] │  main │ work ~1 │ new 1", context)
            self.assertEqual(prompt, "❯")
            # Normalize the render-time clock so minute boundaries cannot flake.
            normalized = re.sub(r"\d{2}:\d{2}", "HH:MM", context)
            if previous is not None:
                self.assertEqual(normalized, previous)  # Minimum padding remains.
            previous = normalized
            self.assert_context_background(self.command("starship", *args).stdout)

    def assert_context_background(self, rendered):
        # Check every rendered cell, including spaces and directory segments:
        # top-level styles do not propagate into modules and can leave holes.
        rendered = rendered.replace("%{", "").replace("%}", "")
        background = foreground = None
        rows = [[]]
        for token in re.split(r"(\x1b\[[0-9;]*m)", rendered):
            if token.startswith("\x1b["):
                codes = iter(int(code or "0") for code in token[2:-1].split(";"))
                for code in codes:
                    if code in (38, 48):
                        mode = next(codes)
                        color = tuple(next(codes) for _ in range(3 if mode == 2 else 1))
                        if code == 48:
                            background = color
                        else:
                            foreground = color
                    else:
                        if code in (0, 49):
                            background = None
                        if code in (0, 39):
                            foreground = None
                continue
            for char in token:
                if char == "\n":
                    rows.append([])
                else:
                    rows[-1].append((char, background, foreground))
        context, prompt = [row for row in rows if row]
        text = "".join(cell[0] for cell in context)
        boundary = text.index("")
        self.assertEqual(text.count(""), 1)
        self.assertNotIn("", text)
        self.assertEqual(context[0][0], " ")
        self.assertEqual(context[-1][0], " ")
        for _, background, _ in context[: boundary + 1]:
            self.assertEqual(background, (37, 37, 54))
        # The clock's rounded transition sits on the divider, not terminal base.
        self.assertEqual(context[boundary][2], (49, 50, 68))
        for _, background, _ in context[boundary + 1 :]:
            self.assertEqual(background, (49, 50, 68))
        for _, background, _ in prompt:
            self.assertIsNone(background)

    def test_starship_git_counts_separate_index_and_worktree(self):
        self.prepare_git(
            "staged", "unstaged", "staged-delete", "unstaged-delete", "partial"
        )
        self.assertEqual(self.starship_text("module", "git_status"), "")
        self.assertEqual(self.starship_text("module", "git_branch"), "│  main")
        self.assertIn("│  main ", self.starship_text("prompt"))
        for name in ("added", "staged", "partial"):
            (self.work / name).write_text("staged content\n")
        self.command("git", "add", "--", "added", "staged", "partial")
        self.command("git", "rm", "--quiet", "staged-delete")
        for name in ("unstaged", "partial"):
            (self.work / name).write_text("unstaged content\n")
        (self.work / "unstaged-delete").unlink()
        for name in ("new-one", "new-two"):
            (self.work / name).write_text("untracked\n")
        self.assertEqual(
            self.starship_text("module", "git_status"),
            "│ staged +1 ~2 -1 │ work ~2 -1 │ new 2",
        )
        self.command("git", "stash", "push", "--quiet", "--include-untracked")
        self.assertEqual(self.starship_text("module", "git_status"), "│ stash 1")

    def test_starship_renames_and_type_changes(self):
        self.prepare_git("old", "typed")
        self.command("git", "mv", "old", "new")
        self.assertEqual(self.starship_text("module", "git_status"), "│ staged r1")
        (self.work / "typed").unlink()
        (self.work / "typed").symlink_to("new")
        self.assertEqual(
            self.starship_text("module", "git_status"), "│ staged r1 │ work t1"
        )
        self.command("git", "add", "typed")
        self.assertEqual(self.starship_text("module", "git_status"), "│ staged t1 r1")

    def test_starship_conflict_count(self):
        self.prepare_git("conflict")
        self.command("git", "switch", "--quiet", "-c", "other")
        (self.work / "conflict").write_text("other side\n")
        self.command("git", "commit", "--quiet", "-am", "Other change")
        self.command("git", "switch", "--quiet", "main")
        (self.work / "conflict").write_text("main side\n")
        self.command("git", "commit", "--quiet", "-am", "Main change")
        self.command("git", "merge", "--no-edit", "other", expected=1)
        self.assertIn("conflict 1", self.starship_text("module", "git_status"))

    def test_starship_divergence_and_detached_head(self):
        self.prepare_git("baseline")
        baseline = self.command("git", "rev-parse", "HEAD").stdout.strip()
        self.command("git", "commit", "--quiet", "--allow-empty", "-m", "Local change")
        self.command("git", "switch", "--quiet", "-c", "upstream", baseline)
        for number in range(2):
            self.command(
                "git", "commit", "--quiet", "--allow-empty", "-m", f"Remote {number}"
            )
        # Local tracking refs only: no network requests in this fixture.
        self.command("git", "update-ref", "refs/remotes/origin/main", "HEAD")
        self.command("git", "remote", "add", "origin", str(self.home / "upstream.git"))
        self.command("git", "switch", "--quiet", "main")
        self.command("git", "branch", "--set-upstream-to=origin/main")
        self.assertEqual(self.starship_text("module", "git_status"), "│ ↑1 ↓2")
        self.command("git", "switch", "--quiet", "--detach")
        commit = self.command("git", "rev-parse", "--short=7", "HEAD").stdout.strip()
        prompt = self.starship_text("prompt")
        self.assertIn(f"│ @{commit} ", prompt)
        self.assertNotIn("", prompt)
        self.assertEqual(self.starship_text("module", "git_branch"), "")

    def test_ghostty_configuration_and_application_keys(self):
        target = self.config / "ghostty"
        shutil.copytree(DOTFILES / ".config/ghostty", target)
        validation = self.command("ghostty", "+validate-config")
        self.assertEqual(validation.stdout + validation.stderr, "")
        rendered = self.command(
            "ghostty", "+show-config", "--changes-only=false"
        ).stdout
        self.assertIn("theme = Catppuccin Mocha", rendered)
        for setting in (
            "window-padding-x = 0",
            "window-padding-y = 0",
            "window-padding-balance = true",
            "window-padding-color = extend",
        ):
            self.assertIn(setting, rendered.splitlines())
        self.assertIn("clipboard-read = ask", rendered)
        self.assertIn("shell-integration-features =", rendered)
        self.assertIn("keybind = ctrl+alt+f=toggle_fullscreen", rendered)
        self.assertNotIn("keybind = ctrl+enter=", rendered)
        self.assertNotIn("keybind = ctrl+shift+enter=", rendered)
        (target / "local.ghostty").write_text("font-size = 15\n")
        rendered = self.command("ghostty", "+show-config").stdout
        self.assertIn("font-size = 15", rendered)

    def test_tmux_runtime_and_directory_inheritance(self):
        target = self.config / "tmux"
        shutil.copytree(DOTFILES / ".config/tmux", target)
        (target / "local.conf").write_text("set -g @cxf-local loaded\n")
        socket = str(self.home / "tmux.sock")
        tmux = ["tmux", "-S", socket]

        # Never connect to or reload a developer's real tmux server.
        def cleanup():
            subprocess.run(
                tmux + ["kill-server"],
                env=self.env,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=10,
            )

        self.addCleanup(cleanup)
        self.command(
            *tmux,
            "-f",
            str(target / "tmux.conf"),
            "new-session",
            "-d",
            "-s",
            "test",
            "-c",
            str(self.work),
            "sleep 120",
        )
        # source-file reports parse errors directly, including during reload.
        self.command(*tmux, "source-file", str(target / "tmux.conf"))
        for option, value in (
            ("prefix", "C-a"),
            ("extended-keys", "on"),
            ("extended-keys-format", "csi-u"),
            ("set-clipboard", "external"),
            ("@cxf-local", "loaded"),
        ):
            self.assertEqual(
                self.command(
                    *tmux,
                    "show-options",
                    "-sv"
                    if option
                    in ("extended-keys", "extended-keys-format", "set-clipboard")
                    else "-gv",
                    option,
                ).stdout.strip(),
                value,
            )
        self.assertEqual(
            self.command(
                *tmux, "display-message", "-p", "#{window_index}"
            ).stdout.strip(),
            "1",
        )

        # Expand the actual status formats, including nested dynamic colors.
        left = self.command(*tmux, "display-message", "-p", "#{E:status-left}").stdout
        right = self.command(*tmux, "display-message", "-p", "#{T:status-right}").stdout
        current = self.command(
            *tmux, "display-message", "-p", "#{E:window-status-current-format}"
        ).stdout
        for segment in (left, right, current):
            self.assertNotIn("#{", segment)
        # Only inner boundaries are rounded. The first and last spaces carry
        # the segment background all the way to the terminal's outer edges.
        self.assertTrue(left.startswith("#[fg=#1e1e2e,bg=#89b4fa,bold] "))
        self.assertNotIn("", left)
        self.assertIn("", left)
        self.assertRegex(
            right, r"#\[fg=#1e1e2e,bg=#89b4fa,bold\] \d{2}:\d{2} #\[default\]\n$"
        )
        self.assertIn("", right)
        self.assertNotIn("", right)
        self.assertIn("", current)
        self.assertIn("", current)
        self.assertIn("#89b4fa", left)
        self.assertNotIn("COPY", left)
        self.assertRegex(right, r"\d{2}:\d{2}")
        self.command(*tmux, "copy-mode")
        copy_status = self.command(
            *tmux, "display-message", "-p", "#{E:status-left}"
        ).stdout
        self.assertIn("test : COPY", copy_status)
        self.assertIn("#f9e2af", copy_status)
        self.command(*tmux, "send-keys", "-X", "cancel")

        def binding_args(table, key):
            bindings = self.command(*tmux, "list-keys", "-T", table).stdout
            for line in bindings.splitlines():
                parts = shlex.split(line)
                start = parts.index(table) + 1
                if parts[start] == key:
                    return parts[start + 1 :]
            self.fail(f"Missing binding: {table} {key}")

        for key, operation in (
            ("|", "split-window"),
            ("-", "split-window"),
            ("c", "new-window"),
        ):
            args = binding_args("prefix", key)
            self.assertEqual(args[0], operation)
            self.assertIn("#{pane_current_path}", args)
            self.command(*tmux, *args, "sleep 120")
            directory = self.command(
                *tmux, "display-message", "-p", "#{pane_current_path}"
            ).stdout.strip()
            self.assertEqual(directory, str(self.work))
        self.assertIn("copy-selection-and-cancel", binding_args("copy-mode-vi", "y"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
