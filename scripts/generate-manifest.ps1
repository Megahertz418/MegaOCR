param(
  [string]$ShaFile = "$PSScriptRoot\..\SHA256SUMS.txt",
  [string]$OutFile = "$PSScriptRoot\..\MANIFEST.json",
  [string]$BundleVersion = "win64-v0.1.0",
  [string]$BuiltFor = "Windows 10/11 x64",
  [string]$Notes = "Full manifest auto-generated from SHA256SUMS.txt"
)

$ErrorActionPreference = "Stop"

# --- normalize to absolute paths (compatible with PS5) ---
function To-AbsPath([string]$p) {
  try {
    return (Resolve-Path -Path $p -ErrorAction Stop).Path
  } catch {
    # if not existing yet (e.g., OutFile), build absolute path from current location
    return [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $p))
  }
}

$ShaFileAbs = To-AbsPath $ShaFile
$OutFileAbs = To-AbsPath $OutFile

if (!(Test-Path $ShaFileAbs)) { throw "SHA file not found: $ShaFileAbs" }

function Normalize-PathForJson([string]$p) {
  $p = $p -replace '^\*',''
  $p = $p -replace '\\','/'  # backslash -> forward slash
  return $p
}

function Guess-License([string]$rel) {
  $relLow = $rel.ToLowerInvariant()
  if ($relLow -like "vendor/tessdata/*") { return "Apache-2.0" }
  if ($relLow -like "vendor/fonts/vazirmatn-*") { return "OFL-1.1" }
  if ($relLow -like "vendor/fonts/noto*") { return "CC BY 4.0 (OnlineWebFonts)" }
  if ($relLow -like "vendor/*.dll" -or $relLow -like "vendor/tesseract.exe") { return "Apache-2.0 / respective" }
  if ($relLow -like "vendor/*.html") { return "Apache-2.0 (Tesseract docs)" }
  if ($relLow -like "vendor/*.exe") { return "Apache-2.0 / respective" }
  return "see THIRD_PARTY_NOTICES.md"
}

$regex = '^(?<hash>[A-Fa-f0-9]{64}) \*(?<path>.+)$'
$items = @()

Get-Content -LiteralPath $ShaFileAbs | ForEach-Object {
  $m = [regex]::Match($_, $regex)
  if ($m.Success) {
    $hash = $m.Groups['hash'].Value.ToUpperInvariant()
    $rel  = Normalize-PathForJson $m.Groups['path'].Value

    $full = Join-Path (Get-Location) $rel
    $full = [System.IO.Path]::GetFullPath($full)

    $size = $null
    if (Test-Path -LiteralPath $full) {
      $size = [int64](Get-Item -LiteralPath $full).Length
    }

    $items += [pscustomobject]@{
      path         = $rel
      sha256       = $hash
      size         = $size
      license_hint = (Guess-License $rel)
    }
  }
}

$root = [ordered]@{
  bundle_version   = $BundleVersion
  built_for        = $BuiltFor
  notes            = $Notes
  generated_at_utc = (Get-Date).ToUniversalTime().ToString("yyyy-MM-ddTHH:mm:ssZ")
  checksum_source  = (Split-Path -Leaf $ShaFileAbs)
  files            = $items | Sort-Object path
}

# Ensure parent dir for output exists
$outDir = Split-Path -Parent $OutFileAbs
if (![string]::IsNullOrWhiteSpace($outDir) -and !(Test-Path $outDir)) {
  New-Item -ItemType Directory -Path $outDir -Force | Out-Null
}

# Write JSON using Set-Content (UTF8)
$json = ($root | ConvertTo-Json -Depth 5 -Compress:$false)
$json | Set-Content -LiteralPath $OutFileAbs -Encoding UTF8

if (!(Test-Path -LiteralPath $OutFileAbs)) {
  throw "Failed to write manifest to $OutFileAbs"
}

Write-Host "Wrote manifest: $OutFileAbs"
Write-Host "Files count  : $($items.Count)"