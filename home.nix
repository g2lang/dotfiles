{ config, pkgs, ... }:

{
  home.username = "gabe";
  home.homeDirectory = "/home/gabe";
  home.stateVersion = "26.05";

  home.packages = with pkgs; [
    # Editor runtime and plugin build helpers.
    neovim
    nodejs
    git
    gcc
    gnumake
    tree-sitter
    wl-clipboard

    # Search/navigation tools used by Telescope and editor workflows.
    ripgrep
    fd
    fzf
    zoxide
    lazygit

    # Rust language server, debugger, formatting, linting, and test tooling.
    rustc
    cargo
    rustfmt
    clippy
    rust-analyzer
    lldb
    cargo-nextest
    cargo-watch
    cargo-audit
    cargo-deny
    cargo-llvm-cov
    bacon

    # Python tooling. uv still owns per-project environments.
    uv
    basedpyright
    ruff
    black
    isort
    (python312.withPackages (
      ps: with ps; [
        debugpy
        pynvim
      ]
    ))

    # Markdown/prose tooling.
    marksman
    markdownlint-cli2
    prettierd
    prettier
    glow
    vale
    typos
    typos-lsp

    # Nix, Lua, shell, TOML, YAML, JSON, and web language tooling.
    nixd
    nixfmt
    statix
    deadnix
    lua-language-server
    stylua
    bash-language-server
    shellcheck
    shfmt
    taplo
    yaml-language-server
    vscode-langservers-extracted

    # General CLI/desktop packages.
    tmux
    zsh
    starship
    nerd-fonts.jetbrains-mono
    gh
    jq
    bat
    btop
    rsync
    eza
    tree
    file
    curl
    wget
    unzip
    zip
    just
    signal-desktop
    tailscale
    emacs
    pi-coding-agent
    ghostty
    pkg-config
  ];

  home.file = {
    ".zshrc".source = ./.zshrc;
    ".config/starship.toml".source = ./.config/starship.toml;
    ".config/zsh/plugins/zsh-autosuggestions.zsh".source =
      "${pkgs.zsh-autosuggestions}/share/zsh-autosuggestions/zsh-autosuggestions.zsh";
    ".config/zsh/plugins/zsh-syntax-highlighting".source =
      "${pkgs.zsh-syntax-highlighting}/share/zsh-syntax-highlighting";

    ".config/ghostty" = {
      source = ./.config/ghostty;
      recursive = true;
    };

    ".config/nvim" = {
      source = ./.config/nvim;
      recursive = true;
    };

    ".config/tmux" = {
      source = ./.config/tmux;
      recursive = true;
    };

    ".config/git" = {
      source = ./.config/git;
      recursive = true;
    };

    ".config/gh" = {
      source = ./.config/gh;
      recursive = true;
    };
  };

  # The hand-written .zshrc owns the hook; avoid a second generated shell config.
  programs.direnv = {
    enable = true;
    nix-direnv.enable = true;
    enableZshIntegration = false;
    enableBashIntegration = false;
    enableFishIntegration = false;
  };

  fonts.fontconfig.enable = true;
  programs.home-manager.enable = true;
}
