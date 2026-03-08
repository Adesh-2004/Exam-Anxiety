import pandas as pd
import random
import os

# Define sample datasets for each anxiety level
low_anxiety = [
    "I feel fairly prepared for the exam tomorrow.",
    "Just a bit nervous, but I've studied well.",
    "Looking forward to getting this test over with.",
    "I'm calm. I've covered all the material.",
    "It's just another exam, I will do fine.",
    "I feel confident about most of the topics.",
    "Studying went well, so I think I'll be okay.",
    "I'm relaxed and ready to take the test.",
    "A little normal pre-test jitter, but mostly feeling good.",
    "I've got a good grasp on the syllabus.",
    "I've slept well and I'm ready.",
    "Not too worried, I passed the practice tests easily."
]

moderate_anxiety = [
    "I'm starting to feel the pressure for the finals.",
    "I'm a bit overwhelmed with the amount of syllabus left.",
    "Hopefully, the questions aren't too tricky. I'm anxious.",
    "My heart rate is up a bit thinking about tomorrow.",
    "I feel like I forgot what I read yesterday.",
    "I'm stressing over the math section, but I think I can pass.",
    "Not feeling 100% confident, my stomach is in knots.",
    "I need to revise everything again, feeling tense.",
    "I'm getting stressed out. What if I fail?",
    "It's hard to concentrate right now with the exam so close.",
    "Nervous but trying to stay positive.",
    "The pressure is definitely building up tonight."
]

high_anxiety = [
    "I can't breathe, I'm panicking so much about this exam.",
    "I'm terrified I'm going to fail no matter how much I study.",
    "My mind is completely blank and my hands are shaking.",
    "This stress is unbearable. I can't sleep or eat.",
    "I feel like giving up, the pressure is too much.",
    "I'm having a panic attack just thinking about the test.",
    "I keep crying because I'm so overwhelmed by everything.",
    "I am absolutely freezing up. I can't remember anything.",
    "So dreading tomorrow. I can't stop my thoughts racing.",
    "I feel sick to my stomach with worry.",
    "It feels like the end of the world if I mess this up.",
    "Complete breakdown over here. I can't cope with the stress."
]

def generate_dataset(num_samples=300):
    data = []
    for _ in range(num_samples):
        label = random.choice(['Low', 'Moderate', 'High'])
        if label == 'Low':
            text = random.choice(low_anxiety)
        elif label == 'Moderate':
            text = random.choice(moderate_anxiety)
        else:
            text = random.choice(high_anxiety)
            
        # Add slight variations to make it slightly distinct
        # In a real scenario, this would be real user data.
        data.append({'text': text, 'label': label})
        
    df = pd.DataFrame(data)
    
    # Shuffle the dataset
    df = df.sample(frac=1).reset_index(drop=True)
    
    os.makedirs('data', exist_ok=True)
    df.to_csv('data/anxiety_dataset.csv', index=False)
    print(f"Dataset generated with {len(df)} samples and saved to data/anxiety_dataset.csv")

if __name__ == '__main__':
    generate_dataset()
