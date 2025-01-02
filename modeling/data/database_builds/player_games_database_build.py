import sqlite3
import pandas as pd
import nfl_data_py as nfl

years = list(range(2006, 2025))

def create_players_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS players (
            player_id INTEGER PRIMARY KEY,
            espn_id INTEGER UNIQUE,
            nfl_data_py_id INTEGER,
            player_name TEXT,
            player_first_name TEXT,
            player_last_name TEXT,
            player_position TEXT,
            player_birth_date TEXT,
            player_height TEXT,
            player_college TEXT,
            player_weight INTEGER,
            player_draft_year INTEGER,
            player_draft_number INTEGER
        )
    ''')

def create_player_team_membership_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_team_membership (
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
        CREATE TABLE IF NOT EXISTS player_health (
            player_health_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            status TEXT,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_general_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_offense_general (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            fumbles INTEGER,
            fumbles_lost INTEGER,
            penalties INTEGER,
            penalty_yards INTEGER,
            blocks INTEGER,
            twopt_conversions INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_kicking_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_offense_kicking (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            fg_made INTEGER,
            fg_attempts INTEGER,
            fg_long INTEGER,
            fg_total_yards INTEGER,
            xp_made INTEGER,
            xp_attempts INTEGER,
            kickoffs INTEGER,
            kickoff_yards INTEGER,
            kickoff_touchbacks INTEGER,
            kickoff_out_of_bounds INTEGER,
            kickoff_onside INTEGER,
            kickoff_onside_success INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_punting_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_offense_punting (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            punts INTEGER,
            punt_yards INTEGER,
            punt_long INTEGER,
            punt_inside_20 INTEGER,
            punt_touchbacks INTEGER,
            punt_fair_catches INTEGER,
            punt_return_yards INTEGER,
            punt_net_yards INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_returning_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_offense_returning (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            kick_returns INTEGER,
            kick_return_yards INTEGER,
            kick_return_tds INTEGER,
            kick_return_long INTEGER,
            punt_returns INTEGER,
            punt_return_yards INTEGER,
            punt_return_tds INTEGER,
            punt_return_long INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_passing_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_offense_passing (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            pass_attempts INTEGER,
            pass_completions INTEGER,
            pass_yards INTEGER,
            pass_tds INTEGER,
            pass_ints INTEGER,
            pass_long INTEGER,
            pass_sacks INTEGER,
            pass_sack_yards INTEGER,
            qb_rating INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_rushing_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_offense_rushing (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            rush_attempts INTEGER,
            rush_yards INTEGER,
            rush_tds INTEGER,
            rush_long INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_offense_receiving_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_offense_receiving (
            player_game_stats_offense_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            game_id INTEGER,
            receptions INTEGER,
            receiving_yards INTEGER,
            receiving_tds INTEGER,
            receiving_long INTEGER,
            targets INTEGER,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_defense_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_defense (
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

def populate_players_table(conn):
    players = build_players_table()

    data = list(players.itertuples(index=False, name=None))

    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO players (
            espn_id,
            nfl_data_py_id,
            player_name,
            player_first_name,
            player_last_name,
            player_position,
            player_birth_date,
            player_height,
            player_college,
            player_weight,
            player_draft_year,
            player_draft_number
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', data)

    conn.commit()
    c.close()

def build_players_table():
    weekly_rosters = nfl.import_weekly_rosters(years)

    # trim db to only take 1 row for each unique player_id
    weekly_rosters = weekly_rosters.drop_duplicates(subset='player_id')

    weekly_rosters = weekly_rosters[['espn_id', 'player_id', 'player_name', 'first_name', 'last_name', 'position', 'birth_date', 'height', 'college', 'weight', 'rookie_year', 'draft_number']]

    # if birth_date is not listed for player, set birth_date to 1900-01-01
    weekly_rosters['birth_date'] = weekly_rosters['birth_date'].fillna('1900-01-01')
    weekly_rosters['birth_date'] = pd.to_datetime(weekly_rosters['birth_date'], format='%Y-%m-%d').dt.strftime('%Y-%m-%d')

    # if height is not listed for player, set height to 0
    weekly_rosters['height'] = weekly_rosters['height'].fillna(0)
    # if weight is not listed for player, set weight to 0
    weekly_rosters['weight'] = weekly_rosters['weight'].fillna(0)

    # if player was not drafted, set draft number to 0
    weekly_rosters['draft_number'] = weekly_rosters['draft_number'].fillna(0)
    # if player was not drafted, set rookie year to 0
    weekly_rosters['rookie_year'] = weekly_rosters['rookie_year'].fillna(0)
    
    return weekly_rosters

def create_all_tables(conn):
    create_players_table(conn)
    create_player_team_membership_table(conn)
    create_player_status_table(conn)
    create_player_game_stats_offense_general_table(conn)
    create_player_game_stats_offense_kicking_table(conn)
    create_player_game_stats_offense_punting_table(conn)
    create_player_game_stats_offense_returning_table(conn)
    create_player_game_stats_offense_passing_table(conn)
    create_player_game_stats_offense_rushing_table(conn)
    create_player_game_stats_offense_receiving_table(conn)
    create_player_game_stats_defense_table(conn)

def main():
    conn = sqlite3.connect('db.sqlite3')
    create_all_tables(conn)
    populate_players_table(conn)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()