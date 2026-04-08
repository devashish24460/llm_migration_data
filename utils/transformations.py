from datetime import datetime
import re

def normalize_phone(x):
    x = str(x)
    digits = re.sub(r"\D", "", x)

    if len(digits) == 10:
        return "+91" + digits
    elif digits.startswith("91"):
        return "+" + digits
    return digits

def parse_date(x):
    try:
        return str(datetime.fromisoformat(x))
    except:
        return x

def clean_name(x):
    return str(x).strip().title()