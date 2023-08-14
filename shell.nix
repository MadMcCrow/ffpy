# Dev shell for ffmpeg
{ pkgs, pycnixm ffpy }:
with pkgs;
mkShell {
  buildInputs = [
    ffpy
    nixpkgs-fmt
    ffmpeg
    python3
    libva-utils
  ];
}