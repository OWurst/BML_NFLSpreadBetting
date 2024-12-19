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