import pandas as pd

def read_csv(path, dtype=str):
    return pd.read_csv(path, dtype=dtype, keep_default_na=False)

def df_to_csv_text(df):
    return df.to_csv(index=False, lineterminator="\n")