param(
  [string]$VendorDir = "$PSScriptRoot\..\vendor"
)

$ErrorActionPreference = "Stop"

Write-Host "== MegaOCR Build (no staging) =="
Write-Host "VendorDir: $VendorDir"

if (!(Test-Path "$VendorDir\tesseract.exe")) { throw "Missing tesseract.exe in $VendorDir" }
if (!(Test-Path "$VendorDir\tessdata"))     { throw "Missing tessdata folder in $VendorDir" }
if (!(Test-Path "$VendorDir\fonts"))        { throw "Missing fonts folder in $VendorDir" }

# Clean old builds
Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue

# Build; note absolute paths before semicolon
pyinstaller --onefile --noconsole `
  --add-data "$VendorDir\tesseract.exe;." `
  --add-data "$VendorDir\tessdata;tessdata" `
  --add-data "$VendorDir\fonts;fonts" `
  --add-data "$VendorDir\*.dll;." `
  --add-data "$VendorDir\mega_ocr.ico;." `
  --icon="$VendorDir\mega_ocr.ico" Mega_OCR.py
Write-Host "== Done. Output: dist\Mega_OCR.exe =="