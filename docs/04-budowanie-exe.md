# Budowanie EXE

## Przygotowanie

Zainstaluj zaleznosci:

```powershell
python -m pip install -r requirements.txt
```

Do budowania potrzebny jest PyInstaller. Skrypt builda sprawdza go automatycznie.

## Build onefile

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1
```

Wynik:

```text
dist\OpenGD77PromptStudio.exe
```

Domyslny build jest typu `windowed`, wiec po dwukliku startuje okno GUI bez konsoli.

Przed buildem zamknij uruchomiony `OpenGD77PromptStudio.exe`. Jezeli EXE z `dist` dziala, PyInstaller nie moze go nadpisac i zakonczy sie bledem `PermissionError` albo `Odmowa dostepu`.

## Build z konsola diagnostyczna

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -Console
```

To jest przydatne, gdy program na innym komputerze zamyka sie od razu i trzeba zobaczyc blad startu.

## Wbudowany ffmpeg

Domyslny build probuje znalezc `ffmpeg.exe` i dolaczyc go do jednoplikowego EXE.

Kolejnosc szukania:

- parametr `-FfmpegExe`,
- zmienna srodowiskowa `FFMPEG_EXE`,
- znana lokalizacja `Documents\fmdx-webserver-src\node_modules\ffmpeg-static\ffmpeg.exe`,
- `ffmpeg.exe` obok repozytorium,
- `ffmpeg.exe` z PATH.

Wskazanie konkretnego ffmpeg:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -FfmpegExe C:\Tools\ffmpeg.exe
```

Build bez wbudowanego ffmpeg:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -NoBundledFfmpeg
```

Taki wariant wymaga pozniej `FFMPEG_EXE`, pliku `ffmpeg.exe` obok EXE albo ffmpeg w PATH.

## Wbudowany RHVoice.dll

Domyslny build probuje znalezc `RHVoice.dll` i dolaczyc go do jednoplikowego EXE.

Kolejnosc szukania:

- parametr `-RhVoiceDll`,
- zmienna srodowiskowa `RHVOICE_DLL`,
- zainstalowany dodatek NVDA `RHVoice` w `%APPDATA%\NVDA\addons\RHVoice\synthDrivers\RHVoice\lib\x64\RHVoice.dll`.

Wskazanie konkretnego DLL:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -RhVoiceDll C:\RHVoice\RHVoice.dll
```

Build bez wbudowanego RHVoice:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -NoBundledRhVoice
```

Ten wariant wymaga pozniej zainstalowanego dodatku NVDA `RHVoice`, pliku `RHVoice.dll` obok EXE albo zmiennej `RHVOICE_DLL`.

## Testy

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-test.ps1
```

Test sprawdza:

- kompilacje Pythona,
- pomoc CLI,
- obecnosc artefaktu EXE, jezeli zostal zbudowany,
- SHA256 istniejacego EXE.

Szybki test samego EXE:

```powershell
.\dist\OpenGD77PromptStudio.exe -h
```

## Release GitHub

Aktualizator programu szuka release w repozytorium `kazek5p-git/OpenGD77-PromptStudio` i assetu o nazwie `OpenGD77PromptStudio.exe`.

Przy publikacji release trzeba dolaczyc dokladnie taki plik:

```text
OpenGD77PromptStudio.exe
```

Po publikacji warto sprawdzic digest SHA256 assetu na GitHubie i lokalny hash:

```powershell
Get-FileHash -Algorithm SHA256 .\dist\OpenGD77PromptStudio.exe
```