# Changelog

## 0.3.2 - 2026-05-17

- Puste wpisy w wordliscie, na przyk?ad `PROMPT_SPACE`, sa teraz zapisywane jako krotka cisza zamiast przerywac synteze RHVoice.

## 0.3.1 - 2026-05-17

- Zmieniono GUI z Tkinter na wxPython, bo NVDA nie odczytywal poprawnie kontrolek Tk w gotowym EXE.
- Dodano jawne nazwy dostepnosciowe dla pol edycji, przyciskow, checkboxow, radiobuttonow i listy portow.

## 0.3.0

- Domyslny build EXE bundluje `RHVoice.dll`, jezeli jest dostepny lokalnie.
- Gotowy release pozwala uzyc glosu RHVoice `.nvda-addon` bez instalowania dodatku NVDA `RHVoice` i bez recznego wskazywania DLL.
- Dodano parametr builda `-NoBundledRhVoice` do tworzenia wariantu bez wbudowanego silnika.
- Dodano `licenses/RHVoice-GPL-3.0.txt` i `THIRD_PARTY_NOTICES.md`.

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
