# OpenGD77 Prompt Studio

OpenGD77 Prompt Studio to dostepne dla czytnikow ekranu narzedzie Windows do tworzenia pakietow komunikatow glosowych VPR dla OpenGD77.

Program bazuje na skrypcie `GD77VoicePromptsBuilder.py`, ale jest uporzadkowany jako osobny projekt z GUI, dokumentacja, przykladami i buildem do jednego pliku EXE.

## Co robi program

- Pobiera mowe z TTSMP3 na podstawie pliku wordlist CSV.
- Generuje mowe lokalnie z glosu RHVoice dostarczonego jako `.nvda-addon`.
- Pozwala regulowac wysokosc glosu RHVoice przy lokalnej syntezie.
- Konwertuje audio przez `ffmpeg` do surowego PCM 8 kHz, 16-bit, mono.
- Gotowy release ma wbudowany `ffmpeg.exe`, wiec zwykly uzytkownik nie musi wpisywac sciezki.
- Koduje probki AMBE przez radio OpenGD77 podlaczone przez port COM.
- Buduje pliki VPR w wariantach `UV380-like` i `monochrome`.
- Ma natywny interfejs `wxPython` z normalnymi kontrolkami Windows: pola edycji, przyciski, checkboxy, radiobuttony, liste portow i log.
- Pokazuje postep pracy na dostepnym pasku postepu; fokus na postep ustawisz skrotem `Alt+P`.

## Najszybsze uzycie

1. Pobierz `OpenGD77PromptStudio.exe` z najnowszego release GitHub.
2. Uruchom EXE.
3. Wybierz `Wordlist CSV`.
4. Wpisz nazwe glosu lub folderu, np. `Polish`, `Kazek` albo `Zuza`.
5. Wybierz zrodlo mowy: `TTSMP3` albo `Dodatek NVDA/RHVoice`.
6. Przy zrodle NVDA/RHVoice wskaz plik `.nvda-addon` z glosem RHVoice.
7. Wybierz operacje: tworzenie mowy, kodowanie AMBE, budowanie VPR.
8. Wskaz port COM radia, jesli kodujesz AMBE.
9. Nacisnij `Uruchom Alt+R`.

Szczegolowy opis jest w folderze `docs`.

## Wazne o dodatkach NVDA

Program obsluguje pliki `.nvda-addon`, ktore sa glosami RHVoice i zawieraja `data/voice.info`, `data/voice.params` oraz `langdata`.

Nie kazdy dodatek NVDA jest syntezatorem albo glosem. Dodatki typu plugin, narzedzie globalne albo sterownik innego silnika zostana odrzucone z czytelnym komunikatem.

Do syntezy RHVoice potrzebny jest `RHVoice.dll`. Gotowy EXE z release ma ten silnik wbudowany. Przy pracy ze zrodel albo w niestandardowym buildzie program moze tez wykryc DLL z zainstalowanego dodatku NVDA `RHVoice`, z pliku obok EXE albo ze zmiennej `RHVOICE_DLL`.

## Wymagania

Dla gotowego EXE:

- Windows 10 lub Windows 11.
- `ffmpeg.exe` tylko przy buildach bez wbudowanego ffmpeg albo przy pracy ze zrodel. Standardowy release ma ffmpeg w EXE.
- `RHVoice.dll`, jesli uzywasz glosu `.nvda-addon` RHVoice i korzystasz z builda bez wbudowanego silnika. Gotowy release ma DLL w EXE.
- Radio z OpenGD77 podlaczone jako port COM, jesli kodujesz AMBE.

Dla pracy ze zrodel:

- Python 3.10 lub nowszy.
- Pakiety z `requirements.txt`.
- PyInstaller, jesli budujesz EXE.

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
- `docs/06-dodatki-nvda-rhvoice.md`

## Status

Wersja projektu: `0.3.0`.
