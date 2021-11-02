import psycopg2
from io import StringIO


def upload_data(df, config, table_name):
    """
    Upload the stock price data to TimescaleDB
    """

    with psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            connect_timeout=5
    ) as conn:
        with conn.cursor() as cursor:
            # Truncate the existing table (i.e. remove all existing rows)
            # cursor.execute(f"TRUNCATE {table_name}")
            # conn.commit()

            # Now insert the brand-new data
            # Initialize a string buffer
            sio = StringIO()
            # Write the Pandas DataFrame as a CSV file to the buffer
            sio.write(df.to_csv(index=None, header=None))
            # Be sure to reset the position to the start of the stream
            sio.seek(0)
            cursor.copy_from(
                file=sio,
                table=table_name,
                sep=",",
                null="",
                size=8192,
                columns=df.columns
            )
            conn.commit()
            print("DataFrame uploaded to TimescaleDB")


def get_tickers_list(config, table_name):
    """
    Upload the stock price data to TimescaleDB
    """

    with psycopg2.connect(
            host=config.POSTGRES_HOST,
            port=config.POSTGRES_PORT,
            dbname=config.POSTGRES_DB,
            user=config.POSTGRES_USER,
            password=config.POSTGRES_PASSWORD,
            connect_timeout=5
    ) as conn:
        with conn.cursor() as cursor:
            cursor.execute(f"SELECT ticker FROM {table_name};")
            response = cursor.fetchall()
            print("Got ticker names from TimescaleDB")

            return response


# TODO function that returns the last data point, and then you download yahoo data from this point and until now. if there is no last point, go back 5 years or maybe go to max?

# TODO function then inserts a new ticker to the stocks_tickers table. iterates a csv file with columns, ticker, name, exchange, industry.