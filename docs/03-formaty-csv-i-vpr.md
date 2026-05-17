# Formaty CSV, probek i VPR

## Wordlist CSV

Minimalne kolumny:

```csv
PromptName,PromptSpeechPrefix,PromptText,PromptSpeechPostfix
```

Znaczenie:

- `PromptName`: identyfikator promptu. Tak samo nazywa sie plik `.mp3`, `.wav`, `.raw` i `.amb`.
- `PromptSpeechPrefix`: opcjonalny prefiks tekstu dla TTS.
- `PromptText`: wlasciwy tekst wypowiadany przez synteze.
- `PromptSpeechPostfix`: opcjonalny dopisek po tekscie.

Przyklad jest w `examples/wordlist_sample.csv`.

## Config CSV

Kolumny trybu konfiguracyjnego:

```csv
Wordlist_file,Voice_name,Voice_pack_name,Download,Encode,Createpack,Volume_change_db,Remove_silence,Audio_tempo,Compact_audio_tempo,Nvda_addon_file,RHVoice_dll,RHVoice_pitch
```

Wartosci `Download`, `Encode`, `Createpack` i `Remove_silence` przyjmuja `y` albo `n`.

`Nvda_addon_file` jest opcjonalne. Jezeli `Download` ma wartosc `y` i `Nvda_addon_file` jest wypelnione, program uzyje lokalnego RHVoice z dodatku NVDA zamiast TTSMP3.

`RHVoice_dll` jest opcjonalne. Jezeli jest puste, program sprobuje wykryc DLL automatycznie.

`Compact_audio_tempo` jest opcjonalne. Ustawia osobne tempo dla pojedynczych liter, cyfr, spacji i kropki. Jezeli jest puste, program uzywa wartosci `Audio_tempo`. Dla zgodnosci akceptowana jest tez kolumna `Letter_audio_tempo`.

`RHVoice_pitch` jest opcjonalne. Wartosc `1.0` oznacza normalna wysokosc glosu; np. `0.94` delikatnie obniza glos RHVoice.

## Surowe probki przed AMBE

Po pobraniu albo lokalnej syntezie program wywoluje `ffmpeg` i tworzy pliki RAW w formacie:

- PCM signed 16-bit little endian,
- 8000 Hz,
- mono,
- bez naglowka WAV,
- rozszerzenie `.raw`.

To jest strumien probek wysylany do radia do kompresji AMBE.

Jezeli tempo liter/cyfr rozni sie od zwyklego tempa, folder RAW/AMBE dostaje nazwe w stylu `tempo_1.5_letters_1.2`, zeby nie pomieszac probek ze starszymi ustawieniami.

## Pliki WAV z RHVoice

Przy zrodle `Dodatek NVDA/RHVoice` program zapisuje tymczasowe pliki `.wav` w folderze glosu. Ich probkowanie zalezy od modelu RHVoice, zwykle 16000 Hz albo 24000 Hz. Dopiero ffmpeg przeksztalca je do 8000 Hz RAW.

## Pliki AMBE

Pliki `.amb` zawieraja ramki AMBE odebrane z radia. Program nie koduje AMBE programowo, tylko uzywa radia jako sprzetowego kodera.

## Kontener VPR

Kontener VPR tworzony przez program sklada sie z naglowka, tablicy koncowych offsetow promptow i danych AMBE.

Poczatek pliku:

- bajty magiczne: `56 50 00 00`, czyli `VP\0\0`,
- wersja `08 00 00 00` dla `monochrome`,
- wersja `09 00 00 00` dla `UV380-like`,
- tablica offsetow po 4 bajty little endian.

Limity promptow:

- `monochrome`: 331 pozycji,
- `UV380-like`: 368 pozycji.

Limit rozmiaru gotowego VPR w kodzie: `0x28C00` bajtow.

### Zgodnosc wariantow z radiami

`UV380-like` jest dla kolorowych i nowszych radii OpenGD77: TYT MD-UV380/MD-UV390, Retevis RT3S, TYT MD-9600/Retevis RT-90, TYT MD-2017/Retevis RT-82 oraz Baofeng DM-1701/Retevis RT-84.

`monochrome` jest dla starszej rodziny z monochromatycznym ekranem: Radioddity GD-77/GD-77S, Baofeng DM-1801/DM-1801A oraz Baofeng RD-5R.

Retevis RT3 bez S nie powinien byc traktowany jak RT3S. Wersja RT3S z GPS i bez GPS uzywa wariantu `UV380-like`.
