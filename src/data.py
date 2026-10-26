import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path
import json

# ── Configuration ──────────────────────────────────────────────────────────────
INPUT_DIR  = "./diabetes/diabetes-data"   # folder containing the individual CSVs
OUTPUT_JSON = "./diabetes/glucose_timeseries.json"      # json containing the glucose timeseries
ID_SOURCE  = "index"          # "filename" → use the CSV name as ID
                                 # "index"    → use P001, P002, … as ID
# ──────────────────────────────────────────────────────────────────────────────


def clean_data(input_dir: str = INPUT_DIR, output_file: str = OUTPUT_JSON, id_source: str = ID_SOURCE) -> None:
    """
    
    """

    # Search all csv in the input folder
    csv_files = glob.glob(os.path.join(INPUT_DIR , "data*"))
    # If not found
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in '{input_dir}'") # Lanzamos una excepción
    
    csv_files.sort() # Sort by name

    series = pd.Series() # Serie to store all Time Series
    # For each csv found
    for i, path in enumerate(csv_files, start = 1):
        # Read the csv
        df = pd.read_csv(path, sep= "	", names=["Date", "Time", "Code", "Value"])
        # We obtain the patient ID
        patient_id = (
            path.stem                          # e.g. "patient_042"
            if id_source == "filename"
            else f"P{i:03d}"                   # e.g. "P001"
        )
        # We unify the Date and Time to a datetime type. If format does not match, nullify the value
        try: 
            df["datetime"] = pd.to_datetime(df["Date"] + " " + df["Time"], format="mixed")  # "mixed" induces the format
        except ValueError as ve:
            df["datetime"] = pd.NA

        # We drop the NA values
        df_valid_timestamp = df.dropna()            

        # Reset index to be the time
        df_by_date = df_valid_timestamp.drop(["Date", "Time"], axis = 1).set_index("datetime").sort_index()
        
        # Create a Series with just the glucose meassures (codes bewteen 48 and 64)
        patient_serie_dirty = pd.Series(df_by_date.query("(48 <= Code) and (Code<= 64)")['Value'])
        
        # We convert format to numeric (mostly to avoid strings, converted to NAN)
        patient_serie_cleaned = pd.to_numeric(patient_serie_dirty, errors="coerce")
        
        # If the length is high enough we keep the record
        if len(patient_serie_cleaned) > 72:     # Proxy: Assuming 1 meassure per hour, 72 is 3 whole days
            series[patient_id] = patient_serie_cleaned  # We store the data in the dict

    series.to_json(output_file, indent = 5)



if __name__ == "__main__":
    import matplotlib.pyplot as plt
    clean_data()
    print("Hello World")
    #print(i_d)