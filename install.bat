@echo off
:: Installation script for Renaissance Stock Ranking System (Windows)

echo Setting up Renaissance Stock Ranking System...

:: Create virtual environment if it doesn't exist
if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
) else (
    echo Virtual environment already exists.
)

:: Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate

:: Install requirements
echo Installing dependencies...
pip install -r requirements.txt

:: Install the package in development mode
echo Installing Renaissance Stock Ranking package...
pip install -e .

echo Installation complete!
echo.
echo To use the system:
echo 1. Activate the virtual environment: venv\Scripts\activate
echo 2. Run the ranking: python scripts\run_ranking.py
echo 3. Generate visualizations: python scripts\visualize_results.py
echo 4. Analyze sectors: python scripts\analyze_sectors.py
echo.
echo Alternatively, you can use the command-line tools:
echo - renaissance-rank
echo - renaissance-visualize
echo - renaissance-analyze
echo - renaissance-extract

pause 