import csv
import avro.schema
from avro.datafile import DataFileWriter
from avro.io import DatumWriter
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

schema_path = BASE_DIR / "schemas" / "transactions_v2.avsc"
schema = avro.schema.parse(schema_path.read_text())

output_path = BASE_DIR / "data" / "transactions_v2.avro"
csv_path = BASE_DIR / "data" / "transactions_v2.csv"

with open(output_path, "wb") as out_file:
    writer = DataFileWriter(out_file, DatumWriter(), schema)

    with open(csv_path, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            writer.append({
                "id": row["id"],
                "event_time": row["event_time"],
                "total_amount": float(row["total_amount"]),
                "user_email": row["user_email"],
                "currency": row["currency"]
            })
    writer.close()
