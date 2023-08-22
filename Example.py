from SavConverter import sav_to_json, SavReader

def read_sav(path):
    with open(path, 'rb') as f:
        file = f.read()
    sav_reader = SavReader(file)
    properties = sav_reader.read_whole_buffer()
    return properties

output = sav_to_json(read_sav('ExampleSavFiles/SaveSlot.sav'))

with open('output.json', 'w') as json_file:
    json_file.write(output)