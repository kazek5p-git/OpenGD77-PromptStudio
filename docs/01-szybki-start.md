# Szybki start

## Gotowy EXE

1. Pobierz `OpenGD77PromptStudio.exe` z najnowszego release GitHub.
2. Uruchom program.
3. Jezeli chcesz zmienic jezyk, na zakladce `Projekt` ustaw `Jezyk interfejsu`: `Polski` albo `English`.
4. Po zmianie jezyka program zapyta, czy uruchomic sie ponownie. `Tak` startuje nowe okno i zamyka aktualne, `Nie` zostawia zmiane do nastepnego uruchomienia.
5. W trybie recznym wybierz plik `Wordlist CSV`.
6. Wpisz `Nazwa glosu`. To jest tez nazwa folderu roboczego na pliki audio, np. `Polish`, `Kazek`, `Zuza` albo `Natan`.
7. Wybierz `Plik wynikowy VPR`.
8. Na zakladce `Mowa` wybierz zrodlo: `TTSMP3.com` albo `RHVoice z dodatku NVDA`.
9. Przy zrodle RHVoice wskaz plik `.nvda-addon` z glosem.
10. Wybierz operacje: `Pobierz / syntezuj audio`, `Koduj AMBE w radiu`, `Zbuduj VPR`.
11. W standardowym EXE nie wybierasz `ffmpeg.exe` ani `RHVoice.dll`; sa wbudowane i wykrywane automatycznie.
12. Wskaz port COM radia, jesli zaznaczasz kodowanie AMBE.
13. Opcjonalnie ustaw `Tempo`, `Tempo liter/cyfr`, `Alias tempa`, `Glosnosc dB`, `Wysokosc RHVoice`, `Nadpisuj istniejace pliki` i `Usun cisze z poczatku`.
14. Nacisnij `Uruchom Alt+R`.

## Zrodla mowy

`TTSMP3.com` pobiera mowe z internetu, zapisuje MP3 i konwertuje je lokalnie przez wbudowany ffmpeg.

`RHVoice z dodatku NVDA` uzywa lokalnego pliku `.nvda-addon` z glosem RHVoice. Program rozpakowuje glos do folderu roboczego, generuje WAV lokalnie i konwertuje WAV do RAW przez ffmpeg.

Nie kazdy `.nvda-addon` jest glosem. Obslugiwane sa dodatki RHVoice z plikami `data/voice.info`, `data/voice.params` i `langdata`.

## Wybieranie glosu RHVoice

Pole `Nazwa glosu` ma dwa znaczenia:

- jest nazwa folderu na pliki audio,
- przy RHVoice jest tez nazwa profilu glosu, jezeli taki profil istnieje w dodatku.

Przyklad: jezeli dodatek zawiera profile `Kazek`, `Zuza` i `Natan`, wpisanie `Zuza` wybierze profil `Zuza`. Jezeli wpisana nazwa nie istnieje w dodatku, program uzyje pierwszego profilu zwroconego przez RHVoice i zapisze to w logu.

## Operacje

`Pobierz / syntezuj audio` tworzy pliki mowy ze zrodla wybranego na zakladce `Mowa`.

`Koduj AMBE w radiu` wysyla surowe probki PCM do radia i odbiera zakodowane ramki AMBE. Radio musi miec OpenGD77 i dzialac w trybie obslugujacym komendy CPS.

`Zbuduj VPR` sklada pliki `.amb` do kontenera VPR. Program tworzy dwa pliki: `UV380-like` oraz `monochrome`.

## Jaki wariant VPR wybrac

`UV380-like` wybierz dla kolorowych i nowszych radii OpenGD77, m.in. TYT MD-UV380/MD-UV390, Retevis RT3S, TYT MD-9600/Retevis RT-90, TYT MD-2017/Retevis RT-82 oraz Baofeng DM-1701/Retevis RT-84.

`monochrome` wybierz dla starszej rodziny z monochromatycznym ekranem, m.in. Radioddity GD-77/GD-77S, Baofeng DM-1801/DM-1801A oraz Baofeng RD-5R.

Retevis RT3 bez S nie jest tym samym co RT3S. Jezeli radio to RT3S z GPS albo RT3S bez GPS, zostaje `UV380-like`.

## Tryb z plikiem konfiguracyjnym

Tryb `Plik konfiguracyjny CSV` uruchamia wiele zestawow naraz. Po wybraniu tego trybu program wykonuje ustawienia zapisane w CSV, a wiele pol trybu recznego jest pomijanych.

Przyklad jest w `examples/config_sample.csv`.

## Skroty

- `Alt+R`: uruchom.
- `Alt+S`: zatrzymaj proces potomny.
- `Alt+L`: przejdz do logu.
- `Alt+P`: przejdz do pola postepu.
- `F5`: odswiez porty COM.
- `Ctrl+Tab` albo `Ctrl+PageDown`: nastepna zakladka.
- `Ctrl+Shift+Tab` albo `Ctrl+PageUp`: poprzednia zakladka.
- `Alt+1` do `Alt+5`: bezposredni wybor zakladki.

## Profile ustawien

Na zakladce `Projekt` wpisz nazwe profilu i wybierz `Zapisz profil`, zeby zachowac aktualne sciezki i opcje. `Wczytaj profil` przywraca zapisane ustawienia, `Usun profil` kasuje profil, a `Folder profili` otwiera katalog profili w Eksploratorze.

Profile sa zapisywane w `%APPDATA%\OpenGD77PromptStudio\profiles` jako pliki JSON.

## Aktualizacja programu

Na ostatniej zakladce `Aktualizacja i pomoc` uzyj `Sprawdz aktualizacje`, a potem `Pobierz i zainstaluj`, jezeli GitHub ma nowszy release.

W gotowym EXE aktualizator pobiera nowy plik, zamyka program, podmienia EXE i uruchamia go ponownie. Przy pracy ze zrodel program pobiera EXE do `%APPDATA%\OpenGD77PromptStudio\updates`, ale nie podmienia uruchomionego Pythona.

## Domyslne foldery

Domyslny folder roboczy to `%APPDATA%\OpenGD77PromptStudio\work`. Domyslny plik wynikowy trafia do folderu `OpenGD77PromptStudio` w dokumentach aktualnego uzytkownika. Ustawienia jezyka sa w `%APPDATA%\OpenGD77PromptStudio\settings.json`.