import psycopg2
from io import StringIO


class TmDB(object):

    def __init__(self, config):
        with psycopg2.connect(
                host=config.POSTGRES_HOST,
                port=config.POSTGRES_PORT,
                dbname=config.POSTGRES_DB,
                user=config.POSTGRES_USER,
                password=config.POSTGRES_PASSWORD,
                connect_timeout=5
        ) as conn:
            self.conn = conn
            self.cursor = conn.cursor()

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def upload_data(self, df, table_name):
        """
        Upload the stock price data to TimescaleDB
        """

        # Initialize a string buffer
        sio = StringIO()
        # Write the Pandas DataFrame as a CSV file to the buffer
        sio.write(df.to_csv(index=None, header=None))
        # Be sure to reset the position to the start of the stream
        sio.seek(0)

        self.cursor.copy_from(
            file=sio,
            table=table_name,
            sep=",",
            null="",
            size=8192,
            columns=df.columns
        )
        self.conn.commit()
        print("DataFrame uploaded to TimescaleDB")

    def get_tickers_list(self, table_name):
        """
        Get Stocks Ticker list
        ":return: stocks ticker list from TimescaleDB
        """

        self.cursor.execute(f"SELECT ticker FROM {table_name};")
        response = self.cursor.fetchall()
        self.conn.commit()
        print("Got ticker names from TimescaleDB")

        return response

    def truncate(self, table_name):
        self.cursor.execute(f"TRUNCATE {table_name}")
        self.conn.commit()


    # def return_last(self, table_name):


# TODO function that returns the last data point, and then you download yahoo data from this point and until now. if there is no last point, go back 5 years or maybe go to max?

# TODO function then inserts a new ticker to the stocks_tickers table. iterates a csv file with columns, ticker, name, exchange, industry.

# then you can just set a cron and let it do magic.
