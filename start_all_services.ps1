# CGM Butler - 启动所有服务
# 请在 PowerShell 中运行: .\start_all_services.ps1

Write-Host "=" -NoNewline
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host "  🚀 CGM Butler - 启动所有服务" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

# 检查 Python
Write-Host "📋 检查 Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ Python: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ❌ Python 未找到！请先安装 Python" -ForegroundColor Red
    exit 1
}

# 检查 Node.js/npm
Write-Host "📋 检查 Node.js..." -ForegroundColor Yellow

# 尝试多个可能的 Node.js 路径
$nodePaths = @(
    "C:\Program Files\nodejs",
    "C:\Program Files (x86)\nodejs",
    "$env:LOCALAPPDATA\Programs\nodejs",
    "$env:APPDATA\npm"
)

$nodeFound = $false
foreach ($path in $nodePaths) {
    if (Test-Path $path) {
        $env:Path += ";$path"
        $nodeFound = $true
    }
}

$npmVersion = npm --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✅ npm: v$npmVersion" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  npm 未找到！将跳过前端服务" -ForegroundColor Yellow
    $skipFrontend = $true
}

Write-Host ""
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""

# 服务 1: Flask Dashboard
Write-Host "🔧 启动服务 1/3: Flask Dashboard (端口 5000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd 'D:\cgm butler\dashboard'; Write-Host '🟢 Flask Dashboard 启动中...' -ForegroundColor Green; python app.py"
) -WindowStyle Normal

Start-Sleep -Seconds 2

# 服务 2: Minerva FastAPI Backend
Write-Host "🔧 启动服务 2/3: Minerva Backend (端口 8000)..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList @(
    "-NoExit",
    "-Command",
    "cd 'D:\cgm butler\minerva'; Write-Host '🟢 Minerva Backend 启动中...' -ForegroundColor Green; python -m uvicorn main:app --reload --port 8000"
) -WindowStyle Normal

Start-Sleep -Seconds 2

# 服务 3: Vite Frontend
if (-not $skipFrontend) {
    Write-Host "🔧 启动服务 3/3: Vite Frontend (端口 5173)..." -ForegroundColor Cyan
    
    # 构建 npm 路径设置命令
    $pathSetup = ""
    foreach ($path in $nodePaths) {
        if (Test-Path $path) {
            $pathSetup += "`$env:Path += ';$path'; "
        }
    }
    
    Start-Process powershell -ArgumentList @(
        "-NoExit",
        "-Command",
        "$pathSetup cd 'D:\cgm butler\cgm-avatar-app'; Write-Host '🟢 Vite Frontend 启动中...' -ForegroundColor Green; npm run dev"
    ) -WindowStyle Normal
    
    Start-Sleep -Seconds 2
} else {
    Write-Host "⚠️  跳过前端服务 (npm 未找到)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host "  ✅ 所有服务启动命令已执行！" -ForegroundColor Green
Write-Host ("=" * 60) -ForegroundColor Cyan
Write-Host ""
Write-Host "📝 请检查新打开的 3 个 PowerShell 窗口，确认服务启动成功：" -ForegroundColor Yellow
Write-Host "   1️⃣  Flask Dashboard:  http://localhost:5000" -ForegroundColor White
Write-Host "   2️⃣  Minerva Backend:  http://localhost:8000" -ForegroundColor White
Write-Host "   3️⃣  Vite Frontend:    http://localhost:5173" -ForegroundColor White
Write-Host ""
Write-Host "🌐 前端访问地址: http://localhost:5173" -ForegroundColor Green
Write-Host ""
Write-Host "⚠️  如果某个服务启动失败，请查看对应窗口的错误信息" -ForegroundColor Yellow
Write-Host ""

