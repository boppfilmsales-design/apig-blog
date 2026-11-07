@echo off
chcp 65001 >nul
cd /d "%~dp0"
echo ==========================================
echo  aenmgroup.com product crawler
echo ==========================================
C:\Python314\python.exe crawl_products.py
echo.
echo Done. Output: products.json
pause