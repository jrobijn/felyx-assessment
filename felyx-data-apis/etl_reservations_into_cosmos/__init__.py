import logging
import csv
import codecs
from shared.data import reservation_schema, location_schema
from shared.utils import parse_csv_blob

import azure.functions as func


def main(reservationsBlob: func.InputStream, locationsBlob: func.InputStream, document: func.Out[func.DocumentList]):
    logging.info(f"Python blob trigger function processed blob \n"
                 f"Name: {reservationsBlob.name}\n"
                 f"Blob Size: {reservationsBlob.length} bytes")

    
    reservations = parse_csv_blob(reservationsBlob, reservation_schema)
    locations = parse_csv_blob(locationsBlob, location_schema)

    for r in reservations:
        # Denormalize each reservation by adding location information
        location = next((l for l in locations if l["id"] == r["location_id"]), None)
        r["location_title"] = location["title"] if location else None
        r["location_wgs84_polygon"] = location["wgs84_polygon"] if location else None

        # Cosmos DB requires string id's
        r["id"] = str(r["id"])

    # Store all reservations in CosmosDB
    document.set(func.DocumentList(reservations))