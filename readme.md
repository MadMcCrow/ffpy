# ffpy

A simple to use tool to convert videos and save space.

## requirements

- python (at least 3.10)
- ffmpeg (preferably 4.4.2 - might work with other versions)
- (optional) vainfo (VA-API version 1.16.0)

## nix

this works on linux and darwin systems thanks to the nix flake/shell

### usage :
```
nix-shell -p ffmpeg python3 --run "python3 ./ffpy videos videos_hevc"   
```

## TODO
these would be the next improvements for this repo :
- [ ] easy to use settings
- [ ] run with nix-shell
- [ ] add GUI
- [ ] compiled and packaged version

