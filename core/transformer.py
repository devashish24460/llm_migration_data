from utils.transformations import normalize_phone, parse_date, clean_name

TRANSFORM_MAP = {
    "normalize_phone": normalize_phone,
    "parse_date": parse_date,
    "clean_name": clean_name
}

def apply_transformations(row, mapping, transformations):
    new_row = {}

    for src, tgt in mapping.items():
        value = row[src]

        if tgt in transformations:
            func_name = transformations[tgt]
            func = TRANSFORM_MAP.get(func_name)

            if func:
                value = func(value)

        new_row[tgt] = value

    return new_row