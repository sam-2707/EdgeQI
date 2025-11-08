# EDGE-QI Integration Script - Simplified
# Consolidates main folder and EDGE_QI subfolder into unified structure

Write-Host "=== EDGE-QI Project Integration ===" -ForegroundColor Cyan
Write-Host ""

$baseDir = "d:\DS LiT\Distri Sys\EDGE-QI"
$edgeQISubdir = Join-Path $baseDir "EDGE_QI"

# Step 1: Create backup
Write-Host "[1/8] Creating backup..." -ForegroundColor Green
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $baseDir "BACKUP_$timestamp"

if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Write-Host "  Backup directory created" -ForegroundColor Gray
}

# Step 2: Create new directory structure
Write-Host "[2/8] Creating unified directory structure..." -ForegroundColor Green

$directories = @(
    "src\backend",
    "src\frontend",
    "src\core",
    "src\edge-nodes",
    "src\ml",
    "src\simulations",
    "docs\academic",
    "docs\api",
    "docs\deployment",
    "docs\user-guides",
    "infrastructure\docker",
    "infrastructure\scripts",
    "datasets",
    "models\trained",
    "tests\integration",
    "tools"
)

foreach ($dir in $directories) {
    $fullPath = Join-Path $baseDir $dir
    if (!(Test-Path $fullPath)) {
        New-Item -ItemType Directory -Path $fullPath -Force | Out-Null
        Write-Host "  Created: $dir" -ForegroundColor Gray
    }
}

# Step 3: Copy backend
Write-Host "[3/8] Copying backend files..." -ForegroundColor Green
$backendSrc = Join-Path $edgeQISubdir "backend"
$backendDst = Join-Path $baseDir "src\backend"
if (Test-Path $backendSrc) {
    Copy-Item -Path "$backendSrc\*" -Destination $backendDst -Recurse -Force
    Write-Host "  Backend files copied" -ForegroundColor Gray
}

# Step 4: Copy frontend
Write-Host "[4/8] Copying frontend files..." -ForegroundColor Green
$frontendSrc = Join-Path $edgeQISubdir "frontend"
$frontendDst = Join-Path $baseDir "src\frontend"
if (Test-Path $frontendSrc) {
    Copy-Item -Path "$frontendSrc\*" -Destination $frontendDst -Recurse -Force
    Write-Host "  Frontend files copied" -ForegroundColor Gray
}

# Step 5: Copy edge_nodes
Write-Host "[5/8] Copying edge node files..." -ForegroundColor Green
$edgeNodesSrc = Join-Path $edgeQISubdir "edge_nodes"
$edgeNodesDst = Join-Path $baseDir "src\edge-nodes"
if (Test-Path $edgeNodesSrc) {
    Copy-Item -Path "$edgeNodesSrc\*" -Destination $edgeNodesDst -Recurse -Force
    Write-Host "  Edge node files copied" -ForegroundColor Gray
}

# Step 6: Copy Core framework
Write-Host "[6/8] Copying core framework..." -ForegroundColor Green
$coreSrc = Join-Path $baseDir "Core"
$coreDst = Join-Path $baseDir "src\core"
if (Test-Path $coreSrc) {
    Copy-Item -Path "$coreSrc\*" -Destination $coreDst -Recurse -Force
    Write-Host "  Core framework copied" -ForegroundColor Gray
}

# Step 7: Copy simulations
Write-Host "[7/8] Copying simulation files..." -ForegroundColor Green
$simFiles = @(
    "realistic_intersection_sim.py",
    "simple_intersection_sim.py",
    "high_performance_intersection.py",
    "demo_realtime_integration.py",
    "demo_realistic_intersection.py",
    "demo_anomaly_detection.py",
    "demo_bandwidth_optimization.py",
    "demo_headless_realtime.py"
)

$simDst = Join-Path $baseDir "src\simulations"
foreach ($file in $simFiles) {
    $srcFile = Join-Path $baseDir $file
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $simDst -Force
        Write-Host "  Copied: $file" -ForegroundColor Gray
    }
}

# Step 8: Organize documentation
Write-Host "[8/8] Organizing documentation..." -ForegroundColor Green

# Academic documents
$academicFiles = @(
    "EDGE_QI_IEEE_Paper.tex",
    "EDGE_QI_Performance_Report_Balanced.tex",
    "IMPLEMENTATION_STATUS.md",
    "NOVEL_CONTRIBUTIONS.md",
    "PERFORMANCE_COMPARISON.md",
    "INDUSTRY_STANDARDS_ANALYSIS.md",
    "ANALYTICS_FIX_REPORT.md"
)

$academicDst = Join-Path $baseDir "docs\academic"
foreach ($file in $academicFiles) {
    $srcFile = Join-Path $baseDir $file
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $academicDst -Force
    }
}
Write-Host "  Academic documents organized" -ForegroundColor Gray

# User guides
$userGuideDst = Join-Path $baseDir "docs\user-guides"
$userGuideFiles = @(
    "QUICK_START.md",
    "QUICK_START_WEB_SIM.md",
    "REALISTIC_INTERSECTION_README.md",
    "WEB_SIMULATION_MIGRATION.md"
)

foreach ($file in $userGuideFiles) {
    $srcFile = Join-Path $baseDir $file
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $userGuideDst -Force
    }
}
Write-Host "  User guides organized" -ForegroundColor Gray

# Tools
$toolFiles = @(
    "generate_architecture_diagram.py",
    "generate_comparison_table.py",
    "generate_performance_plots.py",
    "generate_response_time_plots.py",
    "performance_analyzer.py",
    "hardcoded_data_pipeline.py",
    "quick_demo.py"
)

$toolsDst = Join-Path $baseDir "tools"
foreach ($file in $toolFiles) {
    $srcFile = Join-Path $baseDir $file
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $toolsDst -Force
    }
}
Write-Host "  Tools organized" -ForegroundColor Gray

# Copy integrated README
if (Test-Path (Join-Path $baseDir "README_INTEGRATED.md")) {
    Copy-Item -Path (Join-Path $baseDir "README_INTEGRATED.md") -Destination (Join-Path $baseDir "README_NEW.md") -Force
    Write-Host "  Master README created as README_NEW.md" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "=== Integration Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "New structure created in: $baseDir" -ForegroundColor White
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review the new structure" -ForegroundColor White
Write-Host "2. Update import paths (Core.* -> src.core.*)" -ForegroundColor White
Write-Host "3. Consolidate requirements.txt files" -ForegroundColor White
Write-Host "4. Test the integrated system" -ForegroundColor White
Write-Host "5. Rename README_NEW.md to README.md" -ForegroundColor White
Write-Host ""
Write-Host "Done!" -ForegroundColor Green
