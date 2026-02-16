import sys
from avro.datafile import DataFileReader
from avro.io import DatumReader
from pathlib import Path

file_path = sys.argv[1] if len(sys.argv) > 1 else None

if not file_path:
    print("Usage: python unified_reader.py <path_to_avro_file>")
    sys.exit(1)

with open(file_path, "rb") as f:
    # Read without reader schema to avoid schema resolution issues
    reader = DataFileReader(f, DatumReader())

    for record in reader:
        # Handle schema evolution: v1 uses "amount", v2 uses "total_amount"
        # Normalize to "total_amount" for unified output (use key presence, not truthiness, so 0.0 is correct)
        amount = record["total_amount"] if "total_amount" in record else record.get("amount", 0.0)
        
        print(
            record["id"],
            record["event_time"],
            amount,
            record["user_email"],
            record["currency"],
            sep=","
        )

    reader.close()
