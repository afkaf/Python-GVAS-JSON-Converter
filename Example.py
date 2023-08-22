from SavConverter import sav_to_json, read_sav

properties = read_sav('ExampleSavFiles/SaveSlot.sav')

output = sav_to_json(properties)

with open('output.json', 'w') as json_file:
    json_file.write(output)