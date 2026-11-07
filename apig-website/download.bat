@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================
echo  Downloading product images -> images/
echo ==========================================
C:\Python314\python.exe download_images.py
echo.
echo Done. Images saved in images/
pause