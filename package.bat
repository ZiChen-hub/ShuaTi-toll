@echo off
title 小辰伴学 一键打包脚本
color 0A

echo ========================================
echo      小辰伴学 一键打包脚本
echo ========================================
echo.

echo 步骤1：检查PyInstaller是否安装...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
) else (
    echo √ PyInstaller已安装
)
echo.

echo 步骤2：清理旧构建产物...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
echo √ 清理完成
echo.

echo 步骤3：开始打包（需要1-3分钟）...
echo.

pyinstaller --noconfirm --clean xiaochenbanxue.spec

echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo √ 打包成功
    echo ========================================
    echo.
    echo 产物位置: dist\小辰伴学.exe
    echo.
) else (
    echo ========================================
    echo × 打包失败，请检查上方错误信息
    echo ========================================
)

pause