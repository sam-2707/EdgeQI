# EDGE-QI Integration Script
# Consolidates main folder and EDGE_QI subfolder into unified structure

Write-Host "=== EDGE-QI Project Integration ===" -ForegroundColor Cyan
Write-Host "This script will merge the production and research codebases" -ForegroundColor Yellow
Write-Host ""

$baseDir = "d:\DS LiT\Distri Sys\EDGE-QI"
$edgeQISubdir = Join-Path $baseDir "EDGE_QI"

# Step 1: Create backup
Write-Host "[1/8] Creating backup..." -ForegroundColor Green
$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$backupDir = Join-Path $baseDir "BACKUP_$timestamp"

if (!(Test-Path $backupDir)) {
    New-Item -ItemType Directory -Path $backupDir | Out-Null
    Write-Host "  ✓ Backup directory created: $backupDir" -ForegroundColor Gray
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

# Step 3: Move EDGE_QI backend files
Write-Host "[3/8] Moving backend files..." -ForegroundColor Green

if (Test-Path (Join-Path $edgeQISubdir "backend")) {
    $backendSrc = Join-Path $edgeQISubdir "backend"
    $backendDst = Join-Path $baseDir "src\backend"
    
    Get-ChildItem -Path $backendSrc -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($backendSrc.Length + 1)
        $destination = Join-Path $backendDst $relativePath
        
        if ($_.PSIsContainer) {
            if (!(Test-Path $destination)) {
                New-Item -ItemType Directory -Path $destination -Force | Out-Null
            }
        } else {
            Copy-Item -Path $_.FullName -Destination $destination -Force
        }
    }
    Write-Host "  Backend files copied" -ForegroundColor Gray
}

# Step 4: Move EDGE_QI frontend files
Write-Host "[4/8] Moving frontend files..." -ForegroundColor Green

if (Test-Path (Join-Path $edgeQISubdir "frontend")) {
    $frontendSrc = Join-Path $edgeQISubdir "frontend"
    $frontendDst = Join-Path $baseDir "src\frontend"
    
    Get-ChildItem -Path $frontendSrc -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($frontendSrc.Length + 1)
        $destination = Join-Path $frontendDst $relativePath
        
        if ($_.PSIsContainer) {
            if (!(Test-Path $destination)) {
                New-Item -ItemType Directory -Path $destination -Force | Out-Null
            }
        } else {
            Copy-Item -Path $_.FullName -Destination $destination -Force
        }
    }
    Write-Host "  ✓ Frontend files copied" -ForegroundColor Gray
}

# Step 5: Move edge_nodes
Write-Host "[5/8] Moving edge node files..." -ForegroundColor Green

if (Test-Path (Join-Path $edgeQISubdir "edge_nodes")) {
    $edgeNodesSrc = Join-Path $edgeQISubdir "edge_nodes"
    $edgeNodesDst = Join-Path $baseDir "src\edge-nodes"
    
    Get-ChildItem -Path $edgeNodesSrc -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($edgeNodesSrc.Length + 1)
        $destination = Join-Path $edgeNodesDst $relativePath
        
        if ($_.PSIsContainer) {
            if (!(Test-Path $destination)) {
                New-Item -ItemType Directory -Path $destination -Force | Out-Null
            }
        } else {
            Copy-Item -Path $_.FullName -Destination $destination -Force
        }
    }
    Write-Host "  ✓ Edge node files copied" -ForegroundColor Gray
}

# Step 6: Consolidate Core files
Write-Host "[6/8] Consolidating core framework..." -ForegroundColor Green

$coreSrc = Join-Path $baseDir "Core"
$coreDst = Join-Path $baseDir "src\core"

if (Test-Path $coreSrc) {
    Get-ChildItem -Path $coreSrc -Recurse | ForEach-Object {
        $relativePath = $_.FullName.Substring($coreSrc.Length + 1)
        $destination = Join-Path $coreDst $relativePath
        
        if ($_.PSIsContainer) {
            if (!(Test-Path $destination)) {
                New-Item -ItemType Directory -Path $destination -Force | Out-Null
            }
        } else {
            Copy-Item -Path $_.FullName -Destination $destination -Force
        }
    }
    Write-Host "  ✓ Core framework copied" -ForegroundColor Gray
}

