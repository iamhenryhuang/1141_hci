@echo off
chcp 65001 >nul
echo 手勢控制程式啟動器
echo ==================

echo 正在檢查環境...
python test_setup.py

echo.
echo 是否要啟動手勢控制程式？ (Y/N)
set /p choice=
if /i "%choice%"=="Y" (
    echo 啟動手勢控制程式...
    python gesture_control.py
) else (
    echo 程式已取消
)

pause
