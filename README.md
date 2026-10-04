# Personal NixOS and dotfiles

Gabe's laptop and Home Manager configuration, separate from CXF. The Git remote is [g2lang/dotfiles](https://github.com/g2lang/dotfiles). CXF does not import this repository, and this repository does not require a CXF checkout.

## Layout

- `hosts/dev-laptop/`: NixOS configuration and the existing hardware configuration.
- `home.nix`: Home Manager module.
- `.zshrc` and `.config/`: managed dotfiles, mirroring their locations in your home.
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

## Check changes

From this repository's root:

```bash
nix flake check "path:$PWD" --no-build --no-write-lock-file
nix develop "path:$PWD" --command python3 tests/test_terminal_config.py
nix develop "path:$PWD" --command python3 tests/test_nvim_completion.py
```

The development shell supplies test tools and the pinned Zsh plugins. The Neovim test also needs the configured Lazy plugins already installed. Terminal tests isolate temporary homes and a private tmux socket; graphical appearance still needs a visual check.

Credentials, machine state, plugin caches, and personal override files do not belong in Git. Review the new repository before making its initial commit or pushing it.
