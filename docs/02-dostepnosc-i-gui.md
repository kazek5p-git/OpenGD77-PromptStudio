# Dostepnosc i GUI

Interfejs jest zrobiony w `wxPython`, czyli korzysta z natywnych kontrolek Windows widocznych dla czytnikow ekranu. Glowne kontrolki maja jawne nazwy, opisy i tekst statusu.

## Zakladki

GUI jest podzielone na piec zakladek:

- `Projekt`: tryb pracy, jezyk interfejsu, profile ustawien, CSV, port COM i operacje.
- `Mowa`: wybor zrodla mowy i dodatku NVDA/RHVoice.
- `Opcje`: folder roboczy, glosnosc, tempo, tempo liter/cyfr, alias tempa, wysokosc RHVoice i opcje audio.
- `Praca`: przyciski uruchamiania, pasek postepu i log.
- `Aktualizacja i pomoc`: sprawdzanie GitHub Releases, pobieranie aktualizacji, linki, pomoc i autor.

Pasek zakladek jest zrobiony ze zwyklych radiobuttonow: `Projekt`, `Mowa`, `Opcje`, `Praca` oraz `Aktualizacja i pomoc`. Po uruchomieniu programu fokus trafia na `Projekt`.

Kazdy radiobutton ma jako nazwe sama nazwe zakladki. Numer pozycji jest podany jako opis dostepnosciowy. Dla NVDA oczekiwany uklad to na przyklad:

```text
Projekt  przycisk opcji  oznaczone  Zakladka 1 z 5
```

W jezyku angielskim analogicznie:

```text
Project  radio button  checked  Tab 1 of 5
```

Rzeczywista kolejnosc moze zalezec od ustawien gadatliwosci NVDA, ale program przekazuje nazwe jako `Projekt`, a opis jako `Zakladka 1 z 5`.

## Nawigacja po zakladkach

- `Strzalka w prawo` albo `Strzalka w dol`: nastepna zakladka, gdy fokus jest na pasku zakladek.
- `Strzalka w lewo` albo `Strzalka w gore`: poprzednia zakladka, gdy fokus jest na pasku zakladek.
- `Home`: pierwsza zakladka.
- `End`: ostatnia zakladka.
- `Ctrl+Tab` albo `Ctrl+PageDown`: nastepna zakladka.
- `Ctrl+Shift+Tab` albo `Ctrl+PageUp`: poprzednia zakladka.
- `Alt+1` do `Alt+5`: bezposredni wybor zakladki.
- Przyciski `Poprzednia` i `Nastepna` pozwalaja przelaczac zakladki bez skrotow klawiaturowych.

## Kontrolki

Program uzywa zwyklych elementow Windows: pola edycji, przyciski, checkboxy, radiobuttony, listbox, pasek postepu i pole tekstowe logu.

Po wejściu fokusem w wazne pole program aktualizuje tekst statusu. NVDA moze odczytac status opisujacy przeznaczenie kontrolki.

## Jezyk interfejsu

`Jezyk interfejsu` jest na zakladce `Projekt`. Dostepne wartosci:

- `Polski`,
- `English`.

Po zmianie jezyka program zapisuje ustawienie do `%APPDATA%\OpenGD77PromptStudio\settings.json` i pyta, czy uruchomic sie ponownie.

- `Tak`: program startuje nowa instancje i zamyka aktualne okno.
- `Nie`: zmiana zostaje zapisana i zostanie zastosowana przy nastepnym uruchomieniu.

Jezeli builder aktualnie pracuje, program nie restartuje sie od razu. Najpierw trzeba zatrzymac dzialajacy proces.

## Profile ustawien

Profile sa zwyklymi plikami JSON w `%APPDATA%\OpenGD77PromptStudio\profiles`. Profil zapisuje aktualne wartosci pol GUI, lacznie ze sciezkami, operacjami, zrodlem mowy, tempem, portem COM i opcjami RHVoice.

Profil nie jest tym samym co globalne ustawienia programu. Jezyk interfejsu jest zapisywany osobno w `settings.json`.

## Kolejnosc pracy z klawiatury

1. Po starcie fokus jest na `Projekt` w pasku zakladek.
2. Tabulatorem przejdz do trybu pracy, jezyka, profili i pol trybu recznego.
3. Wybierz plik CSV przyciskiem `Wybierz...` albo wpisz sciezke recznie.
4. Ustaw checkboxy operacji spacja.
5. Port COM mozesz odswiezyc `F5` i wybrac z listy.
6. Uruchom `Alt+R`.
7. Log ustawisz fokusem przez `Alt+L`.
8. Postep pracy ustawisz fokusem przez `Alt+P`.

## Zakladka Projekt

`Tryb reczny` oznacza, ze ustawiasz wszystko w oknie programu: wordlist, glos, wynik, port i operacje.

`Plik konfiguracyjny CSV` oznacza prace z gotowym plikiem konfiguracji. Po wybraniu tego trybu program wykonuje ustawienia zapisane w CSV, a wiele pol trybu recznego jest pomijanych.

`Profil ustawien` to nazwa profilu JSON. `Zapisz profil` zapisuje aktualne ustawienia, `Wczytaj profil` przywraca zapisany profil, `Usun profil` kasuje wybrany profil, a `Folder profili` otwiera katalog profili w Eksploratorze.

