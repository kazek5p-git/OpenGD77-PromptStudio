# Rozwiazywanie problemow

## Program nie startuje albo od razu sie zamyka

Najpierw sprawdz najnowszy release GitHub i pobierz `OpenGD77PromptStudio.exe` jeszcze raz.

Jezeli budujesz samodzielnie, zrob build z konsola diagnostyczna:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -Console
```

Potem uruchom `dist\OpenGD77PromptStudio.exe` z PowerShella i sprawdz komunikat bledu.

## CSV nie wczytuje sie albo pokazuje `PromptName`

Od wersji `0.4.9` program sam wykrywa typowe kodowania CSV: UTF-8 bez BOM, UTF-8 z BOM, UTF-16 z BOM, UTF-16 bez BOM oraz ANSI/Windows-1250. Sam wykrywa tez separator: przecinek, srednik albo tabulator.

Jezeli blad nadal mowi o brakujacej kolumnie, to najczesciej problemem nie jest kodowanie, tylko faktyczna nazwa naglowka. Dla wordlisty wymagane sa dokladnie: `PromptName`, `PromptSpeechPrefix`, `PromptText`, `PromptSpeechPostfix`. Komunikat bledu pokazuje wykryte kolumny, kodowanie i separator.

## Windows blokuje pobrany EXE

Po pobraniu z internetu Windows moze pokazac SmartScreen albo oznaczyc plik jako pobrany z sieci. Jezeli ufasz plikowi z release, odblokuj go we wlasciwosciach pliku albo uruchom mimo ostrzezenia.

## Aktualizacja z GitHuba nie dziala

Zakladka `Aktualizacja i pomoc` sprawdza najnowszy release w repozytorium `kazek5p-git/OpenGD77-PromptStudio`. Aktualizator szuka assetu `OpenGD77PromptStudio.exe`.

W gotowym EXE program po pobraniu zamyka sie, podmienia plik i uruchamia ponownie. Przy pracy ze zrodel pobiera EXE do `%APPDATA%\OpenGD77PromptStudio\updates`, ale nie podmienia uruchomionego Pythona.

Jezeli podmiana sie nie udaje, zamknij wszystkie okna Prompt Studio i uruchom pobrany EXE recznie.

## Build konczy sie bledem odmowy dostepu

Jezeli PyInstaller pokazuje `PermissionError`, `WinError 5` albo `Odmowa dostepu` przy pliku `dist\OpenGD77PromptStudio.exe`, najczesciej dziala juz stary EXE z tego folderu.

Zamknij wszystkie okna Prompt Studio i uruchom build ponownie:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1
```

Nie tworz alternatywnych folderow `dist-v...`, jezeli nie jest to swiadome jednorazowe obejscie. Standardowym miejscem wyniku jest `dist\OpenGD77PromptStudio.exe`.

## Jezyk interfejsu nie zmienil sie od razu

Po zmianie `Jezyk interfejsu` program pyta, czy uruchomic sie ponownie.

- `Tak`: program startuje nowe okno i zamyka stare.
- `Nie`: zmiana zostaje zapisana do nastepnego uruchomienia.

Ustawienie jest w `%APPDATA%\OpenGD77PromptStudio\settings.json`. Jezeli ustawienie jest uszkodzone, zamknij program i usun ten plik. Program odtworzy go przy kolejnej zmianie ustawien.

## NVDA czyta zakladki w zlej kolejnosc

Od wersji `0.4.8` radiobutton zakladki ma nazwe, np. `Projekt`, a numer pozycji jest opisem, np. `Zakladka 1 z 5`. Oczekiwany odczyt to mniej wiecej:

```text
Projekt  przycisk opcji  oznaczone  Zakladka 1 z 5
```

Jezeli NVDA nadal czyta stary format `Zakladka 1 z 5: Projekt`, upewnij sie, ze uruchamiasz wersje `0.4.8` albo nowsza. Sprawdz `O programie` na zakladce `Aktualizacja i pomoc`.

