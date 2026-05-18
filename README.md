# OpenGD77 Prompt Studio

OpenGD77 Prompt Studio to dostepne dla czytnikow ekranu narzedzie Windows do tworzenia pakietow komunikatow glosowych VPR dla OpenGD77.

Program bazuje na skrypcie `GD77VoicePromptsBuilder.py`, ale jest uporzadkowany jako osobny projekt z natywnym GUI Windows, dokumentacja, profilami ustawien, aktualizatorem i buildem do jednego pliku EXE.

## Aktualny release

Aktualna wersja projektu: `0.4.9`.

- Release: https://github.com/kazek5p-git/OpenGD77-PromptStudio/releases/latest
- Plik EXE w release: `OpenGD77PromptStudio.exe`
- Lokalny wynik builda: `dist\OpenGD77PromptStudio.exe`

## Co robi program

- Pobiera mowe z TTSMP3 na podstawie pliku wordlist CSV.
- Wczytuje wordlist i config CSV w typowych formatach: UTF-8, UTF-8 z BOM, UTF-16 oraz ANSI/Windows-1250; automatycznie wykrywa przecinek, srednik albo tabulator.
- Generuje mowe lokalnie z glosu RHVoice dostarczonego jako `.nvda-addon`.
- Pozwala wybrac profil glosu RHVoice, np. Kazek, Zuza, Natan, jezeli taki profil jest w dodatku.
- Pozwala regulowac wysokosc glosu RHVoice przy lokalnej syntezie.
- Konwertuje audio przez `ffmpeg` do surowego PCM 8 kHz, 16-bit, mono.
- Pozwala ustawic osobne tempo dla pojedynczych liter, cyfr, spacji i kropki.
- Gotowy release ma wbudowany `ffmpeg.exe` oraz `RHVoice.dll`, wiec zwykly uzytkownik nie musi wpisywac sciezek do tych skladnikow.
- Koduje probki AMBE przez radio OpenGD77 podlaczone przez port COM.
- Buduje pliki VPR w wariantach `UV380-like` i `monochrome` oraz opisuje, dla jakich rodzin radii wybrac kazdy wariant.
- Ma natywny interfejs `wxPython` z dostepnym paskiem zakladek opartym o radiobuttony oraz normalnymi kontrolkami Windows.
- Ma wybor jezyka interfejsu: polski albo angielski. Po zmianie jezyka program pyta o restart i moze uruchomic sie ponownie automatycznie.
- Pokazuje postep pracy na dostepnym pasku postepu; fokus na postep ustawisz skrotem `Alt+P`.
- Zapisuje i wczytuje profile ustawien z folderu `%APPDATA%\OpenGD77PromptStudio\profiles`.
- Ma zakladke aktualizacji, ktora sprawdza i pobiera najnowszy release z GitHuba.

## Najszybsze uzycie

1. Pobierz `OpenGD77PromptStudio.exe` z najnowszego release GitHub.
2. Uruchom EXE.
3. Opcjonalnie ustaw `Jezyk interfejsu` na `Polski` albo `English`. Po zmianie program zapyta o restart.
4. W trybie recznym wybierz `Wordlist CSV`. Plik moze byc zapisany jako UTF-8, UTF-8 z BOM, UTF-16 albo ANSI/Windows-1250; separator moze byc przecinkiem, srednikiem albo tabulatorem.
5. Wpisz nazwe glosu lub folderu, np. `Polish`, `Kazek`, `Zuza` albo `Natan`.
6. Wybierz zrodlo mowy: `TTSMP3.com` albo `RHVoice z dodatku NVDA`.
7. Przy zrodle RHVoice wskaz plik `.nvda-addon` z glosem.
8. Wybierz operacje: `Pobierz / syntezuj audio`, `Koduj AMBE w radiu`, `Zbuduj VPR`.
9. Wskaz port COM radia, jesli kodujesz AMBE.
10. Nacisnij `Uruchom Alt+R`.

## Warianty VPR

Program buduje dwa warianty pliku `.vpr`:

- `UV380-like`: dla kolorowych i nowszych radii OpenGD77, m.in. TYT MD-UV380/MD-UV390, Retevis RT3S, TYT MD-9600/Retevis RT-90, TYT MD-2017/Retevis RT-82 oraz Baofeng DM-1701/Retevis RT-84.
- `monochrome`: dla starszej rodziny z monochromatycznym ekranem, m.in. Radioddity GD-77/GD-77S, Baofeng DM-1801/DM-1801A oraz Baofeng RD-5R.

Retevis RT3 bez S nie jest tym samym co RT3S. GPS albo brak GPS w RT3S nie zmienia wyboru promptu: uzyj `UV380-like`.

## Foldery uzytkownika

Program nie powinien pokazywac sciezek z komputera osoby, ktora zbudowala EXE. Domyslne lokalizacje sa zalezne od aktualnego uzytkownika Windows:

- ustawienia programu: `%APPDATA%\OpenGD77PromptStudio\settings.json`,
- profile ustawien: `%APPDATA%\OpenGD77PromptStudio\profiles`,
- folder roboczy: `%APPDATA%\OpenGD77PromptStudio\work`,
- pobrane aktualizacje: `%APPDATA%\OpenGD77PromptStudio\updates`,
- domyslny wynik VPR: `Dokumenty\OpenGD77PromptStudio\voice_prompts.vpr`.

## Wymagania

Dla gotowego EXE:

- Windows 10 lub Windows 11.
- Radio z OpenGD77 podlaczone jako port COM, jesli kodujesz AMBE.
- `ffmpeg.exe` i `RHVoice.dll` nie sa potrzebne jako osobne pliki w standardowym release, bo sa wbudowane.

Dla pracy ze zrodel:

- Python 3.10 lub nowszy.
- Pakiety z `requirements.txt`.
- PyInstaller, jesli budujesz EXE.
- Opcjonalnie `ffmpeg.exe` i `RHVoice.dll`, jezeli budujesz wariant bez wbudowanych skladnikow.

## Dokumentacja

- `docs/00-spis-tresci.md`: indeks dokumentacji i najwazniejsze sciezki.
- `docs/01-szybki-start.md`: pierwszy przebieg i najwazniejsze opcje.
- `docs/02-dostepnosc-i-gui.md`: opis GUI, NVDA, zakladek, jezyka, profili i skrotow.
- `docs/03-formaty-csv-i-vpr.md`: format wordlist, config CSV, probek audio, AMBE i VPR.
- `docs/04-budowanie-exe.md`: budowanie jednoplikowego EXE, bundlowanie ffmpeg/RHVoice i testy.
- `docs/05-rozwiazywanie-problemow.md`: typowe awarie i sposoby naprawy.
- `docs/06-dodatki-nvda-rhvoice.md`: obsluga glosow RHVoice z plikow `.nvda-addon`.

## Budowanie EXE

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1
```

Wynik:

```text
dist\OpenGD77PromptStudio.exe
```

Test podstawowy:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-test.ps1
```