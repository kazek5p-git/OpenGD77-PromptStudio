# Spis dokumentacji

Dokumentacja dotyczy OpenGD77 Prompt Studio `0.4.9`.

## Kolejnosc czytania

1. `01-szybki-start.md` - pierwszy przebieg w GUI i najwazniejsze decyzje.
2. `02-dostepnosc-i-gui.md` - szczegolowy opis interfejsu, zakladek, NVDA, jezyka, profili i skrotow.
3. `03-formaty-csv-i-vpr.md` - formaty wordlist CSV, config CSV, profili JSON, probek RAW/AMBE i kontenera VPR.
4. `04-budowanie-exe.md` - budowanie jednoplikowego EXE, bundlowanie ffmpeg/RHVoice i testy.
5. `05-rozwiazywanie-problemow.md` - typowe problemy: start, aktualizacja, blokada EXE, port COM, RHVoice, ffmpeg, VPR.
6. `06-dodatki-nvda-rhvoice.md` - obsluga glosow RHVoice z dodatkow `.nvda-addon`.

## Najwazniejsze sciezki

- Program release: `OpenGD77PromptStudio.exe`.
- Wynik lokalnego builda: `dist\OpenGD77PromptStudio.exe`.
- Ustawienia programu: `%APPDATA%\OpenGD77PromptStudio\settings.json`.
- Profile GUI: `%APPDATA%\OpenGD77PromptStudio\profiles`.
- Folder roboczy: `%APPDATA%\OpenGD77PromptStudio\work`.
- Pobrane aktualizacje: `%APPDATA%\OpenGD77PromptStudio\updates`.
- Domyslny wynik VPR: `Dokumenty\OpenGD77PromptStudio\voice_prompts.vpr`.

## Najwazniejsze zmiany w aktualnym GUI

- Zakladki sa radiobuttonami, a nie natywnym paskiem `wx.Notebook`.
- Czytnik ekranu powinien najpierw czytac nazwe zakladki, np. `Projekt`, a numer pozycji jako opis, np. `Zakladka 1 z 5`.
- Interfejs ma wybor jezyka `Polski`/`English`.
- Po zmianie jezyka program pyta, czy uruchomic sie ponownie.
- Standardowy EXE ma wbudowany `ffmpeg.exe` i `RHVoice.dll`.
- CSV jest wczytywany tolerantnie: UTF-8, UTF-8 z BOM, UTF-16 i Windows-1250 oraz separatory przecinek/srednik/tabulator.
- Standardowe GUI nie pokazuje pol wyboru `ffmpeg.exe` ani `RHVoice.dll`, bo skladniki sa wykrywane automatycznie.