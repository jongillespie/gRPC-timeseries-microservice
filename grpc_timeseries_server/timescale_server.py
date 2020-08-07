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
# CONNECTION = f"dbname={os.getenv('DBNAME')} user={os.getenv('DBUSER')} host=localhost port=5432 connect_timeout=10" # sslmode=require password=secret"
# CONNECTION = f"postgres://{os.getenv('DBUSER')}:{os.getenv('DBPASS')}@{os.getenv('DBHOST')}:{os.getenv('DBPORT')}/{os.getenv('DBNAME')}"
db_connection = psycopg2.connect(CONNECTION)
# To utilise 'to_sql' for the dataframe, create an SQLAlchemy Engine w/ Connection
alchemy_engine = create_engine(CONNECTION)
postgreSQLConnection = alchemy_engine.connect()


def db_cursor_execute(queries, is_multiple_queries=False):
    """Timescale Cursor Method for executing one or more queries.

    Args:
        queries ([list]): [List of SQL queries to execute]
        multiple_queries (bool, optional): [flag for single vs. multiple queries in above list]. Defaults to False.
    """

    try:
        cursor = db_connection.cursor()
        print("> DB Cursor activated")
        if is_multiple_queries:
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
    
    query_create_meterusage_table = f"""CREATE TABLE {db_table_name} (
                                            time        TIMESTAMPTZ     NOT NULL,
                                            meterusage  FLOAT           NOT NULL
                                            );"""
    query_create_meterusage_hypertable = f"SELECT create_hypertable ('{db_table_name}', 'time');"
    queries = [query_create_meterusage_table, query_create_meterusage_hypertable]
    db_cursor_execute(queries, is_multiple_queries=True)


def insert_cleaned_meterusage_data():
    """Inserts all of the meterusage data provided by the original CSV, cleaned via pandas dataframe
    """    

    print('> Cleaning CSV Data via Dataframe')
    cleaned_data = clean_csv_data.clean_csv()
    # cleaned_data.to_sql(name=f'{db_table_name}', con=db_connection, schema='postgres', if_exists='replace', index=False)
    try:
        print('> Translating Dataframe into Database')
        cleaned_data.to_sql(db_table_name, postgreSQLConnection, if_exists='replace')
    except ValueError as vx:
        print(vx)
    except Exception as ex:  
        print(ex)



create_meterusage_hypertable()
insert_cleaned_meterusage_data()


# get_all = f"SELECT * FROM {db_table_name}"
# db_cursor_execute([get_all])
