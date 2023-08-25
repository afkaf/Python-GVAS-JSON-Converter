import json

def load_json(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def obj_to_json(obj):
    return json.dumps(obj, indent=2)

def get_object_by_path(data, path):
    obj = data
    for p in path:
        if isinstance(p, dict):
            key, value = list(p.items())[0]
            if isinstance(obj, list):
                obj = next((item for item in obj if item.get(key) == value), None)
            elif isinstance(obj, dict):
                obj = obj.get(key) if obj.get(key) == value else None
        elif isinstance(p, str):
            obj = obj.get(p)
        elif isinstance(p, int):
            obj = obj[p] if isinstance(obj, list) else None
        else:
            return None
        if obj is None:
            return None
    return obj

def insert_object_by_path(data, path, new_object, position='after'):
    # Get the parent object by considering the path except the last item
    parent_obj = get_object_by_path(data, path[:-1])
    last_path_item = path[-1]
    
    if isinstance(parent_obj, list) and isinstance(last_path_item, dict):
        key_to_insert, value_to_insert = list(last_path_item.items())[0]
        # Find the index of the object to insert before or after
        index_to_insert = next((i for i, item in enumerate(parent_obj) if item.get(key_to_insert) == value_to_insert), None)
        if index_to_insert is not None:
            if position == 'before':
                parent_obj.insert(index_to_insert, new_object)
            elif position == 'after':
                parent_obj.insert(index_to_insert + 1, new_object)


def replace_object_by_path(data, path, new_object):
    # Get the parent object by considering the path except the last item
    parent_obj = get_object_by_path(data, path[:-1])
    last_path_item = path[-1]

    if isinstance(last_path_item, dict):
        key_to_replace, value_to_replace = list(last_path_item.items())[0]
        if isinstance(parent_obj, list):
            for i, item in enumerate(parent_obj):
                if item.get(key_to_replace) == value_to_replace:
                    parent_obj[i] = new_object
                    break

def update_property_by_path(data, path, new_value):
    obj, key = get_object_by_path(data, path[:-1]), path[-1]
    if obj is not None and isinstance(obj, dict):
        obj[key] = new_value

def print_json(data):
    print(obj_to_json(data))