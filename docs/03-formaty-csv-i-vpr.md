# Formaty CSV, próbek i VPR

## Wordlist CSV

Minimalne kolumny:

```csv
PromptName,PromptSpeechPrefix,PromptText,PromptSpeechPostfix
```

Znaczenie:

- `PromptName`: identyfikator promptu. Tak samo nazywa się plik `.mp3`, `.raw` i `.amb`.
- `PromptSpeechPrefix`: opcjonalny prefiks tekstu dla TTS.
- `PromptText`: właściwy tekst wypowiadany przez syntezę.
- `PromptSpeechPostfix`: opcjonalny dopisek po tekście.

Przykład jest w `examples/wordlist_sample.csv`.

## Config CSV

Kolumny trybu konfiguracyjnego:

```csv
Wordlist_file,Voice_name,Voice_pack_name,Download,Encode,Createpack,Volume_change_db,Remove_silence,Audio_tempo
```

Wartości `Download`, `Encode`, `Createpack` i `Remove_silence` przyjmują `y` albo `n`.

## Surowe próbki przed AMBE

Po pobraniu TTS program wywołuje `ffmpeg` i tworzy pliki RAW w formacie:

- PCM signed 16-bit little endian,
- 8000 Hz,
- mono,
- bez nagłówka WAV,
- rozszerzenie `.raw`.

To jest strumień próbek wysyłany do radia do kompresji AMBE.

## Pliki AMBE

Pliki `.amb` zawierają ramki AMBE odebrane z radia. Program nie koduje AMBE programowo, tylko używa radia jako sprzętowego kodera.

## Kontener VPR

Kontener VPR tworzony przez program składa się z nagłówka, tablicy końcowych offsetów promptów i danych AMBE.

Początek pliku:

- bajty magiczne: `56 50 00 00`, czyli `VP\0\0`,
- wersja `08 00 00 00` dla `monochrome`,
- wersja `09 00 00 00` dla `UV380-like`,
- tablica offsetów po 4 bajty little endian.

Limity promptów:

- `monochrome`: 331 pozycji,
- `UV380-like`: 368 pozycji.

Limit rozmiaru gotowego VPR w kodzie: `0x28C00` bajtów.