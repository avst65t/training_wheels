import json

def merge_field_outputs(outputs: list) -> dict:
    combined = {}
    for output in outputs:
        try:
            data = json.loads(output)
        except json.JSONDecodeError:
            continue
        for k, v in data.items():
            if k not in combined or not combined[k]:
                combined[k] = v
    return combined
