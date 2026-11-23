from pathlib import Path
import pandas as pd

data_dir = Path("data")

files = {
    "demo": "DEMO_L.xpt",
    "bmi": "BMX_L.xpt",
    "bp": "BPXO_L.xpt",
    "activity": "PAQ_L.xpt",
    "diet": "DBQ_L.xpt"
}

datasets = {}

# Load and validate each dataset
for name, filename in files.items():
    path = data_dir / filename

    if not path.exists():
        raise FileNotFoundError(f"Missing file: {path}")

    df = pd.read_sas(path, format="xport")

    if "SEQN" not in df.columns:
        raise ValueError(f"SEQN is missing from {filename}")

    if df["SEQN"].duplicated().any():
        raise ValueError(
            f"Duplicate participant IDs found in {filename}. "
            "Inspect this file before merging."
        )

    datasets[name] = df

    print(f"{filename}: {df.shape}")

# Merge records by participant ID
combined = datasets["demo"]

for name in ["bmi", "bp", "activity", "diet"]:
    combined = combined.merge(
        datasets[name],
        on="SEQN",
        how="left",
        validate="one_to_one"
    )

# Save combined dataset
output_file = data_dir / "nhanes_combined.csv"

combined.to_csv(output_file, index=False)

print("\nNHANES datasets combined successfully!")
print("Rows and columns:", combined.shape)
print("Saved to:", output_file)

print("\nColumns:")
print(combined.columns.tolist())