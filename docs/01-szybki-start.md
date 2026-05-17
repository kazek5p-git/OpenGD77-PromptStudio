# Szybki start

## Gotowy EXE

1. Uruchom `OpenGD77PromptStudio.exe`.
2. W trybie recznym wybierz plik `Wordlist CSV`.
3. Wpisz nazwe glosu. To jest tez nazwa folderu roboczego na pliki audio, np. `Polish`, `Kazek` albo `Zuza`.
4. Wybierz plik wyjsciowy VPR.
5. Wybierz zrodlo mowy.
6. Wybierz operacje.
7. Wskaz `ffmpeg.exe`, jesli nie jest w zmiennej PATH.
8. Wskaz port COM radia, jesli zaznaczasz kodowanie AMBE.
9. Nacisnij `Uruchom Alt+R`.

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
