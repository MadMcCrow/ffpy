# Dev shell for ffmpeg
{ pkgs, ... }:
with pkgs;
mkShell {
  buildInputs = [
    nixpkgs-fmt
    ffmpeg
    python3
    libva-utils
  ];

  # Shell hook if you need one
  #shellHook = ''
  #  # ...
  #'';
}