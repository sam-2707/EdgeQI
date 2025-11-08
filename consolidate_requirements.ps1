# Consolidate Requirements Script
# Merges all requirements.txt files into one unified file

Write-Host "=== Consolidating Requirements ===" -ForegroundColor Cyan
Write-Host ""

$baseDir = "d:\DS LiT\Distri Sys\EDGE-QI"

# Find all requirements.txt files
$reqFiles = @(
    "requirements.txt",
    "EDGE_QI\requirements.txt",
    "src\backend\requirements.txt"
)

$allPackages = @{}

foreach ($reqFile in $reqFiles) {
    $fullPath = Join-Path $baseDir $reqFile
    if (Test-Path $fullPath) {
        Write-Host "Reading: $reqFile" -ForegroundColor Yellow
        
        $content = Get-Content -Path $fullPath
        foreach ($line in $content) {
            $line = $line.Trim()
            
            # Skip empty lines and comments
            if ($line -eq "" -or $line.StartsWith("#")) {
                continue
            }
            
            # Parse package name and version
            if ($line -match "^([a-zA-Z0-9_-]+)(.*)$") {
                $packageName = $matches[1].ToLower()
                $version = $matches[2]
                
                # Keep the most specific version
                if (!$allPackages.ContainsKey($packageName)) {
                    $allPackages[$packageName] = $line
                } elseif ($version -match "==") {
                    # Prefer exact versions over >= or no version
                    $allPackages[$packageName] = $line
                }
            }
        }
    }
}

# Sort packages alphabetically
$sortedPackages = $allPackages.Keys | Sort-Object | ForEach-Object { $allPackages[$_] }

# Write consolidated requirements
$outputFile = Join-Path $baseDir "requirements_consolidated.txt"
$header = @"
# EDGE-QI Unified Requirements
# Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
# Consolidated from multiple requirements.txt files

"@

$header | Set-Content -Path $outputFile
$sortedPackages | Add-Content -Path $outputFile

Write-Host ""
Write-Host "=== Consolidation Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Total unique packages: $($allPackages.Count)" -ForegroundColor White
Write-Host "Output file: requirements_consolidated.txt" -ForegroundColor White
Write-Host ""
Write-Host "Review and rename to requirements.txt when ready" -ForegroundColor Yellow
Write-Host ""
Write-Host "Done!" -ForegroundColor Green
