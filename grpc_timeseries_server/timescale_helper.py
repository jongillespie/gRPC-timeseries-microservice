"""
Initialise the Timescale Hypertable & populate with cleaned 'meterusage' data.
"""

import os

from sqlalchemy import create_engine
import psycopg2
import pandas as pds

import clean_csv_data


db_table_name = 'meter_usage'


# Connect to the database
CONNECTION = f"postgres://postgres:None@localhost:5432/meterusage"
# TODO Set password, amend all to be .env Vars.
# conn = psycopg2.connect(dbname='my-db-name',
#                         user='postgres',
#                         password='super-secret',
#                         host='localhost',
#                         port='5432')
# CONNECTION = f"dbname={os.getenv('DBNAME')} user={os.getenv('DBUSER')} host=localhost port=5432 connect_timeout=10" # sslmode=require password=secret"
# CONNECTION = f"postgres://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{os.getenv('DBPORT')}/{os.getenv('DBNAME')}"
db_connection = psycopg2.connect(CONNECTION)
# To utilise 'to_sql' for the dataframe, create an SQLAlchemy Engine w/ Connection
alchemy_engine = create_engine(CONNECTION)
postgreSQLConnection = alchemy_engine.connect()


def _db_cursor_execute(queries, is_multiple_queries=False, is_expecting_results=False):
    """Timescale Cursor Method for executing one or more queries.

    Args:
        queries ([list]): [List of SQL queries to execute]
        is_multiple_queries (bool, optional): [flag for single vs. multiple queries in above list]. Defaults to False.
        is_expecting_results (bool, optional): [flag for the cursor to return results or none]. Defaults to False.

    Returns:
        [DBrecords]: [Query results from the database]
    """

    try:
        cursor = db_connection.cursor()
        print("timescale_helper    | > DB Cursor activated")
        if is_multiple_queries:
            for query in queries:
                print("timescale_helper    | > Running Query: ", query)
                cursor.execute(query)
        else:
            print("timescale_helper    | > Running Query: ", queries)
            cursor.execute(queries)
        print("timescale_helper    | > Committing to DB")
        db_connection.commit()
        if is_expecting_results:
            results = cursor.fetchall()
            print("timescale_helper    | > Closing Cursor Connection")
            cursor.close()
            return results
        else: 
            print("timescale_helper    | > Closing Cursor Connection")
            cursor.close()
            return
    except (Exception, psycopg2.Error) as error:        
        print(error.pgerror)
        db_connection.rollback()
        cursor.close()


def _create_meterusage_hypertable():
    """Initialises the 'meterusage' hypertable within the TimescaleDB 
    """    
    
    query_create_meterusage_table = f"""CREATE TABLE {db_table_name} (
                                            time        TIMESTAMPTZ     NOT NULL,
                                            meterusage  FLOAT           NOT NULL
                                            );"""
    query_create_meterusage_hypertable = f"SELECT create_hypertable ('{db_table_name}', 'time');"
    queries = [query_create_meterusage_table, query_create_meterusage_hypertable]
    _db_cursor_execute(queries, is_multiple_queries=True, is_expecting_results=False)


def _insert_cleaned_meterusage_data():
    """Inserts all of the meterusage data provided by the original CSV, cleaned via pandas dataframe
    """    

    print('timescale_helper    | > Cleaning CSV Data via Dataframe')
    cleaned_data = clean_csv_data.clean_csv()
    # cleaned_data.to_sql(name=f'{db_table_name}', con=db_connection, schema='postgres', if_exists='replace', index=False)
    try:
        print('timescale_helper    | > Translating Dataframe into Database')
        cleaned_data.to_sql(db_table_name, postgreSQLConnection, if_exists='replace')
    except ValueError as vx:
        print(vx)
    except Exception as ex:  
        print(ex)


def get_all_data():
    """Returns all data from the meter_usage hypertable
    """

    # query_get_all_data = f"SELECT * FROM {db_table_name};"
    query_get_all_data = f"SELECT time, meterusage FROM {db_table_name};"
    results_raw = _db_cursor_execute(query_get_all_data, is_multiple_queries=False, is_expecting_results=True)
    return results_raw


_create_meterusage_hypertable()
_insert_cleaned_meterusage_data()
# get_all_data()
