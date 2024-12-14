import sqlite3
import pandas as pd

def create_historical_games_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS historical_games (
            id INTEGER PRIMARY KEY,
            season INTEGER,
            week TEXT,
            home_team_id INTEGER,
            away_team_id INTEGER,
            home_score INTEGER,
            away_score INTEGER,
            home_line_close REAL,
            score_diff REAL,
            home_spread_diff REAL,
            home_vs_spread TEXT,
            total_score_close REAL,
            total_score INTEGER,
            total_score_diff REAL,
            over_vs_ou TEXT,
            FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
            UNIQUE (season, week, home_team_id, away_team_id)
        )
    ''')
    c.close()
    conn.commit()

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

def create_team_weekly_stats_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS team_weekly_stats (
            id INTEGER PRIMARY KEY,
            team_id INTEGER,
            season INTEGER,
            week TEXT,
            FOREIGN KEY (team_id) REFERENCES teams(team_id),
            UNIQUE (season, week, team_id)
        )
    ''')
    c.close()
    conn.commit()

def populate_team_weekly_stats_table(conn):
    pass

def team_rebalance(df, old_new_list):
    for old_team, new_team in old_new_list:
        df['Home Team'] = df['Home Team'].replace(old_team, new_team)
        df['Away Team'] = df['Away Team'].replace(old_team, new_team)
    
    return df

def get_teams_table(conn):
    c = conn.cursor()
    c.execute('SELECT team_id, team_name_full FROM teams')
    teams = c.fetchall()
    c.close()
    teams_df = pd.DataFrame(teams, columns=['team_id', 'team_name_full'])
    return teams_df

def build_historical_games_df():
    df = pd.read_excel('Australia_Historical_Game_Outcomes.xlsx', engine='openpyxl')
    df = df[['Date', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Home Line Close', 'Total Score Close']]

    df['Score Diff'] = df['Home Score'] - df['Away Score']
    df['Total Score'] = df['Home Score'] + df['Away Score']
    df['Home Spread Diff'] = df['Home Line Close'] + df['Score Diff']
    df['Total Score Diff'] = df['Total Score'] - df['Total Score Close']
    df['Home vs Spread'] = df['Home Spread Diff'].apply(lambda x: 'Win' if x > 0 else ('Push' if x == 0 else 'Lose'))
    df['Over vs O/U'] = df['Total Score Diff'].apply(lambda x: 'Win' if x > 0 else ('Push' if x == 0 else 'Lose'))
    df['Date'] = pd.to_datetime(df['Date'])
    df['Season'] = df['Date'].apply(lambda x: x.year if x.month >= 3 else x.year - 1)
    season_start_dates = df.groupby('Season')['Date'].min()
    df['Week'] = df.apply(lambda row: get_week_number(row, season_start_dates), axis=1)
    
    # Rebalance team names
    df = team_rebalance(df, [
        ('Washington Football Team', 'Washington Commanders'),
        ('Washington Redskins', 'Washington Commanders'),
        ('St. Louis Rams', 'Los Angeles Rams'),
        ('Oakland Raiders', 'Las Vegas Raiders'),
        ('San Diego Chargers', 'Los Angeles Chargers')
    ])

    teams_df = get_teams_table(conn)
    df['home_team_id'] = df['Home Team'].apply(lambda x: get_team_id(teams_df, x))
    df['away_team_id'] = df['Away Team'].apply(lambda x: get_team_id(teams_df, x))

    # Remove the 'Date' column and reorder columns
    df = df[['Season', 'Week', 'home_team_id', 'away_team_id', 'Home Score', 'Away Score', 'Home Line Close', 'Score Diff', 'Home Spread Diff', 'Home vs Spread', 'Total Score Close', 'Total Score', 'Total Score Diff', 'Over vs O/U']]

    return df

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

def get_team_id(df, team_name):
    return df[df['team_name_full'] == team_name]['team_id'].values[0]

def populate_historical_games_table(conn):
    df = build_historical_games_df()

    data = list(df.itertuples(index=False, name=None))
    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO historical_games (
            season, week, home_team_id, away_team_id, home_score, away_score, 
            home_line_close, score_diff, home_spread_diff, home_vs_spread, 
            total_score_close, total_score, total_score_diff, over_vs_ou
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    c.close()

if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    
    create_teams_table(conn)
    populate_teams_table(conn)
    create_historical_games_table(conn)
    populate_historical_games_table(conn)
    create_team_weekly_stats_table(conn)
    populate_team_weekly_stats_table(conn)

    conn.close()