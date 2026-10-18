# Personal NixOS and dotfiles

Gabe's laptop and Home Manager configuration, separate from CXF. The Git remote is [g2lang/dotfiles](https://github.com/g2lang/dotfiles). CXF does not import this repository, and this repository does not require a CXF checkout.

## Layout

- `hosts/dev-laptop/`: NixOS configuration and the existing hardware configuration.
- `home.nix`: Home Manager module; `modules/agents.nix` manages shared agent files.
- `.agents/`: shared personal instructions and declarative skills ([agent guide](docs/agents.md)).
- `.zshrc`, `.config/`, and `.ssh/config`: managed dotfiles, mirroring their locations in your home.
- `tests/`: terminal and Neovim configuration regression tests.
- [Terminal guide](docs/terminal.md): controls, appearance, and personal overrides.

The migration preserves the existing Nixpkgs and Home Manager revisions in `flake.lock`. It does not upgrade packages or change the machine's hostname (`nixos`) or state versions.

## Rebuild the laptop

Review changes, then run from any directory:

```bash
sudo nixos-rebuild switch --flake path:/home/gabe/Projects/dotfiles#dev-laptop
```

This flake connects the laptop's NixOS configuration to its Home Manager module. Home Manager still installs reproducible Nix-store-backed files; nothing needs a symlink back into CXF. Do not replace installed Home Manager symlinks manually.

After activation from the new path, the system's `dotfiles` Nix registry entry points to this checkout. Until then, an existing registry entry may still point to the old location; use the explicit path above for the first rebuild after moving. Subsequent rebuilds can use:

```bash
sudo nixos-rebuild switch --flake dotfiles#dev-laptop
```

Use an explicit `--flake`: the old installation-time files in `/etc/nixos` are not this configuration and are not rewritten by this migration. No activation is needed merely to edit or evaluate this repository.

The `path:` form works even before the new repository has an initial commit or tracked files. It includes untracked source files; review them before rebuilding. A normal Git-based flake reference such as `.#dev-laptop` requires the intended source files to be tracked.

After activation, open a new shell, reload tmux with prefix-r, and reload Ghostty with Ctrl-Alt-R. Ghostty padding geometry changes require a new window or tab. If an existing shell exports `STARSHIP_CONFIG` pointing into CXF, the old checkout location, or the old nested layout, unset it to use the installed config, or set it to `$HOME/Projects/dotfiles/.config/starship.toml`.

## Orca package and updates

`pkgs/orca-ide.nix` pins the official stablyai Orca x86-64 Linux AppImage,
not the GNOME screen reader (`pkgs.orca`). The initial pin is 1.4.229.
The package is exposed as `packages.x86_64-linux.orca-ide` and included in
`home.packages` in `home.nix`. Activate with `just switch`, then launch **Orca**
from GNOME's application menu or run `orca-ide`. The package includes the upstream
desktop entry and icons; it does not replace GNOME's `orca` screen-reader command.

```bash
just update-orca          # Latest stable GitHub release
just update-orca 1.4.229  # Explicit stable version (also accepts v1.4.229)
just test-update-orca     # Offline updater regression tests
```

The updater fetches release metadata, downloads the selected AppImage into the
Nix store, and verifies its SHA-256 against GitHub's published asset digest before
atomically changing only the package's version and checksum. An unchanged pin is
a no-op; missing assets/digests, failed downloads, and checksum mismatches leave
the file untouched. Network access is required; GitHub API rate limits can cause
a failure. It never updates `flake.lock`, builds the application/system, activates
a generation, runs the AppImage, or commits changes. `nix develop` may realize the
pinned development shell used to run the updater.

Review and optionally build the package independently:

```bash
git diff -- pkgs/orca-ide.nix
# Until the new package file is tracked, inspect it directly or use just status.
nix build "path:$PWD#orca-ide" --no-write-lock-file --no-link
```

