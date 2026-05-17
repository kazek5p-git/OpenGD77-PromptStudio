# Dodatki NVDA i RHVoice

## Co jest obslugiwane

Obslugiwane sa pliki `.nvda-addon`, ktore sa glosami RHVoice. Program rozpoznaje je po strukturze:

```text
data/voice.info
data/voice.params
langdata/
manifest.ini
```

Przykladowe glosy: Kazek, Natan, Zuza, Jan, Agata, Monika, jezeli sa spakowane jako dodatki RHVoice.

## Co nie jest obslugiwane

Nie sa obslugiwane dowolne dodatki NVDA. Plik `.nvda-addon` moze byc pluginem, narzedziem, paczka dzwiekow albo sterownikiem innego syntezatora. Taki plik nie zawiera danych RHVoice i nie da sie z niego wygenerowac mowy ta metoda.

## Wymagany silnik RHVoice

Glos RHVoice i silnik RHVoice to dwie rozne rzeczy.

Plik glosu `.nvda-addon` zawiera dane glosu i jezyka. Do syntezy potrzebny jest jeszcze `RHVoice.dll`.

Program szuka `RHVoice.dll` automatycznie. Najprostsze warianty:

- zainstaluj dodatek NVDA `RHVoice`,
- albo wpisz pelna sciezke do `RHVoice.dll`,
- albo skopiuj `RHVoice.dll` obok `OpenGD77PromptStudio.exe`,
- albo ustaw zmienna srodowiskowa `RHVOICE_DLL`.

## Tryb reczny

1. Zaznacz zrodlo mowy `Dodatek NVDA/RHVoice`.
2. Wybierz plik `.nvda-addon`.
3. Jezeli program nie wykryl DLL, wskaz `RHVoice.dll`.
4. Zaznacz `Utworz pliki mowy`.
5. Uruchom `Alt+R`.

## Tryb CLI

```powershell
OpenGD77PromptStudio.exe -f wordlist_polish.csv -n Kazek -N Kazek.nvda-addon -g 0 -t 1.0
```

Z recznie wskazanym DLL:

```powershell
OpenGD77PromptStudio.exe -f wordlist_polish.csv -n Kazek -N Kazek.nvda-addon -L C:\RHVoice\RHVoice.dll
```

## Tryb config CSV

Wypelnij kolumne `Nvda_addon_file`. Jezeli `Download` ma wartosc `y`, program uzyje lokalnej syntezy RHVoice.
