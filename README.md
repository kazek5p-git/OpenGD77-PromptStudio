# OpenGD77 Prompt Studio

OpenGD77 Prompt Studio to dostępne dla czytników ekranu narzędzie Windows do tworzenia pakietów komunikatów głosowych VPR dla OpenGD77.

Program bazuje na skrypcie `GD77VoicePromptsBuilder.py`, ale jest uporządkowany jako osobny projekt z GUI, dokumentacją, przykładami i buildem do jednego pliku EXE.

## Co robi program

- Pobiera mowę z TTSMP3 na podstawie pliku wordlist CSV.
- Konwertuje audio przez `ffmpeg` do surowego PCM 8 kHz, 16-bit, mono.
- Koduje próbki AMBE przez radio OpenGD77 podłączone przez port COM.
- Buduje pliki VPR w wariantach `UV380-like` i `monochrome`.
- Ma prosty interfejs `tkinter` z normalnymi kontrolkami Windows: pola edycji, przyciski, checkboxy, radiobuttony, listę portów i log.

## Najszybsze użycie

1. Pobierz `OpenGD77PromptStudio.exe` z najnowszego release GitHub.
2. Uruchom EXE.
3. Wybierz `Wordlist CSV`.
4. Wpisz nazwę głosu lub folderu, np. `Polish`.
5. Wybierz operacje: pobieranie mowy, kodowanie AMBE, budowanie VPR.
6. Wskaż port COM radia, jeśli kodujesz AMBE.
7. Naciśnij `Uruchom Alt+R`.

Szczegółowy opis jest w folderze `docs`.

## Wymagania

Dla gotowego EXE:

- Windows 10 lub Windows 11.
- `ffmpeg.exe`, jeśli pobierasz i konwertujesz mowę.
- Radio z OpenGD77 podłączone jako port COM, jeśli kodujesz AMBE.

Dla pracy ze źródeł:

- Python 3.10 lub nowszy.
- Pakiety z `requirements.txt`.
- PyInstaller, jeśli budujesz EXE.

## Budowanie EXE

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1
```

Wynik:

```text
dist\OpenGD77PromptStudio.exe
```

## Dokumentacja

- `docs/01-szybki-start.md`
- `docs/02-dostepnosc-i-gui.md`
- `docs/03-formaty-csv-i-vpr.md`
- `docs/04-budowanie-exe.md`
- `docs/05-rozwiazywanie-problemow.md`

## Status

Wersja projektu: `0.1.0`.