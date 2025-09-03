import random
import string
import os
from cryptography.fernet import Fernet

# ---------------- Password Generator ----------------
def generate_password(length=16):
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    return password

# ---------------- Encryption Key ----------------
def generate_key():
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    if not os.path.exists("key.key"):
        print("Encryption key not found. Generating a new one...")
        generate_key()
    return open("key.key", "rb").read()

cipher = Fernet(load_key())

# ---------------- Password Storage ----------------
def store_password(service, password):
    encrypted = cipher.encrypt(password.encode())
    with open(f"{service}.txt", "wb") as f:
        f.write(encrypted)

def get_password(service):
    try:
        with open(f"{service}.txt", "rb") as f:
            encrypted = f.read()
        return cipher.decrypt(encrypted).decode()
    except FileNotFoundError:
        return "No password found for this service."

# ---------------- Main Program ----------------
if __name__ == "__main__":
    print("🔐 Password Manager")
    service = input("Enter service name: ").strip()

    action = input("Do you want to (G)enerate a new password or (R)etrieve existing one? ").strip().lower()

    if action == 'g':
        password = generate_password(20)
        store_password(service, password)
        print(f"✅ Generated and stored password for '{service}': {password}")
    elif action == 'r':
        retrieved = get_password(service)
        print(f"🔎 Retrieved password for '{service}': {retrieved}")
    else:
        print("❌ Invalid option. Please choose 'G' or 'R'.")
