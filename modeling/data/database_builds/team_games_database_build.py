import sqlite3
import pandas as pd
import nfl_data_py as nfl
from . import build_helper_classes as helper

years = range(2000, 2001)

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

def create_pbp_stats_table(conn):
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS pbp_stats (
            play_id INTEGER PRIMARY KEY,
            game_id INTEGER,
            season_type TEXT,

            posteam_id INTEGER,
            drive INTEGER,

            half TEXT,
            qtr_ending BOOLEAN,
            qtr INTEGER,
            quarter_seconds_remaining REAL,
            half_seconds_remaining REAL,
            game_seconds_remaining REAL,

            yards_gained REAL,
            down INTEGER,
            goal_to_go BOOLEAN,
            series INTEGER,
            series_result TEXT,
            distance_from_endzone REAL,
            yds_on_drive REAL,

            play_type TEXT,
            shotgun BOOLEAN,
            no_huddle BOOLEAN,
            qb_dropback BOOLEAN,
            qb_kneel BOOLEAN,
            qb_spike BOOLEAN,
            qb_scramble BOOLEAN,
            dropback_pct_oe REAL,

            first_down_rush BOOLEAN,
            first_down_pass BOOLEAN,
            first_down_penalty BOOLEAN,
            third_down_converted BOOLEAN,
            third_down_failed BOOLEAN,
            fourth_down_converted BOOLEAN,
            fourth_down_failed BOOLEAN,

            rush BOOLEAN,
            run_location TEXT,
            run_gap TEXT,
            rushing_yards REAL,

            pass BOOLEAN,            
            pass_length REAL,
            pass_location TEXT,
            air_yards REAL,
            yards_after_catch REAL,
            incomplete_pass BOOLEAN,
            interception BOOLEAN,
            complete_pass BOOLEAN,
            receiving_yards REAL,
            completion_probability REAL,
            cpoe REAL,
            air_wpa REAL,
            yac_wpa REAL,
            comp_air_wpa REAL,
            comp_yac_wpa REAL,
            air_epa REAL,
            yac_epa REAL,
            comp_air_epa REAL,
            comp_yac_epa REAL,
            
            st_play_type TEXT,
            field_goal_result TEXT,
            kick_distance REAL,
            extra_point_result TEXT,
            two_point_conv_result TEXT,
            punt_blocked BOOLEAN,
            touchback BOOLEAN,
            punt_inside_twenty BOOLEAN,
            punt_in_endzone BOOLEAN,
            punt_out_of_bounds BOOLEAN,
            punt_downed BOOLEAN,
            punt_fair_catch BOOLEAN,
            kickoff_inside_twenty BOOLEAN,
            kickoff_in_endzone BOOLEAN,
            kickoff_out_of_bounds BOOLEAN,
            kickoff_downed BOOLEAN,
            kickoff_fair_catch BOOLEAN,

            home_TO_remaining INTEGER,
            away_TO_remaining INTEGER,
            timeout_team_id INTEGER,
            
            td_team_id INTEGER,
            home_score INTEGER,
            away_score INTEGER,
            
            ep REAL,
            epa REAL,
            wp REAL,
            wpa REAL,
            
            fumble BOOLEAN,
            fumble_forced BOOLEAN,
            fumble_not_forced BOOLEAN,
            fumble_oob BOOLEAN,
            fumble_lost BOOLEAN,
            tfl BOOLEAN,
            sack BOOLEAN,

            penalty BOOLEAN,
            penalty_type TEXT,
            penalty_yards REAL,

            return_team_id INTEGER,            
            return_yards REAL,

            drive_play_count INTEGER,
            drive_time_of_possession REAL,
            drive_first_downs INTEGER,
            drive_inside20 BOOLEAN,
            drive_ended_with_score BOOLEAN,
            drive_yards_penalized REAL,
            drive_start_transition TEXT,
            drive_end_transition TEXT,
            drive_play_id_start INTEGER,
            drive_play_id_end INTEGER,

            FOREIGN KEY (game_id) REFERENCES games(game_id),
            FOREIGN KEY (posteam_id) REFERENCES teams(team_id),
            FOREIGN KEY (timeout_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (td_team_id) REFERENCES teams(team_id),
            FOREIGN KEY (return_team_id) REFERENCES teams(team_id)
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
        INSERT INTO games (
            date, season, week, home_team_id, away_team_id, home_score, away_score
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(season, week, home_team_id, away_team_id) DO UPDATE SET
            season=excluded.season,
            week=excluded.week,
            home_score=excluded.home_score,
            away_score=excluded.away_score
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

def populate_pbp_stats_table(conn):
    df = build_pbp_stats_df(conn)

    data = list(df.itertuples(index=False, name=None))
    c = conn.cursor()
    c.executemany('''
        INSERT OR IGNORE INTO pbp_stats (
            game_id,
            season_type,

            posteam_id,
            drive,

            half,
            qtr_ending,
            qtr,
            quarter_seconds_remaining,
            half_seconds_remaining,
            game_seconds_remaining,

            yards_gained,
            down,
            goal_to_go,
            series,
            series_result,
            distance_from_endzone,
            yds_on_drive,

            play_type,
            shotgun,
            no_huddle,
            qb_dropback,
            qb_kneel,
            qb_spike,
            qb_scramble,
            dropback_pct_oe,

            first_down_rush,
            first_down_pass,
            first_down_penalty,
            third_down_converted,
            third_down_failed,
            fourth_down_converted,
            fourth_down_failed,

            rush,
            run_location,
            run_gap,
            rushing_yards,

            pass,            
            pass_length,
            pass_location,
            air_yards,
            yards_after_catch,
            incomplete_pass,
            interception,
            complete_pass,
            receiving_yards,
            completion_probability,
            cpoe,
            air_wpa,
            yac_wpa,
            comp_air_wpa,
            comp_yac_wpa,
            air_epa,
            yac_epa,
            comp_air_epa,
            comp_yac_epa,
            
            st_play_type,
            field_goal_result,
            kick_distance,
            extra_point_result,
            two_point_conv_result,
            punt_blocked,
            touchback,
            punt_inside_twenty,
            punt_in_endzone,
            punt_out_of_bounds,
            punt_downed,
            punt_fair_catch,
            kickoff_inside_twenty,
            kickoff_in_endzone,
            kickoff_out_of_bounds,
            kickoff_downed,
            kickoff_fair_catch,

            home_TO_remaining,
            away_TO_remaining,
            timeout_team_id,
            
            td_team_id,
            home_score,
            away_score,
            
            ep,
            epa,
            wp,
            wpa,
            
            fumble,
            fumble_forced,
            fumble_not_forced,
            fumble_oob,
            fumble_lost,
            tfl,
            sack,

            penalty,
            penalty_type,
            penalty_yards,

            return_team_id,            
            return_yards,

            drive_play_count,
            drive_time_of_possession,
            drive_first_downs,
            drive_inside20,
            drive_ended_with_score,
            drive_yards_penalized,
            drive_start_transition,
            drive_end_transition,
            drive_play_id_start,
            drive_play_id_end,
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''')

###############################################################################################
# Helper functions
###############################################################################################

def build_pbp_stats_df(conn):
    df = nfl.import_pbp_data(years, downcast=True)
    
    game_helper = helper.date_game_helper(conn)
    team_helper = helper.team_id_helper(conn)

    id_fields = ['home_team', 'away_team', 'posteam', 'timeout_team', 'td_team', 'return_team']

    df = team_helper.update_team_abbv(df, id_fields)

    df = team_helper.add_team_id(df, 'team_abbreviation', None, add_fieldnames=id_fields)

    df = df['home_team_id', 'away_team_id', 'posteam_id', 'timeout_team_id', 'td_team_id', 'return_team_id']

    print(df.head(2))

    #df = game_helper.add_game_id_single_team(df, df)

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
    # create_games_table(conn)
    # create_pbp_stats_table(conn)

    # populate_teams_table(conn)
    # populate_games_table(conn)
    #populate_pbp_stats_table(conn)

    conn.close()

if __name__ == '__main__':
    main()