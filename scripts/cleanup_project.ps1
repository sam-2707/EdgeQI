# EDGE-QI Project Cleanup Script
# Organizes all files into proper directories

Write-Host "=== EDGE-QI Project Cleanup ===" -ForegroundColor Cyan
Write-Host ""

$baseDir = "d:\DS LiT\Distri Sys\EDGE-QI"

# Step 1: Clean up LaTeX auxiliary files
Write-Host "[1/10] Cleaning LaTeX auxiliary files..." -ForegroundColor Green

$latexAux = @("*.aux", "*.log", "*.out", "*.toc", "*.lof", "*.lot")
$latexDir = Join-Path $baseDir "docs\academic\latex_build"
if (!(Test-Path $latexDir)) {
    New-Item -ItemType Directory -Path $latexDir -Force | Out-Null
}

foreach ($pattern in $latexAux) {
    $files = Get-ChildItem -Path $baseDir -Filter $pattern -File
    foreach ($file in $files) {
        Move-Item -Path $file.FullName -Destination $latexDir -Force
        Write-Host "  Moved: $($file.Name)" -ForegroundColor Gray
    }
}

# Step 2: Organize Python scripts
Write-Host "[2/10] Organizing Python scripts..." -ForegroundColor Green

# Demo scripts
$demoScripts = @(
    "demo_anomaly_detection.py",
    "demo_bandwidth_optimization.py",
    "demo_headless_realtime.py",
    "demo_realistic_intersection.py",
    "demo_realtime_integration.py",
    "realistic_intersection_sim.py",
    "simple_intersection_sim.py",
    "high_performance_intersection.py",
    "high_performance_matplotlib.py",
    "verify_intersection_sim.py"
)

foreach ($script in $demoScripts) {
    $srcFile = Join-Path $baseDir $script
    $dstFile = Join-Path $baseDir "src\simulations\$script"
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Move-Item -Path $srcFile -Destination $dstFile -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $script" -ForegroundColor Gray
    }
}

# Utility scripts
$utilityScripts = @(
    "check_paper_improvements.py",
    "verify_paper_images.py",
    "test_analytics_fix.py"
)

foreach ($script in $utilityScripts) {
    $srcFile = Join-Path $baseDir $script
    $dstFile = Join-Path $baseDir "tools\$script"
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Move-Item -Path $srcFile -Destination $dstFile -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $script" -ForegroundColor Gray
    }
}

# Core scripts
$coreScripts = @(
    "edge_qi.py",
    "main.py",
    "integrate_framework.py"
)

foreach ($script in $coreScripts) {
    $srcFile = Join-Path $baseDir $script
    $dstFile = Join-Path $baseDir "src\core\$script"
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Move-Item -Path $srcFile -Destination $dstFile -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $script" -ForegroundColor Gray
    }
}

# Step 3: Organize generated reports and data
Write-Host "[3/10] Organizing reports and data..." -ForegroundColor Green

$reportsDir = Join-Path $baseDir "reports"
if (!(Test-Path $reportsDir)) {
    New-Item -ItemType Directory -Path $reportsDir -Force | Out-Null
}

$reportFiles = @(
    "edge_qi_demo_report.json",
    "integration_report.json",
    "quick_demo_report.json",
    "edge_qi_complete_analysis.json",
    "edge_qi_complete_analysis_summary.txt"
)

