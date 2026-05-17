# Third-party notices

## RHVoice

This project can bundle `RHVoice.dll` in the Windows onefile release so that users can synthesize RHVoice `.nvda-addon` voice packages without installing the RHVoice NVDA add-on separately.

RHVoice is distributed under the GNU General Public License. The bundled license text is available in `licenses/RHVoice-GPL-3.0.txt`.

Project/source information:

- https://github.com/RHVoice/RHVoice
- https://rhvoice.org/

If you build your own EXE, `scripts/build-onefile.ps1` can include a locally installed `RHVoice.dll` by default, or skip it with `-NoBundledRhVoice`.

## FFmpeg

The Windows onefile release can bundle `ffmpeg.exe` so audio conversion works without asking users for a separate path.

The bundled binary used on this machine reports: `ffmpeg version 6.0-essentials_build-www.gyan.dev` and is configured with GPL options.

Project/source information:

- https://ffmpeg.org/
- https://www.gyan.dev/ffmpeg/builds/

If you build your own EXE, `scripts/build-onefile.ps1` includes a locally available `ffmpeg.exe` by default, or skips it with `-NoBundledFfmpeg`.
