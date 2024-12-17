import sqlite3
import database_builds.team_games_database_build as tgb
import database_builds.player_games_database_build as tsb

def build_teams_db(conn):
    tgb.create_teams_table(conn)
    tgb.populate_teams_table(conn)
    tgb.create_historical_games_table(conn)
    tgb.populate_historical_games_table(conn)
    tgb.create_team_weekly_stats_table(conn)
    tgb.populate_team_weekly_stats_table(conn)

if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    
    build_teams_db(conn)

    conn.close()