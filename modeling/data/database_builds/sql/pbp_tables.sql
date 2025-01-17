CREATE TABLE IF NOT EXISTS pbp_stats (
    play_id INT PRIMARY KEY,
    game_id INT,
    season_type VARCHAR(255),

    posteam_id INT,
    drive INT,

    half VARCHAR(255),
    qtr_ending TINYINT(1),
    qtr INT,
    quarter_seconds_remaining FLOAT,
    half_seconds_remaining FLOAT,
    game_seconds_remaining FLOAT,

    yards_gained FLOAT,
    down INT,
    goal_to_go TINYINT(1),
    series INT,
    series_result VARCHAR(255),
    distance_from_endzone FLOAT,
    yds_on_drive FLOAT,

    play_type VARCHAR(255),
    shotgun TINYINT(1),
    no_huddle TINYINT(1),
    qb_dropback TINYINT(1),
    qb_kneel TINYINT(1),
    qb_spike TINYINT(1),
    qb_scramble TINYINT(1),
    dropback_pct_oe FLOAT,

    first_down_rush TINYINT(1),
    first_down_pass TINYINT(1),
    first_down_penalty TINYINT(1),
    third_down_converted TINYINT(1),
    third_down_failed TINYINT(1),
    fourth_down_converted TINYINT(1),
    fourth_down_failed TINYINT(1),

    rush TINYINT(1),
    run_location VARCHAR(255),
    run_gap VARCHAR(255),
    rushing_yards FLOAT,

    pass TINYINT(1),            
    pass_length FLOAT,
    pass_location VARCHAR(255),
    air_yards FLOAT,
    yards_after_catch FLOAT,
    incomplete_pass TINYINT(1),
    interception TINYINT(1),
    complete_pass TINYINT(1),
    receiving_yards FLOAT,
    completion_probability FLOAT,
    cpoe FLOAT,
    air_wpa FLOAT,
    yac_wpa FLOAT,
    comp_air_wpa FLOAT,
    comp_yac_wpa FLOAT,
    air_epa FLOAT,
    yac_epa FLOAT,
    comp_air_epa FLOAT,
    comp_yac_epa FLOAT,
    
    st_play_type VARCHAR(255),
    field_goal_result VARCHAR(255),
    kick_distance FLOAT,
    extra_point_result VARCHAR(255),
    two_point_conv_result VARCHAR(255),
    punt_blocked TINYINT(1),
    touchback TINYINT(1),
    punt_inside_twenty TINYINT(1),
    punt_in_endzone TINYINT(1),
    punt_out_of_bounds TINYINT(1),
    punt_downed TINYINT(1),
    punt_fair_catch TINYINT(1),
    kickoff_inside_twenty TINYINT(1),
    kickoff_in_endzone TINYINT(1),
    kickoff_out_of_bounds TINYINT(1),
    kickoff_downed TINYINT(1),
    kickoff_fair_catch TINYINT(1),

    home_TO_remaining INT,
    away_TO_remaining INT,
    timeout_team_id INT,
    
    td_team_id INT,
    home_score INT,
    away_score INT,
    
    ep FLOAT,
    epa FLOAT,
    wp FLOAT,
    wpa FLOAT,
    
    fumble TINYINT(1),
    fumble_forced TINYINT(1),
    fumble_not_forced TINYINT(1),
    fumble_oob TINYINT(1),
    fumble_lost TINYINT(1),
    tfl TINYINT(1),
    sack TINYINT(1),

    penalty TINYINT(1),
    penalty_type VARCHAR(255),
    penalty_yards FLOAT,

    return_team_id INT,            
    return_yards FLOAT,

    drive_play_count INT,
    drive_time_of_possession FLOAT,
    drive_first_downs INT,
    drive_inside20 TINYINT(1),
    drive_ended_with_score TINYINT(1),
    drive_yards_penalized FLOAT,
    drive_start_transition VARCHAR(255),
    drive_end_transition VARCHAR(255),
    drive_play_id_start INT,
    drive_play_id_end INT,

    FOREIGN KEY (game_id) REFERENCES games(game_id),
    FOREIGN KEY (posteam_id) REFERENCES teams(team_id),
    FOREIGN KEY (timeout_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (td_team_id) REFERENCES teams(team_id),
    FOREIGN KEY (return_team_id) REFERENCES teams(team_id)
);

