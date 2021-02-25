import logging
import pyodbc
from shared.data import reservation_schema, location_schema
from shared.utils import parse_csv_blob
from shared.sql import get_sql_connection_string

import azure.functions as func


def main(reservationsBlob: func.InputStream):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {reservationsBlob.name}\n"
                 f"Blob Size: {reservationsBlob.length} bytes")
    
    reservations = parse_csv_blob(reservationsBlob, reservation_schema)
    reservations = [
        (r["id"], r["customer_id"], r["net_price"], r["start_latitude"], r["start_longitude"], r["srid"], r["location_id"])
        for r in reservations
    ]

    with pyodbc.connect(get_sql_connection_string()) as conn:
        with conn.cursor() as cursor:
            cursor.execute("SET IDENTITY_INSERT Reservations ON")
            cursor.executemany("""
                INSERT INTO 
                    Reservations
                    (id, customer_id, net_price, start_latitude, start_longitude, srid, location_id)
                VALUES
                    (?, ?, ?, ?, ?, ?, ?)
            """, reservations)
            cursor.execute("SET IDENTITY_INSERT Reservations OFF")