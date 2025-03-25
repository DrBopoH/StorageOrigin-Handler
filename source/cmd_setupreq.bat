@echo off
cd /d "%~dp0"

if not exist "venv\Scripts\activate" (
    echo Виртуальное окружение python не найдено; Запуск скрипта создания python venv...
    python -m venv venv
)

call venv\Scripts\activate
pip install -r requirements.txt
pause