from .SavProperties import *
import json

def json_to_sav(json_string):
    properties = json.loads(json_string)
    output = bytearray()
    last = 0
    for raw_property in properties:
        property_instance = assign_prototype(raw_property)
        bytestring = property_instance.to_bytes()
        test = bytestring == test_file[last:len(bytestring)+last]
        last += len(bytestring)
        if not test:
            quit()
        output.extend(bytestring)

    return bytes(output)
