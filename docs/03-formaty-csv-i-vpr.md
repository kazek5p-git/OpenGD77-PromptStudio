# Formaty CSV, probek, profili i VPR

## Kodowanie i separator CSV

Program wczytuje wordlist CSV i config CSV w najczestszych wariantach spotykanych na Windows:

- UTF-8 bez BOM,
- UTF-8 z BOM,
- UTF-16 z BOM,
- UTF-16 bez BOM, jezeli uklad bajtow jednoznacznie wskazuje UTF-16,
- ANSI/Windows-1250,
- awaryjnie Windows-1252 i Latin-1.

Separator jest wykrywany automatycznie na podstawie naglowka. Obslugiwane sa:

- przecinek,
- srednik,
- tabulator.

Program usuwa niewidoczny znak BOM i spacje z nazw kolumn oraz toleruje wielkosc liter w znanych naglowkach. To oznacza, ze plik zapisany przez Excel, LibreOffice albo Notatnik Windows zwykle powinien wczytac sie bez recznego konwertowania. Nazwy wymaganych kolumn nadal musza miec poprawna tresc, np. `PromptName`, a nie `Prompt Name`.

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

Wiersze zaczynajace sie od `#` sa traktowane jako komentarze i pomijane.

Puste wpisy w wordliscie, na przyklad prompt spacji, sa obslugiwane jako krotka cisza zamiast bledu syntezy RHVoice.

Przyklad jest w `examples/wordlist_sample.csv`.

## Config CSV

Tryb `Plik konfiguracyjny CSV` sluzy do uruchamiania wielu zestawow naraz.

Kolumny trybu konfiguracyjnego:

```csv
Wordlist_file,Voice_name,Voice_pack_name,Download,Encode,Createpack,Volume_change_db,Remove_silence,Audio_tempo,Compact_audio_tempo,Nvda_addon_file,RHVoice_dll,RHVoice_pitch
```

Znaczenie najwazniejszych pol:

- `Wordlist_file`: sciezka do wordlist CSV.
- `Voice_name`: nazwa glosu i folderu audio. Przy RHVoice moze byc tez nazwa profilu glosu.
- `Voice_pack_name`: bazowa nazwa wynikowego pliku VPR.
- `Download`: `y` albo `n`; tworzy audio przez TTSMP3 albo RHVoice.
- `Encode`: `y` albo `n`; koduje RAW do AMBE przez radio.
- `Createpack`: `y` albo `n`; buduje pliki VPR.
- `Volume_change_db`: zmiana glosnosci w dB.
- `Remove_silence`: `y` albo `n`; usuwa poczatkowa cisze, jezeli dany etap moze to zastosowac.
- `Audio_tempo`: tempo audio od `0.5` do `2`.
- `Compact_audio_tempo`: osobne tempo pojedynczych liter, cyfr, spacji i kropki.
- `Nvda_addon_file`: opcjonalna sciezka do glosu RHVoice `.nvda-addon`.
- `RHVoice_dll`: opcjonalna sciezka do `RHVoice.dll` w trybie serwisowym.
- `RHVoice_pitch`: opcjonalna wysokosc RHVoice; `1.0` to normalna wysokosc.

Dla zgodnosci akceptowana jest tez kolumna `Letter_audio_tempo`, jezeli nie ma `Compact_audio_tempo`.

## Profile GUI JSON

Profile GUI sa w `%APPDATA%\OpenGD77PromptStudio\profiles` i maja rozszerzenie `.json`.

Profil zapisuje m.in.:

- tryb pracy,
- sciezke config CSV,
- wordlist CSV,
- nazwe glosu,
- wynikowy VPR,
- port COM,
- operacje: download, encode, build,
- zrodlo mowy: TTSMP3 albo NVDA/RHVoice,
- sciezke `.nvda-addon`,
- folder roboczy,
- glosnosc, tempo, tempo liter/cyfr, alias tempa,
- wysokosc RHVoice,
- `Nadpisuj istniejace pliki`,
- `Usun cisze z poczatku`.

Jezyk interfejsu nie jest czescia profilu. Jest globalnym ustawieniem w `%APPDATA%\OpenGD77PromptStudio\settings.json`.

## Settings JSON

Plik `%APPDATA%\OpenGD77PromptStudio\settings.json` przechowuje ustawienia programu niezalezne od profili. Aktualnie najwazniejsze pole to:

```json
{
  "ui_language": "pl"
}
```

Dozwolone wartosci:

- `pl`: polski interfejs,
- `en`: angielski interfejs.

## Surowe probki przed AMBE

Po pobraniu albo lokalnej syntezie program wywoluje `ffmpeg` i tworzy pliki RAW w formacie:

- PCM signed 16-bit little endian,
- 8000 Hz,
- mono,
- bez naglowka WAV,
- rozszerzenie `.raw`.

To jest strumien probek wysylany do radia do kompresji AMBE.

Jezeli tempo liter/cyfr rozni sie od zwyklego tempa, folder RAW/AMBE dostaje nazwe w stylu `tempo_1.5_letters_1.2`, zeby nie pomieszac probek ze starszymi ustawieniami.

## Pliki WAV i MP3

Przy zrodle `TTSMP3.com` program zapisuje pliki `.mp3`, a potem konwertuje je do RAW.

Przy zrodle `RHVoice z dodatku NVDA` program zapisuje tymczasowe pliki `.wav` w folderze glosu. Ich probkowanie zalezy od modelu RHVoice, zwykle 16000 Hz albo 24000 Hz. Dopiero ffmpeg przeksztalca je do 8000 Hz RAW.

## Pliki AMBE

Pliki `.amb` zawieraja ramki AMBE odebrane z radia. Program nie koduje AMBE programowo, tylko uzywa radia jako sprzetowego kodera.

## Nazwy wynikowych plikow

`Plik wynikowy VPR` jest bazowa nazwa. Program dopisuje wariant radia i tempo, zeby rozroznic wyniki.

Przyklady nazw:

```text
voice_prompts-UV380-like-tempo_1.5.vpr
voice_prompts-monochrome-tempo_1.5.vpr
voice_prompts-UV380-like-czytelny.vpr
```

`Alias tempa` zastapi liczbe tempa w nazwie wyniku. Nie zmienia dzwieku.

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

## Zgodnosc wariantow z radiami

`UV380-like` jest dla kolorowych i nowszych radii OpenGD77: TYT MD-UV380/MD-UV390, Retevis RT3S, TYT MD-9600/Retevis RT-90, TYT MD-2017/Retevis RT-82 oraz Baofeng DM-1701/Retevis RT-84.

`monochrome` jest dla starszej rodziny z monochromatycznym ekranem: Radioddity GD-77/GD-77S, Baofeng DM-1801/DM-1801A oraz Baofeng RD-5R.

Retevis RT3 bez S nie powinien byc traktowany jak RT3S. Wersja RT3S z GPS i bez GPS uzywa wariantu `UV380-like`.