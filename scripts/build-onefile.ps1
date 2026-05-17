param(
    [string]$Python = "python",
    [switch]$Console,
    [string]$RhVoiceDll = "",
    [switch]$NoBundledRhVoice
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $Root "src\prompt_studio.py"
$Dist = Join-Path $Root "dist"
$Work = Join-Path $Root "build\pyinstaller"
$Spec = Join-Path $Root "build"
$Name = "OpenGD77PromptStudio"

if (!(Test-Path $Source)) {
    throw "Nie znaleziono pliku ?r?d?owego: $Source"
}

function Find-RhVoiceDll {
    param([string]$ExplicitPath)

    $candidates = @()
    if (![string]::IsNullOrWhiteSpace($ExplicitPath)) {
        $candidates += $ExplicitPath
    }
    if (![string]::IsNullOrWhiteSpace($env:RHVOICE_DLL)) {
        $candidates += $env:RHVOICE_DLL
    }
    if (![string]::IsNullOrWhiteSpace($env:APPDATA)) {
        $candidates += (Join-Path $env:APPDATA "NVDA\addons\RHVoice\synthDrivers\RHVoice\lib\x64\RHVoice.dll")
        $candidates += (Join-Path $env:APPDATA "nvda\addons\RHVoice\synthDrivers\RHVoice\lib\x64\RHVoice.dll")
    }

    foreach ($candidate in $candidates) {
        if ($candidate -and (Test-Path -LiteralPath $candidate)) {
            return (Resolve-Path -LiteralPath $candidate).Path
        }
    }
    return ""
}

& $Python -m PyInstaller --version | Out-Host
if ($LASTEXITCODE -ne 0) {
    throw "PyInstaller nie jest dost?pny. Uruchom: python -m pip install -r requirements.txt"
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
    "--hidden-import", "serial.tools.list_ports_common"
)

$bundledRhVoice = ""
if (!$NoBundledRhVoice) {
    $bundledRhVoice = Find-RhVoiceDll -ExplicitPath $RhVoiceDll
    if ($bundledRhVoice) {
        Write-Host "Bundled RHVoice.dll: $bundledRhVoice"
        $args += @("--add-binary", ($bundledRhVoice + ";."))
    } else {
        Write-Host "RHVoice.dll nie znaleziony. EXE zostanie zbudowany bez wbudowanego silnika RHVoice."
    }
} else {
    Write-Host "Pomijam bundlowanie RHVoice.dll na ??danie parametru -NoBundledRhVoice."
}

$args += $Source

& $Python @args
if ($LASTEXITCODE -ne 0) {
    throw "Build nie powi?d? si?. Kod: $LASTEXITCODE"
}

$Exe = Join-Path $Dist ($Name + ".exe")
if (!(Test-Path $Exe)) {
    throw "Build zako?czony, ale nie znaleziono EXE: $Exe"
}

$hash = Get-FileHash -Algorithm SHA256 -LiteralPath $Exe
Write-Host ""
Write-Host "Gotowe: $Exe"
Write-Host "SHA256: $($hash.Hash)"
if ($bundledRhVoice) {
    Write-Host "Wbudowano RHVoice.dll: $bundledRhVoice"
}
