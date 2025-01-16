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