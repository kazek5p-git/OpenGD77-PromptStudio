# Dostępność i GUI

Interfejs jest zrobiony w `wxPython`, czyli korzysta z natywnych kontrolek Windows widocznych dla czytników ekranu.

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

## NVDA

Program nie wymaga specjalnego dodatku NVDA. Najważniejsze komunikaty trafiają do tekstu statusu i logu.

Podczas pracy program aktualizuje pasek postępu i wysyła zdarzenia dostępnościowe przy większych zmianach procentu, dzięki czemu NVDA może ogłaszać postęp bez czytania całego logu.

Jeżeli okno czytnika mowy nie odczytuje nowych linii logu automatycznie, przejdź do pola logu `Alt+L` i czytaj je standardowymi komendami pola edycji.