{
  description = "Examen parcial 1 Sistemas Distribuidos G31";
  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-25.05";
  };
  outputs = {self, nixpkgs}: let
    pkgs = nixpkgs.legacyPackages."x86_64-linux";
  in {
    devshells."x86_64-linux".default = pkgs.mkShell {
      packages = with pkgs; [
	python312
	python312Packages.pandas
      ];
    };
  };
}
