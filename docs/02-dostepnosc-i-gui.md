# Dostępność i GUI

Interfejs jest zrobiony w `wxPython`, czyli korzysta z natywnych kontrolek Windows widocznych dla czytników ekranu.


## Zakladki

GUI wxPython jest podzielone na zakladki:

- `Projekt`: tryb pracy, profile ustawien, CSV, port COM i operacje.
- `Mowa`: wybor zrodla mowy i dodatku NVDA/RHVoice. `RHVoice.dll` jest wykrywana automatycznie.
- `Opcje`: folder roboczy, glosnosc, tempo, tempo liter/cyfr i wysokosc RHVoice.
- `Praca`: przyciski uruchamiania, pasek postepu i log.
- `Aktualizacja i pomoc`: sprawdzanie GitHub Releases, pobieranie aktualizacji, pomoc i autor.

Pasek zakladek jest zrobiony ze zwyklych radiobuttonow: `Projekt`, `Mowa`, `Opcje`, `Praca` oraz `Aktualizacja i pomoc`. Po uruchomieniu programu fokus trafia na `Projekt`. Strzalki, Tab oraz skroty `Ctrl+Tab`, `Ctrl+Shift+Tab`, `Ctrl+PageDown`, `Ctrl+PageUp` i `Alt+1` do `Alt+5` przelaczaja zakladki bez wchodzenia w problematyczny natywny pasek `wx.Notebook`.

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


## Opcje tempa

Pole `Tempo` ustawia predkosc wszystkich promptow. Pole `Tempo liter/cyfr` jest opcjonalne i dotyczy tylko pojedynczych liter, cyfr, spacji i kropki. Puste pole oznacza, ze litery i cyfry uzyja zwyklego tempa.

## NVDA

Program nie wymaga specjalnego dodatku NVDA. Najważniejsze komunikaty trafiają do tekstu statusu i logu.

Podczas pracy program aktualizuje pasek postępu i wysyła zdarzenia dostępnościowe przy większych zmianach procentu, dzięki czemu NVDA może ogłaszać postęp bez czytania całego logu.

Jeżeli okno czytnika mowy nie odczytuje nowych linii logu automatycznie, przejdź do pola logu `Alt+L` i czytaj je standardowymi komendami pola edycji.