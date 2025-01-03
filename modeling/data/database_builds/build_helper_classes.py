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