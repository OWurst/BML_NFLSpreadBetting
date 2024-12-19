'''
    This file contains functions that interact with the database.
    This includes inserts, updates, and a variety of queries. Also will be used to get rollup fields
    All inserts and updates are done in a bulk fashion to reduce the number of queries.
'''

import sqlite3
import pandas as pd
