import pandas as pd
from core.transformer import apply_transformations

def execute_migration(df, mapping_output):
    mapping = mapping_output["mapping"]
    transformations = mapping_output.get("transformations", {})

    new_data = []

    errors = 0

    for _, row in df.iterrows():
        try:
            new_row = apply_transformations(row, mapping, transformations)
            new_data.append(new_row)
        except Exception:
            errors += 1

    result_df = pd.DataFrame(new_data)

    report = {
        "rows_processed": len(df),
        "rows_success": len(result_df),
        "errors": errors,
        "confidence": mapping_output.get("confidence", 0)
    }

    return result_df, report