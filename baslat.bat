@echo off
title ED Mission Tracker Baslatici
echo Gerekli paketler kontrol ediliyor, lutfen bekleyin...

:: PyQt6 paketini sessiz modda (-q) kurmayi dener. Zaten varsa hizlica gecer.
pip install PyQt6 -q

if %errorlevel% neq 0 (
    echo.
    echo =======================================================
    echo HATA: Paketler yuklenemedi!
    echo Lutfen bilgisayarinda Python'un kurulu oldugundan ve
    echo kurulum sirasinda "Add Python to PATH" secenegini
    echo isaretlediginden emin ol.
    echo =======================================================
    echo.
    pause
    exit /b
)

:: pythonw komutu scripti arkadaki siyah cmd penceresi olmadan calistirir.
start pythonw mission.py