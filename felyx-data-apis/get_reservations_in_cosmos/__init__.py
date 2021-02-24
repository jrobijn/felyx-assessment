import logging
import json
from shared.data import reservation_attributes
from shared.utils import convert_dict_list_to_csv_string

import azure.functions as func


def parse_document(doc: func.Document, attributes: list) -> dict:
    return {attr: doc[attr] if attr in doc else None for attr in attributes}


def main(req: func.HttpRequest, documents: func.DocumentList) -> func.HttpResponse:
    logging.info("The CosmosDB API is fetching all reservation records")

    try:
        output_format = req.params.get("format", "json")

        if output_format == "json":
            reservations = [parse_document(d, reservation_attributes) for d in documents]
            output = json.dumps(reservations)
        elif output_format == "csv":
            reservations = [parse_document(d, reservation_attributes) for d in documents]
            output = convert_dict_list_to_csv_string(reservations, reservation_attributes)
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
