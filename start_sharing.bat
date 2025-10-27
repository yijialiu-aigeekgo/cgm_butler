@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        CGM Butler - 共享启动脚本                               ║
echo ║        Share Application with Colleagues                       ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

echo 选择部署方案:
echo.
echo 1. Cloudflare Tunnel (推荐 - 完全免费)
echo    ✅ 最简单 ✅ 完全免费 ✅ 支持多用户
echo.
echo 2. ngrok (快速 - 免费版有限制)
echo    ⚡ 快速启动 💰 免费/付费
echo.
echo 3. 本地共享 (仅限局域网)
echo    🔒 无需工具 📍 仅同一网络
echo.

set /p choice="请选择 (1/2/3): "

if "%choice%"=="1" (
    call :cloudflare_tunnel
) else if "%choice%"=="2" (
    call :ngrok_share
) else if "%choice%"=="3" (
    call :local_share
) else (
    echo ❌ 无效选择
    goto end
)

goto end

:cloudflare_tunnel
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║           Cloudflare Tunnel 部署方案                           ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📋 步骤 1: 检查 cloudflared 是否已安装
cloudflared --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ cloudflared 未找到
    echo.
    echo 📥 请下载安装:
    echo    https://developers.cloudflare.com/cloudflare-one/connections/connect-applications/
    echo.
    echo 或使用 Windows 包管理器:
    echo    winget install Cloudflare.cloudflared
    echo.
    pause
    goto end
)

echo ✅ cloudflared 已安装
echo.

echo 📋 步骤 2: 启动应用程序...
echo.
echo 启动 Flask 仪表板 (端口 5000)...
start cmd /k "cd /d "%~dp0dashboard" && python app.py"
timeout /t 3 /nobreak

echo 启动 React 视频数字人 (端口 5173)...
cd /d "%~dp0cgm-avatar-app"
start cmd /k "npm run dev"
timeout /t 5 /nobreak

echo.
echo 📋 步骤 3: 启动 Cloudflare Tunnel...
echo.
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║  运行以下命令启动 Tunnel:                                     ║
echo ║                                                                ║
echo ║  cloudflared tunnel run cgm-butler                            ║
echo ║                                                                ║
echo ║  如果是第一次，请先运行:                                      ║
echo ║  cloudflared tunnel create cgm-butler                         ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 按任意键打开新窗口运行 cloudflared...
pause

start cmd /k "cloudflared tunnel run cgm-butler"

echo.
echo ✅ Cloudflare Tunnel 已启动！
echo.
echo 📌 共享这些链接给同事:
echo.
echo    📊 仪表板: https://cgm-butler-dashboard.pages.dev
echo    🎥 视频数字人: https://cgm-butler-avatar.pages.dev
echo.
echo 💡 同事可以直接访问这些链接，无需安装任何软件！
echo.
pause
goto end

:ngrok_share
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║              ngrok 部署方案                                    ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📋 步骤 1: 检查 ngrok 是否已安装
ngrok --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ❌ ngrok 未找到
    echo.
    echo 📥 请下载安装:
    echo    https://ngrok.com/download
    echo.
    echo 或使用 chocolatey:
    echo    choco install ngrok
    echo.
    pause
    goto end
)

echo ✅ ngrok 已安装
echo.

echo 📋 步骤 2: 启动应用程序...
echo.
echo 启动 Flask 仪表板 (端口 5000)...
start cmd /k "cd /d "%~dp0dashboard" && python app.py"
timeout /t 3 /nobreak

echo 启动 React 视频数字人 (端口 5173)...
cd /d "%~dp0cgm-avatar-app"
start cmd /k "npm run dev"
timeout /t 5 /nobreak

echo.
echo 📋 步骤 3: 启动 ngrok Tunnel...
echo.
echo 为仪表板创建公网URL...
start cmd /k "ngrok http 5000 --log=stdout --log-level=info"
timeout /t 3 /nobreak

echo 为视频数字人创建公网URL...
start cmd /k "ngrok http 5173 --log=stdout --log-level=info"

echo.
echo ✅ ngrok 已启动！
echo.
echo 📌 查看生成的公网URL:
echo.
echo    1. 打开浏览器访问 http://localhost:4040
echo    2. 你会看到两个 ngrok URL
echo    3. 复制这些URL分享给同事
echo.
echo 💡 免费版在每次重启时URL会变化
echo    ✨ 升级到 ngrok Pro 可以使用固定URL ($5/月)
echo.
pause
goto end

:local_share
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║             本地网络共享方案                                   ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo 📋 获取你的计算机IP地址...
echo.

for /f "tokens=2 delims=: " %%a in ('ipconfig ^| findstr /R /C:"IPv4.*[0-9]"') do (
    set "ipaddr=%%a"
)

echo 你的计算机 IPv4 地址: %ipaddr%
echo.

echo 📋 步骤 1: 启动所有服务...
echo.
echo 启动 Flask 仪表板 (端口 5000)...
start cmd /k "cd /d "%~dp0dashboard" && python app.py"
timeout /t 3 /nobreak

echo 启动 React 视频数字人 (端口 5173)...
cd /d "%~dp0cgm-avatar-app"
start cmd /k "npm run dev"
timeout /t 5 /nobreak

echo.
echo ✅ 所有服务已启动！
echo.
echo 📌 分享这些链接给同事 (需要在同一网络):
echo.
echo    📊 仪表板: http://%ipaddr%:5000
echo    🎥 视频数字人: http://%ipaddr%:5173
echo.
echo 💡 同事需要:
echo    1. 与你在同一网络 (WiFi或有线)
echo    2. 在浏览器中输入上述URL即可访问
echo.
pause
goto end

:end
echo.
echo 谢谢使用 CGM Butler！ 👋
echo.
endlocal

