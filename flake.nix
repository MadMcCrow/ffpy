# nix flake for ffpy
#
{
  description = "ffpy the python tool to use ffmpeg";

  inputs = {
    # Nixpkgs
    nixpkgs.url     = "github:nixos/nixpkgs/release-23.05";

    # supports linux and macOS
    flake-utils.url = "github:numtide/flake-utils";

    # pycnix is a tool to compile scripts to efficient binaries
    pycnix.url = "github:MadMcCrow/pycnix";
    pycnix.inputs.nixpkgs.follows = "nixpkgs";
  };

  outputs = { self, nixpkgs, pycnix, flake-utils }@inputs:
  with builtins;
  let
  # find python files in this repo :
  pythonFiles = lib : filter (x : lib.strings.hasSuffix ".py" x) (attrNames (readDir self));

  # use them in our package :
  ffpy = pkgs : system : pycnix.lib.${system}.mkCythonBin { 
    name = "ffpy";
    main = "__main__";
    modules = pythonFiles pkgs.lib;
    };

  in
    flake-utils.lib.eachDefaultSystem
      (system: let pkgs = nixpkgs.legacyPackages.${system}; in
        {
          devShells.default = import ./shell.nix { inherit pkgs pycnix ffpy ;};
          packages = {
            default = ffpy pkgs system;
          };
        }
      );
}
