'''
    These classes will make it a lot easier to interact with the database. Database tables
    have many fields and it can be difficult to keep track of them all.
'''

class team:
    def __init__(
        self, 
        team_name_full=None,
        team_name=None,
        team_city=None, 
        team_abbreviation=None, 
        team_conference=None, 
        team_division=None
    ):
        self.team_id = team_id
        self.team_name = team_name
        self.team_abbreviation = team_abbreviation
        self.team_conference = team_conference
        self.team_division = team_division

class game:
    def __init__(
        self,
        game_id=None,
        season=None,
        week=None,
        home_team_id=None,
        away_team_id=None,
        home_score=None,
        away_score=None,
        home_line_close=None,
        total_score_close=None    
    ):
        self.game_id = game_id
        self.season = season
        self.week = week
        self.home_team_id = home_team_id
        self.away_team_id = away_team_id
        self.home_score = home_score
        self.away_score = away_score
        self.home_line_close = home_line_close
        self.total_score_close = total_score_close