# The weekly roast reel

1080x1920, narrated, about a minute. Canvas page + Playwright + ffmpeg. No API keys.

1. **Script**: `script.json`, one entry per scene: `[scene_name, [spoken lines]]`. Write numbers the way
   they should be *said* ("one seventy-eight seventy-eight"); the on-screen caption is mapped back to digits
   in the caption step. Spell awkward names phonetically ("Nih-sheel", "Ah-bee-shake", "Uh-nooj").
2. **Voice**: `pip install kokoro-onnx soundfile`, download `kokoro-v1.0.int8.onnx` (save as `kokoro.onnx`) and
   `voices-v1.0.bin` from github.com/thewh1teagle/kokoro-onnx releases into `$KOKORO_DIR`, then
   `python3 vo.py` (voice `am_michael`, speed 1.28). Writes `vo/*.wav` + `vo.json`.
3. **Timeline**: `python3 timeline.py` sets each scene's length from its lines, writes `tl.json` + `voice.wav`.
   Then swap caption text in `tl.json` for the digit version.
4. **Picture**: put `archivo-latin-wdth-normal.woff2` (from `npm pack @fontsource-variable/archivo`) next to
   `reel.html`, edit the week's data arrays (`WEEK`, `PR`, `RR`) and scene functions in `reel.html`, then
   `node render.js preview 4.5 12` for stills and `node render.js full` for `silent.mp4`.
5. **Sound**: `MUSIC=funkgame.mp3 python3 mix.py` loops the bed and ducks it under the voice, then
   `ffmpeg -i silent.mp4 -i mix.wav -c:v copy -c:a aac -b:a 160k -af loudnorm=I=-15:TP=-1.5:LRA=11 -shortest -movflags +faststart video/<season>-wk<NN>.mp4`.
   Keep it under 8 MB.

Music in use: "Funk Game Loop", Kevin MacLeod (incompetech.com), CC BY 4.0, from archive.org item
`KevinMacLeod_2019-04_Discography`. Credit it on the end card and in the video blurb. Same item has
"Volatile Reaction", "Pump" and "Movement Proposition" for rotation.

Check the voice before shipping: nobody on the build side can hear it, so run a quick `faster-whisper`
transcription of the final mp4 and fix any name it mishears.
