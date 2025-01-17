CREATE PROCEDURE CreateAndDropTables()
BEGIN
    -- Drop tables if they exist
    DROP TABLE IF EXISTS games;
    DROP TABLE IF EXISTS teams;
    
    -- Create tables
    CREATE TABLE teams (
        team_id INT PRIMARY KEY,
        team_name_full VARCHAR(255) UNIQUE,
        team_city VARCHAR(255),
        team_name VARCHAR(255) UNIQUE,
        team_abbreviation VARCHAR(255) UNIQUE,
        team_conference VARCHAR(255),
        team_division VARCHAR(255)
    );
    
    CREATE TABLE games (
        game_id INT PRIMARY KEY,
    );
END $$
--     date DATE,
--     season INT,
--     week VARCHAR(25),
--     home_team_id INT,
--     away_team_id INT,
--     home_score INT,
--     away_score INT,
--     home_line_close FLOAT,
--     total_score_close FLOAT,
--     home_ml INT,
--     away_ml INT,

--     FOREIGN KEY (home_team_id) REFERENCES teams(team_id),
--     FOREIGN KEY (away_team_id) REFERENCES teams(team_id),
--     UNIQUE (season, week, home_team_id, away_team_id)

-- CREATE TABLE IF NOT EXISTS players (
--     player_id INT PRIMARY KEY,
--     espn_id INT UNIQUE,
--     -- nfl_data_py_id INT,
--     -- player_name VARCHAR(255),
--     -- player_first_name VARCHAR(255),
--     -- player_last_name VARCHAR(255),
--     -- player_position VARCHAR(255),
--     -- player_birth_date DATE,
--     -- player_height VARCHAR(255),
--     -- player_college VARCHAR(255),
--     -- player_weight INT,
--     -- player_draft_year INT,
--     -- player_draft_number INT
-- );

-- CREATE TABLE IF NOT EXISTS player_status (
--     player_health_id INT PRIMARY KEY,
--     player_id INT,
--     team_id INT,
--     game_id INT,
--     status VARCHAR(255),
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_off_st_general (
--     player_game_stats_offense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     fumbles INT,
--     fumbles_lost INT,
--     penalties INT,
--     penalty_yards INT,
--     blocks INT,
--     twopt_conversions INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_st_kicking (
--     player_game_stats_offense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     fg_made INT,
--     fg_attempts INT,
--     fg_long INT,
--     fg_total_yards INT,
--     xp_made INT,
--     xp_attempts INT,
--     kickoffs INT,
--     kickoff_yards INT,
--     kickoff_touchbacks INT,
--     kickoff_out_of_bounds INT,
--     kickoff_onside INT,
--     kickoff_onside_success INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_st_punting (
--     player_game_stats_offense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     punts INT,
--     punt_yards INT,
--     punt_long INT,
--     punt_inside_20 INT,
--     punt_touchbacks INT,
--     punt_fair_catches INT,
--     punt_return_yards INT,
--     punt_net_yards INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_st_returning (
--     player_game_stats_offense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     kick_returns INT,
--     kick_return_yards INT,
--     kick_return_tds INT,
--     kick_return_long INT,
--     punt_returns INT,
--     punt_return_yards INT,
--     punt_return_tds INT,
--     punt_return_long INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_off_passing (
--     player_game_stats_offense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     pass_attempts INT,
--     pass_completions INT,
--     pass_yards INT,
--     pass_tds INT,
--     pass_ints INT,
--     pass_long INT,
--     pass_sacks INT,
--     pass_sack_yards INT,
--     qb_rating INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_off_rushing (
--     player_game_stats_offense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     rush_attempts INT,
--     rush_yards INT,
--     rush_tds INT,
--     rush_long INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_off_receiving (
--     player_game_stats_offense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     receptions INT,
--     receiving_yards INT,
--     receiving_tds INT,
--     receiving_long INT,
--     targets INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );

-- CREATE TABLE IF NOT EXISTS player_game_stats_def (
--     player_game_stats_defense_id INT PRIMARY KEY,
--     player_id INT,
--     game_id INT,
--     tackles INT,
--     assists INT,
--     sacks INT,
--     sack_yards INT,
--     interceptions INT,
--     interception_yards INT,
--     interception_tds INT,
--     pass_defenses INT,
--     forced_fumbles INT,
--     fumble_recoveries INT,
--     fumble_recovery_yards INT,
--     fumble_recovery_tds INT,
--     qb_hits INT,
--     tfl INT,
--     penalties INT,
--     penalty_yards INT,
--     FOREIGN KEY (player_id) REFERENCES players (player_id),
--     FOREIGN KEY (game_id) REFERENCES games (game_id)
-- );