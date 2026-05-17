# Dostępność i GUI

Interfejs jest zrobiony w `tkinter`, czyli korzysta ze standardowych kontrolek Windows widocznych dla czytników ekranu.

## Kontrolki

Program używa zwykłych elementów: pola edycji, przyciski, checkboxy, radiobuttony, listbox i pole tekstowe logu.

Po wejściu fokusem w ważne pole program aktualizuje tekst statusu. NVDA może odczytać, do czego służy dana kontrolka.

## Kolejność pracy z klawiatury

1. Tabulatorem przejdź po polach trybu ręcznego.
2. Wybierz plik CSV przyciskiem `Wybierz...` albo wpisz ścieżkę ręcznie.
3. Ustaw checkboxy operacji spacją.
4. Port COM możesz wybrać z listy portów po `F5`.
5. Uruchom `Alt+R`.
6. Log możesz szybko ustawić fokusem przez `Alt+L`.

## NVDA

Program nie wymaga specjalnego dodatku NVDA. Najważniejsze komunikaty trafiają do tekstu statusu i logu.

Jeżeli okno czytnika mowy nie odczytuje nowych linii logu automatycznie, przejdź do pola logu `Alt+L` i czytaj je standardowymi komendami pola edycji.