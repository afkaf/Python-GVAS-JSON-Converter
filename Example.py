from SavConverter import sav_to_json, read_sav, json_to_sav


# Get .sav property classes
properties = read_sav('ExampleSavFiles/SaveSlot.sav')

# Convert properties to json
output = sav_to_json(properties)

# Write json string to file
with open('SaveSlot.json', 'w') as json_file:
    json_file.write(output)


# Test converting json string back to binary
binary_data = json_to_sav(output)

# write new .sav file converted from .json
with open('NewSaveSlot.sav', 'wb') as file:
        # Write the binary data to the file
        file.write(binary_data)

# compare new .sav binary_data with original .sav binary data
with open('ExampleSavFiles/SaveSlot.sav', 'rb') as f:
    print(f.read() == binary_data)