# Third-party notices

## RHVoice

This project can bundle `RHVoice.dll` in the Windows onefile release so that users can synthesize RHVoice `.nvda-addon` voice packages without installing the RHVoice NVDA add-on separately.

RHVoice is distributed under the GNU General Public License. The bundled license text is available in `licenses/RHVoice-GPL-3.0.txt`.

Project/source information:

- https://github.com/RHVoice/RHVoice
- https://rhvoice.org/

If you build your own EXE, `scripts/build-onefile.ps1` can include a locally installed `RHVoice.dll` by default, or skip it with `-NoBundledRhVoice`.
