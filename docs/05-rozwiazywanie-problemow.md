# Rozwiązywanie problemów

## Program nie startuje

Uruchom build z konsolą diagnostyczną:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -Console
```

Potem uruchom `dist\OpenGD77PromptStudio.exe` z PowerShella i sprawdź komunikat.

## Brak ffmpeg

Jeśli zaznaczasz pobieranie mowy, program potrzebuje `ffmpeg.exe`. Możesz:

- wpisać ścieżkę w polu `ffmpeg.exe`,
- skopiować `ffmpeg.exe` obok EXE,
- dodać folder ffmpeg do PATH.

## Brak portu COM radia

Naciśnij `F5`. Jeśli port nadal się nie pojawia, sprawdź sterownik USB i czy radio jest widoczne w Menedżerze urządzeń.

## Kodowanie AMBE nie działa

Kodowanie wymaga radia z OpenGD77, które obsługuje komendy używane przez builder. Sam komputer nie koduje AMBE.

## Plik VPR jest za duży

Kod usuwa plik, jeśli przekroczy limit `0x28C00` bajtów. Pomaga skrócenie komunikatów, mniejsza liczba promptów albo spokojniejsze ustawienia TTS, które generują krótszy dźwięk.

## TTSMP3 nie odpowiada

TTSMP3 to zewnętrzna usługa internetowa. Jeśli zwraca błąd, spróbuj później albo użyj już pobranych plików audio i pomiń etap pobierania.