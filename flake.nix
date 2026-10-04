{
  description = "Gabe's NixOS and Home Manager configuration";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    home-manager = {
      url = "github:nix-community/home-manager/master";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs = { nixpkgs, home-manager, ... }:
    let
      system = "x86_64-linux";
      pkgs = nixpkgs.legacyPackages.${system};
    in
    {
      nixosConfigurations.dev-laptop = nixpkgs.lib.nixosSystem {
        inherit system;
        modules = [
          ./hosts/dev-laptop/configuration.nix
          home-manager.nixosModules.home-manager
          {
            home-manager.useGlobalPkgs = true;
            home-manager.useUserPackages = true;
            home-manager.users.gabe = import ./home.nix;
          }
        ];
      };

      # Configuration checks are independent of CXF's development environment.
      devShells.${system}.default = pkgs.mkShell {
        packages = with pkgs; [
          (python312.withPackages (ps: [ ps.pynvim ]))
          ruff
          git
          neovim
          zsh
          tmux
          ghostty
          starship
          fzf
          direnv
          zoxide
          bat
          eza
        ];
        CXF_TEST_AUTOSUGGESTIONS_FILE =
          "${pkgs.zsh-autosuggestions}/share/zsh-autosuggestions/zsh-autosuggestions.zsh";
        CXF_TEST_HIGHLIGHTING_DIR =
          "${pkgs.zsh-syntax-highlighting}/share/zsh-syntax-highlighting";
      };
    };
}
