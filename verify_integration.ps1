# EDGE-QI Integration Verification Script
# Verifies the integrated project structure

Write-Host "=== EDGE-QI Integration Verification ===" -ForegroundColor Cyan
Write-Host ""

$baseDir = "d:\DS LiT\Distri Sys\EDGE-QI"

# Check directory structure
Write-Host "[1/5] Checking directory structure..." -ForegroundColor Green

$requiredDirs = @(
    "src\backend",
    "src\frontend",
    "src\core",
    "src\edge-nodes",
    "src\ml",
    "src\simulations",
    "docs\academic",
    "docs\user-guides",
    "infrastructure",
    "tools",
    "tests"
)

$allDirsExist = $true
foreach ($dir in $requiredDirs) {
    $fullPath = Join-Path $baseDir $dir
    if (Test-Path $fullPath) {
        Write-Host "  OK: $dir" -ForegroundColor Gray
    } else {
        Write-Host "  MISSING: $dir" -ForegroundColor Red
        $allDirsExist = $false
    }
}

# Check key files
Write-Host ""
Write-Host "[2/5] Checking key files..." -ForegroundColor Green

$keyFiles = @(
    "src\backend\src\main.py",
    "src\frontend\package.json",
    "src\core\scheduler\__init__.py",
    "src\edge-nodes\edge_node_complete.py",
    "src\simulations\realistic_intersection_sim.py",
    "docs\academic\EDGE_QI_IEEE_Paper.tex",
    "requirements_consolidated.txt",
    "README_NEW.md",
    "INTEGRATION_SUMMARY.md"
)

$allFilesExist = $true
foreach ($file in $keyFiles) {
    $fullPath = Join-Path $baseDir $file
    if (Test-Path $fullPath) {
        Write-Host "  OK: $file" -ForegroundColor Gray
    } else {
        Write-Host "  MISSING: $file" -ForegroundColor Red
        $allFilesExist = $false
    }
}

# Check Python environment
Write-Host ""
Write-Host "[3/5] Checking Python environment..." -ForegroundColor Green

$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.\d+") {
    Write-Host "  Python: $pythonVersion" -ForegroundColor Gray
} else {
    Write-Host "  WARNING: Python 3.x not found" -ForegroundColor Yellow
}

# Check Node.js
Write-Host ""
Write-Host "[4/5] Checking Node.js environment..." -ForegroundColor Green

try {
    $nodeVersion = node --version 2>&1
    Write-Host "  Node.js: $nodeVersion" -ForegroundColor Gray
} catch {
    Write-Host "  WARNING: Node.js not found (needed for frontend)" -ForegroundColor Yellow
}

# Count files
Write-Host ""
Write-Host "[5/5] Counting project files..." -ForegroundColor Green

$pyFiles = (Get-ChildItem -Path (Join-Path $baseDir "src") -Filter "*.py" -Recurse -File).Count
$jsFiles = (Get-ChildItem -Path (Join-Path $baseDir "src\frontend") -Filter "*.js","*.jsx","*.ts","*.tsx" -Recurse -File).Count
$mdFiles = (Get-ChildItem -Path (Join-Path $baseDir "docs") -Filter "*.md" -Recurse -File).Count

Write-Host "  Python files: $pyFiles" -ForegroundColor Gray
Write-Host "  JavaScript/TypeScript files: $jsFiles" -ForegroundColor Gray
Write-Host "  Documentation files: $mdFiles" -ForegroundColor Gray

# Summary
Write-Host ""
Write-Host "=== Verification Summary ===" -ForegroundColor Cyan
Write-Host ""

if ($allDirsExist -and $allFilesExist) {
    Write-Host "Status: PASSED" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your integrated EDGE-QI project is ready!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Run: update_imports.ps1" -ForegroundColor White
    Write-Host "2. Configure .env files" -ForegroundColor White
    Write-Host "3. Install dependencies: pip install -r requirements_consolidated.txt" -ForegroundColor White
    Write-Host "4. Test backend: cd src\backend; python src\main.py" -ForegroundColor White
    Write-Host "5. Test frontend: cd src\frontend; npm install; npm run dev" -ForegroundColor White
    Write-Host ""
    Write-Host "Read INTEGRATION_SUMMARY.md for complete details" -ForegroundColor Cyan
} else {
    Write-Host "Status: FAILED" -ForegroundColor Red
    Write-Host ""
    Write-Host "Some directories or files are missing." -ForegroundColor Red
    Write-Host "Re-run integrate_project.ps1 to fix the integration." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Done!" -ForegroundColor Green
