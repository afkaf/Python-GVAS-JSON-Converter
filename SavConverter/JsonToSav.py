from .SavProperties import *
import json

# with open('ExampleSavFiles/SaveSlot.sav','rb') as f:
#     original = f.read()

def json_to_sav(json_string):
    properties = json.loads(json_string)
    output = bytearray()
    last = 0
    for raw_property in properties:
        property_instance = assign_prototype(raw_property)
        bytestring = property_instance.to_bytes()
        output.extend(bytestring)
        # if not original[last:len(output)] == bytestring:
        #     print(original[last:len(output)], '\n', bytestring)
        #     quit()
        # last += len(bytestring)

    return bytes(output)
