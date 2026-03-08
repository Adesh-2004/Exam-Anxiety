# AI-Based Exam Anxiety Detector

The AI-Based Exam Anxiety Detector is an intelligent mental-wellness support system designed to identify and categorize exam-related anxiety from student-generated text inputs. The platform classifies anxiety into three categories: Low, Moderate, and High Anxiety. 

## Project Architecture
- **Presentation Layer**: Streamlit
- **Application Layer**: FastAPI (Inference Endpoint) & BERT Model (Anxiety Classifier)
- **Data Layer**: Synthetic Anxiety Dataset & Trained BERT PyTorch Model.

## Project Structure
```
d:\Exam Anxiety\
├── backend/
│   └── main.py              # FastAPI endpoint for inference
├── frontend/
│   └── app.py               # Streamlit application UI
├── scripts/
│   ├── generate_dataset.py  # Generates synthetic training dataset
│   └── train_model.py       # Fine-tunes BERT model for classification
├── requirements.txt         # Project dependencies
└── run.bat                  # Batch script to run backend and frontend
```

## Setup & Execution

### 1. Set up the Environment
```cmd
python -m venv venv
.\venv\Scripts\python -m pip install -r requirements.txt
```

### 2. Generate Dataset and Train Model
Run the following scripts to generate synthetic data and train your local BERT model. Note: Training may take some time depending on hardware.
```cmd
.\venv\Scripts\python scripts\generate_dataset.py
.\venv\Scripts\python scripts\train_model.py
```

### 3. Run the Application
Execute the provided batch script to launch both the FastAPI backend and Streamlit frontend.
```cmd
run.bat
```

## Note on Ethics
This project handles mental health states. It strictly operates as a supportive and non-diagnostic tool, to help student well-being rather than replace professional counseling.
