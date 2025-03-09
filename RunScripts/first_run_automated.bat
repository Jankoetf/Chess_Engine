@echo off

REM Check if the current directory name is "Chess_Engine"
for %%* in (.) do set currentDir=%%~n*
if /I not "%currentDir%"=="Chess_Engine" (
    cd Chess_Engine
)

REM Create virtual environment
python -m venv venv
REM Activate virtual environment
call venv\Scripts\activate
REM Install dependencies
pip install -r requirements.txt
REM Run the application
python main.py