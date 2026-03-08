import os
import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from transformers import BertTokenizer, BertForSequenceClassification, Trainer, TrainingArguments
from torch.utils.data import Dataset

class AnxietyDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_length):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_length = max_length

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, idx):
        text = str(self.texts[idx])
        label = self.labels[idx]

        encoding = self.tokenizer(
            text,
            add_special_tokens=True,
            max_length=self.max_length,
            return_token_type_ids=False,
            padding='max_length',
            truncation=True,
            return_attention_mask=True,
            return_tensors='pt',
        )

        return {
            'text': text,
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(label, dtype=torch.long)
        }

def train_model():
    print("Loading dataset...")
    df = pd.read_csv('data/anxiety_dataset.csv')
    
    # Encode labels
    label_encoder = LabelEncoder()
    df['encoded_label'] = label_encoder.fit_transform(df['label'])
    # Mapping: High, Low, Moderate -> 0, 1, 2 (Depends on alphabetical order)
    # Let's see the mapping
    mapping = dict(zip(label_encoder.classes_, range(len(label_encoder.classes_))))
    print("Label mapping:", mapping)

    X = df['text'].values
    y = df['encoded_label'].values

    # Split dataset
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model_name = 'bert-base-uncased'
    tokenizer = BertTokenizer.from_pretrained(model_name)
    model = BertForSequenceClassification.from_pretrained(model_name, num_labels=3)

    train_dataset = AnxietyDataset(X_train, y_train, tokenizer, max_length=128)
    val_dataset = AnxietyDataset(X_test, y_test, tokenizer, max_length=128)

    training_args = TrainingArguments(
        output_dir='./results',
        num_train_epochs=3,
        per_device_train_batch_size=8,
        per_device_eval_batch_size=8,
        warmup_steps=10,
        weight_decay=0.01,
        logging_dir='./logs',
        logging_steps=10,
        eval_strategy="epoch",
        save_strategy="epoch"
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_dataset,
        eval_dataset=val_dataset
    )

    try:
        print("Starting training...")
        trainer.train()

        print("Evaluating...")
        print(trainer.evaluate())

        # Save model and tokenizer
        os.makedirs('models/bert_anxiety_model', exist_ok=True)
        model.save_pretrained('models/bert_anxiety_model')
        tokenizer.save_pretrained('models/bert_anxiety_model')
        
        # Save label mapping
        import json
        with open('models/label_mapping.json', 'w') as f:
            json.dump(mapping, f)
            
        print("Model saved to models/bert_anxiety_model")
    except Exception as e:
        import traceback
        with open('error.txt', 'w') as f:
            traceback.print_exc(file=f)
        raise e

if __name__ == '__main__':
    train_model()
