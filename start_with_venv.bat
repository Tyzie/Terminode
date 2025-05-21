@echo off
call "venv\Scripts\activate.bat"

REM Check activation
python -c "import sys; print(sys.prefix != sys.base_prefix)" >nul
if %errorlevel% equ 0 (
    echo VENV activated. Loading Terminode
    python main.py
    pause
) else (
    echo Error while activating VENV
    pause
)