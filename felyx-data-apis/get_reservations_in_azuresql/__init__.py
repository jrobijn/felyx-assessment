import logging
import json
import pyodbc
from dotenv import load_dotenv
from shared.data import reservation_schema
from shared.utils import convert_dict_list_to_csv_string, parse_boolean
from shared.sql import get_sql_connection_string

import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info("The Azure SQL DB API is fetching all reservation records")

    try:
        output_format = req.params.get("format", "json")
        add_location = req.params.get("addLocation", "False")

        columns = reservation_schema.keys()
        if parse_boolean(add_location):
            columns += ["wgs84_polygon", "title"]
            query = "SELECT * FROM Reservations r LEFT JOIN Locations l ON r.location_id = l.id"
        else:
            query = "SELECT * FROM Reservations"

        with pyodbc.connect(get_sql_connection_string()) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                reservations = [dict(zip(columns, row)) for row in cursor.fetchall()]

        if output_format == "json":
            output = json.dumps(reservations)
        elif output_format == "csv":
            output = convert_dict_list_to_csv_string(reservations, columns)
        else:
            raise ValueError(f"Unsupported format '{output_format}'")

    except ValueError as e:
        return func.HttpResponse(
            str(e),
            status_code=400
        )

    except Exception as e:
        return func.HttpResponse(
            str(e),
            status_code=500
        )

    else:
        return func.HttpResponse(
            output,
            status_code=200,
            headers={
                "Content-Disposition": f"attachment; filename=reservations.{output_format}",
                "Content-Type": f"text/{output_format}"
            }
        )