`Plik konfiguracyjny CSV` wskazuje plik z wieloma zadaniami. Uzywaj go tylko w trybie `Plik konfiguracyjny CSV`.

`Wordlist CSV` wskazuje plik z tekstami promptow. To podstawowy plik wejsciowy w trybie recznym.

`Nazwa glosu` jest nazwa profilu RHVoice albo nazwa folderu roboczego na pliki audio. Przyklad: `Kazek`, `Zuza`, `Natan`, `Polish`.

`Plik wynikowy VPR` jest bazowa nazwa pliku wynikowego. Program dopisuje warianty i tempo do nazwy, na przyklad wariant `UV380-like` albo `monochrome`.

`Informacja o wariantach VPR` jest polem tylko do odczytu. NVDA moze wejsc w nie Tabem i odczytac, ze `UV380-like` jest dla nowszych kolorowych modeli, takich jak MD-UV380/MD-UV390 i Retevis RT3S, a `monochrome` dla GD-77/GD-77S, DM-1801/DM-1801A i RD-5R.

`Port COM radia` jest potrzebny przy kodowaniu AMBE przez radio. `Odswiez porty` ponownie wyszukuje porty, a `Lista wykrytych portow` pozwala wybrac port z listy.

`Pobierz / syntezuj audio` tworzy pliki mowy ze zrodla wybranego na zakladce `Mowa`.

`Koduj AMBE w radiu` wysyla probki audio do radia i odbiera zakodowane ramki AMBE. Wymaga podlaczonego radia z OpenGD77 i poprawnego portu COM.

`Zbuduj VPR` sklada gotowe pliki AMBE do pakietu VPR dla radia.

## Zakladka Mowa

`TTSMP3.com` wybiera internetowe zrodlo mowy. Program pobiera audio i konwertuje je lokalnie przez wbudowany ffmpeg.

`RHVoice z dodatku NVDA` wybiera lokalny syntezator z pliku `.nvda-addon`. To jest zalecane, gdy chcesz uzyc glosow takich jak Kazek, Zuza, Natan albo inne glosy RHVoice.

`Plik dodatku NVDA` wskazuje plik `.nvda-addon` z glosem RHVoice. Przycisk `Wybierz...` otwiera okno wyboru pliku. `RHVoice.dll` jest wykrywana automatycznie i nie ma osobnego pola w glownym GUI.

## Zakladka Opcje

`Folder roboczy` to miejsce na pliki tymczasowe i posrednie: WAV, MP3, RAW, AMBE oraz rozpakowane dodatki NVDA.

`Glosnosc dB` zmienia poziom audio przed kodowaniem. Wartosci dodatnie podbijaja glosnosc, ujemne sciszaja.

`Tempo` ustawia predkosc wszystkich promptow.

`Tempo liter/cyfr` ustawia osobna predkosc pojedynczych liter, cyfr, spacji i kropki. Puste pole oznacza uzycie zwyklego pola `Tempo`.

`Alias tempa` jest tylko etykieta w nazwie pliku wynikowego. Nie zmienia dzwieku.

`Wysokosc RHVoice` zmienia wysokosc glosu dla lokalnej syntezy RHVoice. `1.0` oznacza normalna wysokosc, mniejsza wartosc obniza glos.

`Nadpisuj istniejace pliki` wymusza ponowne tworzenie audio i plikow posrednich. Zaznacz po zmianie glosu, tempa, glosnosci, wysokosci glosu albo tekstow promptow.

`Usun cisze z poczatku` usuwa poczatkowa cisze z probek audio tam, gdzie dany etap przetwarzania moze to zastosowac.

## Zakladka Praca

`Uruchom Alt+R` startuje wybrane operacje. `Zatrzymaj Alt+S` zatrzymuje dzialajacy proces. `Test zaleznosci` sprawdza, czy program widzi potrzebne skladniki, porty i pliki. `Otworz folder` otwiera folder roboczy. `Wyczysc log` kasuje widoczny log. `Zamknij` zamyka program.

`Status programu` podaje ostatni wazny komunikat. `Postep pracy` pokazuje procent i etap pracy. `Log dzialania buildera` zawiera szczegoly uruchomienia, komunikaty bledow i postep przetwarzania.

Podczas pracy program aktualizuje pasek postepu i wysyla zdarzenia dostepnosciowe przy wiekszych zmianach procentu, dzieki czemu NVDA moze oglaszac postep bez czytania calego logu.

## Zakladka Aktualizacja i pomoc

`Sprawdz aktualizacje` pyta GitHub Releases o najnowsza wersje programu. `Pobierz i zainstaluj` pobiera nowszy EXE i w wersji uruchomionej jako EXE potrafi podmienic program po zamknieciu. `Releases` otwiera strone wydan. `GitHub` otwiera repozytorium. `Pomoc` otwiera dokumentacje albo repozytorium, jezeli dokumentacja nie jest obok EXE. `O programie` pokazuje wersje, autora i link do repozytorium.

`Status aktualizacji` pokazuje wynik sprawdzania GitHuba, informacje o najnowszym release i ewentualne bledy pobierania.

## NVDA

Program nie wymaga specjalnego dodatku NVDA. Najwazniejsze komunikaty trafiaja do tekstu statusu i logu.

Jezeli okno czytnika mowy nie odczytuje nowych linii logu automatycznie, przejdz do pola logu `Alt+L` i czytaj je standardowymi komendami pola edycji.