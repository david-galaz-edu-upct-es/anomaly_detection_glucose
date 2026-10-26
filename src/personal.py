import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path
import json

# ── Configuration ──────────────────────────────────────────────────────────────
INPUT_PATH  = "diabetes/personal-data/pacient_1.csv"   # file containing the time series
OUTPUT_JSON = "./diabetes/personal-data/glucose_timeseries.json"      # json containing the glucose timeseries
# ──────────────────────────────────────────────────────────────────────────────


def clean_personal_data(input_dir: str = INPUT_PATH, output_file: str = OUTPUT_JSON) -> None:
    df = pd.read_csv(input_dir, sep= ",", usecols= ["Sello de tiempo del dispositivo","Historial de glucosa mg/dL"]).rename(columns={"Sello de tiempo del dispositivo":"date","Historial de glucosa mg/dL":"glucose"})
    df = df.dropna()
    df['date']= pd.to_datetime(df['date'], format = "%d-%m-%Y %H:%M")
    ts = pd.Series(df.sort_values("date").set_index("date")['glucose'])
    ts = ts[~ts.index.duplicated(keep="first")]
    ts.to_json(output_file, indent = 5)
    return (ts)


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    data = clean_personal_data()
    data.plot()
    plt.show()
    print(data)