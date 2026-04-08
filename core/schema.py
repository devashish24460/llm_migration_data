import pandas as pd
from dateutil.parser import parse

def is_datetime(val):
    try:
        parse(val)
        return True
    except:
        return False
def analyze_schema(df: pd.DataFrame):
    columns_info = []

    for col in df.columns:
        sample_values = df[col].dropna().astype(str).head(5).tolist()

        inferred_type = "string"
        if pd.api.types.is_numeric_dtype(df[col]):
            inferred_type = "number"
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            inferred_type = "datetime"

        columns_info.append({
            "name": col,
            "sample_values": sample_values,
            "inferred_type": inferred_type
        })

    return {"columns": columns_info}