# Step 7: Move simulations
Write-Host "[7/8] Moving simulation files..." -ForegroundColor Green

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
        Write-Host "  ✓ Moved: $file" -ForegroundColor Gray
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
Write-Host "  ✓ Academic documents organized" -ForegroundColor Gray

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
Write-Host "  ✓ User guides organized" -ForegroundColor Gray

# Deployment docs
if (Test-Path (Join-Path $baseDir "docs")) {
    $docsSrc = Join-Path $baseDir "docs"
    $deploymentDst = Join-Path $baseDir "docs\deployment"
    
    $deploymentFiles = @(
        "COMPILATION_SUCCESS.md",
        "DASHBOARD_FIXES.md",
        "DASHBOARD_TROUBLESHOOTING.md",
        "ISSUE_RESOLUTION.md"
    )
    
    foreach ($file in $deploymentFiles) {
        $srcFile = Join-Path $docsSrc $file
        if (Test-Path $srcFile) {
            Copy-Item -Path $srcFile -Destination $deploymentDst -Force
        }
    }
}
Write-Host "  ✓ Deployment documentation organized" -ForegroundColor Gray

# Move infrastructure files
Write-Host "Organizing infrastructure..." -ForegroundColor Green

if (Test-Path (Join-Path $edgeQISubdir "docker-compose.yml")) {
    Copy-Item -Path (Join-Path $edgeQISubdir "docker-compose.yml") -Destination (Join-Path $baseDir "infrastructure") -Force
}

if (Test-Path (Join-Path $edgeQISubdir "deploy_system.sh")) {
    Copy-Item -Path (Join-Path $edgeQISubdir "deploy_system.sh") -Destination (Join-Path $baseDir "infrastructure\scripts") -Force
}

if (Test-Path (Join-Path $edgeQISubdir "deploy_edge_qi.sh")) {
    Copy-Item -Path (Join-Path $edgeQISubdir "deploy_edge_qi.sh") -Destination (Join-Path $baseDir "infrastructure\scripts") -Force
}

Write-Host "  ✓ Infrastructure files organized" -ForegroundColor Gray

# Move tools
Write-Host "Organizing tools..." -ForegroundColor Green

$toolFiles = @(
    "generate_architecture_diagram.py",
    "generate_comparison_table.py",
    "generate_performance_plots.py",
    "generate_response_time_plots.py",
    "performance_analyzer.py",
    "hardcoded_data_pipeline.py",
    "quick_demo.py",
    "integrate_framework.py"
)

$toolsDst = Join-Path $baseDir "tools"
foreach ($file in $toolFiles) {
    $srcFile = Join-Path $baseDir $file
    if (Test-Path $srcFile) {
        Copy-Item -Path $srcFile -Destination $toolsDst -Force
    }
}
Write-Host "  ✓ Tools organized" -ForegroundColor Gray

# Copy integrated README
Write-Host "Setting up master README..." -ForegroundColor Green
if (Test-Path (Join-Path $baseDir "README_INTEGRATED.md")) {
    Copy-Item -Path (Join-Path $baseDir "README_INTEGRATED.md") -Destination (Join-Path $baseDir "README_NEW.md") -Force
    Write-Host "  ✓ Master README created as README_NEW.md" -ForegroundColor Gray
    Write-Host "  ⚠ Review and rename to README.md when ready" -ForegroundColor Yellow
}

# Summary
Write-Host ""
Write-Host "=== Integration Complete ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Yellow
Write-Host "1. Review the new structure in: $baseDir" -ForegroundColor White
Write-Host "2. Update import paths in Python files (from Core.* to src.core.*)" -ForegroundColor White
Write-Host "3. Consolidate requirements.txt files" -ForegroundColor White
Write-Host "4. Test the integrated system" -ForegroundColor White
Write-Host "5. Update docker-compose.yml paths" -ForegroundColor White
Write-Host "6. Rename README_NEW.md to README.md" -ForegroundColor White
Write-Host ""
Write-Host "Backup location: $backupDir" -ForegroundColor Gray
Write-Host ""
Write-Host "✓ All files copied successfully!" -ForegroundColor Green
