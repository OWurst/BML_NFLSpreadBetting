import pandas as pd

class date_game_helper:
    def __init__(self, conn):
        self.conn = conn
    
    def get_games_table(self):
        c = self.conn.cursor()

        c.execute('SELECT game_id, date, season, week, home_team_id, away_team_id FROM games')
        games = c.fetchall()
        c.close()
        games_df = pd.DataFrame(games, columns=['game_id', 'date', 'season', 'week', 'home_team_id', 'away_team_id'])
        return games_df

    def switch_weeks_format(self, df):
        df['week'] = df.apply(lambda row: self.get_week_number(row['season'], row['week']), axis=1)
        return df

    def get_week_number(self, season, week):
        regular_season_weeks = 18 if season >= 2021 else 17
        if week > regular_season_weeks:
            playoff_week_number = week - regular_season_weeks
            if playoff_week_number == 1:
                return "Wild Card"
            elif playoff_week_number == 2:
                return "Divisional"
            elif playoff_week_number == 3:
                return "Championship"
            else:
                return "Super Bowl"
        return week        
    
    def add_game_id(self, new_df, full_df):
        games_df = self.get_games_table()

        new_df['game_id'] = full_df.apply(lambda row: self.get_game_id(games_df, row['Season'], row['week'], row['home_team_id'], row['away_team_id']), axis=1)
        return new_df

    def add_game_id_single_team(self, new_df, full_df):
        games_df = self.get_games_table()

        new_df['game_id'] = full_df.apply(lambda row: self.get_game_id_single_team(games_df, row['season'], row['week'], row['team_id']), axis=1)
        return new_df

    def get_game_id(self, df, season, week, home_team_id, away_team_id):
        game = df[(df['season'] == season) & (df['week'] == str(week)) & (df['home_team_id'] == home_team_id) & (df['away_team_id'] == away_team_id)]
        if not game.empty:
            return game.iloc[0]['game_id']
        elif week == 'Super Bowl':
                game = df[(df['season'] == season) & (df['week'] == str(week)) & (df['away_team_id'] == home_team_id) & (df['home_team_id'] == away_team_id)]
        else: 
            raise ValueError(f"Game not found for season: {season}, week: {week}, home_team_id: {home_team_id}, away_team_id: {away_team_id}")

    def get_game_id_single_team(self, df, season, week, team_id):
        game = df[(df['season'] == season) & (df['week'] == str(week)) & ((df['home_team_id'] == team_id) | (df['away_team_id'] == team_id))]
        if not game.empty:
            return game.iloc[0]['game_id']
        else:
            print(f"Game not found for season: {season}, week: {week}, team_id: {team_id}")
            return None

class team_id_helper:
    def __init__(self, conn):
        self.conn = conn

    def get_teams_table(self, field_to_check):
        c = self.conn.cursor()

        query = f'SELECT team_id, {field_to_check} FROM teams'
        c.execute(query)
        teams = c.fetchall()
        c.close()
        teams_df = pd.DataFrame(teams, columns=['team_id', 'team_name'])

        return teams_df

    def get_team_id(self, df, team_name):
        team = df[df['team_name'] == team_name]
        if not team.empty:
            return team.iloc[0]['team_id']
        else:
            raise ValueError(f"Team name '{team_name}' not found in teams table")

    def add_home_away_team_id(self, df, search_fieldname, add_fieldnames):
        teams_df = self.get_teams_table(search_fieldname)

        df['home_team_id'] = df[add_fieldnames[0]].apply(lambda x: self.get_team_id(teams_df, x))
        df['away_team_id'] = df[add_fieldnames[1]].apply(lambda x: self.get_team_id(teams_df, x))

        return df
    
    def add_team_id(self, df, search_fieldname, add_fieldname, add_fieldnames=None):
        teams_df = self.get_teams_table(search_fieldname)

        if add_fieldname is not None:
            add_fieldnames = [add_fieldname]

        for field in add_fieldnames:
            id_fieldname = field + '_id'
            df[id_fieldname] = df[add_fieldname].apply(lambda x: self.get_team_id(teams_df, x))

        return df
    
    def update_team_abbv(self, df, fields=['team']):
        old_new_list = [
            ('BLT', 'BAL'),
            ('CLV', 'CLE'),
            ('SL', 'LAR'),
            ('HST', 'HOU'),
            ('ARZ', 'ARI'),
            ('OAK', 'LV'),
            ('SD', 'LAC'),
            ('LA', 'LAR'),
            ('STL', 'LAR')
        ]

        for old_team, new_team in old_new_list:
            for field in fields:
                df[field] = df[field].replace(old_team, new_team)
        
        return df
