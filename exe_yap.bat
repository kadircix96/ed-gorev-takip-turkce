@echo off
title ED Mission Tracker EXE Derleyici
color 0A

echo ===================================================
echo   ED Mission Tracker - EXE Olusturma Araci
echo ===================================================
echo.
echo 1. Gerekli paketler kontrol ediliyor (PyQt6, PyInstaller)...
python -m pip install PyQt6 pyinstaller -q

if %errorlevel% neq 0 (
    echo.
    echo HATA: Python yuklu degil veya PATH'e eklenmemis!
    pause
    exit /b
)

echo 2. mission.py dosyasi EXE formatina donusturuluyor...
echo Lutfen bekleyin, bu islem 1-2 dakika surebilir...
echo.

:: BURASI DEĞİŞTİ: pyinstaller yerine "python -m PyInstaller" kullanıyoruz
python -m PyInstaller --noconsole --onefile --clean mission.py

echo.
echo ===================================================
echo ISLEM TAMAMLANDI!
echo ===================================================
echo "dist" adli yeni bir klasor olusturuldu. 
echo Bu klasorun icindeki "mission.exe" dosyasini 
echo istedigin kisiyle paylasabilirsin!
echo Baska hicbir seye (Python dahil) ihtiyaclari yok.
echo.
pause