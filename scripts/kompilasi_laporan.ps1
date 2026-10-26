[CmdletBinding()]
param(
    [switch]$Draf
)

$ErrorActionPreference = 'Stop'

$taskRepo = Split-Path -Parent $PSScriptRoot
$taskProject = Join-Path $taskRepo 'laporan\latex'
$taskSource = Join-Path $taskProject 'main.tex'
$taskImages = Join-Path $taskProject 'images'
$taskCompiler = Join-Path $taskRepo '.tools\tectonic\tectonic.exe'
$taskExpectedImages = @(
    '01-struktur.png'
    '02-fungsi-denda-batas.png'
    '03-fungsi-pinjam.png'
    '04-fixture-cleanup.png'
    '05-parametrize-bva.png'
    '06-test-negatif.png'
    '07-mock-email.png'
    '08-mock-gagal-timeout.png'
    '09-hasil-pytest.png'
    '10-coverage-terminal.png'
    '11-coverage-html.png'
)

$taskMissingImages = @(
    $taskExpectedImages | Where-Object {
        -not (Test-Path -LiteralPath (Join-Path $taskImages $_) -PathType Leaf)
    }
)

if ($taskMissingImages.Count -gt 0) {
    Write-Host ('Screenshot belum tersedia ({0}/11):' -f $taskMissingImages.Count)
    $taskMissingImages | ForEach-Object { Write-Host ('  - {0}' -f $_) }
    Write-Host ('Simpan gambar di: {0}' -f $taskImages)
    if (-not $Draf) {
        Write-Host 'Kompilasi final dihentikan. Lengkapi 11 gambar, atau gunakan -Draf untuk pratinjau berpenanda DRAF.' -ForegroundColor Yellow
        exit 2
    }
    Write-Warning 'Mode DRAF: PDF menggunakan penanda untuk screenshot yang belum tersedia.'
}

if (-not (Test-Path -LiteralPath $taskSource -PathType Leaf)) {
    Write-Host ('Sumber LaTeX belum ditemukan: {0}' -f $taskSource) -ForegroundColor Red
    exit 3
}

if (-not (Test-Path -LiteralPath $taskCompiler -PathType Leaf)) {
    Write-Host ('Compiler portabel belum ditemukan: {0}' -f $taskCompiler) -ForegroundColor Red
    Write-Host 'Gunakan Tectonic Windows x86_64 resmi di folder .tools\tectonic, atau kompilasi folder laporan\latex melalui editor LaTeX.'
    exit 4
}

$taskExitCode = 1
Push-Location -LiteralPath $taskProject
try {
    & $taskCompiler --untrusted --keep-logs --color never --outdir $taskProject 'main.tex'
    $taskExitCode = $LASTEXITCODE
}
finally {
    Pop-Location
}

if ($taskExitCode -ne 0) {
    Write-Host ('Kompilasi gagal; exit code Tectonic: {0}' -f $taskExitCode) -ForegroundColor Red
    exit $taskExitCode
}

$taskPdf = Join-Path $taskProject 'main.pdf'
if (-not (Test-Path -LiteralPath $taskPdf -PathType Leaf)) {
    Write-Host 'Tectonic selesai tanpa menghasilkan main.pdf.' -ForegroundColor Red
    exit 5
}

Write-Host ('PDF tersedia: {0}' -f $taskPdf) -ForegroundColor Green
exit 0
