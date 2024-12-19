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

class game_stats:
    def __init__(
            week_team_performance_id=None,
            team_id=None,
            game_id=None,
            def_st_td=None,
            drives=None,
            first_downs=None,
            first_downs_by_passing=None,
            first_downs_by_penalty=None,
            first_downs_by_rushing=None,
            fourth_down_attempts=None,
            fourth_down_conversions=None,
            fumbles=None,
            interceptions=None,
            pass_attempts=None,
            pass_completions=None,
            pass_yards=None,
            penalties=None,
            penalty_yards=None,
            plays=None,
            possession_seconds=None,
            red_zone_attempts=None,
            red_zone_conversions=None,
            rush_attempts=None,
            rush_yards=None,
            sacks=None,
            sack_yards=None,
            third_down_attempts=None,
            third_down_conversions=None,
            yards=None
        ):

        self.week_team_performance_id = week_team_performance_id
        self.team_id = team_id
        self.game_id = game_id
        self.def_st_td = def_st_td
        self.drives = drives
        self.first_downs = first_downs
        self.first_downs_by_passing = first_downs_by_passing
        self.first_downs_by_penalty = first_downs_by_penalty
        self.first_downs_by_rushing = first_downs_by_rushing
        self.fourth_down_attempts = fourth_down_attempts
        self.fourth_down_conversions = fourth_down_conversions
        self.fumbles = fumbles
        self.interceptions = interceptions
        self.pass_attempts = pass_attempts
        self.pass_completions = pass_completions
        self.pass_yards = pass_yards
        self.penalties = penalties
        self.penalty_yards = penalty_yards
        self.plays = plays
        self.possession_seconds = possession_seconds
        self.red_zone_attempts = red_zone_attempts
        self.red_zone_conversions = red_zone_conversions
        self.rush_attempts = rush_attempts
        self.rush_yards = rush_yards
        self.sacks = sacks
        self.sack_yards = sack_yards
        self.third_down_attempts = third_down_attempts
        self.third_down_conversions = third_down_conversions
        self.yards = yards