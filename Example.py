# imports to conver between .sav and .json
from SavConverter import sav_to_json, read_sav, json_to_sav
# imports to navigate and manipulate the json structure
from SavConverter import load_json, obj_to_json, print_json, get_object_by_path, insert_object_by_path, replace_object_by_path, update_property_by_path

# The following lines are an example of the .sav to .json conversion process
# Get .sav property classes
properties = read_sav('ExampleSavFiles/SaveSlot_without_AutoSave.sav')

# Convert properties to json
output = sav_to_json(properties, string = True)

# Write json string to file
with open('SaveSlot.json', 'w') as json_file:
    json_file.write(output)



# The following lines are an example of the traversal and manipulation of this specific .json structure using paths
# load your converted json file
data = load_json('SaveSlot.json')

# path to the first Weapon object (0) in the list of Weapon objects ('value') in the RankedWeapons object ({"name": "RankedWeapons"})
path_to_find = [{"name": "RankedWeapons"}, "value", 0]

# Full path to the value ('value') in Rank object ({'name':'Rank'}) within that first weapon object
path_to_update = [{"name": "RankedWeapons"}, "value", 0, {'name':'Rank'}, 'value']

# new value for the 'value' key in the Rank object
new_value = 'ECrabRank::Gold'

# find and display the first weapon object
obj = get_object_by_path(data, path_to_find)
print("Found first Weapon object:")
print_json(obj)

# update the value property of the Rank object
update_property_by_path(data, path_to_update, new_value)
print("\nUpdated Rank object value:")
print_json(get_object_by_path(data, path_to_find))

# same path for will be used to show object replacement
path_to_replace = [{"name": "RankedWeapons"}, "value", 0, {'name': 'Rank'}]

# new Rank object
new_object = {
    "type": "EnumProperty",
    "name": "Rank",
    "enum": "ECrabRank",
    "value": "ECrabRank::Bronze"
}

# replace the rank object with the new one
replace_object_by_path(data, path_to_replace, new_object)
print("\nReplaced Rank object:")
print_json(get_object_by_path(data, path_to_find))

# Check if SaveSlot has an AutoSave object and insert test AutoSave if not
path_to_autosave = [{'name': 'AutoSave'}]
autosave = get_object_by_path(data, path_to_autosave)
if autosave == None:
    print('\nNo AutoSave object found. Inserting AutoSave.')

    # path of object to insert new object before or after
    path_to_insert = [{"type": "FileEndProperty"}]

    # Reading in previously extracted AutoSave object
    autosave = load_json('ExampleSavFiles/AutoSave.json')

    # insert AutoSave object before FileEndProperty object
    insert_object_by_path(data, path_to_insert, autosave, position='before')
    if get_object_by_path(data, path_to_autosave) != None:
        print("\nFound inserted AutoSave.")



# The following lines show the process of converting the edited .json back to .sav
# Converting json string back to binary
binary_data = json_to_sav(obj_to_json(data))

# write new .sav file converted from .json
with open('NewSaveSlot.sav', 'wb') as file:
        # Write the binary data to the file
        file.write(binary_data)