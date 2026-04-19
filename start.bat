chcp 65001
@echo off
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
    echo Запусти Ollama командой: ollama serve
    pause
    exit
)

echo.
echo Запуск сервера...
python -m uvicorn backend.app.main:app

echo.
echo ================= ERROR (если была) =================
pause