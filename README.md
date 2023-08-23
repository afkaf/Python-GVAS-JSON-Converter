---

# Python-GVAS-JSON-Converter

Python-GVAS-JSON-Converter is a library designed to convert Unreal Engine's Game Variable and Attribute System (GVAS) files between `.sav` and `.json` formats. It provides a way to read and interpret the binary structure of `.sav` files and translate them into human-readable JSON format, as well as convert JSON back to the original `.sav` format.

## Features

- **Convert from .sav to .json**: Supports converting Unreal Engine's `.sav` files into `.json` format.
- **Convert from .json to .sav**: Includes the ability to convert `.json` files back to the original `.sav` format.
- **JSON Editing Functions**: Offers a range of functions to navigate, manipulate, and modify JSON structures with ease.
- **Tested Games**: The conversion has been tested with Crab Champions, and it may work for other games as well.
- **Actively Developed**: This project is actively being developed, with new features and improvements being added.

## Warning

- **Untested .sav Files**: Some classes in [SavProperties.py](SavConverter/SavProperties.py) may not function correctly with untested `.sav` files, and certain [SavReader.py](SavConverter/SavReader.py) code segments may be broken for untested datatypes. While the library has been designed with flexibility in mind, full compatibility with all `.sav` files cannot be guaranteed at this stage. Efforts will continue to progressively test other games' `.sav` files and refine the code accordingly.

## Using the Conversion Functions

The conversion functions provide an easy way to translate between Unreal Engine's `.sav` and `.json` formats.

### Converting from .sav to .json

1. **Read .sav**: Use `read_sav` to get the property instances from the `.sav` file.
2. **Convert to JSON**: Use `sav_to_json` to convert properties to a JSON string.
3. **Write to File**: Write the JSON string output to a `.json` file.

### Converting from .json to .sav

1. **Load JSON**: Use `load_json` to read a JSON file.
2. **Convert to Binary**: Use `json_to_sav` to convert JSON to binary data.
3. **Write to File**: Write the binary data to a `.sav` file.

## Using JSON Editing Functions

The JSON editing functions allow users to manipulate the JSON structure using paths, providing functions like:

- **Finding Objects**: Using `get_object_by_path`, you can locate objects in JSON by specifying the path.
- **Inserting Objects**: With `insert_object_by_path`, you can add new objects to specified locations.
- **Replacing Objects**: `replace_object_by_path` enables object replacement at a specified path.
- **Updating Properties**: Use `update_property_by_path` to modify specific keys within an object.

### Understanding the Path Structure

- `path`: A list that describes the path to the object you're looking for. Each element in the list can be:
- **A dictionary**, to match a specific key-value pair.
- **A string**, to reference a key.
- **An integer**, to reference an index in a list.

For example:
```python
path_to_find = [{"name": "RankedWeapons"}, "value", 0]
```

---
