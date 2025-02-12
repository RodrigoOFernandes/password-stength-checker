import sys
import re
import pandas as pd
import requests
import hashlib
import math 
import joblib
from utils import extract_features, has_sequence, has_keyboard_walk

model = joblib.load("password_strength_model.pkl")

def calculate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in password):
        charset_size += 32
    
    entropy = len(password) * math.log2(charset_size)
    return entropy 

def has_repetition(password):
    return any(password[i] == password[i+1] == password[i+2] == password[i+3] for i in range(len(password) - 3))

def is_breached(password):
    sha1_hash = hashlib.sha1(password.encode()).hexdigest().upper()
    prefix, suffix = sha1_hash[:5], sha1_hash[5:]
    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix}", timeout=5)
        if response.status_code == 200:
            return suffix in response.text
    except requests.exceptions.RequestException:
        pass  
    return False

'''
def calculate_score(password):
    if is_breached(password):
        return 0  

    score = 0
    length = len(password)
    entropy = calculate_entropy(password)
    
    if length >= 12:
        score += 3
    elif length >= 8:
        score += 2
    elif length >= 6:
        score += 1
    
    if entropy > 50:
        score += 5
    elif entropy > 30:
        score += 3
    elif entropy > 20:
        score += 1
    
    if has_repetition(password):
        score -= 2
    if has_sequence(password):
        score -= 2
    if has_keyboard_walk(password):
        score -= 2
    
    return max(score, 0)  
'''
''''''
def calculate_score(password):
    features = extract_features(password)
    features_df = pd.DataFrame([features])
    strength = model.predict(features_df)[0]
    return strength

'''
def classify_password(score):
    if score >= 8:
        return "Strong"
    elif score >= 5:
        return "Medium"
    else:
        return "Weak"
'''

def classify_password(strength):
    if strength == 2:
        return "Strong"
    elif strength == 1:
        return "Medium"
    else:
        return "Weak"

def main():    
    if len(sys.argv) != 2:
        print("Usage: python password_checker.py \"<password>\"")
        sys.exit(1)
    
    password = sys.argv[1]
    score = calculate_score(password)
    classification = classify_password(score)
    
    print(f"Password Score: {score}")
    print(f"Password Classification: {classification}")
    
    if is_breached(password):
        print("⚠️ WARNING: This password has been breached! Do not use it.")

if __name__ == "__main__":
    main()
