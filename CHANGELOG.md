# Changelog

## 0.4.4 - 2026-05-17

- Zakladki maja teraz numeracje dla czytnikow ekranu, np. `Zakladka 1 z 5: Projekt`, zeby bylo jasne, na ktorej zakladce znajduje sie fokus.

## 0.4.3 - 2026-05-17

- Zastapiono natywny pasek `wx.Notebook` dostepnym paskiem zakladek z radiobuttonow. NVDA widzi teraz kazda zakladke jako zwykla kontrolke z nazwa.
- Po starcie fokus trafia na radiobutton `Projekt` w pasku zakladek.
- Usunieto widoczne pole wyboru `ffmpeg.exe` z GUI. Standardowy EXE korzysta z wbudowanego ffmpeg automatycznie, a tryb serwisowy moze nadal uzyc `FFMPEG_EXE` albo pliku obok programu.
- Usunieto widoczne pole `RHVoice.dll` z GUI, zeby NVDA nie czytal tymczasowej sciezki `_MEI`; DLL jest wykrywana automatycznie.

## 0.4.2 - 2026-05-17

- Po starcie GUI fokus czytnika ekranu trafia na pasek zakladek z wybrana pierwsza zakladka `Projekt`, zamiast do pola wordlisty.
## 0.4.1 - 2026-05-17

- Poprawiono dostepnosc zakladek: dodano liste wyboru aktywnej zakladki, przyciski poprzednia/nastepna zakladka oraz skroty Ctrl+Tab, Ctrl+Shift+Tab, Ctrl+PageUp/Ctrl+PageDown i Alt+1..Alt+5.
- Domyslny folder roboczy jest teraz w `%APPDATA%\OpenGD77PromptStudio\work`, a plik wynikowy w dokumentach aktualnego uzytkownika.
- Pole `ffmpeg.exe` jest domyslnie puste, bo standardowy EXE uzywa wbudowanego ffmpeg automatycznie i nie pokazuje lokalnej sciezki z komputera budujacego.
- Usunieto runtime'owa podpowiedz do developerskiego folderu `fmdx-webserver-src`.

## 0.4.0 - 2026-05-17

- GUI wxPython zostalo podzielone na zakladki: Projekt, Mowa, Opcje, Praca oraz Aktualizacja i pomoc.
- Dodano profile ustawien zapisywane jako JSON w `%APPDATA%\OpenGD77PromptStudio\profiles`.
- Dodano bezposredni aktualizator oparty o GitHub Releases repozytorium `kazek5p-git/OpenGD77-PromptStudio`.
- Ostatnia zakladka zawiera aktualizacje, linki do GitHuba, pomoc i informacje o autorze `kazek5p`.

## 0.3.6 - 2026-05-17

- Dodano osobne tempo dla pojedynczych liter, cyfr, spacji i kropki.
- GUI ma nowe pole `Tempo liter/cyfr`; CLI ma parametr `-l` oraz `--letter-tempo`.
- Tryb CSV obsluguje opcjonalna kolumne `Compact_audio_tempo` albo zgodnosciowo `Letter_audio_tempo`.
- Folder roboczy RAW/AMBE zawiera teraz dopisek `_letters_<tempo>`, jezeli tempo liter/cyfr rozni sie od zwyklego tempa.

## 0.3.5 - 2026-05-17

- Build jednoplikowego EXE bundluje teraz `ffmpeg.exe`, jezeli jest dostepny lokalnie podczas budowania.
- Program wykrywa `ffmpeg.exe` wbudowany przez PyInstaller i uzywa go bez wpisywania sciezki.

## 0.3.4 - 2026-05-17

- Dodano regulacje wysokosci glosu RHVoice przez pole `Wysokosc RHVoice` w GUI i parametr `-p`.
- Tryb CSV obsluguje opcjonalna kolumne `RHVoice_pitch`; `1.0` oznacza normalna wysokosc, mniejsze wartosci obnizaja glos.

## 0.3.3 - 2026-05-17

- Dodano dostępny dla NVDA pasek postępu oraz pole `Postęp pracy` ze skrótem Alt+P.
- GUI pokazuje postęp syntezy RAW, kodowania AMBE i budowania VPR na podstawie logu buildera.

## 0.3.2 - 2026-05-17

- Puste wpisy w wordliscie, na przyk?ad `PROMPT_SPACE`, sa teraz zapisywane jako krotka cisza zamiast przerywac synteze RHVoice.

## 0.3.1 - 2026-05-17

- Zmieniono GUI z Tkinter na wxPython, bo NVDA nie odczytywal poprawnie kontrolek Tk w gotowym EXE.
- Dodano jawne nazwy dostepnosciowe dla pol edycji, przyciskow, checkboxow, radiobuttonow i listy portow.

## 0.3.0

- Domyslny build EXE bundluje `RHVoice.dll`, jezeli jest dostepny lokalnie.
- Gotowy release pozwala uzyc glosu RHVoice `.nvda-addon` bez instalowania dodatku NVDA `RHVoice` i bez recznego wskazywania DLL.
- Dodano parametr builda `-NoBundledRhVoice` do tworzenia wariantu bez wbudowanego silnika.
- Dodano `licenses/RHVoice-GPL-3.0.txt` i `THIRD_PARTY_NOTICES.md`.

## 0.2.0

- Dodano zrodlo mowy `Dodatek NVDA/RHVoice`.
- Dodano opcje CLI `-N=<nvda_addon>` i `-L=<RHVoice.dll>`.
- Program rozpoznaje glosy RHVoice w plikach `.nvda-addon`, rozpakowuje je do folderu roboczego i generuje WAV/RAW lokalnie.
- Dodano wykrywanie `RHVoice.dll` z dodatku NVDA RHVoice, folderu programu, `_MEIPASS` PyInstaller albo zmiennej `RHVOICE_DLL`.
- GUI ma pola wyboru `.nvda-addon` i opcjonalnego `RHVoice.dll`.
- Dodano dokumentacje dodatkow NVDA/RHVoice.

## 0.1.0

- Utworzono osobny projekt OpenGD77 Prompt Studio.
- Dodano dostepne GUI uruchamiane bez argumentow.
- Dodano obsluge dzialania jako PyInstaller onefile EXE.
- Dodano dokumentacje, przykladowe CSV i skrypty budowania/testowania.
- Poprawiono `-h` i `--help`, aby konczyly sie kodem 0.
