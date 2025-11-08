# EDGE-QI 3D Traffic Simulation Setup Script
# Run this to set up the Next.js web simulation

Write-Host "🚦 EDGE-QI 3D Traffic Simulation Setup" -ForegroundColor Cyan
Write-Host "=" * 50 -ForegroundColor Cyan

# Check Node.js installation
Write-Host "`n📦 Checking Node.js installation..." -ForegroundColor Yellow
try {
    $nodeVersion = node --version
    Write-Host "✓ Node.js found: $nodeVersion" -ForegroundColor Green
    
    # Check if version is 18+
    $versionNumber = [int]($nodeVersion -replace 'v(\d+)\..*', '$1')
    if ($versionNumber -lt 18) {
        Write-Host "⚠ Warning: Node.js 18+ recommended (found: $nodeVersion)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "✗ Node.js not found! Please install Node.js 18+ from https://nodejs.org" -ForegroundColor Red
    exit 1
}

# Check npm installation
Write-Host "`n📦 Checking npm installation..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✓ npm found: v$npmVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ npm not found!" -ForegroundColor Red
    exit 1
}

# Navigate to project directory
Write-Host "`n📂 Navigating to project directory..." -ForegroundColor Yellow
$projectPath = Join-Path $PSScriptRoot "traffic-sim-web"

if (-not (Test-Path $projectPath)) {
    Write-Host "✗ Project directory not found!" -ForegroundColor Red
    exit 1
}

Set-Location $projectPath
Write-Host "✓ In directory: $projectPath" -ForegroundColor Green

# Install dependencies
Write-Host "`n📦 Installing dependencies..." -ForegroundColor Yellow
Write-Host "This may take a few minutes..." -ForegroundColor Gray

npm install

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ Dependencies installed successfully!" -ForegroundColor Green
} else {
    Write-Host "✗ Failed to install dependencies!" -ForegroundColor Red
    exit 1
}

# Create .gitignore if it doesn't exist
Write-Host "`n📝 Creating .gitignore..." -ForegroundColor Yellow
$gitignoreContent = @"
# dependencies
/node_modules
/.pnp
.pnp.js

# testing
/coverage

# next.js
/.next/
/out/

# production
/build

# misc
.DS_Store
*.pem

# debug
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# local env files
.env*.local

# vercel
.vercel

# typescript
*.tsbuildinfo
next-env.d.ts
"@

Set-Content -Path ".gitignore" -Value $gitignoreContent
Write-Host "✓ .gitignore created" -ForegroundColor Green

# Setup complete
Write-Host "`n✅ Setup Complete!" -ForegroundColor Green
Write-Host "`nYou can now run the simulation with:" -ForegroundColor Cyan
Write-Host "  npm run dev                    # Development mode" -ForegroundColor White
Write-Host "  npm run build && npm start     # Production mode" -ForegroundColor White

Write-Host "`nOr from the EDGE-QI root directory:" -ForegroundColor Cyan
Write-Host "  python edge_qi.py web-sim      # Launch web simulation" -ForegroundColor White

Write-Host "`n🌐 The simulation will be available at: http://localhost:3000" -ForegroundColor Yellow

Write-Host "`n" -NoNewline
Read-Host "Press Enter to exit"
