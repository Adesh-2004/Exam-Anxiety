import os
import json
import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import BertTokenizer, BertForSequenceClassification

app = FastAPI(title="Exam Anxiety Detector API", version="1.0.0")

# Request Model
class TextRequest(BaseModel):
    text: str

# Globals for model and tokenizer
model = None
tokenizer = None
label_mapping = {}
reverse_mapping = {}

import threading

def load_model_background():
    global model, tokenizer, label_mapping, reverse_mapping
    model_dir = "models/bert_anxiety_model"
    mapping_file = "models/label_mapping.json"
    
    if os.path.exists(model_dir) and os.path.exists(mapping_file):
        print("Loading pre-trained model in the background...")
        tokenizer = BertTokenizer.from_pretrained(model_dir)
        model = BertForSequenceClassification.from_pretrained(model_dir)
        model.eval()
        
        with open(mapping_file, 'r') as f:
            label_mapping = json.load(f)
            reverse_mapping = {v: k for k, v in label_mapping.items()}
        print("Model loaded successfully!")
    else:
        print("Model or mapping not found. Please train the model first.")

@app.on_event("startup")
def startup_event():
    # Start loading the model in a background thread so Uvicorn can bind the port immediately
    thread = threading.Thread(target=load_model_background)
    thread.start()

@app.post("/predict")
def predict_anxiety(request: TextRequest):
    if model is None or tokenizer is None:
        raise HTTPException(status_code=503, detail="Model is not loaded. Train the model first.")
    
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text cannot be empty.")

    try:
        inputs = tokenizer(
            request.text,
            return_tensors="pt",
            truncation=True,
            padding=True,
            max_length=128
        )
        
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            predicted_class_id = torch.argmax(logits, dim=1).item()
            
        anxiety_level = reverse_mapping.get(predicted_class_id, "Unknown")
        
        return {
            "text": request.text,
            "anxiety_level": anxiety_level
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": model is not None}

if __name__ == "__main__":
    import uvicorn
    # Render assigns a dynamic port via the PORT environment variable
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port)
