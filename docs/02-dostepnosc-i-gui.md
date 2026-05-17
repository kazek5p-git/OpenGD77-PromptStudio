# Dostępność i GUI

Interfejs jest zrobiony w `wxPython`, czyli korzysta z natywnych kontrolek Windows widocznych dla czytników ekranu.


## Zakladki

GUI wxPython jest podzielone na zakladki:

- `Projekt`: tryb pracy, profile ustawien, CSV, port COM i operacje.
- `Mowa`: wybor zrodla mowy i dodatku NVDA/RHVoice. `RHVoice.dll` jest wykrywana automatycznie.
- `Opcje`: folder roboczy, glosnosc, tempo, tempo liter/cyfr i wysokosc RHVoice.
- `Praca`: przyciski uruchamiania, pasek postepu i log.
- `Aktualizacja i pomoc`: sprawdzanie GitHub Releases, pobieranie aktualizacji, pomoc i autor.

Pasek zakladek jest zrobiony ze zwyklych radiobuttonow: `Projekt`, `Mowa`, `Opcje`, `Praca` oraz `Aktualizacja i pomoc`. Po uruchomieniu programu fokus trafia na `Projekt`. Czytnik ekranu dostaje tez pozycje zakladki, na przyklad `Zakladka 1 z 5: Projekt` albo `Zakladka 3 z 5: Opcje`. Strzalki, Tab oraz skroty `Ctrl+Tab`, `Ctrl+Shift+Tab`, `Ctrl+PageDown`, `Ctrl+PageUp` i `Alt+1` do `Alt+5` przelaczaja zakladki bez wchodzenia w problematyczny natywny pasek `wx.Notebook`.

## Profile ustawien

Profile sa zwyklymi plikami JSON w `%APPDATA%\OpenGD77PromptStudio\profiles`. Profil zapisuje aktualne wartosci pol GUI, lacznie ze sciezkami, operacjami, zrodlem mowy, tempem, portem COM i opcjami RHVoice.

## Kontrolki

Program używa zwykłych elementów: pola edycji, przyciski, checkboxy, radiobuttony, listbox i pole tekstowe logu.

Pasek `Postęp pracy` jest natywnym paskiem postępu oraz polem tekstowym. Fokus na postęp ustawisz skrótem `Alt+P`.

Po wejściu fokusem w ważne pole program aktualizuje tekst statusu. NVDA odczytuje jawne nazwy kontrolek oraz może odczytać status opisujący ich przeznaczenie.

## Kolejność pracy z klawiatury

1. Tabulatorem przejdź po polach trybu ręcznego.
2. Wybierz plik CSV przyciskiem `Wybierz...` albo wpisz ścieżkę ręcznie.
3. Ustaw checkboxy operacji spacją.
4. Port COM możesz wybrać z listy portów po `F5`.
5. Uruchom `Alt+R`.
6. Log możesz szybko ustawić fokusem przez `Alt+L`.
7. Postęp pracy możesz szybko ustawić fokusem przez `Alt+P`.



## Opis elementow interfejsu

### Pasek zakladek

`Projekt`, `Mowa`, `Opcje`, `Praca` oraz `Aktualizacja i pomoc` sa radiobuttonami. Kazdy radiobutton ma w nazwie numer pozycji, na przyklad `Zakladka 1 z 5: Projekt`. Oznaczony radiobutton pokazuje aktywna zakladke. `Poprzednia` i `Nastepna` przelaczaja zakladki bez uzywania skrotow klawiaturowych.

### Zakladka Projekt

`Tryb reczny` oznacza, ze ustawiasz wszystko w oknie programu: wordlist, glos, wynik, port i operacje.

`Plik konfiguracyjny CSV` oznacza prace z gotowym plikiem konfiguracji. Po wybraniu tego trybu program wykonuje ustawienia zapisane w CSV, a wiele pol trybu recznego jest pomijanych.

`Profil ustawien` to nazwa profilu JSON. `Zapisz profil` zapisuje aktualne ustawienia, `Wczytaj profil` przywraca zapisany profil, `Usun profil` kasuje wybrany profil, a `Folder profili` otwiera katalog profili w Eksploratorze.

`Jezyk interfejsu` wybiera polski albo angielski interfejs programu. Po zmianie jezyka uruchom program ponownie, aby wszystkie zakladki, przyciski, opisy dostepnosciowe i komunikaty startowe zostaly zaladowane w wybranym jezyku. Ustawienie jest zapisywane w `%APPDATA%\OpenGD77PromptStudio\settings.json`.

`Plik konfiguracyjny CSV` wskazuje plik z wieloma zadaniami. Uzywaj go tylko w trybie `Plik konfiguracyjny CSV`.

`Wordlist CSV` wskazuje plik z tekstami promptow. To podstawowy plik wejsciowy w trybie recznym.

`Nazwa glosu` jest nazwa profilu RHVoice albo nazwa folderu roboczego na pliki audio. Przyklad: `Kazek`, `Zuza`, `Polish`.

`Plik wynikowy VPR` jest bazowa nazwa pliku wynikowego. Program dopisuje warianty i tempo do nazwy, na przyklad wariant `UV380-like` albo `monochrome`.

`Informacja o wariantach VPR` jest polem tylko do odczytu. NVDA moze wejsc w nie Tabem i odczytac, ze `UV380-like` jest dla nowszych kolorowych modeli, takich jak MD-UV380/MD-UV390 i Retevis RT3S, a `monochrome` dla GD-77/GD-77S, DM-1801/DM-1801A i RD-5R.

