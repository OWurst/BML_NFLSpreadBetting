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

#### team_weekly_stats

This table contains weekly stats for teams. Build from source 3

Fields:
