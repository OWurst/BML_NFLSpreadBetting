import sqlite3
import pandas as pd
import nfl_data_py as nfl
from . import build_helper_classes as helper

years = range(2000, 2025)

def create_teams_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            team_id INTEGER PRIMARY KEY,
            team_name_full TEXT UNIQUE,
            team_city TEXT,
            team_name TEXT UNIQUE,
            team_abbreviation TEXT UNIQUE,
            team_conference TEXT,
            team_division TEXT
        )
    ''')
    c.close()
    conn.commit()

def create_games_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS games (
            game_id INTEGER PRIMARY KEY,
            date DATE,
            season INTEGER,
            week TEXT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_score REAL,
            away_score REAL,
            home_line_close REAL,
            total_score_close REAL,
            home_ml INTEGER,
            away_ml INTEGER,
            FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
            UNIQUE (season, week, home_team_id, away_team_id)
        )
    ''')
    c.close()
    conn.commit()

def create_team_game_stats_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS team_game_stats (
            week_team_performance_id INTEGER PRIMARY KEY,
            team_id INTEGER,
            game_id INTEGER,
            def_st_td INTEGER,
            drives INTEGER,
            first_downs INTEGER,
            first_downs_by_passing INTEGER,
            first_downs_by_penalty INTEGER,
            first_downs_by_rushing INTEGER,
            fourth_down_attempts INTEGER,
            fourth_down_conversions INTEGER,
            fumbles INTEGER,
            interceptions INTEGER,
            pass_attempts INTEGER,
            pass_completions INTEGER,
            pass_yards INTEGER,
            total_pass_yards_oe,
            penalties INTEGER,
            penalty_yards INTEGER,
            plays INTEGER,
            possession_seconds INTEGER,
            red_zone_attempts INTEGER,
            red_zone_conversions INTEGER,
            rush_attempts INTEGER,
            rush_yards INTEGER,
            sacks INTEGER,
            sack_yards INTEGER,
            third_down_attempts INTEGER,
            third_down_conversions INTEGER,
            yards INTEGER,
            FOREIGN KEY (team_id) REFERENCES teams(team_id),
            FOREIGN KEY (game_id) REFERENCES games(game_id),
            UNIQUE (game_id, team_id)
        )
    ''')
    c.close()
    conn.commit()

def populate_teams_table(conn):
    teams_df = pd.read_csv('nfl_teams.csv')

    teams_df['team_city'] = teams_df['Name'].apply(lambda x: ' '.join(x.split()[:-1]))
    teams_df['team_name'] = teams_df['Name'].apply(lambda x: x.split()[-1])

    teams_df = teams_df[['Name', 'team_city', 'team_name', 'Abbreviation', 'Conference', 'Division']]
    data = list(teams_df.itertuples(index=False, name=None))

    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO teams (
            team_name_full, team_city, team_name, team_abbreviation, team_conference, team_division
        ) VALUES (?, ?, ?, ?, ?, ?)
    ''', data)

    conn.commit()
    c.close()

def populate_games_table(conn):
    df = build_games_df(conn)

    data = list(df.itertuples(index=False, name=None))
    c = conn.cursor()
    c.executemany('''
        INSERT OR UPDATE INTO games (
            date, season, week, home_team_id, away_team_id, home_score, away_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    c.close()

def build_games_df(conn):
    df = nfl.import_schedules(years)

    teams_helper = helper.team_id_helper(conn)
    df = teams_helper.update_team_abbv(df, ['home_team', 'away_team'])
    df = teams_helper.add_home_away_team_id(df, 'team_abbreviation', ['home_team', 'away_team'])

    df['gameday'] = pd.to_datetime(df['gameday'])
    df['date'] = df['gameday'].dt.strftime('%Y-%m-%d')

    week_helper = helper.date_game_helper(conn)
    df = week_helper.switch_weeks_format(df)

    required_columns = ['date', 'season', 'week', 'home_team_id', 'away_team_id', 'home_score', 'away_score']
    df = df[required_columns]    
    return df

def populate_team_game_stats_table(conn):
   df = build_team_game_stats_df(conn)

    c = conn.cursor()
    c.executemany('''
        INSERT OR UPDATE INTO team_game_stats (
            team_id, game_id, def_st_td, drives, first_downs, first_downs_by_passing, first_downs_by_penalty, first_downs_by_rushing, fourth_down_attempts, fourth_down_conversions, fumbles, interceptions, pass_attempts, pass_completions, pass_yards, penalties, penalty_yards, plays, possession_seconds, red_zone_attempts, red_zone_conversions, rush_attempts, rush_yards, sacks, sack_yards, third_down_attempts, third_down_conversions, yards)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?)
        ''', data)
    
    conn.commit()
    c.close()

###############################################################################################
# Helper functions
###############################################################################################

def build_team_game_stats_df(conn):
    df = nfl.

    team_stats = 

   
def team_rebalance(df, team_col=False):
    old_new_list = [
        ('Washington Football Team', 'Washington Commanders'),
        ('Washington Redskins', 'Washington Commanders'),
        ('St. Louis Rams', 'Los Angeles Rams'),
        ('Oakland Raiders', 'Las Vegas Raiders'),
        ('San Diego Chargers', 'Los Angeles Chargers')
    ]

    for old_team, new_team in old_new_list:
        if team_col:
            df['team'] = df['team'].replace(old_team, new_team)
        else:
            df['Home Team'] = df['Home Team'].replace(old_team, new_team)
            df['Away Team'] = df['Away Team'].replace(old_team, new_team)
    
    return df

def get_teams_table(conn, name_only=False):
    c = conn.cursor()

    if name_only:
        c.execute('SELECT team_id, team_name FROM teams')
    else:
        c.execute('SELECT team_id, team_name_full FROM teams')
    
    teams = c.fetchall()
    c.close()
    teams_df = pd.DataFrame(teams, columns=['team_id', 'team_name'])
    return teams_df

def get_week_number(row, season_start_dates):
    season_start_date = season_start_dates[row['Season']]
    delta = row['Date'] - season_start_date
    regular_season_weeks = 18 if row['Season'] >= 2021 else 17
    week_number = (delta.days // 7) + 1
    if week_number > regular_season_weeks:
        playoff_week_number = week_number - regular_season_weeks
        if playoff_week_number == 1:
            return "Wild Card"
        elif playoff_week_number == 2:
            return "Divisional"
        elif playoff_week_number == 3:
            return "Championship"
        else:
            return "Super Bowl"
        
    return week_number

def main():
    conn = sqlite3.connect('db.sqlite3')
    
    create_teams_table(conn)
    create_games_table(conn)
    create_team_game_stats_table(conn)

    populate_teams_table(conn)
    populate_games_table(conn)
    #populate_team_game_stats_table(conn)

    conn.close()

if __name__ == '__main__':
    main()