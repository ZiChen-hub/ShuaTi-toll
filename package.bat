@echo off
chcp 65001 >nul
title 小辰伴学 一键打包工具
color 0A

echo ========================================
echo      小辰伴学 一键打包工具
echo ========================================
echo.

echo 步骤1：检查PyInstaller是否安装...
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 正在安装PyInstaller...
    pip install pyinstaller
) else (
    echo ✅ PyInstaller已安装
)
echo.

echo 步骤2：清理旧文件...
rmdir /s /q build 2>nul
rmdir /s /q dist 2>nul
del *.spec 2>nul
echo ✅ 清理完成
echo.

echo 步骤3：开始打包（这可能需要1-3分钟）...
echo.

pyinstaller ^
    --noconfirm ^
    --onedir ^
    --windowed ^
    --name "小辰伴学" ^
    --add-data "config.py;." ^
    --hidden-import=tkinter ^
    --hidden-import=requests ^
    --hidden-import=threading ^
    --hidden-import=datetime ^
    --hidden-import=hashlib ^
    --hidden-import=json ^
    --hidden-import=os ^
    --hidden-import=collections ^
    main.py

echo.
if %errorlevel% equ 0 (
    echo ========================================
    echo ✅ 打包成功！
    echo ========================================
    echo.
    echo 📁 程序位置: dist\小辰伴学\小辰伴学.exe
    echo.
    echo 📝 使用说明：
    echo 1. 整个 dist\小辰伴学 文件夹都可以分享给别人
    echo 2. 对方直接运行 小辰伴学.exe 即可
    echo 3. 无需安装Python，双击就能用
    echo.
    echo 🔧 文件列表：
    dir /b dist\小辰伴学
    echo.
    echo ========================================
) else (
    echo ========================================
    echo ❌ 打包失败！
    echo ========================================
    echo.
    echo 请按任意键查看错误信息...
)

pause