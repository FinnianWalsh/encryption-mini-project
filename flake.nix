{
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

    nixpkgs-python.url = "github:cachix/nixpkgs-python";
  };

  outputs =
    {
      self,
      nixpkgs,
      nixpkgs-python,
    }:
    let
      lib = nixpkgs.lib;

      supportedSystems = [
        "x86_64-linux"
        "aarch64-linux"
        "x86_64-darwin"
        "aarch64-darwin"
      ];

      pythonPackages = lib.genAttrs supportedSystems (system: nixpkgs-python.packages.${system}."3.8.2");
    in
    {
      packages = lib.genAttrs supportedSystems (system: {
        default = pythonPackages.${system};
      });

      devShells = lib.genAttrs supportedSystems (
        system:
        let
          pkgs = nixpkgs.legacyPackages.${system};
        in
        {
          default = pkgs.mkShell {
            name = "Python 3.8.2";

            buildInputs = [
              pythonPackages.${system}
            ];
          };
        }
      );
    };
}
