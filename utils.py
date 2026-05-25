import json
import pandas as pd


def extract_json_array(result):
    start = result.find("[")
    end = result.rfind("]") + 1

    if start == -1 or end == 0:
        raise ValueError("No JSON array found.")

    clean_result = result[start:end]
    return json.loads(clean_result)


def risks_to_dataframe(risks):
    return pd.DataFrame(risks)
