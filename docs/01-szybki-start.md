# Szybki start

## Gotowy EXE

1. Uruchom `OpenGD77PromptStudio.exe`.
2. W trybie ręcznym wybierz plik `Wordlist CSV`.
3. Wpisz nazwę głosu. To jest też nazwa folderu roboczego na pliki audio, np. `Polish` albo `Kazek`.
4. Wybierz plik wyjściowy VPR.
5. Wybierz operacje.
6. Wskaż `ffmpeg.exe`, jeśli nie jest w zmiennej PATH.
7. Wskaż port COM radia, jeśli zaznaczasz kodowanie AMBE.
8. Naciśnij `Uruchom Alt+R`.

## Operacje

`Pobierz mowę z TTSMP3` pobiera pliki MP3 i od razu konwertuje je do RAW przez ffmpeg.

`Koduj AMBE przez radio` wysyła surowe próbki PCM do radia i odbiera zakodowane ramki AMBE. Radio musi mieć OpenGD77 i działać w trybie, który obsługuje komendy CPS.

`Zbuduj plik VPR` składa pliki `.amb` do kontenera VPR. Program tworzy dwa pliki: `UV380-like` oraz `monochrome`.

## Tryb z plikiem konfiguracyjnym

Tryb `Plik konfiguracyjny CSV` uruchamia wiele zestawów naraz. Przykład jest w `examples/config_sample.csv`.

## Skróty

- `Alt+R`: uruchom.
- `Alt+S`: zatrzymaj proces potomny.
- `Alt+L`: przejdź do logu.
- `F5`: odśwież porty COM.