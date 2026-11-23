from pathlib import Path
import pandas as pd

data_dir = Path("data")

files = [
    "DEMO_L.xpt",
    "BMX_L.xpt",
    "BPXO_L.xpt",
    "PAQ_L.xpt",
    "DBQ_L.xpt"
]

for filename in files:
    input_file = data_dir / filename

    if not input_file.exists():
        print(f"FILE NOT FOUND: {input_file}")
        continue

    print(f"\nConverting {filename}...")

    try:
        df = pd.read_sas(input_file, format="xport")

        output_file = data_dir / f"{input_file.stem}.csv"

        df.to_csv(output_file, index=False)

        print("Conversion successful!")
        print("Rows and columns:", df.shape)
        print("Saved to:", output_file)

    except Exception as error:
        print(f"Conversion failed: {error}")

print("\nConversion process completed.")