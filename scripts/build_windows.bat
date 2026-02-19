@echo off
echo Starting Build Process for RestaurantOS...

:: Ensure script runs from repository root (scripts\build_windows.bat -> repo_root\scripts)
pushd "%~dp0\.."

:: Create virtual environment if missing
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

:: Prefer venv python executable to avoid activation issues across shells
set "VENV_PY=%CD%\.venv\Scripts\python.exe"
if not exist "%VENV_PY%" (
    echo Virtual environment python not found, falling back to system python.
    set "VENV_PY=python"
)

:: Install dependencies
echo Installing dependencies...
"%VENV_PY%" -m pip install -r "%CD%\requirements.txt"

:: Run PyInstaller using the venv python to ensure correct interpreter
echo Bundling application with PyInstaller...
"%VENV_PY%" -m PyInstaller --clean "%CD%\restaurant_os.spec"

echo.
echo Build Complete!
echo The executable can be found in the "dist/RestaurantOS" folder.
popd
pause
