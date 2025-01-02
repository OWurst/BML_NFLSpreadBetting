import sqlite3
import database_builds.team_games_database_build as tgb
import database_builds.player_games_database_build as pgb

if __name__ == '__main__':
    conn = sqlite3.connect('db.sqlite3')
    
    tgb.main()
    pgb.main()

    conn.close()