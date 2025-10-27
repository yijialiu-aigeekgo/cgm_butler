@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        CGM Butler - Cloudflare Tunnel 完整启动脚本             ║
echo ║        Complete Launch with Tunnel for Sharing                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM 检查 cloudflared 是否已安装
echo 📋 检查 cloudflared 是否已安装...
cloudflared --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ cloudflared 未找到！
    echo.
    echo 请先安装 Cloudflare Tunnel:
    echo.
    echo 方式1: 直接下载
    echo   https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/
    echo.
    echo 方式2: 使用 winget (Windows包管理器)
    echo   winget install Cloudflare.cloudflared
    echo.
    echo 方式3: 使用 Chocolatey
    echo   choco install cloudflare-warp
    echo.
    pause
    exit /b 1
)

echo ✅ cloudflared 已安装
echo.

REM 设置项目路径
set PROJECT_ROOT=%~dp0
cd /d "%PROJECT_ROOT%"

echo 📂 项目路径: %PROJECT_ROOT%
echo.

REM 第1步：启动 Flask 仪表板
echo ╔════════════════════════════════════════════════════════════════╗
echo ║ 第1步: 启动 Flask 仪表板 (端口 5000)                          ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

if not exist "dashboard\app.py" (
    echo ❌ 错误: 找不到 dashboard\app.py
    pause
    exit /b 1
)

echo 启动 Flask...
start "CGM Butler - Dashboard" cmd /k "cd /d "%PROJECT_ROOT%dashboard" && python app.py"
timeout /t 3 /nobreak

echo ✅ Flask 已启动
echo.

REM 第2步：启动 React 视频数字人
echo ╔════════════════════════════════════════════════════════════════╗
echo ║ 第2步: 启动 React 视频数字人 (端口 5173)                     ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

if not exist "cgm-avatar-app\package.json" (
    echo ❌ 错误: 找不到 cgm-avatar-app\package.json
    pause
    exit /b 1
)

echo 启动 Vite 开发服务器...
start "CGM Butler - Avatar" cmd /k "cd /d "%PROJECT_ROOT%cgm-avatar-app" && npm run dev"
timeout /t 5 /nobreak

echo ✅ Vite 已启动
echo.

REM 第3步：启动 Cloudflare Tunnel
echo ╔════════════════════════════════════════════════════════════════╗
echo ║ 第3步: 启动 Cloudflare Tunnel                                 ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 启动 Tunnel...
start "CGM Butler - Tunnel" cmd /k "cloudflared tunnel run cgm-butler"

timeout /t 3 /nobreak

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    🎉 启动完成！                              ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ✅ 所有服务已启动！
echo.
echo 📊 仪表板:     http://localhost:5000
echo                https://cgm-butler-dashboard.pages.dev
echo.
echo 🎥 视频数字人: http://localhost:5173
echo                https://cgm-butler-avatar.pages.dev
echo.
echo.
echo 📌 分享给同事的链接:
echo.
echo    📊 仪表板: https://cgm-butler-dashboard.pages.dev
echo    🎥 视频数字人: https://cgm-butler-avatar.pages.dev
echo.
echo 💡 提示:
echo    • 本地访问: 使用 localhost 链接 (最快)
echo    • 远程访问: 使用 pages.dev 链接 (分享给同事)
echo    • 代码修改会自动同步到远程 (刷新浏览器即可看到)
echo    • 按 Ctrl+C 停止任何窗口
echo.
echo 📞 故障排除:
echo    1. 如果 Tunnel 断开，重启这个脚本
echo    2. 如果看不到更新，清除浏览器缓存 (Ctrl+Shift+Del)
echo    3. 检查防火墙设置
echo.

pause

