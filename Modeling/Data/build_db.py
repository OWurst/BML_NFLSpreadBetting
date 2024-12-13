import sqlite3
import pandas as pd

def create_historical_games_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS historical_games (
            id INTEGER PRIMARY KEY,
            game_id TEXT UNIQUE,
            season REAL,
            week TEXT,
            home_team TEXT,
            away_team TEXT,
            home_score REAL,
            away_score REAL,
            home_line_close REAL,
            score_diff REAL,
            home_spread_diff REAL,
            home_vs_spread TEXT,
            total_score_close REAL,
            total_score REAL,
            total_score_diff REAL,
            over_vs_ou TEXT
        )
    ''')
    c.close()
    conn.commit()

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
    
    # Create a unique game_id
    df['game_id'] = df['Date'].dt.strftime('%Y/%m/%d') + df['Home Team'] + df['Away Team']

    # Remove the 'Date' column
    df = df[['game_id', 'Season', 'Week', 'Home Team', 'Away Team', 'Home Score', 'Away Score', 'Home Line Close', 'Score Diff', 'Home Spread Diff', 'Home vs Spread', 'Total Score Close', 'Total Score', 'Total Score Diff', 'Over vs O/U']]

    # Ensure correct data types
    df['Season'] = df['Season'].astype(float)
    df['Home Score'] = df['Home Score'].astype(float)
    df['Away Score'] = df['Away Score'].astype(float)
    df['Home Line Close'] = df['Home Line Close'].astype(float)
    df['Score Diff'] = df['Score Diff'].astype(float)
    df['Home Spread Diff'] = df['Home Spread Diff'].astype(float)
    df['Total Score Close'] = df['Total Score Close'].astype(float)
    df['Total Score'] = df['Total Score'].astype(float)
    df['Total Score Diff'] = df['Total Score Diff'].astype(float)

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

def populate_historical_games_table(conn):
    df = build_historical_games_df()
    data = df.to_records(index=False)
    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO historical_games (
            game_id, season, week, home_team, away_team, home_score, away_score, 
            home_line_close, score_diff, home_spread_diff, home_vs_spread, 
            total_score_close, total_score, total_score_diff, over_vs_ou
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()
    c.close()

if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    create_historical_games_table(conn)
    populate_historical_games_table(conn)
    conn.close()