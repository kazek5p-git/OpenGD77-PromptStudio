# Changelog

## 0.2.0

- Dodano zrodlo mowy `Dodatek NVDA/RHVoice`.
- Dodano opcje CLI `-N=<nvda_addon>` i `-L=<RHVoice.dll>`.
- Program rozpoznaje glosy RHVoice w plikach `.nvda-addon`, rozpakowuje je do folderu roboczego i generuje WAV/RAW lokalnie.
- Dodano wykrywanie `RHVoice.dll` z dodatku NVDA RHVoice, folderu programu, `_MEIPASS` PyInstaller albo zmiennej `RHVOICE_DLL`.
- GUI ma pola wyboru `.nvda-addon` i opcjonalnego `RHVoice.dll`.
- Dodano dokumentacje dodatkow NVDA/RHVoice.

## 0.1.0

- Utworzono osobny projekt OpenGD77 Prompt Studio.
- Dodano dostepne GUI uruchamiane bez argumentow.
- Dodano obsluge dzialania jako PyInstaller onefile EXE.
- Dodano dokumentacje, przykladowe CSV i skrypty budowania/testowania.
- Poprawiono `-h` i `--help`, aby konczyly sie kodem 0.
