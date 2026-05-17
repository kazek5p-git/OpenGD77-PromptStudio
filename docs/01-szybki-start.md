# Szybki start

## Gotowy EXE

1. Uruchom `OpenGD77PromptStudio.exe`.
2. W trybie recznym wybierz plik `Wordlist CSV`.
3. Wpisz nazwe glosu. To jest tez nazwa folderu roboczego na pliki audio, np. `Polish`, `Kazek` albo `Zuza`.
4. Wybierz plik wyjsciowy VPR.
5. Wybierz zrodlo mowy.
6. Wybierz operacje.
7. W standardowym EXE nie wybierasz `ffmpeg.exe`; program uzywa wbudowanego ffmpeg automatycznie.
8. Wskaz port COM radia, jesli zaznaczasz kodowanie AMBE.
9. Opcjonalnie ustaw `Tempo liter/cyfr`, jezeli pojedyncze litery albo cyfry maja byc wolniejsze lub szybsze niz reszta promptow.
10. Nacisnij `Uruchom Alt+R`.

## Zrodla mowy

`TTSMP3` pobiera mowe z internetu, zapisuje MP3 i konwertuje je do RAW przez ffmpeg.

`Dodatek NVDA/RHVoice` uzywa lokalnego pliku `.nvda-addon` z glosem RHVoice. Program rozpakowuje glos do folderu roboczego, generuje WAV lokalnie i konwertuje WAV do RAW przez ffmpeg.

Nie kazdy `.nvda-addon` jest glosem. Obslugiwane sa dodatki RHVoice z plikami `data/voice.info`, `data/voice.params` i `langdata`.

## Operacje

`Utworz pliki mowy` pobiera albo generuje audio, zaleznie od wybranego zrodla mowy.

`Koduj AMBE przez radio` wysyla surowe probki PCM do radia i odbiera zakodowane ramki AMBE. Radio musi miec OpenGD77 i dzialac w trybie, ktory obsluguje komendy CPS.

`Zbuduj plik VPR` sklada pliki `.amb` do kontenera VPR. Program tworzy dwa pliki: `UV380-like` oraz `monochrome`.

## Tryb z plikiem konfiguracyjnym

Tryb `Plik konfiguracyjny CSV` uruchamia wiele zestawow naraz. Przyklad jest w `examples/config_sample.csv`.

## Skroty

- `Alt+R`: uruchom.
- `Alt+S`: zatrzymaj proces potomny.
- `Alt+L`: przejdz do logu.
- `F5`: odswiez porty COM.


## Profile ustawien

Na zakladce `Projekt` wpisz nazwe profilu i wybierz `Zapisz profil`, zeby zachowac aktualne sciezki i opcje. `Wczytaj profil` przywraca zapisane ustawienia.

## Aktualizacja programu

Na ostatniej zakladce `Aktualizacja i pomoc` uzyj `Sprawdz aktualizacje`, a potem `Pobierz i zainstaluj`, jezeli GitHub ma nowszy release.

## Domyslne foldery

Domyslny folder roboczy to `%APPDATA%\OpenGD77PromptStudio\work`. Domyslny plik wynikowy trafia do folderu `OpenGD77PromptStudio` w dokumentach aktualnego uzytkownika. Program nie powinien pokazywac sciezek z komputera osoby, ktora zbudowala EXE.
