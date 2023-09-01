from .SavWriter import *
print
def assign_prototype(raw_property):
    property_type = raw_property["type"]
    property_mapping = {
        "HeaderProperty": HeaderProperty,
        "NoneProperty": NoneProperty,
        "BoolProperty": BoolProperty,
        "IntProperty": IntProperty,
        "Int64Property": Int64Property,
        "UInt32Property": UInt32Property,
        "StrProperty": StrProperty,
        "NameProperty": NameProperty,
        "ByteProperty": ByteProperty,
        "EnumProperty": EnumProperty,
        "FloatProperty": FloatProperty,
        "StructProperty": StructProperty,
        "ArrayProperty": ArrayProperty,
        "MulticastInlineDelegateProperty": MulticastInlineDelegateProperty,
        "MapProperty": MapProperty,
        "SetProperty": SetProperty,
        "ObjectProperty": ObjectProperty,
        "SoftObjectProperty": SoftObjectProperty,
        "FileEndProperty": FileEndProperty
    }
    
    if property_type in property_mapping:
        return property_mapping[property_type].from_json(raw_property) # Call the from_json method
    else:
        raise Exception(f"Unknown property type: {property_type}")

class HeaderProperty:
    GVAS = bytes([0x47, 0x56, 0x41, 0x53])
    type = "HeaderProperty"

    def __init__(self, sav_reader):
        self.type = "HeaderProperty"
        sav_reader.read_bytes(len(HeaderProperty.GVAS))
        self.save_game_version = sav_reader.read_int32()
        self.package_version = sav_reader.read_int32()
        engine_version_parts = [sav_reader.read_int16() for _ in range(3)]
        self.engine_version = ".".join(map(str, engine_version_parts))
        self.engine_build = sav_reader.read_uint32()
        self.engine_branch = sav_reader.read_string()
        self.custom_version_format = sav_reader.read_int32()
        number_of_custom_versions = sav_reader.read_int32()
        self.custom_versions = [
            (sav_reader.read_bytes(16), sav_reader.read_int32())
            for _ in range(number_of_custom_versions)
        ]
        self.save_game_class_name = sav_reader.read_string()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        result_array = bytearray(HeaderProperty.GVAS)
        result_array += write_int32(self.save_game_version)
        result_array += write_int32(self.package_version)
        result_array += write_int16(int(self.engine_version.split(".")[0]))
        result_array += write_int16(int(self.engine_version.split(".")[1]))
        result_array += write_int16(int(self.engine_version.split(".")[2]))
        result_array += write_uint32(self.engine_build)
        result_array += write_string(self.engine_branch)
        result_array += write_int32(self.custom_version_format)
        result_array += write_int32(len(self.custom_versions))
        for version in self.custom_versions:
            result_array += write_bytes(version[0])
            result_array += write_int32(version[1])
        result_array += write_string(self.save_game_class_name)
        return bytes(result_array)

class NoneProperty:
    def __init__(self):
        self.type = "NoneProperty"
    
    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    bytes = bytes([0x05, 0x00, 0x00, 0x00, 0x4E, 0x6F, 0x6E, 0x65, 0x00])
    type = "NoneProperty"

    def to_bytes(self):
        return NoneProperty.bytes


class BoolProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    type = "BoolProperty"

    def __init__(self, name, sav_reader):
        self.type = "BoolProperty"
        self.name = name
        sav_reader.read_bytes(len(BoolProperty.padding))
        self.value = sav_reader.read_boolean()
        sav_reader.read_bytes(1)

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        result = bytearray(write_string(self.name))
        result += write_string(self.type)
        result += BoolProperty.padding
        result.append(0x01 if self.value else 0x00)
        result.append(0x00)
        return bytes(result)


class IntProperty:
    padding = bytes([0x04] + [0x00] * 8)
    type = "IntProperty"

    def __init__(self, name, sav_reader):
        self.type = "IntProperty"
        self.name = name
        sav_reader.read_bytes(len(IntProperty.padding))
        self.value = sav_reader.read_int32()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return write_string(self.name) + write_string(self.type) + IntProperty.padding + write_int32(self.value)


