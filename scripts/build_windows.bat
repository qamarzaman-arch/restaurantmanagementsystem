@echo off
echo Starting Build Process for RestaurantOS...

:: Check for virtual environment
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Activate virtual environment
call .venv\Scripts\activate

:: Install dependencies
echo Installing dependencies...
pip install -r requirements.txt

:: Run PyInstaller
echo Bundling application with PyInstaller...
pyinstaller --clean restaurant_os.spec

echo.
echo Build Complete!
echo The executable can be found in the "dist/RestaurantOS" folder.
pause
