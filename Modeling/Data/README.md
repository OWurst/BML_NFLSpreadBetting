## Data Sources

* 1. https://www.aussportsbetting.com/data/historical-nfl-results-and-odds-data/
* 2. https://www.kaggle.com/datasets/cviaxmiwnptr/nfl-team-stats-20022019-espn?resource=download 
* 3. https://gist.github.com/cnizzardini/13d0a072adb35a0d5817#file-nfl_teams-csv 

## Tables

#### teams

This table contains data about all the nfl teams and comes from source 2

Fields:
* <ins>team_id</ins> INTEGER
* team_name_full TEXT (UNIQUE)
* team_city TEXT
* team_name TEXT (UNIQUE)
* team_abbreviation TEXT (UNIQUE)
* team_conference TEXT
* team_division TEXT

#### historical games

This table contains data about games, their outcomes, and spreads. Built from source 1

Fields:
* <ins>game_id</ins>,
* <span style="text-decoration:overline">team_id</span> INTEGER,
* season INTEGER,
* week TEXT,
* def_st_td INTEGER,
* drives INTEGER,
* first_downs INTEGER,
* first_downs_by_passing INTEGER,
* first_downs_by_penalty INTEGER,
* first_downs_by_rushing INTEGER,
* fourth_down_attempts INTEGER,
* fourth_down_conversions INTEGER,
* fumbles INTEGER,
* interceptions INTEGER,
* pass_attempts INTEGER,
* pass_completions INTEGER,
* pass_yards INTEGER,
* penalties INTEGER,
* penalty_yards INTEGER,
* plays INTEGER,
* possession_seconds INTEGER,
* red_zone_attempts INTEGER,
* red_zone_conversions INTEGER,
* rush_attempts INTEGER,
* rush_yards INTEGER,
* sacks INTEGER,
* sack_yards INTEGER,
* third_down_attempts INTEGER,
* third_down_conversions INTEGER,
* yards INTEGER

notes:

* FOREIGN KEY (team_id) REFERENCES teams(team_id),
* (season, week, team_id) must be unique

#### team_weekly_stats

This table contains weekly stats for teams. Build from source 3

Fields:
