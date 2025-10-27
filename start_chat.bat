@echo off
echo ========================================
echo CGM Butler - 启动智能对话系统
echo ========================================
echo.

echo [1/2] 启动Dashboard服务...
start "CGM Dashboard" cmd /k "cd dashboard && python app.py"

timeout /t 3 /nobreak >nul

echo [2/2] 打开聊天界面...
start "" "digital_avatar\chat.html"

echo.
echo ========================================
echo ✓ 服务已启动！
echo ========================================
echo.
echo 服务信息：
echo - Dashboard: http://localhost:5000
echo - 聊天界面: 已在浏览器中打开
echo.
echo 功能说明：
echo - 默认使用 GPT-4o 进行智能对话
echo - 可以查询实时CGM数据、识别模式、获取建议
echo - 点击"启动数字人"按钮可切换到视频模式（即将推出）
echo.
echo 按任意键关闭此窗口...
pause >nul


