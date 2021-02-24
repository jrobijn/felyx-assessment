import io
import csv
import codecs

import azure.functions as func


def parse_record(raw_dict: dict, schema: dict) -> dict:
    new_dict = {}
    for k, v in raw_dict.items():
        if k in schema.keys():
            # Try to convert to the expected type. Set to None if not possible (invalid data)
            try:
                new_dict[k] = schema[k](v)
            except ValueError:
                new_dict[k] = None
    return new_dict


def parse_csv_blob(blob: func.InputStream, schema: dict) -> list:
    decoded_stream = codecs.iterdecode(blob, 'utf-8')

    return [parse_record(row, schema) for row in csv.DictReader(decoded_stream)]


def convert_dict_list_to_csv_string(reservations: list, headers: list) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, headers)

    writer.writeheader()
    writer.writerows(reservations)

    return output.getvalue()