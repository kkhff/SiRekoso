import json
import os

# --- PATH FILE ---
SETTINGS_PATH = 'config/settings.json'
RECORDS_PATH = 'data/records.json'

def load_data(file_path):
    if not os.path.exists(file_path):
        # Jika file belum ada, buat file kosong
        if file_path == RECORDS_PATH:
            default_data = [] 
        elif file_path == SETTINGS_PATH:
            default_data = {} 
        
        # Tulis data default
        with open(file_path, 'w') as f:
            json.dump(default_data, f, indent=4)
            
        return default_data

    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        print(f"Error: File {file_path} rusak. Mengembalikan data kosong.")
        return []

def save_data(data, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saat menyimpan data ke {file_path}: {e}")

# --- FUNGSI UTAMA ---

def load_settings():
    return load_data(SETTINGS_PATH)

def save_settings(settings):
    save_data(settings, SETTINGS_PATH)

def load_records():
    return load_data(RECORDS_PATH)

def save_records(records):
    save_data(records, RECORDS_PATH)

def reset_records():
    try:
        # Menulis list kosong ke file records.json
        with open(RECORDS_PATH, 'w') as f:
            json.dump([], f, indent=4)
        return True
    except Exception as e:
        print(f"Gagal mereset data: {e}")
        return False