After updating the pin, use `just check`, `just diff`, and `just switch` to validate,
build, and activate it. Quit Orca before switching and reopen it afterward. Keep
updates Nix-managed rather than using an in-app installer. Back up Orca's mutable
state before significant upgrades: reverting the package pin and rebuilding
restores the executable, not database migrations. Agent logins and Orca's mutable
state remain outside Git and Home Manager's managed files.

## Shared agent configuration

`.agents/AGENTS.md` supplies personal instructions at `~/.agents/AGENTS.md`.
Pi's `~/.pi/agent/AGENTS.md` and Codex's `~/.codex/AGENTS.md` are aliases pointing
to that canonical installed file. Both agents discover `~/.agents/skills/`
natively; Home Manager installs each skill directory in `.agents/skills/`
individually, leaving existing unrelated skills writable and unmanaged.

To manage a new skill, add `.agents/skills/<name>/SKILL.md` and any supporting
files, run `just test-agents` and `just check`, then activate when ready with
`just switch`. Edit managed files here, not through their installed symlinks.
No authentication, sessions, installer state, or mutable agent settings are
managed. See the [agent guide](docs/agents.md) for migration, conflicts,
third-party skills, and adding another agent.

## SSH client configuration

Home Manager manages only `~/.ssh/config`, not the whole SSH directory. Its
versioned source includes `~/.ssh/config.local` before shared defaults, so private
host entries and per-host overrides remain writable and outside this published
repository. The local file is optional; it is not created by Home Manager on a
new machine.

Private keys, public-key files, `known_hosts`, and `config.local` remain in the
actual `~/.ssh/`. Do not copy keys into this checkout or reference their contents
from Nix: ignored files can still enter the store through a `path:` flake. The
repository's `.ssh/` allowlist admits only `config` to Git. GNOME supplies the SSH
agent; do not enable a competing agent or start one in each shell.

Before the first activation, an existing regular `~/.ssh/config` must be moved
to an **unused backup filename**, after preserving its host entries in
`~/.ssh/config.local`. Move only that configuration file, never the directory or
its keys. Then use the normal laptop rebuild above. Home Manager will refuse a
conflicting file rather than overwrite it. No forced replacement is configured.

Preview the proposed configuration without connecting or activating:

```bash
ssh -G -F /home/gabe/Projects/dotfiles/.ssh/config HOST_ALIAS
```

## Check changes

Use `just` to list the available workflows. Recipes run from the checkout root,
even when called from a subdirectory, and use `path:` flake references so edits
and new source files are available immediately without staging them. As with the
rebuild command above, keep credentials and private files outside the checkout.

```bash
just status         # Review existing changes and untracked files
just check          # Fast whitespace, shell syntax, and Nix evaluation checks
just test-terminal  # Focused terminal regression tests
just test-nvim      # Focused Neovim regression test
just test-agents    # Shared instructions, skill metadata, and Home Manager wiring
just verify         # Run checks and all test suites
just plan           # Preview required builds and downloads
just build          # Build NixOS + Home Manager into ./result
just diff           # Build and compare packages against the running system
just switch         # Activate and set the boot default (uses sudo)
```

`just boot` selects a configuration for the next reboot. `just shell` opens the
pinned development environment; `just run COMMAND ARGS...` runs a single command
inside it. Validation and build recipes do not activate changes or update the
lock file. The default flake host is `dev-laptop`; override it with
`DOTFILES_HOST=OTHER_HOST just build` when adding another configuration.

The equivalent test commands can also be run directly
from this repository's root:

```bash
nix flake check "path:$PWD" --no-build --no-write-lock-file
nix develop "path:$PWD" --command python3 tests/test_terminal_config.py
nix develop "path:$PWD" --command python3 tests/test_nvim_completion.py
```

The development shell supplies test tools and the pinned Zsh plugins. The Neovim test also needs the configured Lazy plugins already installed. Terminal tests isolate temporary homes and a private tmux socket; graphical appearance still needs a visual check.

Credentials, machine state, plugin caches, and personal override files do not belong in Git. Review the new repository before making its initial commit or pushing it.
