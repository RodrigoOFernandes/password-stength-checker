import sys
import re

def has_repetition(password):
    for i in range(len(password) - 3):
        if password[i] == password[i+1] == password[i+2] == password[i+3] == password(i+4) == password(i+5):
            return True
    return False

def has_sequence(password):
    sequences = [
        "abcdefghijklmnopqrstuvwxyz",  
        "zyxwvutsrqponmlkjihgfedcba",  
        "0123456789",                  
        "9876543210",                  
    ]
    for seq in sequences:
        if password.lower() in seq or seq in password.lower():
            return True
    return False

def has_keyboard_walk(password):
    keyboard_rows = [
        "qwertyuiop",
        "asdfghjkl",
        "zxcvbnm",
        "1234567890",
    ]
    password_lower = password.lower()
    for row in keyboard_rows:
        for i in range(len(row) - 3):
            sequence = row[i:i+7]
            if sequence in password_lower or sequence[::-1] in password_lower:
                return True
    return False

def basic_rules(password):
    if len(password) < 12:
        return "Too short(min 12 characters)"
    
    has_upper = re.search(r'[A-Z]', password) is not None
    has_lower = re.search(r'[a-z]', password) is not None
    has_digit = re.search(r'\d', password) is not None
    has_symbol = re.search(r'[^A-Za-z0-9]', password) is not None
    
    if not (has_upper and has_lower and has_digit and has_symbol):
        return "Must include a combination of uppercase, lowercase, numbers, and symbols"
    
    with open('top10000common.txt') as f:
        common_passwords = [line.strip() for line in f]
        if password in common_passwords:
            return "Too common"
        
    if has_repetition(password):
        return "Password contains repeated characters"
    
    if has_sequence(password):
        return "Password contains a simple sequence"
    
    if has_keyboard_walk(password):
        return "Password contains a keyboard walk"
    
def main():
    if len(sys.argv) != 2:
        print("Usage: python password_checker.py <password>")
        sys.exit(1)
    
    password = sys.argv[1]
    result = basic_rules(password)
    
    if result:
        print(f"❌ Weak password: {result}")
    else:
        print("✅ Password meets basic requirements")

if __name__ == "__main__":
    main()