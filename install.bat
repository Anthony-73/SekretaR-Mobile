@echo off
echo ===============================
echo Установка SekretaR...
echo ===============================

echo.
echo Активация виртуальной среды...
call .venv\Scripts\activate

echo.
echo Обновление pip...
python -m pip install --upgrade pip

echo.
echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo ===============================
echo Установка завершена!
echo ===============================
pause