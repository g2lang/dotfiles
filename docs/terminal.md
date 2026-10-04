# Gabe's terminal environment

Home Manager installs the terminal configuration and its dependencies. This is the laptop's managed configuration, not the future devbox seed-once implementation. Nothing automatically attaches tmux, starts a network service, or downloads shell plugins at startup.

## Everyday controls

### tmux

The status bar matches Neovim's lualine: Mocha segments for the session, active window, host, and time, with flat outer edges flush against the terminal and rounded inner boundaries. The session segment turns yellow and shows `PREFIX` or `COPY` when active; `[Z]` marks a zoomed window. Git details remain in the prompt rather than being polled by tmux.

The prefix remains **Ctrl-a**. Press it, release it, then use:

| Key | Action |
| --- | --- |
| `|` / `-` | Split right / down in the current directory |
| `c` | New window in the current directory |
| `h`, `j`, `k`, `l` | Select a pane |
| `H`, `J`, `K`, `L` | Resize a pane; repeat without immediately pressing the prefix again |
| `z` | Zoom/unzoom the pane |
| `s` / `w` | Choose a session / window |
| `g` | Open lazygit in a popup; quit lazygit to close it |
| `[` | Enter vi copy mode; `v` selects, `y` or Enter copies, `q` exits |
| `r` / `?` | Reload configuration / show keybinding help |

Copying uses the outer terminal's OSC 52 clipboard support, including over SSH. The terminal must permit clipboard writes. Existing modified-key support is retained for applications such as pi. Sessions survive client disconnection, not container replacement or host failure.

### Zsh

- Vi editing remains enabled. The two-line prompt starts with a full-width, low-contrast divider containing the full path (`~` replaces your home), Git details, and any jobs or durations of at least ten seconds. One shared background continues through the directory and padding to the clock bubble, with flat outer edges flush against the terminal. On narrow terminals, padding shrinks and long context wraps rather than silently losing path details. The input line stays unshaded. Routine Nix/Python labels are hidden. `❯` is insert mode and `❮` is command mode; an insert-mode prompt turns red after a failed command.
- A muted local `HH:MM` ends the first context line in its own slightly lighter bubble: rounded on its inner left boundary, flat at the terminal's right edge. It records prompt-render time rather than ticking continuously. There is no clock or right prompt on the command-input line.
- Ctrl-R searches history with fzf; Ctrl-T selects files with a preview; Alt-C selects directories. `z` and `zi` provide zoxide navigation.
- Up/Down or Ctrl-P/Ctrl-N search history by the current prefix. Right-arrow at the end of the line or Ctrl-Space accepts a history suggestion.
- Ctrl-X Ctrl-E opens the current command in Neovim. `mkcd <directory>` creates and enters a directory; `croot` returns to the Git worktree root.
- Direnv's hook and nix-direnv are installed, but each checkout still needs a reviewed, approved `.envrc`. CXF's root `.envrc` is currently empty; use `nix develop` until it is configured.

The first line might look like this; the spaces to the right carry the same subtle background:

```text
 ~/Projects/cxf │  main │ staged +1 ~2 │ work ~3 │ new 4 │ ↑2              09:42
```

Only the branch uses an icon. Routine status text is neutral gray, with blue for the branch and red reserved for conflicts. `staged` and `work` distinguish staged and unstaged changes; `+`, `~`, `-`, `r`, and `t` count added, modified, deleted, renamed, and type-changed files. `new` counts untracked files, `conflict` unresolved files, `stash` saved stashes, and `↑`/`↓` commits relative to the locally known upstream. Empty groups and their separators disappear; outside Git, the directory divider remains without a Git section. These count file states, not lines; a partially staged file can appear in both groups. Use `gs` or lazygit for filenames.

### Ghostty

Catppuccin Mocha and JetBrains Mono Nerd Font match the other tools. Explicit window padding is zero; `window-padding-color = extend` extends adjacent backgrounds horizontally into leftover pixels outside the character grid. Its vertical safeguards suppress extension for rows containing Powerline separators, avoiding stretched tmux status segments while leaving any bottom remainder in the terminal's default background. Native tabs, splits, search (Ctrl-Shift-F), and the command palette (Ctrl-Shift-P) remain available.

Ctrl-Alt-F toggles fullscreen, Ctrl-Alt-Z zooms a Ghostty split, and Ctrl-Alt-R reloads configuration. Ctrl-Enter and Ctrl-Shift-Enter are no longer consumed by Ghostty, so applications can receive them. SSH compatibility falls back to a widely supported terminal type without installing remote terminfo automatically.

## Personal overrides

These optional files are not managed by Home Manager:

- `~/.zshrc.local`
- `~/.config/tmux/local.conf`
- `~/.config/ghostty/local.ghostty`

For a personal Starship configuration, set `STARSHIP_CONFIG` in `.zshrc.local` to a separate TOML file. Do not edit Home Manager's generated Nix store links.

## Apply and check

To preview the working-tree prompt in your current Zsh session, run from the repository root:

```bash
export STARSHIP_CONFIG="$PWD/.config/starship.toml"
```

This includes the first-line clock bubble. A shell without this variable uses the Home Manager-installed copy, which may still be older. To keep the changes across sessions, activate Home Manager through the NixOS rebuild below; do not overwrite the installed store symlink manually.

Review the diff first. The `path:` reference below includes the working tree even before the repository's initial commit; Git-based references require the intended source files to be tracked. See the [repository guide](../README.md) for rebuild and registry details.

Home Manager may refuse to replace an existing unmanaged Ghostty `config.ghostty`. Inspect and back it up before activation; do not enable forced overwrites. Then apply the existing laptop configuration through the normal NixOS workflow:

```bash
sudo nixos-rebuild switch --flake path:/home/gabe/Projects/dotfiles#dev-laptop
```

Open a new shell, reload tmux with prefix-r, and reload Ghostty with Ctrl-Alt-R. Padding geometry changes require a new terminal window or tab after reloading; existing surfaces retain their padding. New fonts or shell-integration changes may also require a new terminal window.

After activation, run from the repository root:

```bash
nix develop "path:$PWD" --command python3 tests/test_terminal_config.py
nix develop "path:$PWD" --command python3 tests/test_nvim_completion.py
```

The terminal tests use temporary homes and a private tmux socket. They validate actual configuration loading and keybindings without reloading live sessions. They do not replace a visual check of font rendering, clipboard behavior, or modified keys in a graphical terminal.
