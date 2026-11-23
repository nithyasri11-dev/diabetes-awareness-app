from pathlib import Path

import pandas as pd
from ucimlrepo import fetch_ucirepo

# Create the data folder
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)

print("Connecting to UCI repository...")

try:
    # Download the UCI Diabetes Health Indicators dataset
    dataset = fetch_ucirepo(id=891)

    # Get the input features
    X = dataset.data.features

    # Get the target
    y = dataset.data.targets

    # Combine features and target
    df = pd.concat(
        [
            X.reset_index(drop=True),
            y.reset_index(drop=True)
        ],
        axis=1
    )

    # Save the dataset
    output_file = data_folder / "diabetes_health_indicators.csv"

    df.to_csv(output_file, index=False)

    print("\nSUCCESS! Dataset downloaded.")
    print("Number of rows:", df.shape[0])
    print("Number of columns:", df.shape[1])

    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst five rows:")
    print(df.head())

    print("\nSaved at:", output_file.resolve())

except Exception as error:
    print("\nDownload failed.")
    print("Error:", error)