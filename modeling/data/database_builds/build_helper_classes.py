import pandas as pd

class date_week_helper:
    def __init__(self, conn):
        self.conn = conn

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
