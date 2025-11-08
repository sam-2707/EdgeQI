# Update Import Paths Script
# Updates all Python imports from old structure to new unified structure

Write-Host "=== Updating Import Paths ===" -ForegroundColor Cyan
Write-Host ""

$baseDir = "d:\DS LiT\Distri Sys\EDGE-QI"

# Define import path mappings
$importMappings = @{
    "from Core." = "from src.core."
    "import Core." = "import src.core."
    "from App." = "from src.core.app."
    "import App." = "import src.core.app."
    "from ML." = "from src.ml."
    "import ML." = "import src.ml."
}

Write-Host "Scanning Python files..." -ForegroundColor Green

$directories = @(
    "src\backend",
    "src\frontend",
    "src\core",
    "src\edge-nodes",
    "src\ml",
    "src\simulations",
    "tools",
    "tests"
)

$totalFiles = 0
$totalUpdates = 0

foreach ($dir in $directories) {
    $fullPath = Join-Path $baseDir $dir
    if (!(Test-Path $fullPath)) {
        continue
    }
    
    Write-Host "Processing: $dir" -ForegroundColor Yellow
    
    $pyFiles = Get-ChildItem -Path $fullPath -Filter "*.py" -Recurse -File
    
    foreach ($file in $pyFiles) {
        $content = Get-Content -Path $file.FullName -Raw
        $originalContent = $content
        $fileUpdated = $false
        
        foreach ($oldImport in $importMappings.Keys) {
            $newImport = $importMappings[$oldImport]
            if ($content -match [regex]::Escape($oldImport)) {
                $content = $content -replace [regex]::Escape($oldImport), $newImport
                $fileUpdated = $true
            }
        }
        
        if ($fileUpdated) {
            Set-Content -Path $file.FullName -Value $content -NoNewline
            $totalUpdates++
            Write-Host "  Updated: $($file.Name)" -ForegroundColor Gray
        }
        
        $totalFiles++
    }
}

Write-Host ""
Write-Host "=== Update Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Files scanned: $totalFiles" -ForegroundColor White
Write-Host "Files updated: $totalUpdates" -ForegroundColor White
Write-Host ""
Write-Host "Done!" -ForegroundColor Green