class Int64Property:
    padding = bytes([0x08] + [0x00] * 8)
    type = "Int64Property"

    def __init__(self, name, sav_reader):
        self.type = "Int64Property"
        self.name = name
        sav_reader.read_bytes(len(Int64Property.padding))
        self.value = sav_reader.read_int64()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls)  # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict)  # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return write_string(self.name) + write_string(self.type) + Int64Property.padding + write_int64(self.value)  # Assuming write_int64 writes an int64 to bytes


class UInt32Property:
    padding = bytes([0x04] + [0x00] * 8)
    type = "UInt32Property"

    def __init__(self, name, sav_reader):
        self.type = "UInt32Property"
        self.name = name
        sav_reader.read_bytes(len(UInt32Property.padding))
        self.value = sav_reader.read_uint32()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return write_string(self.name) + write_string(self.type) + UInt32Property.padding + write_uint32(self.value)


class StrProperty:
    padding = bytes([0x00] * 8)
    type = "StrProperty"

    def __init__(self, name, sav_reader):
        self.type = "StrProperty"
        self.name = name
        self.unknown = sav_reader.read_bytes(1)
        sav_reader.read_bytes(len(StrProperty.padding))
        self.value, iswide = sav_reader.read_string_special()
        if iswide:
            self.wide = True
    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return (write_string(self.name) + write_string(self.type) + write_bytes(self.unknown) +
            StrProperty.padding + write_string(self.value, self.wide if hasattr(self, 'wide') else False))


class NameProperty:
    padding = bytes([0x00] * 8)
    type = "NameProperty"

    def __init__(self, name, sav_reader):
        self.type = "NameProperty"
        self.name = name
        self.unknown = sav_reader.read_bytes(1)
        sav_reader.read_bytes(len(NameProperty.padding))
        self.value = sav_reader.read_string()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return (write_string(self.name) + write_string(self.type) + write_bytes(self.unknown) +
                NameProperty.padding + write_string(self.value))


class ByteProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00])
    unknown = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    type = "ByteProperty"

    def __init__(self, name, sav_reader):
        self.type = "ByteProperty"
        self.name = name
        content_size = sav_reader.read_uint32()
        sav_reader.read_bytes(4)
        self.subtype = sav_reader.read_string()
        # print(self.subtype)
        sav_reader.read_bytes(1)

        if self.subtype == "StructProperty":
            content_count = sav_reader.read_uint32()
            name_again = sav_reader.read_string()
            if name_again != self.name:
                raise Exception()
            subtype_again = sav_reader.read_string()
            if subtype_again != self.subtype:
                raise Exception()
            sav_reader.read_uint32()
            sav_reader.read_bytes(len(ByteProperty.padding))
            self.generic_type = sav_reader.read_string()
            unknown = sav_reader.read_bytes(17)
            if unknown != ByteProperty.unknown:
                raise Exception()
            self.value = []
            if self.generic_type == "Guid":
                for _ in range(content_count):
                    self.value.append(sav_reader.read_bytes(16))
            else:
                for _ in range(content_count):
                    struct_element_instance = []
                    struct_element_instance_child_property = None
                    while not isinstance(struct_element_instance_child_property, NoneProperty):
                        struct_element_instance_child_property = sav_reader.read_property()
                        struct_element_instance.append(struct_element_instance_child_property)
                    self.value.append(struct_element_instance)
        else:
            self.value = int.from_bytes(sav_reader.read_bytes(content_size), 'big')

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        if self.subtype == "StructProperty":
            content_count = len(self.value)
            byte_array_content = bytearray()
            
            if self.generic_type == "Guid":
                for value in self.value:
                    byte_array_content += write_bytes(value)
            else:
                for value in self.value:
                    if isinstance(value, list):
                        for child_value in value:
                            child_value = assign_prototype(child_value)
                            byte_array_content += child_value.to_bytes()
                    else:
                        value = assign_prototype(value)
                        byte_array_content += value.to_bytes()
            
            content_size = (
                4 + 4 + len(self.name) + 1
                + 4 + len(self.subtype) + 1
                + 4 + len(ByteProperty.padding)
                + 4 + len(self.generic_type) + 1
                + len(ByteProperty.unknown)
                + len(byte_array_content)
            )
            
            result = (
                write_string(self.name) + write_string(self.type) + write_uint32(content_size)
                + ByteProperty.padding + write_string(self.subtype) + bytes([0x00])
                + write_uint32(content_count) + write_string(self.name)
                + write_string(self.subtype) + write_uint32(len(byte_array_content))
                + ByteProperty.padding + write_string(self.generic_type)
                + ByteProperty.unknown + byte_array_content
            )
        else:
            content_size = (self.value.bit_length() + 7) // 8
            result = (
                write_string(self.name) + write_string(self.type) + write_uint32(content_size)
                + ByteProperty.padding + write_string(self.subtype) + bytes([0x00])
                + write_int_bytes(self.value)
            )

        return bytes(result)



class EnumProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00])
    type = "EnumProperty"

    def __init__(self, name, sav_reader):
        self.type = "EnumProperty"
        self.name = name
        content_size = sav_reader.read_uint32()
        sav_reader.read_bytes(len(EnumProperty.padding))
        self.enum = sav_reader.read_string()
        sav_reader.read_bytes(1)
        self.value = sav_reader.read_string()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        result = write_string(self.name) + write_string(self.type) + write_uint32(len(self.value)+5)
        result += EnumProperty.padding + write_string(self.enum) + bytes([0x00]) + write_string(self.value)
        return bytes(result)


class FloatProperty:
    padding = bytes([0x04] + [0x00] * 8)
    type = "FloatProperty"

    def __init__(self, name, sav_reader):
        self.type = "FloatProperty"
        self.name = name
        sav_reader.read_bytes(len(FloatProperty.padding))
        self.value = sav_reader.read_float32()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return write_string(self.name) + write_string(self.type) + FloatProperty.padding + write_float32(self.value)


class StructProperty:
    padding = bytes([0x00] * 4)
    unknown = bytes([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    type = "StructProperty"

    def __init__(self, name, sav_reader):
        self.type = "StructProperty"
        self.name = name
        content_size = sav_reader.read_uint32()
        sav_reader.read_bytes(4)
        self.subtype = sav_reader.read_string()
        sav_reader.read_bytes(17)
        content_end_position = sav_reader.offset + content_size
        if self.subtype == "Guid":
            self.value = sav_reader.read_bytes(16)
            return

        if self.subtype == "DateTime":
            self.value = sav_reader.read_date_time()
            return

        if self.subtype in ["Quat", "Vector", "Rotator"]:
            self.value = sav_reader.read_bytes(content_size)
            return

        self.value = []
        while sav_reader.offset < content_end_position:
            self.value.append(sav_reader.read_property())

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        if self.subtype == "Guid":
            return (write_string(self.name) + write_string(self.type) + write_uint32(16) +
                    StructProperty.padding + write_string("Guid") + StructProperty.unknown +
                    write_bytes(self.value))

        if self.subtype == "DateTime":
            return (write_string(self.name) + write_string(self.type) + write_uint32(8) +
                    StructProperty.padding + write_string("DateTime") + StructProperty.unknown +
                    write_date_time(self.value))

        if self.subtype in ["Quat", "Vector", "Rotator"]:
            return (write_string(self.name) + write_string(self.type) + write_uint32(len(self.value)//2) +
                    StructProperty.padding + write_string(self.subtype) + StructProperty.unknown +
                    write_bytes(self.value))

        content_bytes = bytearray()
        for value in self.value:
            if isinstance(value, list):
                for item in value:
                    item = assign_prototype(item)
                    content_bytes += item.to_bytes()
            else:
                value = assign_prototype(value)
                content_bytes += value.to_bytes()
        return (write_string(self.name) + write_string(self.type) + write_uint32(len(content_bytes)) +
                StructProperty.padding + write_string(self.subtype) + StructProperty.unknown +
                content_bytes)


class ArrayProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00])
    unknown = bytes([0x00] * 17)
    type = "ArrayProperty"

    def __init__(self, name, sav_reader):
        self.type = "ArrayProperty"
        self.name = name
        content_size = sav_reader.read_uint32()
        sav_reader.read_bytes(4)
        self.subtype = sav_reader.read_string()
        # print(self.subtype)
        sav_reader.read_bytes(1)

        if self.subtype == "StructProperty":
            content_count = sav_reader.read_uint32()
            name_again = sav_reader.read_string()
            if name_again != self.name:
                raise Exception()
            subtype_again = sav_reader.read_string()
            if subtype_again != self.subtype:
                raise Exception()
            sav_reader.read_uint32()  # arraySize
            sav_reader.read_bytes(len(ArrayProperty.padding))
            self.generic_type = sav_reader.read_string()
            unknown = sav_reader.read_bytes(17)
            if unknown != ArrayProperty.unknown:
                raise Exception()
            self.value = []

            if self.generic_type == "Guid":
                for _ in range(content_count):
                    self.value.append(sav_reader.read_bytes(16))
            else:
                for _ in range(content_count):
                    struct_element_instance = []
                    struct_element_instance_child_property = None
                    while not isinstance(struct_element_instance_child_property, NoneProperty):
                        struct_element_instance_child_property = sav_reader.read_property()
                        struct_element_instance.append(struct_element_instance_child_property)
                    self.value.append(struct_element_instance)
        elif self.subtype in ["ObjectProperty", "EnumProperty", "NameProperty", "StrProperty"]:
            # Read the number of ObjectProperty elements in the array
            content_count = sav_reader.read_uint32()
            self.value = [sav_reader.read_string() for _ in range(content_count)]
        else:
            self.value = sav_reader.read_bytes(content_size)

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        if self.subtype == "StructProperty":
            content_count = len(self.value)
            byte_array_content = bytearray()
            if self.generic_type == "Guid":
                for guid in self.value:
                    byte_array_content += bytes.fromhex(guid)
            else:
                for value in self.value:
                    if isinstance(value, list):
                        for item in value:
                            item = assign_prototype(item)
                            byte_array_content += item.to_bytes()
                    else:
                        value = assign_prototype(value)
                        byte_array_content += value.to_bytes()

            content_size = (4 + 4 + len(self.name) + 1 + 4 + len(self.subtype) + 1 + 4 +
                            len(ArrayProperty.padding) + 4 + len(self.generic_type) + 1 +
                            len(ArrayProperty.unknown) + len(byte_array_content))

            return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                    ArrayProperty.padding + write_string(self.subtype) + bytes([0x00]) +
                    write_uint32(content_count) + write_string(self.name) + write_string(self.subtype) +
                    write_uint32(len(byte_array_content)) + ArrayProperty.padding +
                    write_string(self.generic_type) + ArrayProperty.unknown + byte_array_content)
        elif self.subtype in ["ObjectProperty", "EnumProperty", "NameProperty", "StrProperty"]:
            content_count = len(self.value)
            byte_array_content = bytearray()
            for value in self.value:
                byte_array_content += write_string(value)

            content_size = len(byte_array_content) + 4
            return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                    ArrayProperty.padding + write_string(self.subtype) + bytes([0x00]) +
                    write_uint32(content_count) + byte_array_content)
        content_size = len(self.value) // 2
        return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                ArrayProperty.padding + write_string(self.subtype) + bytes([0x00]) + write_bytes(self.value))


class MulticastInlineDelegateProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00, 0x00])
    unknown = bytes([0x01, 0x00, 0x00, 0x00])
    type = "MulticastInlineDelegateProperty"

    def __init__(self, name, sav_reader):
        self.name = name
        self.type = "MulticastInlineDelegateProperty"
        sav_reader.read_uint32()  # contentSize
        sav_reader.read_bytes(len(MulticastInlineDelegateProperty.padding))
        sav_reader.read_bytes(len(MulticastInlineDelegateProperty.unknown))
        self.object_name = sav_reader.read_string()
        self.function_name = sav_reader.read_string()
    
    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        content_size = len(MulticastInlineDelegateProperty.unknown) + 4 + len(self.object_name) + 1 + 4 + len(self.function_name) + 1
        return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                MulticastInlineDelegateProperty.padding + MulticastInlineDelegateProperty.unknown +
                write_string(self.object_name) + write_string(self.function_name))


class MapProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00])
    type = "MapProperty"

    def __init__(self, name, sav_reader):
        self.name = name
        self.type = "MapProperty"
        sav_reader.read_uint32()  # contentSize
        sav_reader.read_bytes(len(MapProperty.padding))
        self.key_type = sav_reader.read_string()
        self.value_type = sav_reader.read_string()
        sav_reader.read_bytes(1)
        self.value = []
        sav_reader.read_bytes(len(MapProperty.padding))
        content_count = sav_reader.read_uint32()

        for _ in range(content_count):
            current_key = None
            current_value = None

            if self.key_type == "StructProperty":
                current_key = sav_reader.read_bytes(16)
            elif self.key_type == "IntProperty":
                current_key = sav_reader.read_int32()
            elif self.key_type in ["StrProperty","NameProperty"]:
                current_key = sav_reader.read_string()
            else:
                raise Exception(f"Key Type not implemented: {self.key_type}")

            if self.value_type == "StructProperty":
                current_value = []
                prop = None
                while not isinstance(prop, NoneProperty):
                    prop = sav_reader.read_property()
                    current_value.append(prop)
            elif self.value_type == "IntProperty":
                current_value = sav_reader.read_int32()
            elif self.value_type == "FloatProperty":
                current_value = sav_reader.read_float32()
            elif self.value_type in ["StrProperty", "EnumProperty"]:
                current_value = sav_reader.read_string()
            elif self.value_type == "BoolProperty":
                current_value = bool(sav_reader.read_bytes(1)[0])
            else:
                raise Exception(f"Value Type not implemented: {self.value_type}")

            self.value.append([current_key, current_value])

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        byte_array_content = bytearray()
        for current_key, current_value in self.value:
            if self.key_type == "StructProperty":
                byte_array_content += write_bytes(current_key)
            elif self.key_type == "IntProperty":
                byte_array_content += write_int32(current_key)
            elif self.key_type in ["StrProperty","NameProperty"]:
                byte_array_content += write_string(current_key)
            else:
                raise Exception(f"Key Type not implemented: {self.key_type}")

            if self.value_type == "StructProperty":
                for item in current_value:
                    item = assign_prototype(item)
                    byte_array_content += item.to_bytes()
            elif self.value_type == "IntProperty":
                byte_array_content += write_int32(current_value)
            elif self.value_type == "FloatProperty":
                byte_array_content += write_float32(current_value)
            elif self.value_type in ["StrProperty", "EnumProperty"]:
                byte_array_content += write_string(current_value)
            elif self.value_type == "BoolProperty":
                byte_array_content += bytes([0x01]) if current_value else bytes([0x00])
            else:
                raise Exception(f"Value Type not implemented: {self.value_type}")

        return (write_string(self.name) + write_string(self.type) + write_uint32(4 + 4 + len(byte_array_content)) +
                MapProperty.padding + write_string(self.key_type) + write_string(self.value_type) +
                MapProperty.padding + bytes([0x00]) + write_uint32(len(self.value)) + byte_array_content)


class SetProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00])
    type = "SetProperty"

    def __init__(self, name, sav_reader):
        self.name = name
        self.type = "SetProperty"
        content_size = sav_reader.read_uint32()
        sav_reader.read_bytes(len(SetProperty.padding))
        self.subtype = sav_reader.read_string()
        sav_reader.read_bytes(1)

        if self.subtype == "StructProperty":
            sav_reader.read_bytes(len(SetProperty.padding))
            content_count = sav_reader.read_uint32()
            self.value = [] #[sav_reader.read_property() for _ in range(content_count)]
            for _ in range(content_count):
                struct_element_instance = []
                struct_element_instance_child_property = None
                while not isinstance(struct_element_instance_child_property, NoneProperty):
                    struct_element_instance_child_property = sav_reader.read_property()
                    struct_element_instance.append(struct_element_instance_child_property)
                self.value.append(struct_element_instance)
        elif self.subtype == "NameProperty":
            sav_reader.read_bytes(4)
            content_count = sav_reader.read_uint32()
            self.value = [sav_reader.read_string() for _ in range(content_count)]
        else:
            self.value = sav_reader.read_bytes(content_size)

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        if self.subtype == "StructProperty":
            content_count = len(self.value)
            byte_array_content = bytearray()
            for value in self.value:
                    if isinstance(value, list):
                        for item in value:
                            item = assign_prototype(item)
                            byte_array_content += item.to_bytes()
                    else:
                        value = assign_prototype(value)
                        byte_array_content += value.to_bytes()
            content_size = 4 + 4 + len(byte_array_content)
            return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                SetProperty.padding + write_string(self.subtype) + bytes([0x00]) + SetProperty.padding + 
                write_uint32(content_count) + byte_array_content)
        elif self.subtype == "NameProperty":
            content_count = len(self.value)
            byte_array_content = bytearray()
            for value in self.value:
                byte_array_content += write_string(value)

            content_size = len(byte_array_content) + 8
            return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                    ArrayProperty.padding + write_string(self.subtype) + bytes([0x00,0x00,0x00,0x00,0x00]) +
                    write_uint32(content_count) + byte_array_content)
        return (write_string(self.name) + write_string(self.type) + write_uint32(len(self.value) // 2) +
                SetProperty.padding + write_string(self.subtype) + bytes([0x00]) + write_bytes(self.value))


class ObjectProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00, 0x00])
    type = "ObjectProperty"

    def __init__(self, name, sav_reader):
        self.type = "ObjectProperty"
        self.name = name
        content_size = sav_reader.read_uint32()  # contentSize
        sav_reader.read_bytes(len(ObjectProperty.padding))
        self.value = sav_reader.read_string()

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return (write_string(self.name) + write_string(self.type) + write_uint32(len(self.value) + 5) +
                ObjectProperty.padding + write_string(self.value))

class SoftObjectProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00, 0x00])
    type = "SoftObjectProperty"

    def __init__(self, name, sav_reader):
        self.type = "SoftObjectProperty"
        self.name = name
        content_size = sav_reader.read_uint32()  # contentSize
        sav_reader.read_bytes(len(SoftObjectProperty.padding))
        self.value = sav_reader.read_string()
        sav_reader.read_bytes(4)

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance

    def to_bytes(self):
        return (write_string(self.name) + write_string(self.type) + write_uint32(len(self.value) + 5 + 4) +
                SoftObjectProperty.padding + write_string(self.value)) + bytes([0x00, 0x00, 0x00, 0x00])

class FileEndProperty:
    def __init__(self):
        self.type = "FileEndProperty"

    @classmethod
    def from_json(cls, json_dict):
        instance = cls.__new__(cls) # Create a new instance without calling the constructor
        instance.__dict__.update(json_dict) # Update the instance attributes with the JSON dictionary
        return instance
    
    bytes = NoneProperty.bytes + bytes([0x00, 0x00, 0x00, 0x00])
    type = "FileEndProperty"

    @staticmethod
    def to_bytes():
        return FileEndProperty.bytes
