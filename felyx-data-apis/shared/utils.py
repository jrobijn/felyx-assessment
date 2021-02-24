import io
import csv


def convert_dict_list_to_csv_string(reservations: list, headers: list) -> str:
    output = io.StringIO()
    writer = csv.DictWriter(output, headers)

    writer.writeheader()
    writer.writerows(reservations)

    return output.getvalue()