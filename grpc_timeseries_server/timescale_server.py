"""
# TODO describe file.
"""

import psycopg2
import os

print(os.environ)

meter = 'meterusage' #os.getenv('DBNAME')

# Connect to the database
CONNECTION = f"postgres://postgres:None@localhost:5432/meterusage"
# TODO Set password, amend all to be .env Vars.
# CONNECTION = f"dbname={os.getenv('DBNAME')} user={os.getenv('DBUSER')} host=localhost port=5432 connect_timeout=10" # sslmode=require password=secret"
# CONNECTION = f"postgres://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{os.getenv('DBPORT')}/{os.getenv('DBNAME')}"
db_connection = psycopg2.connect(CONNECTION)


def db_cursor_execute(queries, multiple_queries=False):
    """Timescale Cursor Method for executing one or more queries.

    Args:
        queries ([list]): [List of SQL queries to execute]
        multiple_queries (bool, optional): [flag for single vs. multiple queries in above list]. Defaults to False.
    """

    try:
        cursor = db_connection.cursor()
        print("> DB Cursor activated")
        if multiple_queries:
            for query in queries:
                print("> Running Query: ", query)
                cursor.execute(query)
        else:
            cursor.execute(queries)
        print("> Committing to DB")
        db_connection.commit()
    except (Exception, psycopg2.Error) as error:        
        print(error.pgerror)
    print("> Closing Cursor Connection")
    cursor.close()


def create_meterusage_hypertable():
    """Initialises the 'meterusage' hypertable within the TimescaleDB 
    """    
    
    query_create_meterusage_table = """CREATE TABLE meter_usage (
                                            time        TIMESTAMPTZ     NOT NULL,
                                            meterusage  FLOAT           NOT NULL
                                            );"""
    query_create_meterusage_hypertable = "SELECT create_hypertable ('meter_usage', 'time');"
    queries = [query_create_meterusage_table, query_create_meterusage_hypertable]
    db_cursor_execute(queries, multiple_queries=True)
    

create_meterusage_hypertable()



