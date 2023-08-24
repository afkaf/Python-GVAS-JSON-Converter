import json

def to_json_structure(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    if isinstance(obj, list):
        return [to_json_structure(item) for item in obj]
    if isinstance(obj, tuple):
        return [to_json_structure(item) for item in obj]
    if isinstance(obj, dict):
        return {key: to_json_structure(value) for key, value in obj.items()}
    if isinstance(obj, bytes):
        return obj.hex()

    # Check if the object has a __dict__ attribute
    if hasattr(obj, '__dict__'):
        return {key: to_json_structure(value) for key, value in vars(obj).items()}

    # Handle other cases (e.g., built-in types)
    return str(obj)

def sav_to_json(props, string=False):
    savJSON = []
    for prop in props:
        savJSON.append(to_json_structure(prop))
    if string:
        json_string = json.dumps(savJSON, indent=2)
        return json_string
    else:
        return savJSON
