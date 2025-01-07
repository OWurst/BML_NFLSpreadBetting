import pandas as pd
import nfl_data_py as nfl

def build_refs_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS refs (
            ref_id INTEGER PRIMARY KEY,
            official_id TEXT UNIQUE,
            name TEXT
        )
    ''')
    c.close()
    conn.commit()

def build_ref_games_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS ref_games (
            game_id INTEGER,
            ref_id INTEGER,
            ref_position TEXT,
            FOREIGN KEY (game_id) REFERENCES games (game_id),
            FOREIGN KEY (ref_id) REFERENCES refs (ref_id)
        )
    ''')
    c.close()
    conn.commit()