## Widze sciezke z komputera Kazka

Standardowy EXE nie powinien pokazywac `C:\Users\Kazek\...` w domyslnych polach. Folder roboczy jest tworzony w `%APPDATA%`, wynikowy VPR w dokumentach aktualnego uzytkownika, a pola wyboru `ffmpeg.exe` i `RHVoice.dll` nie sa pokazywane w glownym GUI.

Jezeli stara sciezka jest nadal widoczna, pochodzi najpewniej ze starego profilu JSON. Otworz `Folder profili`, usun albo popraw stary profil i uruchom program ponownie.

## Brak ffmpeg

Jesli zaznaczasz tworzenie mowy, program potrzebuje `ffmpeg.exe` do konwersji audio.

Mozliwe rozwiazania:

- uzyj standardowego EXE, w ktorym ffmpeg jest wbudowany i wykrywany automatycznie,
- w wersji serwisowej ustaw zmienna `FFMPEG_EXE`,
- skopiuj `ffmpeg.exe` obok EXE,
- dodaj folder ffmpeg do PATH.

## Dodatek NVDA nie dziala

Program obsluguje tylko glosy RHVoice w paczkach `.nvda-addon`. Taki dodatek musi zawierac `data/voice.info`, `data/voice.params` i `langdata`.

Jezeli plik jest zwyklym pluginem NVDA albo dodatkiem innego syntezatora, program pokaze blad, ze to nie jest glos RHVoice.

## Brak RHVoice.dll

Dla zrodla `RHVoice z dodatku NVDA` potrzebny jest silnik RHVoice. Gotowy EXE z release ma go wbudowanego. Jezeli uzywasz builda bez wbudowanego silnika, program szuka go w tych miejscach:

- zmienna srodowiskowa `RHVOICE_DLL`,
- plik `RHVoice.dll` obok EXE,
- folder `rhvoice\RHVoice.dll` obok EXE,
- zainstalowany dodatek NVDA `RHVoice` w profilu uzytkownika,
- zasoby `_MEIPASS` w buildzie PyInstaller.

## Nie moge wybrac glosu Kazek, Zuza albo Natan

Przy RHVoice nazwa wpisana w `Nazwa glosu` musi odpowiadac profilowi, ktory faktycznie jest w wybranym `.nvda-addon`. Program wypisuje dostepne profile w logu jako `RHVoice profiles: ...`.

Jezeli wpisana nazwa nie istnieje, program uzyje pierwszego profilu z dodatku. Popraw `Nazwa glosu` albo uzyj dodatku zawierajacego dany profil.

## Brak portu COM radia

Nacisnij `F5` albo przycisk `Odswiez porty`. Jesli port nadal sie nie pojawia, sprawdz sterownik USB i czy radio jest widoczne w Menedzerze urzadzen.

## Kodowanie AMBE nie dziala

Kodowanie wymaga radia z OpenGD77, ktore obsluguje komendy uzywane przez builder. Sam komputer nie koduje AMBE.

Sprawdz:

- czy wybrany port COM jest poprawny,
- czy radio jest wlaczone i podlaczone,
- czy inne programy nie trzymaja portu COM,
- czy zaznaczono `Koduj AMBE w radiu`.

## Plik VPR jest za duzy

Kod usuwa plik, jesli przekroczy limit `0x28C00` bajtow. Pomaga skrocenie komunikatow, mniejsza liczba promptow albo spokojniejsze ustawienia TTS, ktore generuja krotszy dzwiek.

## TTSMP3 nie odpowiada

TTSMP3 to zewnetrzna usluga internetowa. Jesli zwraca blad, sprobuj pozniej albo uzyj lokalnego zrodla RHVoice.

## Program uzywa starych plikow audio

Jezeli zmieniles glos, tempo, glosnosc, wysokosc glosu albo teksty promptow, zaznacz `Nadpisuj istniejace pliki`. Bez tego program moze uzyc istniejacych plikow WAV, MP3, RAW albo AMBE, jezeli je znajdzie.