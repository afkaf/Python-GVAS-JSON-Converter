from .SavProperties import *
import json

# commented code is for making sure the output binary matches the original during testing of new .sav types
# with open('ExampleSavFiles/SaveSlot.sav','rb') as f:
#     original = f.read()

def json_to_sav(data):
    if isinstance(data, str):
        data = json.loads(data)
    output = bytearray()
    last = 0
    for obj in data:
        property_instance = assign_prototype(obj)
        bytestring = property_instance.to_bytes()
        output.extend(bytestring)
        # if not original[last:len(output)] == bytestring:
        #     print(original[last:len(output)], '\n', bytestring)
        #     quit()
        # last += len(bytestring)

    return bytes(output)
