import sqlite3
import pandas as pd
from . import build_helper_classes as helper

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

def create_historical_games_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS historical_games (
            game_id INTEGER PRIMARY KEY,
            date DATE,
            season INTEGER,
            week TEXT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_score INTEGER,
            away_score INTEGER,
            home_line_close REAL,
            total_score_close REAL,
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
            FOREIGN KEY (game_id) REFERENCES historical_games(game_id),
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

def populate_historical_games_table(conn):
    df = build_historical_games_df(conn)

    # ignore games in 2024
    df = df[df['Season'] < 2024]

    # ignore super bowl games
    df = df[df['Week'] != 'Super Bowl']

    data = list(df.itertuples(index=False, name=None))
    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO historical_games (
            date, season, week, home_team_id, away_team_id, home_score, away_score, 
            home_line_close, total_score_close
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    c.close()

def populate_team_game_stats_table(conn):
    df = pd.read_csv('nfl_team_stats_2002-2023.csv')

    # remove all seasons before 2006
    df = df[df['season'] >= 2006]

    df['date'] = pd.to_datetime(df['date'])
    season_start_dates = df.groupby('season')['date'].min()
    df['Season'] = df['date'].apply(lambda x: x.year if x.month >= 3 else x.year - 1)
    df['Date'] = df['date']
    df['week'] = df.apply(lambda row: get_week_number(row, season_start_dates), axis=1)

    teams_helper = helper.team_id_helper(conn)
    df = teams_helper.add_home_away_team_id(df, 'team_name', ['home', 'away'])

    df['possession_home'] = df['possession_home'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))
    df['possession_away'] = df['possession_away'].apply(lambda x: int(x.split(':')[0]) * 60 + int(x.split(':')[1]))

    games_df = get_games_table(conn)

    home_df = pd.DataFrame()
    home_df['home_team_id'] = df['home_team_id']
    home_df['game_id'] = df.apply(lambda row: get_game_id(games_df, row['Season'], row['week'], row['home_team_id'], row['away_team_id']), axis=1)
    home_df['def_st_td_home'] = df['def_st_td_home']
    home_df['drives_home'] = df['drives_home']
    home_df['first_downs_home'] = df['first_downs_home']
    home_df['first_downs_from_passing_home'] = df['first_downs_from_passing_home']
    home_df['first_downs_from_penalty_home'] = df['first_downs_from_penalty_home']
    home_df['first_downs_from_rushing_home'] = df['first_downs_from_rushing_home']
    home_df['fourth_down_att_home'] = df['fourth_down_att_home']
    home_df['fourth_down_comp_home'] = df['fourth_down_comp_home']
    home_df['fumbles_home'] = df['fumbles_home']
    home_df['interceptions_home'] = df['interceptions_home']
    home_df['pass_att_home'] = df['pass_att_home']
    home_df['pass_comp_home'] = df['pass_comp_home']
    home_df['pass_yards_home'] = df['pass_yards_home']
    home_df['pen_num_home'] = df['pen_num_home']
    home_df['pen_yards_home'] = df['pen_yards_home']
    home_df['plays_home'] = df['plays_home']
    home_df['possession_home'] = df['possession_home']
    home_df['redzone_att_home'] = df['redzone_att_home']
    home_df['redzone_comp_home'] = df['redzone_comp_home']
    home_df['rush_att_home'] = df['rush_att_home']
    home_df['rush_yards_home'] = df['rush_yards_home']
    home_df['sacks_num_home'] = df['sacks_num_home']
    home_df['sacks_yards_home'] = df['sacks_yards_home']
    home_df['third_down_att_home'] = df['third_down_att_home']
    home_df['third_down_comp_home'] = df['third_down_comp_home']
    home_df['yards_home'] = df['yards_home']

    away_df = pd.DataFrame()
    away_df['away_team_id'] = df['away_team_id']
    away_df['game_id'] = df.apply(lambda row: get_game_id(games_df, row['Season'], row['week'], row['home_team_id'], row['away_team_id']), axis=1)
    away_df['def_st_td_away'] = df['def_st_td_away']
    away_df['drives_away'] = df['drives_away']
    away_df['first_downs_away'] = df['first_downs_away']
    away_df['first_downs_from_passing_away'] = df['first_downs_from_passing_away']
    away_df['first_downs_from_penalty_away'] = df['first_downs_from_penalty_away']
    away_df['first_downs_from_rushing_away'] = df['first_downs_from_rushing_away']
    away_df['fourth_down_att_away'] = df['fourth_down_att_away']
    away_df['fourth_down_comp_away'] = df['fourth_down_comp_away']
    away_df['fumbles_away'] = df['fumbles_away']
    away_df['interceptions_away'] = df['interceptions_away']
    away_df['pass_att_away'] = df['pass_att_away']
    away_df['pass_comp_away'] = df['pass_comp_away']
    away_df['pass_yards_away'] = df['pass_yards_away']
    away_df['pen_num_away'] = df['pen_num_away']
    away_df['pen_yards_away'] = df['pen_yards_away']
    away_df['plays_away'] = df['plays_away']
    away_df['possession_away'] = df['possession_away']
    away_df['redzone_att_away'] = df['redzone_att_away']
    away_df['redzone_comp_away'] = df['redzone_comp_away']
    away_df['rush_att_away'] = df['rush_att_away']
    away_df['rush_yards_away'] = df['rush_yards_away']
    away_df['sacks_num_away'] = df['sacks_num_away']
    away_df['sacks_yards_away'] = df['sacks_yards_away']
    away_df['third_down_att_away'] = df['third_down_att_away']
    away_df['third_down_comp_away'] = df['third_down_comp_away']
    away_df['yards_away'] = df['yards_away']

    data_home = list(home_df.itertuples(index=False, name=None))
    data_away = list(away_df.itertuples(index=False, name=None))
    data = data_home + data_away

    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO team_game_stats (
            team_id, game_id, def_st_td, drives, first_downs, first_downs_by_passing, first_downs_by_penalty, first_downs_by_rushing, fourth_down_attempts, fourth_down_conversions, fumbles, interceptions, pass_attempts, pass_completions, pass_yards, penalties, penalty_yards, plays, possession_seconds, red_zone_attempts, red_zone_conversions, rush_attempts, rush_yards, sacks, sack_yards, third_down_attempts, third_down_conversions, yards)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? ,?, ?, ?, ?, ?, ?)
        ''', data)
    
    conn.commit()
    c.close()

def build_historical_games_df(conn):
    df = pd.read_excel('Australia_Historical_Game_Outcomes.xlsx', engine='openpyxl')
    df = df[['Date', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Home Line Close', 'Total Score Close']]
    
    df['Date'] = pd.to_datetime(df['Date'])
    df['Season'] = df['Date'].apply(lambda x: x.year if x.month >= 3 else x.year - 1)
    season_start_dates = df.groupby('Season')['Date'].min()
    df['Week'] = df.apply(lambda row: get_week_number(row, season_start_dates), axis=1)
    
    # Rebalance team names
    df = team_rebalance(df)

    teams_helper = helper.team_id_helper(conn)
    df = teams_helper.add_home_away_team_id(df, 'team_name_full', ['Home Team', 'Away Team'])

    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
    df = df[['Date', 'Season', 'Week', 'home_team_id', 'away_team_id', 'Home Score', 'Away Score', 'Home Line Close', 'Total Score Close']]

    return df

###############################################################################################
# Helper functions
###############################################################################################

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

def get_games_table(conn):
    c = conn.cursor()

    c.execute('SELECT game_id, season, week, home_team_id, away_team_id FROM historical_games')
    games = c.fetchall()
    c.close()
    games_df = pd.DataFrame(games, columns=['game_id', 'season', 'week', 'home_team_id', 'away_team_id'])
    return games_df

def get_game_id(df, season, week, home_team_id, away_team_id):
    game = df[(df['season'] == season) & (df['week'] == str(week)) & (df['home_team_id'] == home_team_id) & (df['away_team_id'] == away_team_id)]
    if not game.empty:
        return game.iloc[0]['game_id']
    elif week == 'Super Bowl':
            game = df[(df['season'] == season) & (df['week'] == str(week)) & (df['away_team_id'] == home_team_id) & (df['home_team_id'] == away_team_id)]
    else: 
        raise ValueError(f"Game not found for season: {season}, week: {week}, home_team_id: {home_team_id}, away_team_id: {away_team_id}")

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
    create_historical_games_table(conn)
    create_team_game_stats_table(conn)

    populate_teams_table(conn)
    populate_historical_games_table(conn)
    populate_team_game_stats_table(conn)

    conn.close()

if __name__ == '__main__':
    main()