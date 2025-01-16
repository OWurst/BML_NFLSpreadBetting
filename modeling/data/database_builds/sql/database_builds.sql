CREATE DATABASE nfl_data;

USE nfl_data;

CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY,
    team_name_full TEXT UNIQUE,
    team_city TEXT,
    team_name TEXT UNIQUE,
    team_abbreviation TEXT UNIQUE,
    team_conference TEXT,
    team_division TEXT
);

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
);

CREATE TABLE IF NOT EXISTS players (
    player_id INT PRIMARY KEY,
    espn_id INT UNIQUE,
    nfl_data_py_id INT,
    player_name VARCHAR(255),
    player_first_name VARCHAR(255),
    player_last_name VARCHAR(255),
    player_position VARCHAR(255),
    player_birth_date DATE,
    player_height VARCHAR(255),
    player_college VARCHAR(255),
    player_weight INT,
    player_draft_year INT,
    player_draft_number INT
);

CREATE TABLE IF NOT EXISTS player_status (
    player_health_id INT PRIMARY KEY,
    player_id INT,
    team_id INT,
    game_id INT,
    status VARCHAR(255),
    FOREIGN KEY (player_id) REFERENCES players (player_id),
    FOREIGN KEY (game_id) REFERENCES games (game_id)
);

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
);

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
);

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
);

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
);

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
);

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
);

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
);

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
);