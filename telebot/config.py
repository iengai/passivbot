import os
import json
import shutil

CONFIG_DIR = 'configs/'
PREDEFINED_DIR = os.path.join(CONFIG_DIR, 'predefined')
SILENT_CONFIG = os.path.join(PREDEFINED_DIR, 'silent.json')

API_KEYS_FILE = 'api-keys.json'

MAIN_SCRIPT = 'main.py'
VENV_PYTHON = os.path.join(os.getcwd(), "venv", "bin", "python")
DB_PATH = 'sqlite'

with open("tele-bot.json") as f:
    TELEGRAM_CONFIG = json.load(f)

BOT_TOKEN = TELEGRAM_CONFIG['bot_token']
ALLOWED_USER_IDS = TELEGRAM_CONFIG.get('allowed_user_ids', [TELEGRAM_CONFIG['allowed_user_ids']])

def get_api_key_file():
    if not os.path.exists(API_KEYS_FILE):
        shutil.copy(API_KEYS_FILE + '.example', API_KEYS_FILE)
    return API_KEYS_FILE
