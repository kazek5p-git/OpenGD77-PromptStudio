# Rozwiazywanie problemow

## Program nie startuje

Uruchom build z konsola diagnostyczna:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -Console
```

Potem uruchom `dist\OpenGD77PromptStudio.exe` z PowerShella i sprawdz komunikat.

## Brak ffmpeg

Jesli zaznaczasz tworzenie mowy, program potrzebuje `ffmpeg.exe`. Mozesz:

- wpisac sciezke w polu `ffmpeg.exe`,
- skopiowac `ffmpeg.exe` obok EXE,
- dodac folder ffmpeg do PATH.

## Dodatek NVDA nie dziala

Program obsluguje tylko glosy RHVoice w paczkach `.nvda-addon`. Taki dodatek musi zawierac `data/voice.info`, `data/voice.params` i `langdata`.

Jezeli plik jest zwyklym pluginem NVDA albo dodatkiem innego syntezatora, program pokaze blad, ze to nie jest glos RHVoice.

## Brak RHVoice.dll

Dla zrodla `Dodatek NVDA/RHVoice` potrzebny jest silnik RHVoice. Gotowy EXE z release ma go wbudowanego. Jezeli uzywasz builda bez wbudowanego silnika, program szuka go w tych miejscach:

- sciezka wpisana w polu `RHVoice.dll`,
- zmienna srodowiskowa `RHVOICE_DLL`,
- plik `RHVoice.dll` obok EXE,
- folder `rhvoice\RHVoice.dll` obok EXE,
- zainstalowany dodatek NVDA `RHVoice` w profilu uzytkownika.

## Brak portu COM radia

Nacisnij `F5`. Jesli port nadal sie nie pojawia, sprawdz sterownik USB i czy radio jest widoczne w Menedzerze urzadzen.

## Kodowanie AMBE nie dziala

Kodowanie wymaga radia z OpenGD77, ktore obsluguje komendy uzywane przez builder. Sam komputer nie koduje AMBE.

## Plik VPR jest za duzy

Kod usuwa plik, jesli przekroczy limit `0x28C00` bajtow. Pomaga skrocenie komunikatow, mniejsza liczba promptow albo spokojniejsze ustawienia TTS, ktore generuja krotszy dzwiek.

## TTSMP3 nie odpowiada

TTSMP3 to zewnetrzna usluga internetowa. Jesli zwraca blad, sprobuj pozniej albo uzyj lokalnego zrodla RHVoice.
