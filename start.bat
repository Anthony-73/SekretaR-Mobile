title SekretaR Launcher

@echo off
chcp 65001 > nul

echo ===============================
echo Запуск SekretaR...
echo ===============================

echo.
echo Активация виртуальной среды...
call .venv\Scripts\activate

echo.
echo Проверка Ollama...
curl http://localhost:11434 >nul 2>&1

if %errorlevel% neq 0 (
    echo ❌ Ollama не запущена!
    echo Запусти: ollama serve
    pause
    exit
)

echo.
echo 🚀 Запуск сервера...

start cmd /k python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000

echo.
echo ✅ SekretaR запущен в новом окне
pause