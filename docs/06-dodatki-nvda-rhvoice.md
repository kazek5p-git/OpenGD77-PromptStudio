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

Gotowy EXE z release ma `RHVoice.dll` wbudowany. Jezeli uzywasz wersji zrodlowej albo builda bez wbudowanego silnika, program szuka `RHVoice.dll` automatycznie. Najprostsze warianty:

- uzyj gotowego EXE z release,
- zainstaluj dodatek NVDA `RHVoice`,
- albo ustaw zmienna srodowiskowa `RHVOICE_DLL`,
- albo skopiuj `RHVoice.dll` obok `OpenGD77PromptStudio.exe`,
- albo ustaw zmienna srodowiskowa `RHVOICE_DLL`.

## Tryb reczny

1. Zaznacz zrodlo mowy `Dodatek NVDA/RHVoice`.
2. Wybierz plik `.nvda-addon`.
3. Jezeli program nie wykryl DLL w wersji serwisowej, ustaw `RHVOICE_DLL`, skopiuj DLL obok EXE albo uzyj CLI `-L`. W zwyklym GUI pole DLL nie jest pokazywane.
4. Zaznacz `Utworz pliki mowy`.
5. Uruchom `Alt+R`.

## Tryb CLI

```powershell
OpenGD77PromptStudio.exe -f wordlist_polish.csv -n Kazek -N Kazek.nvda-addon -g 0 -t 1.0 -l 1.2
```

Z recznie wskazanym DLL:

```powershell
OpenGD77PromptStudio.exe -f wordlist_polish.csv -n Kazek -N Kazek.nvda-addon -L C:\RHVoice\RHVoice.dll
```

## Tryb config CSV

Wypelnij kolumne `Nvda_addon_file`. Jezeli `Download` ma wartosc `y`, program uzyje lokalnej syntezy RHVoice.

## Wysokosc glosu

Parametr `-p` ustawia wzgledna wysokosc glosu RHVoice. `1.0` to wartosc normalna. Mniejsza wartosc, na przyklad `0.94`, delikatnie obniza glos.

## Tempo liter i cyfr

Parametr `-l` albo `--letter-tempo` ustawia tempo tylko dla pojedynczych liter, cyfr, spacji i kropki. Bez tego parametru te prompty uzywaja zwyklego `-t`.
