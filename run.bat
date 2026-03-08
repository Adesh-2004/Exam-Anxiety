@echo off
echo Starting AI-Based Exam Anxiety Detector...

:: Check if virtual environment exists
if not exist "venv\Scripts\python.exe" (
    echo =======================================================
    echo First-time setup detected. Setting up the environment...
    echo This may take a few minutes. Please do not close this window.
    echo =======================================================
    python -m venv venv
    .\venv\Scripts\python -m pip install --upgrade pip
    .\venv\Scripts\python -m pip install -r requirements.txt
    
    echo Generating synthetic dataset...
    .\venv\Scripts\python scripts\generate_dataset.py
    
    echo Training the model...
    .\venv\Scripts\python scripts\train_model.py
    
    echo =======================================================
    echo Setup complete! Starting the application...
    echo =======================================================
)

:: Start the FastAPI Backend
echo Starting FastAPI Backend on port 8000...
start cmd /k ".\venv\Scripts\python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload"

:: Give the backend a few seconds to initialize
timeout /t 5 /nobreak >nul

:: Start the Streamlit Frontend
echo Starting Streamlit Frontend...
start cmd /k ".\venv\Scripts\streamlit run frontend\app.py --browser.gatherUsageStats false"

echo System is running. You can close this window now.
