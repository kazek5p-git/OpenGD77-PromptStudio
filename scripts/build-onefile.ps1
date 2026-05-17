param(
    [string]$Python = "python",
    [switch]$Console
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $Root "src\prompt_studio.py"
$Dist = Join-Path $Root "dist"
$Work = Join-Path $Root "build\pyinstaller"
$Spec = Join-Path $Root "build"
$Name = "OpenGD77PromptStudio"

if (!(Test-Path $Source)) {
    throw "Nie znaleziono pliku źródłowego: $Source"
}

& $Python -m PyInstaller --version | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller nie jest dostępny. Uruchom: python -m pip install -r requirements.txt"
}

$mode = if ($Console) { "--console" } else { "--windowed" }
$args = @(
    "-m", "PyInstaller",
    "--noconfirm",
    "--clean",
    "--onefile",
    $mode,
    "--name", $Name,
    "--distpath", $Dist,
    "--workpath", $Work,
    "--specpath", $Spec,
    "--hidden-import", "serial.tools.list_ports_windows",
    "--hidden-import", "serial.tools.list_ports_common",
    $Source
)

& $Python @args
if ($LASTEXITCODE -ne 0) {
    throw "Build nie powiódł się. Kod: $LASTEXITCODE"
}

$Exe = Join-Path $Dist ($Name + ".exe")
if (!(Test-Path $Exe)) {
    throw "Build zakończony, ale nie znaleziono EXE: $Exe"
}

$hash = Get-FileHash -Algorithm SHA256 -LiteralPath $Exe
Write-Host ""
Write-Host "Gotowe: $Exe"
Write-Host "SHA256: $($hash.Hash)"