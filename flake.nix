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
    packages."x86_64-linux".default = pkgs.python3.pkgs.buildPythonPackage {
      pname = "SD31_325724_ExParcial_1";
      version = "0.1.0";
    };
  };
}
