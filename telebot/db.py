import sqlite3
from .config import DB_PATH

def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS bots (
                bot_id TEXT PRIMARY KEY,
                is_selected BOOLEAN DEFAULT FALSE,
                config_path TEXT NOT NULL,
                enabled BOOLEAN DEFAULT FALSE,
                apikey TEXT NOT NULL,
                secret TEXT NOT NULL
            );
        ''')

def bot_exists(bot_id):
    with sqlite3.connect(DB_PATH) as conn:
        result = conn.execute('SELECT 1 FROM bots WHERE bot_id = ?', (bot_id,)).fetchone()
        return result is not None

def set_selected_bot(bot_id):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('UPDATE bots SET is_selected=0')
        conn.execute('UPDATE bots SET is_selected=1 WHERE bot_id=?', (bot_id,))

def list_all_bots():
    with sqlite3.connect(DB_PATH) as conn:
        return conn.execute('SELECT bot_id, is_selected FROM bots').fetchall()

def upsert_bot(bot_id, apikey, secret, config_path):
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute('UPDATE bots SET is_selected = 0')

        conn.execute('''
            INSERT INTO bots (bot_id, config_path, is_selected, apikey, secret)
            VALUES (?, ?, 1, ?, ?)
            ON CONFLICT(bot_id) DO UPDATE SET
                is_selected = 1,
                apikey = excluded.apikey,
                secret = excluded.secret
        ''', (bot_id, config_path, apikey, secret))