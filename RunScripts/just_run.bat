@echo off
REM Clone the repository (only if it hasn't been cloned already)
git clone https://github.com/Jankoetf/Chess_Engine.git
cd Chess_Engine

REM Create virtual environment
python -m venv venv
REM Activate virtual environment
call venv\Scripts\activate
REM Install dependencies
pip install -r requirements.txt
REM Run the application
python main.py