foreach ($file in $reportFiles) {
    $srcFile = Join-Path $baseDir $file
    if (Test-Path $srcFile) {
        Move-Item -Path $srcFile -Destination $reportsDir -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Step 4: Organize generated images
Write-Host "[4/10] Organizing generated images..." -ForegroundColor Green

$imagesDir = Join-Path $baseDir "docs\academic\figures"
if (!(Test-Path $imagesDir)) {
    New-Item -ItemType Directory -Path $imagesDir -Force | Out-Null
}

$imageFiles = @(
    "architecture_diagram.pdf",
    "architecture_diagram.png",
    "comparison_table.pdf",
    "comparison_table.png",
    "comprehensive_performance_analysis.pdf",
    "comprehensive_performance_analysis.png",
    "response_times_analysis.pdf",
    "response_times_analysis.png"
)

foreach ($file in $imageFiles) {
    $srcFile = Join-Path $baseDir $file
    if (Test-Path $srcFile) {
        Move-Item -Path $srcFile -Destination $imagesDir -Force
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Step 5: Organize LaTeX source files
Write-Host "[5/10] Organizing LaTeX source files..." -ForegroundColor Green

$latexSrcDir = Join-Path $baseDir "docs\academic"
$latexFiles = @(
    "EDGE_QI_IEEE_Paper.tex",
    "EDGE_QI_Performance_Report.tex",
    "EDGE_QI_Performance_Report_Balanced.tex",
    "EDGE_QI_Performance_Report_Balanced_Fixed.tex",
    "EDGE_QI_Performance_Report_Optimized.tex",
    "EDGE_QI_Performance_Report.pdf",
    "EDGE_QI_Performance_Report_Balanced.pdf"
)

foreach ($file in $latexFiles) {
    $srcFile = Join-Path $baseDir $file
    $dstFile = Join-Path $latexSrcDir $file
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Move-Item -Path $srcFile -Destination $dstFile -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $file" -ForegroundColor Gray
    }
}

# Step 6: Organize markdown documentation
Write-Host "[6/10] Organizing markdown documentation..." -ForegroundColor Green

# Academic documentation
$academicDocs = @(
    "IEEE_PAPER_README.md",
    "IMPLEMENTATION_STATUS.md",
    "INDUSTRY_STANDARDS_ANALYSIS.md",
    "NOVEL_CONTRIBUTIONS.md",
    "PERFORMANCE_COMPARISON.md",
    "ANALYTICS_FIX_REPORT.md"
)

foreach ($doc in $academicDocs) {
    $srcFile = Join-Path $baseDir $doc
    $dstFile = Join-Path $baseDir "docs\academic\$doc"
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Move-Item -Path $srcFile -Destination $dstFile -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $doc" -ForegroundColor Gray
    }
}

# User guides
$userGuideDocs = @(
    "QUICK_START.md",
    "QUICK_START_WEB_SIM.md",
    "REALISTIC_INTERSECTION_README.md",
    "WEB_SIMULATION_MIGRATION.md"
)

foreach ($doc in $userGuideDocs) {
    $srcFile = Join-Path $baseDir $doc
    $dstFile = Join-Path $baseDir "docs\user-guides\$doc"
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Move-Item -Path $srcFile -Destination $dstFile -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $doc" -ForegroundColor Gray
    }
}

# Integration documentation
$integrationDir = Join-Path $baseDir "docs\integration"
if (!(Test-Path $integrationDir)) {
    New-Item -ItemType Directory -Path $integrationDir -Force | Out-Null
}

$integrationDocs = @(
    "INTEGRATION_PLAN.md",
    "INTEGRATION_SUMMARY.md",
    "INTEGRATION_COMPLETE.md",
    "INTEGRATION_CHECKLIST.md"
)

foreach ($doc in $integrationDocs) {
    $srcFile = Join-Path $baseDir $doc
    if (Test-Path $srcFile) {
        Move-Item -Path $srcFile -Destination $integrationDir -Force
        Write-Host "  Moved: $doc" -ForegroundColor Gray
    }
}

# Step 7: Organize PowerShell scripts
Write-Host "[7/10] Organizing PowerShell scripts..." -ForegroundColor Green

$scriptsDir = Join-Path $baseDir "scripts"
if (!(Test-Path $scriptsDir)) {
    New-Item -ItemType Directory -Path $scriptsDir -Force | Out-Null
}

$psScripts = @(
    "compile_paper.bat",
    "setup_web_sim.ps1",
    "integrate_project.ps1",
    "update_imports.ps1",
    "consolidate_requirements.ps1",
    "verify_integration.ps1",
    "execute_integration.ps1",
    "cleanup_project.ps1"
)

foreach ($script in $psScripts) {
    $srcFile = Join-Path $baseDir $script
    $dstFile = Join-Path $scriptsDir $script
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Copy-Item -Path $srcFile -Destination $dstFile -Force
        Write-Host "  Copied: $script" -ForegroundColor Gray
    }
}

# Step 8: Organize tool scripts
Write-Host "[8/10] Organizing tool scripts..." -ForegroundColor Green

$toolScripts = @(
    "generate_architecture_diagram.py",
    "generate_comparison_table.py",
    "generate_performance_plots.py",
    "generate_response_time_plots.py",
    "performance_analyzer.py",
    "hardcoded_data_pipeline.py",
    "quick_demo.py"
)

foreach ($script in $toolScripts) {
    $srcFile = Join-Path $baseDir $script
    $dstFile = Join-Path $baseDir "tools\$script"
    if ((Test-Path $srcFile) -and ($srcFile -ne $dstFile)) {
        Move-Item -Path $srcFile -Destination $dstFile -Force -ErrorAction SilentlyContinue
        Write-Host "  Moved: $script" -ForegroundColor Gray
    }
}

