# Always run from this checkout, including when invoked from a subdirectory.
set shell := ["bash", "-euo", "pipefail", "-c"]
set positional-arguments

# Include new, untracked source files without requiring agents to stage them.
# Like the README's rebuild command, path: also includes ignored files.
export DOTFILES_FLAKE := "path:" + justfile_directory()
export DOTFILES_HOST := env("DOTFILES_HOST", "dev-laptop")

# List the available workflows; running just alone never changes the system.
default:
    @just --list

# Inspect tracked edits and discover untracked files before working or building.
status:
    git status --short
    git diff --stat
    git diff --cached --stat

# Fast feedback: whitespace, shell syntax, flake validation, and system evaluation.
check:
    git diff --check
    git diff --cached --check
    zsh -n .zshrc
    nix flake check "$DOTFILES_FLAKE" --no-build --no-write-lock-file
    just evaluate

# Evaluate the complete system derivation without building or activating it.
evaluate:
    nix eval "$DOTFILES_FLAKE#nixosConfigurations.$DOTFILES_HOST.config.system.build.toplevel.drvPath" --raw --no-write-lock-file
    @printf '\n'

# Run all regression suites against the working tree in the pinned environment.
test:
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file --command bash -euc 'python3 tests/test_terminal_config.py; python3 tests/test_nvim_completion.py; python3 -B tests/test_update_orca.py; python3 -B tests/test_agent_config.py'

# Test shell, tmux, prompt, and terminal configuration in isolated temporary homes.
test-terminal:
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file --command python3 tests/test_terminal_config.py

# Test Neovim completion; requires the configured Lazy plugins already installed.
test-nvim:
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file --command python3 tests/test_nvim_completion.py

# Test the Orca updater offline, without downloads or changes to the package pin.
test-update-orca:
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file --command python3 -B tests/test_update_orca.py

# Validate skill references, invocation policies, metadata, and Home Manager wiring.
test-agents:
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file --command python3 -B tests/test_agent_config.py

# Pin the latest stable Orca (or a specific version); never build or activate it.
update-orca version="latest":
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file --command python3 -B scripts/update_orca.py "$1"

# Validate and run regression tests before handing off a change.
verify: check test

# Show what a system build would need to build or download.
plan:
    nix build "$DOTFILES_FLAKE#nixosConfigurations.$DOTFILES_HOST.config.system.build.toplevel" --dry-run --no-link --no-write-lock-file

# Build the system and integrated Home Manager configuration into ./result.
build:
    nix build "$DOTFILES_FLAKE#nixosConfigurations.$DOTFILES_HOST.config.system.build.toplevel" --out-link result --no-write-lock-file --print-build-logs

# Build and compare package closures with the running system, without activation.
diff: build
    nix store diff-closures /run/current-system ./result

# Build and activate the configuration now, making it the boot default (sudo).
switch:
    sudo nixos-rebuild switch --flake "$DOTFILES_FLAKE#$DOTFILES_HOST" --no-write-lock-file

# Build and select the configuration for the next boot without activating it (sudo).
boot:
    sudo nixos-rebuild boot --flake "$DOTFILES_FLAKE#$DOTFILES_HOST" --no-write-lock-file

# Enter the pinned development environment.
shell:
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file

# Run a command in the pinned environment, e.g. just run python3 --version.
run +args:
    nix develop "$DOTFILES_FLAKE" --no-write-lock-file --command "$@"
