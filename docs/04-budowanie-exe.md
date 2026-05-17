# Budowanie EXE

## Przygotowanie

Zainstaluj zależności:

```powershell
python -m pip install -r requirements.txt
```

## Build onefile

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1
```

Wynik:

```text
dist\OpenGD77PromptStudio.exe
```

Domyślny build jest typu `windowed`, więc po dwukliku startuje okno GUI bez konsoli.

## Build z konsolą diagnostyczną

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\build-onefile.ps1 -Console
```

To jest przydatne, gdy trzeba zobaczyć błąd startu na komputerze bez środowiska deweloperskiego.

## Testy

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\smoke-test.ps1
```

Test sprawdza kompilację Pythona, pomoc CLI i obecność artefaktu EXE, jeśli został zbudowany.