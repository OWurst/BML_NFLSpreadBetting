class date_week_helper:
    def __init__(self, conn):
        self.conn = conn


class team_id_helper:
    def __init__(self, conn):
        self.conn = conn

        teams_table = get_teams_table(self.conn)
    
    def get_teams_table(self, conn):
        c = conn.cursor()

        if name_only:
            c.execute('SELECT team_id, team_name, team_name_full FROM teams')
        else:
            c.execute('SELECT team_id, team_name_full FROM teams')
        
        teams = c.fetchall()
        c.close()
        teams_df = pd.DataFrame(teams, columns=['team_id', 'team_name', 'team_name_full'])
        return teams_df

