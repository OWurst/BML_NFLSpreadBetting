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
    
    def add_game_id(self, new_df, full_df):
        games_df = self.get_games_table()

        new_df['game_id'] = full_df.apply(lambda row: self.get_game_id(games_df, row['Season'], row['week'], row['home_team_id'], row['away_team_id']), axis=1)
        return new_df

    def get_game_id(self, df, season, week, home_team_id, away_team_id):
        game = df[(df['season'] == season) & (df['week'] == str(week)) & (df['home_team_id'] == home_team_id) & (df['away_team_id'] == away_team_id)]
        if not game.empty:
            return game.iloc[0]['game_id']
        elif week == 'Super Bowl':
                game = df[(df['season'] == season) & (df['week'] == str(week)) & (df['away_team_id'] == home_team_id) & (df['home_team_id'] == away_team_id)]
        else: 
            raise ValueError(f"Game not found for season: {season}, week: {week}, home_team_id: {home_team_id}, away_team_id: {away_team_id}")

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
        return df[df['team_name'] == team_name]['team_id'].values[0]

    def add_home_away_team_id(self, df, search_fieldname, add_fieldnames):
        teams_df = self.get_teams_table(search_fieldname)

        df['home_team_id'] = df[add_fieldnames[0]].apply(lambda x: self.get_team_id(teams_df, x))
        df['away_team_id'] = df[add_fieldnames[1]].apply(lambda x: self.get_team_id(teams_df, x))

        return df
