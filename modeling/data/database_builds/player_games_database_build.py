import sqlite3
import pandas as pd

def create_players_table(conn):
    conn.execute('''
        CREATE TABLE players (
            player_id INTEGER PRIMARY KEY,
            espn_id INTEGER UNIQUE,
            player_name TEXT,
            player_first_name TEXT,
            player_last_name TEXT,
            player_position TEXT,
            player_birth_date TEXT,
            player_height INTEGER,
            player_college TEXT,
            player_weight INTEGER,
            player_draft_year INTEGER,
            player_draft_number INTEGER
        )
    ''')

def create_player_team_membership_table(conn):
    conn.execute('''
        CREATE TABLE player_team_membership (
            player_team_membership_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            team_id INTEGER,
            start_date TEXT,
            end_date TEXT,
            player_number,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (team_id) REFERENCES teams (team_id)
        )
    ''')

def create_player_status_table(conn):
    conn.execute('''
        CREATE TABLE player_health (
            player_health_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            status TEXT,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_table(conn):
    conn.execute('''
        CREATE TABLE player_game_stats_offense (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            pass_attempts INTEGER,
            pass_completions INTEGER,
            pass_yards INTEGER,
            pass_tds INTEGER,
            interceptions INTEGER,
            rush_attempts INTEGER,
            rush_yards INTEGER,
            rush_tds INTEGER,
            fumbles INTEGER,
            fumbles_lost INTEGER,
            receptions INTEGER,
            receiving_yards INTEGER,
            receiving_tds INTEGER,
            targets INTEGER,
            two_point_attempts INTEGER,
            two_point_makes INTEGER,
            penalties INTEGER,
            penalty_yards INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_defense_table(conn):
    conn.execute('''
        CREATE TABLE player_game_stats_defense (
            player_game_stats_defense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            tackles INTEGER,
            assists INTEGER,
            sacks INTEGER,
            sack_yards INTEGER,
            interceptions INTEGER,
            interception_yards INTEGER,
            interception_tds INTEGER,
            pass_defenses INTEGER,
            forced_fumbles INTEGER,
            fumble_recoveries INTEGER,
            fumble_recovery_yards INTEGER,
            fumble_recovery_tds INTEGER,
            qb_hits INTEGER,
            tfl INTEGER,
            penalties INTEGER,
            penalty_yards INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')