`Port COM radia` jest potrzebny przy kodowaniu AMBE przez radio. `Odswiez porty` ponownie wyszukuje porty, a `Lista wykrytych portow` pozwala wybrac port z listy.

`Pobierz / syntezuj audio` tworzy pliki mowy ze zrodla wybranego na zakladce `Mowa`.

`Koduj AMBE w radiu` wysyla probki audio do radia i odbiera zakodowane ramki AMBE. Wymaga podlaczonego radia z OpenGD77 i poprawnego portu COM.

`Zbuduj VPR` sklada gotowe pliki AMBE do pakietu VPR dla radia.

### Zakladka Mowa

`TTSMP3.com` wybiera internetowe zrodlo mowy. Program pobiera audio i konwertuje je lokalnie przez wbudowany ffmpeg.

`RHVoice z dodatku NVDA` wybiera lokalny syntezator z pliku `.nvda-addon`. To jest zalecane, gdy chcesz uzyc glosow takich jak Kazek, Zuza albo inne glosy RHVoice.

`Plik dodatku NVDA` wskazuje plik `.nvda-addon` z glosem RHVoice. Przycisk `Wybierz...` otwiera okno wyboru pliku. `RHVoice.dll` jest wykrywana automatycznie i nie ma osobnego pola w glownym GUI.

### Zakladka Opcje

`Folder roboczy` to miejsce na pliki tymczasowe i posrednie: WAV, RAW, AMBE oraz rozpakowane dodatki NVDA.

`Glosnosc dB` zmienia poziom audio przed kodowaniem. Wartosci dodatnie podbijaja glosnosc, ujemne sciszaja.

`Tempo` ustawia predkosc wszystkich promptow.

`Tempo liter/cyfr` ustawia osobna predkosc pojedynczych liter, cyfr, spacji i kropki. Puste pole oznacza uzycie zwyklego pola `Tempo`.

`Alias tempa` jest tylko etykieta w nazwie pliku wynikowego. Nie zmienia dzwieku.

`Wysokosc RHVoice` zmienia wysokosc glosu dla lokalnej syntezy RHVoice. `1.0` oznacza normalna wysokosc, mniejsza wartosc obniza glos.

`Nadpisuj istniejace pliki` wymusza ponowne tworzenie audio i plikow posrednich. Zaznacz po zmianie glosu, tempa, glosnosci, wysokosci glosu albo tekstow promptow.

`Usun cisze z poczatku` usuwa poczatkowa cisze z probek audio tam, gdzie dany etap przetwarzania moze to zastosowac.

### Zakladka Praca

`Uruchom Alt+R` startuje wybrane operacje. `Zatrzymaj Alt+S` zatrzymuje dzialajacy proces. `Test zaleznosci` sprawdza, czy program widzi potrzebne skladniki, porty i pliki. `Otworz folder` otwiera folder roboczy. `Wyczysc log` kasuje widoczny log. `Zamknij` zamyka program.

`Status programu` podaje ostatni wazny komunikat. `Postep pracy` pokazuje procent i etap pracy. `Log dzialania buildera` zawiera szczegoly uruchomienia, komunikaty bledow i postep przetwarzania.

### Zakladka Aktualizacja i pomoc

`Sprawdz aktualizacje` pyta GitHub Releases o najnowsza wersje programu. `Pobierz i zainstaluj` pobiera nowszy EXE i w wersji uruchomionej jako EXE potrafi podmienic program po zamknieciu. `Releases` otwiera strone wydan. `GitHub` otwiera repozytorium. `Pomoc` otwiera dokumentacje. `O programie` pokazuje wersje, autora i link do repozytorium.

`Status aktualizacji` pokazuje wynik sprawdzania GitHuba, informacje o najnowszym release i ewentualne bledy pobierania.

## Opcje tempa

Pole `Tempo` ustawia predkosc wszystkich promptow. Pole `Tempo liter/cyfr` jest opcjonalne i dotyczy tylko pojedynczych liter, cyfr, spacji i kropki. Puste pole oznacza, ze litery i cyfry uzyja zwyklego tempa.

Pole `Alias tempa` nie zmienia dzwieku. To tylko krotka etykieta uzywana w nazwie wynikowego pliku VPR, na przyklad `normalny`, `szybki`, `wolny`, `kazek`, `zuza_wolna` albo `czytelny`. Jezeli alias jest pusty, program uzywa liczby tempa w nazwie pliku.

Pole wyboru `Nadpisuj istniejace pliki` wymusza ponowne tworzenie plikow audio i plikow posrednich. Gdy jest nieoznaczone, program uzywa juz istniejacych plikow WAV, RAW albo AMBE, jezeli je znajdzie. Zaznacz je po zmianie glosu, tempa, glosnosci, tekstow promptow albo gdy poprzednie generowanie wyszlo zle.

## NVDA

Program nie wymaga specjalnego dodatku NVDA. Najważniejsze komunikaty trafiają do tekstu statusu i logu.

Podczas pracy program aktualizuje pasek postępu i wysyła zdarzenia dostępnościowe przy większych zmianach procentu, dzięki czemu NVDA może ogłaszać postęp bez czytania całego logu.

Jeżeli okno czytnika mowy nie odczytuje nowych linii logu automatycznie, przejdź do pola logu `Alt+L` i czytaj je standardowymi komendami pola edycji.