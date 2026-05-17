param(
    [string]$Python = "python"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Source = Join-Path $Root "src\prompt_studio.py"
$Exe = Join-Path $Root "dist\OpenGD77PromptStudio.exe"

Write-Host "Python compile..."
& $Python -m py_compile $Source
if ($LASTEXITCODE -ne 0) { throw "py_compile failed" }

Write-Host "CLI help..."
& $Python $Source -h | Out-Host
if ($LASTEXITCODE -ne 0) { throw "CLI help failed with code $LASTEXITCODE" }

if (Test-Path $Exe) {
    Write-Host "EXE exists: $Exe"
    $hash = Get-FileHash -Algorithm SHA256 -LiteralPath $Exe
    Write-Host "EXE SHA256: $($hash.Hash)"
} else {
    Write-Host "EXE not built yet. Run scripts\build-onefile.ps1."
}

Write-Host "Smoke test OK"