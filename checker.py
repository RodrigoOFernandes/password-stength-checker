import sys
import re
import pandas as pd
import requests
import hashlib
import math 
import joblib
import random
import string
from cryptography.fernet import Fernet  # Para criptografar a senha
from utils import extract_features, has_sequence, has_keyboard_walk

# Carrega o modelo treinado
model = joblib.load("password_strength_model.pkl")

# Gera uma chave de criptografia (ou carrega se já existir)
def load_or_generate_key():
    try:
        with open("secret.key", "rb") as key_file:
            key = key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
    return key

key = load_or_generate_key()
cipher_suite = Fernet(key)

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

def calculate_score(password):
    features = extract_features(password)
    features_df = pd.DataFrame([features])
    strength = model.predict(features_df)[0]
    return strength

def classify_password(strength):
    if strength == 2:
        return "Strong"
    elif strength == 1:
        return "Medium"
    else:
        return "Weak"

def generate_strong_password(length=12):
    # Define os conjuntos de caracteres
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = "!@#$%^&*()-_=+[]{}|;:'\",.<>?/`~"
    
    # Combina todos os conjuntos
    all_chars = lowercase + uppercase + digits + symbols
    
    # Garante que a senha tenha pelo menos um caractere de cada tipo
    password = [
        random.choice(lowercase),
        random.choice(uppercase),
        random.choice(digits),
        random.choice(symbols),
    ]
    
    # Completa o restante da senha com caracteres aleatórios
    for _ in range(length - 4):
        password.append(random.choice(all_chars))
    
    # Embaralha os caracteres para evitar padrões previsíveis
    random.shuffle(password)
    
    # Converte a lista de caracteres em uma string
    return ''.join(password)

def save_password(password):
    # Criptografa a senha
    encrypted_password = cipher_suite.encrypt(password.encode())
    
    # Salva a senha criptografada em um arquivo
    with open("passwords.txt", "ab") as file:
        file.write(encrypted_password + b"\n")
    
    print("✅ Password saved securely!")

def main():    
    if len(sys.argv) != 2:
        print("Usage: python password_checker.py \"<password>\"")
        print("Or use: python password_checker.py --generate")
        sys.exit(1)
    
    if sys.argv[1] == "--generate":
        # Gera uma senha forte
        password = generate_strong_password()
        print(f"Generated Password: {password}")
        
        # Valida a senha gerada
        score = calculate_score(password)
        classification = classify_password(score)
        
        print(f"Password Score: {score}")
        print(f"Password Classification: {classification}")
        
        if is_breached(password):
            print("⚠️ WARNING: This password has been breached! Do not use it.")
        
        # Pergunta ao usuário se deseja salvar a senha
        save_option = input("Do you want to save this password? (yes/no): ").strip().lower()
        if save_option == "yes":
            save_password(password)
    else:
        # Verifica a senha fornecida
        password = sys.argv[1]
        score = calculate_score(password)
        classification = classify_password(score)
        
        print(f"Password Score: {score}")
        print(f"Password Classification: {classification}")
        
        if is_breached(password):
            print("⚠️ WARNING: This password has been breached! Do not use it.")

if __name__ == "__main__":
    main()