# Step 9: Clean up Python cache
Write-Host "[9/10] Cleaning Python cache..." -ForegroundColor Green

$pycacheDirs = Get-ChildItem -Path $baseDir -Filter "__pycache__" -Recurse -Directory
foreach ($dir in $pycacheDirs) {
    Remove-Item -Path $dir.FullName -Recurse -Force -ErrorAction SilentlyContinue
    Write-Host "  Removed: $($dir.FullName.Replace($baseDir, ''))" -ForegroundColor Gray
}

$pycFiles = Get-ChildItem -Path $baseDir -Filter "*.pyc" -Recurse -File
foreach ($file in $pycFiles) {
    Remove-Item -Path $file.FullName -Force -ErrorAction SilentlyContinue
}

# Step 10: Organize old directories
Write-Host "[10/10] Organizing legacy directories..." -ForegroundColor Green

$archiveDir = Join-Path $baseDir "archive"
if (!(Test-Path $archiveDir)) {
    New-Item -ItemType Directory -Path $archiveDir -Force | Out-Null
}

# Move old Core, App, ML directories if they still exist and src/ versions exist
$legacyDirs = @("Core", "App", "ML")
foreach ($dir in $legacyDirs) {
    $legacyPath = Join-Path $baseDir $dir
    $newPath = Join-Path $baseDir "src\core"
    if ((Test-Path $legacyPath) -and (Test-Path $newPath)) {
        $archivePath = Join-Path $archiveDir $dir
        if (!(Test-Path $archivePath)) {
            Move-Item -Path $legacyPath -Destination $archivePath -Force -ErrorAction SilentlyContinue
            Write-Host "  Archived: $dir" -ForegroundColor Gray
        }
    }
}

# Archive EDGE_QI subfolder
$edgeQILegacy = Join-Path $baseDir "EDGE_QI"
if (Test-Path $edgeQILegacy) {
    $edgeQIArchive = Join-Path $archiveDir "EDGE_QI"
    if (!(Test-Path $edgeQIArchive)) {
        Move-Item -Path $edgeQILegacy -Destination $edgeQIArchive -Force -ErrorAction SilentlyContinue
        Write-Host "  Archived: EDGE_QI" -ForegroundColor Gray
    }
}

# Step 11: Update main README
Write-Host "[11/10] Updating main README..." -ForegroundColor Green

$readmeNew = Join-Path $baseDir "README_NEW.md"
$readmeMain = Join-Path $baseDir "README.md"
$readmeOld = Join-Path $baseDir "archive\README_OLD.md"

if (Test-Path $readmeNew) {
    if (Test-Path $readmeMain) {
        Move-Item -Path $readmeMain -Destination $readmeOld -Force
    }
    Move-Item -Path $readmeNew -Destination $readmeMain -Force
    Write-Host "  Updated main README" -ForegroundColor Gray
}

# Update requirements
$reqConsolidated = Join-Path $baseDir "requirements_consolidated.txt"
$reqMain = Join-Path $baseDir "requirements.txt"
$reqOld = Join-Path $baseDir "archive\requirements_old.txt"

if (Test-Path $reqConsolidated) {
    if (Test-Path $reqMain) {
        Copy-Item -Path $reqMain -Destination $reqOld -Force
    }
    Copy-Item -Path $reqConsolidated -Destination $reqMain -Force
    Write-Host "  Updated requirements.txt" -ForegroundColor Gray
}

# Summary
Write-Host ""
Write-Host "=== Cleanup Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Project organization:" -ForegroundColor Yellow
Write-Host "  src/          - All source code" -ForegroundColor White
Write-Host "  docs/         - All documentation" -ForegroundColor White
Write-Host "  tools/        - Utility scripts" -ForegroundColor White
Write-Host "  scripts/      - PowerShell/batch scripts" -ForegroundColor White
Write-Host "  reports/      - Generated reports" -ForegroundColor White
Write-Host "  tests/        - Test suites" -ForegroundColor White
Write-Host "  infrastructure/ - Deployment configs" -ForegroundColor White
Write-Host "  archive/      - Legacy files" -ForegroundColor White
Write-Host ""
Write-Host "README.md and requirements.txt updated!" -ForegroundColor Green
Write-Host ""
Write-Host "Done!" -ForegroundColor Green
