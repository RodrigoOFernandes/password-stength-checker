import math

def has_sequence(password):
    sequences = [
        "abcdefghijklmnopqrstuvwxyz", "zyxwvutsrqponmlkjihgfedcba",  
        "0123456789", "9876543210"
    ]
    password_lower = password.lower()
    
    for seq in sequences:
        for i in range(len(seq) - 3):
            if seq[i:i+4] in password_lower:
                return True
    return False

def has_keyboard_walk(password):
    keyboard_rows = ["qwertyuiop", "asdfghjkl", "zxcvbnm", "1234567890"]
    password_lower = password.lower()
    
    for row in keyboard_rows:
        for i in range(len(row) - 3):
            sequence = row[i:i+4]
            if sequence in password_lower or sequence[::-1] in password_lower:
                return True
    return False

def extract_features(password):
    features = {}
    
    # Basic features
    features["length"] = len(password)
    features["has_upper"] = int(any(c.isupper() for c in password))
    features["has_lower"] = int(any(c.islower() for c in password))
    features["has_digit"] = int(any(c.isdigit() for c in password))
    features["has_special"] = int(any(c in "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~" for c in password))
    
    # Advanced features
    features["has_repetition"] = int(any(password[i] == password[i+1] == password[i+2] == password[i+3] for i in range(len(password) - 3)))
    features["has_sequence"] = int(has_sequence(password))
    features["has_keyboard_walk"] = int(has_keyboard_walk(password))
    
    return features