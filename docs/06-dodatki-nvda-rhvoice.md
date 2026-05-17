# Dodatki NVDA i RHVoice

## Co jest obslugiwane

Obslugiwane sa pliki `.nvda-addon`, ktore sa glosami RHVoice. Program rozpoznaje je po strukturze:

```text
data/voice.info
data/voice.params
langdata/
manifest.ini
```

Przykladowe glosy albo profile glosow: Kazek, Natan, Zuza, Jan, Agata, Monika, jezeli sa spakowane jako dodatki RHVoice.

## Co nie jest obslugiwane

Nie sa obslugiwane dowolne dodatki NVDA. Plik `.nvda-addon` moze byc pluginem, narzedziem, paczka dzwiekow albo sterownikiem innego syntezatora. Taki plik nie zawiera danych RHVoice i nie da sie z niego wygenerowac mowy ta metoda.

## Glos a silnik RHVoice

Glos RHVoice i silnik RHVoice to dwie rozne rzeczy.

Plik glosu `.nvda-addon` zawiera dane glosu i jezyka. Do syntezy potrzebny jest jeszcze `RHVoice.dll`.

Gotowy EXE z release ma `RHVoice.dll` wbudowany. Jezeli uzywasz wersji zrodlowej albo builda bez wbudowanego silnika, program szuka `RHVoice.dll` automatycznie.

Najprostsze warianty:

- uzyj gotowego EXE z release,
- zainstaluj dodatek NVDA `RHVoice`,
- ustaw zmienna srodowiskowa `RHVOICE_DLL`,
- skopiuj `RHVoice.dll` obok `OpenGD77PromptStudio.exe`,
- skopiuj `RHVoice.dll` do folderu `rhvoice` obok EXE.

## Wybieranie profilu glosu

Po wczytaniu dodatku program pyta silnik RHVoice o dostepne profile i wypisuje je w logu:

```text
RHVoice profiles: Kazek, Zuza, Natan
```

Pole `Nazwa glosu` jest przekazywane do RHVoice jako prosba o profil. Jezeli wpisana nazwa istnieje w liscie profili, zostanie uzyta. Jezeli nie istnieje, RHVoice uzyje pierwszego profilu z dodatku, a log pokaze faktycznie uzyty profil.

Przyklady:

- wpisz `Kazek`, zeby uzyc profilu Kazek,
- wpisz `Zuza`, zeby uzyc profilu Zuza,
- wpisz `Natan`, zeby uzyc profilu Natan.

Ta sama nazwa tworzy tez folder roboczy na pliki audio.

## Tryb reczny w GUI

1. Na zakladce `Mowa` zaznacz zrodlo `RHVoice z dodatku NVDA`.
2. Wybierz plik `.nvda-addon`.
3. Na zakladce `Projekt` wpisz `Nazwa glosu` zgodna z profilem w dodatku, np. `Kazek` albo `Zuza`.
4. Zaznacz `Pobierz / syntezuj audio`.
5. Uruchom `Alt+R`.

W zwyklym GUI pole DLL nie jest pokazywane, bo `RHVoice.dll` jest wykrywana automatycznie albo wbudowana w EXE.

## Tryb CLI

Synteza z dodatku NVDA/RHVoice:

```powershell
OpenGD77PromptStudio.exe -f wordlist_polish.csv -n Kazek -N Kazek.nvda-addon -g 0 -t 1.0 -l 1.2
```

Z recznie wskazanym DLL:

```powershell
OpenGD77PromptStudio.exe -f wordlist_polish.csv -n Kazek -N Kazek.nvda-addon -L C:\RHVoice\RHVoice.dll
```

Obnizenie wysokosci glosu:

```powershell
OpenGD77PromptStudio.exe -f wordlist_polish.csv -n Kazek -N Kazek.nvda-addon -p 0.94
```

## Tryb config CSV

Wypelnij kolumne `Nvda_addon_file`. Jezeli `Download` ma wartosc `y`, program uzyje lokalnej syntezy RHVoice.

Opcjonalne kolumny RHVoice:

- `RHVoice_dll`: reczna sciezka do DLL w trybie serwisowym,
- `RHVoice_pitch`: wysokosc glosu, gdzie `1.0` oznacza normalna wysokosc.

## Wysokosc glosu

Parametr `-p` i pole `Wysokosc RHVoice` ustawiaja wzgledna wysokosc glosu RHVoice. `1.0` to wartosc normalna. Mniejsza wartosc, na przyklad `0.94`, delikatnie obniza glos.

## Tempo liter i cyfr

Parametr `-l` albo `--letter-tempo` oraz pole `Tempo liter/cyfr` ustawiaja tempo tylko dla pojedynczych liter, cyfr, spacji i kropki. Bez tego parametru te prompty uzywaja zwyklego `Tempo` albo `-t`.

## Nadpisywanie plikow

Po zmianie dodatku, profilu glosu, wysokosci, tempa albo tekstow zaznacz `Nadpisuj istniejace pliki`. W przeciwnym razie program moze uzyc wczesniej wygenerowanych plikow WAV, RAW albo AMBE.