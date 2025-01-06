import sqlite3
import pandas as pd
import nfl_data_py as nfl
from . import team_games_database_build as tgb
from . import build_helper_classes as helper

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

def create_player_status_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_status (
            player_health_id INTEGER PRIMARY KEY,
            player_id INTEGER,
            team_id INTEGER,
            game_id INTEGER,
            status TEXT,
            FOREIGN KEY (player_id) REFERENCES players (player_id),
            FOREIGN KEY (game_id) REFERENCES games (game_id)
        )
    ''')

def create_player_game_stats_off_st_general_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_off_st_general (
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

def create_player_game_stats_st_kicking_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_st_kicking (
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

def create_player_game_stats_st_punting_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_st_punting (
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

def create_player_game_stats_st_returning_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_st_returning (
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

def create_player_game_stats_off_passing_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_off_passing (
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

def create_player_game_stats_off_rushing_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_off_rushing (
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

def create_player_game_stats_off_receiving_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_off_receiving (
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

def create_player_game_stats_def_table(conn):
    conn.execute('''
        CREATE TABLE IF NOT EXISTS player_game_stats_def (
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

def populate_player_status_table(conn):
    player_status_table = build_player_status_table(conn)
    
    data = list(player_status_table.itertuples(index=False, name=None))

    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO player_status (
            player_id,
            team_id,
            game_id,
            status
        ) VALUES (?, ?, ?, ?)''', data)

    conn.commit()
    c.close()
    
def build_player_status_table(conn):
    weekly_rosters = nfl.import_weekly_rosters(years)

    game_helper = helper.date_game_helper(conn)
    team_helper = helper.team_id_helper(conn)

    weekly_rosters = update_team_abbv(weekly_rosters)
    
    weekly_rosters = team_helper.add_team_id(weekly_rosters, 'team_abbreviation', 'team')
    weekly_rosters = game_helper.add_game_id_single_team(weekly_rosters, weekly_rosters)

    return weekly_rosters[['player_id', 'team_id', 'game_id', 'status']]

def update_team_abbv(df):
    old_new_list = [
        ('BLT', 'BAL'),
        ('CLV', 'CLE'),
        ('SL', 'LAR'),
        ('HST', 'HOU'),
        ('ARZ', 'ARI'),
        ('OAK', 'LV'),
        ('SD', 'LAC'),
        ('LA', 'LAR')
    ]

    for old_team, new_team in old_new_list:
        df['team'] = df['team'].replace(old_team, new_team)
    
    return df

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
    create_player_status_table(conn)
    create_player_game_stats_off_st_general_table(conn)
    create_player_game_stats_st_kicking_table(conn)
    create_player_game_stats_st_punting_table(conn)
    create_player_game_stats_st_returning_table(conn)
    create_player_game_stats_off_passing_table(conn)
    create_player_game_stats_off_rushing_table(conn)
    create_player_game_stats_off_receiving_table(conn)
    create_player_game_stats_def_table(conn)

def main():
    conn = sqlite3.connect('db.sqlite3')
    create_all_tables(conn)
    populate_players_table(conn)
    populate_player_status_table(conn)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    main()