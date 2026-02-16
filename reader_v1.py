import avro.schema
from avro.datafile import DataFileReader
from avro.io import DatumReader
from pathlib import Path

# Get the directory where this script is located
BASE_DIR = Path(__file__).resolve().parent

schema_path = BASE_DIR / "schemas" / "transactions_v1.avsc"
schema = avro.schema.parse(schema_path.read_text())

avro_path = BASE_DIR / "data" / "transactions_v1.avro"

with open(avro_path, "rb") as f:
    reader = DataFileReader(f, DatumReader())
    for record in reader:
        # Output must exactly match CSV: id,event_time,user_email,amount,currency
        print(
            record["id"],
            record["event_time"],
            record["user_email"],
            record["amount"],
            record["currency"],
            sep=","
        )
    reader.close()
