import logging

import psycopg2
from io import StringIO
import psycopg2.extras as extras
import os


class TmDB(object):
    """A singleton class that encapsulates all the functionality for interacting with timescaleDB"""

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(TmDB, cls).__new__(cls)
        return cls.instance


    def __init__(self):
        with psycopg2.connect(
            host=os.environ.get("POSTGRES_HOST"),
            port=os.environ.get("POSTGRES_PORT"),
            dbname=os.environ.get("POSTGRES_DB"),
            user=os.environ.get("POSTGRES_USER"),
            password=os.environ.get("POSTGRES_PASSWORD"),
            connect_timeout=5,
        ) as conn:
            self.conn = conn
            self.cursor = conn.cursor()


    def __del__(self):
        self.cursor.close()
        self.conn.close()


    def close_connection(self):
        self.cursor.close()
        self.conn.close()


    def upload_data(self, df, table):
        """
        Upload the stock price data to TimescaleDB
        """

        # Initialize a string buffer
        buffer = StringIO()
        # Write the Pandas DataFrame as a CSV file to the buffer
        buffer.write(df.to_csv(index=None, header=None))
        # Be sure to reset the position to the start of the stream
        buffer.seek(0)

        self.cursor.copy_from(
            file=buffer, table=table, sep=",", null="", size=8192, columns=df.columns
        )
        self.conn.commit()
        logging.debug(f"DataFrame uploaded to TimescaleDB {table} successfully")


    def upsert_data(self, df, table):

        # Create a list of tuples from the dataframe values
        tuples = [tuple(x) for x in df.to_numpy()]
        # Comma-separated dataframe columns
        columns = ",".join(list(df.columns))
        # SQL query to execute
        # TODO should check if it's updating only what should be updated and not ignoring everything
        #  and not inserting at all when there is a little conflict
        query = "INSERT INTO %s(%s) VALUES %%s ON CONFLICT DO NOTHING" % (
            table,
            columns,
        )
        # print(query)

        try:
            extras.execute_values(self.cursor, query, tuples)
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("Error: %s" % error)
            self.conn.rollback()
            self.cursor.close()
            return 1
        logging.debug(f"DataFrame Updated in TimescaleDB {table} successfully")


    def get_tickers_list(self):
        """
        Get Stocks Ticker list
        ":return: stocks ticker list from TimescaleDB
        """

        query = f"SELECT ticker FROM {os.environ.get('DB_STOCK_TICKERS_TABLE')};"
        try:
            self.cursor.execute(query)
            response = self.cursor.fetchall()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("Error: %s" % error)
            self.conn.rollback()
            self.cursor.close()
            return 1
        logging.info("Got ticker names from TimescaleDB")

        return response


    def truncate(self, table_name):
        self.cursor.execute(f"TRUNCATE {table_name}")
        self.conn.commit()


    def get_last(self, table, ticker):
        query = f"""
        SELECT ticker, date
        FROM {table}
        WHERE ticker like '{ticker}'
        ORDER BY date DESC LIMIT 1
        """

        try:
            self.cursor.execute(query)
            response = self.cursor.fetchone()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("Error: %s" % error)
            self.conn.rollback()
            self.cursor.close()
            return 1
        return response


    def get_first(self, table, ticker):
        query = f"""
        SELECT ticker, date
        FROM {table}
        WHERE ticker like '{ticker}'
        ORDER BY date ASC LIMIT 1
        """

        try:
            self.cursor.execute(query)
            response = self.cursor.fetchone()
            self.conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            logging.error("Error: %s" % error)
            self.conn.rollback()
            self.cursor.close()
            return 1
        return response
