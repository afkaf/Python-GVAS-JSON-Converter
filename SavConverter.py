from struct import pack, unpack
import json


class SavReader:
    def __init__(self, file_array_buffer):
        self.offset = 0
        self.file_array_buffer = file_array_buffer
        self.file_size = len(file_array_buffer)

    def has_finished(self):
        return self.offset == self.file_size

    def read_bytes(self, count):
        result = self.file_array_buffer[self.offset:self.offset + count]
        self.offset += count
        return result

    def read_int16(self):
        value = unpack('<h', self.file_array_buffer[self.offset:self.offset + 2])[0]
        self.offset += 2
        return value
    
    def read_int32(self):
        value = unpack('<i', self.file_array_buffer[self.offset:self.offset + 4])[0]
        self.offset += 4
        return value

    def read_uint32(self):
        value = unpack('<I', self.file_array_buffer[self.offset:self.offset + 4])[0]
        self.offset += 4
        return value
    
    def read_float32(self):
        value = unpack('<f', self.file_array_buffer[self.offset:self.offset + 4])[0]
        self.offset += 4
        return value
    
    def read_string(self):
        length = sav_reader.read_int32()
        raw_bytes = self.file_array_buffer[self.offset:self.offset + length - 1] # Exclude the null terminator
        # print(f"Reading string, raw bytes: {raw_bytes if len(raw_bytes) <= 250 else raw_bytes[:250]+b'...(Output Continues)'}")  # Debug print
        result = raw_bytes.decode("utf-8")
        self.offset += length
        return result



    def read_boolean(self):
        result = bool(self.file_array_buffer[self.offset])
        self.offset += 1
        return result

    def read_date_time(self):
        ticks, _ = read_uint32(self.file_array_buffer[self.offset:self.offset + 8], 0)
        self.offset += 8
        return datetime.datetime.utcfromtimestamp(ticks / 10000000 - 62135596800)


    def read_property(self):

        if self.offset + len(FileEndProperty.bytes) == len(self.file_array_buffer):
            assumed_file_end = self.file_array_buffer[self.offset:self.offset + len(FileEndProperty.bytes)]

            if assumed_file_end == FileEndProperty.bytes:
                self.offset += len(FileEndProperty.bytes)
                return FileEndProperty()

    
        property_name = self.read_string()
        if property_name == "None":
            return NoneProperty()

        # Read property type
        property_type = self.read_string()
        # print(f"Reading property: {property_name}, type: {property_type}")
        
        if property_type == "HeaderProperty":
            return HeaderProperty(property_name, self)
        elif property_type == "BoolProperty":
            return BoolProperty(property_name, self)
        elif property_type == "IntProperty":
            return IntProperty(property_name, self)
        elif property_type == "UInt32Property":
            return UInt32Property(property_name, self)
        elif property_type == "FloatProperty":
            return FloatProperty(property_name, self)
        elif property_type == "EnumProperty":
            return EnumProperty(property_name, self)
        elif property_type == "StructProperty":
            return StructProperty(property_name, self)
        elif property_type == "ByteProperty":
            return ByteProperty(property_name, self)
        elif property_type == "StrProperty":
            return StrProperty(property_name, self)
        elif property_type == "NameProperty":
            return NameProperty(property_name, self)
        elif property_type == "ArrayProperty":
            return ArrayProperty(property_name, self)
        elif property_type == "ObjectProperty":
            return ObjectProperty(property_name, self)
        else:
            raise Exception(f"Unknown property type: {property_type}")

    def read_whole_buffer(self):
        output = []
        header_property = HeaderProperty(self)
        output.append(header_property)

        while not self.has_finished():
            next_property = self.read_property()
            output.append(next_property)

        return output


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

    def to_bytes(self):
        return write_string(self.name) + write_string(self.type) + IntProperty.padding + write_int32(self.value)


class UInt32Property:
    padding = bytes([0x04] + [0x00] * 8)
    type = "UInt32Property"

    def __init__(self, name, sav_reader):
        self.type = "UInt32Property"
        self.name = name
        sav_reader.read_bytes(len(UInt32Property.padding))
        self.value = sav_reader.read_uint32()

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
        self.value = sav_reader.read_string()

    def to_bytes(self):
        return (write_string(self.name) + write_string(self.type) + write_bytes(self.unknown) +
                StrProperty.padding + write_string(self.value))


class NameProperty:
    padding = bytes([0x00] * 8)
    type = "NameProperty"

    def __init__(self, name, sav_reader):
        self.type = "NameProperty"
        self.name = name
        self.unknown = sav_reader.read_bytes(1)
        sav_reader.read_bytes(len(NameProperty.padding))
        self.value = sav_reader.read_string()

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
            self.value = sav_reader.read_bytes(content_size)

    def to_bytes(self):
        result = write_string(self.name) + write_string(self.type) + write_uint32(len(self.value) * 16)
        result += ByteProperty.padding + write_string(self.subtype) + bytes([0x00])
        if self.subtype == "StructProperty":
            if self.generic_type == "Guid":
                for value in self.value:
                    result += write_bytes(value)
            else:
                for struct_element_instance in self.value:
                    for struct_element_instance_child_property in struct_element_instance:
                        result += struct_element_instance_child_property.to_bytes()
        return bytes(result)


class EnumProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00])
    type = "EnumProperty"

    def __init__(self, name, sav_reader):
        self.type = "EnumProperty"
        self.name = name
        content_size = sav_reader.read_uint32()
        sav_reader.read_bytes(len(EnumProperty.padding))
        self.subtype = sav_reader.read_string()
        sav_reader.read_bytes(1)
        self.value = sav_reader.read_string()

    def to_bytes(self):
        result = write_string(self.name) + write_string(self.type) + write_uint32(len(self.value))
        result += EnumProperty.padding + write_string(self.subtype) + bytes([0x00]) + write_string(self.value)
        return bytes(result)


class FloatProperty:
    padding = bytes([0x04] + [0x00] * 8)
    type = "FloatProperty"

    def __init__(self, name, sav_reader):
        self.type = "FloatProperty"
        self.name = name
        sav_reader.read_bytes(len(FloatProperty.padding))
        self.value = sav_reader.read_float32()

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

        self.value = []
        while sav_reader.offset < content_end_position:
            self.value.append(sav_reader.read_property())

    def to_bytes(self):
        if self.subtype == "Guid":
            return (write_string(self.name) + write_string(self.type) + write_uint32(16) +
                    StructProperty.padding + write_string("Guid") + StructProperty.unknown +
                    write_bytes(self.value))

        if self.subtype == "DateTime":
            return (write_string(self.name) + write_string(self.type) + write_uint32(8) +
                    StructProperty.padding + write_string("DateTime") + StructProperty.unknown +
                    write_date_time(self.value))

        content_bytes = bytearray()
        for value in self.value:
            if isinstance(value, list):
                for item in value:
                    assign_prototype(item)
                    content_bytes += item.to_bytes()
            else:
                assign_prototype(value)
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
        else:
            self.value = sav_reader.read_bytes(content_size)

    def to_bytes(self):
        if self.subtype == "StructProperty":
            content_count = len(self.value)
            byte_array_content = bytearray()
            for value in self.value:
                if isinstance(value, list):
                    for item in value:
                        assign_prototype(item)
                        byte_array_content += item.to_bytes()
                else:
                    assign_prototype(value)
                    byte_array_content += value.to_bytes()

            content_size = (4 + 4 + len(self.name) + 1 + 4 + len(self.subtype) + 1 + 4 +
                            len(ArrayProperty.padding) + 4 + len(self.generic_type) + 1 +
                            len(ArrayProperty.unknown) + len(byte_array_content))

            return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                    ArrayProperty.padding + write_string(self.subtype) + bytes([0x00]) +
                    write_uint32(content_count) + write_string(self.name) + write_string(self.subtype) +
                    write_uint32(len(byte_array_content)) + ArrayProperty.padding +
                    write_string(self.generic_type) + ArrayProperty.unknown + byte_array_content)

        content_size = len(self.value) // 2
        return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                ArrayProperty.padding + write_string(self.subtype) + bytes([0x00]) + write_bytes(self.value))


class MulticastInlineDelegateProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00, 0x00])
    unknown = bytes([0x01, 0x00, 0x00, 0x00])
    type = "MulticastInlineDelegateProperty"

    def __init__(self, name, sav_reader):
        self.name = name
        sav_reader.read_uint32()  # contentSize
        sav_reader.read_bytes(len(MulticastInlineDelegateProperty.padding))
        sav_reader.read_bytes(len(MulticastInlineDelegateProperty.unknown))
        self.object_name = sav_reader.read_string()
        self.function_name = sav_reader.read_string()

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
        sav_reader.read_uint32()  # contentSize
        sav_reader.read_bytes(len(MapProperty.padding))
        self.key_type = sav_reader.read_string()
        self.value_type = sav_reader.read_string()
        sav_reader.read_bytes(1)
        temp_map = {}
        sav_reader.read_bytes(len(MapProperty.padding))
        content_count = sav_reader.read_uint32()

        for _ in range(content_count):
            current_key = None
            current_value = None

            if self.key_type == "StructProperty":
                current_key = sav_reader.read_bytes(16)
            elif self.key_type == "IntProperty":
                current_key = sav_reader.read_int32()
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
            elif self.value_type == "BoolProperty":
                current_value = bool(sav_reader.read_bytes(1)[0])
            else:
                raise Exception(f"Value Type not implemented: {self.value_type}")

            temp_map[current_key] = current_value

        self.value = temp_map

    def to_bytes(self):
        byte_array_content = bytearray()
        for current_key, current_value in self.value.items():
            if self.key_type == "StructProperty":
                byte_array_content += write_bytes(current_key)
            elif self.key_type == "IntProperty":
                byte_array_content += write_int32(current_key)
            else:
                raise Exception(f"Key Type not implemented: {self.key_type}")

            if self.value_type == "StructProperty":
                for item in current_value:
                    assign_prototype(item)
                    byte_array_content += item.to_bytes()
            elif self.value_type == "IntProperty":
                byte_array_content += write_int32(current_value)
            elif self.value_type == "FloatProperty":
                byte_array_content += write_float32(current_value)
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
        content_size = sav_reader.read_uint32()
        sav_reader.read_bytes(len(SetProperty.padding))
        self.subtype = sav_reader.read_string()
        sav_reader.read_bytes(1)

        if self.subtype == "StructProperty":
            sav_reader.read_bytes(len(SetProperty.padding))
            content_count = sav_reader.read_uint32()
            self.value = [sav_reader.read_bytes(16) for _ in range(content_count)]
        else:
            self.value = sav_reader.read_bytes(content_size)

    def to_bytes(self):
        if self.subtype == "StructProperty":
            content_count = len(self.value)
            byte_array_content = bytearray()
            for value in self.value:
                byte_array_content += write_bytes(value)
            return (write_string(self.name) + write_string(self.type) + write_uint32(4 + 4 + len(byte_array_content)) +
                    SetProperty.padding + write_string(self.subtype) + bytes([0x00]) +
                    SetProperty.padding + write_uint32(content_count) + byte_array_content)

        return (write_string(self.name) + write_string(self.type) + write_uint32(len(self.value) // 2) +
                SetProperty.padding + write_string(self.subtype) + bytes([0x00]) + write_bytes(self.value))


class ObjectProperty:
    padding = bytes([0x00, 0x00, 0x00, 0x00, 0x00])
    type = "ObjectProperty"

    def __init__(self, name, sav_reader):
        self.type = "ObjectProperty"
        self.name = name
        sav_reader.read_uint32()  # contentSize
        sav_reader.read_bytes(len(ObjectProperty.padding))
        self.value = sav_reader.read_string()

    def to_bytes(self):
        content_size = 4 + len(self.value) + 1
        return (write_string(self.name) + write_string(self.type) + write_uint32(content_size) +
                ObjectProperty.padding + write_string(self.value))


class FileEndProperty:
    def __init__(self):
        self.type = "FileEndProperty"

    bytes = NoneProperty.bytes + bytes([0x00, 0x00, 0x00, 0x00])
    type = "FileEndProperty"

    @staticmethod
    def to_bytes():
        return FileEndProperty.bytes


file_path = 'SaveSlot.sav'
with open(file_path, 'rb') as file:
    sav_file_content = file.read()

sav_reader = SavReader(sav_file_content)

properties = sav_reader.read_whole_buffer()

def to_json_structure(obj):
    if isinstance(obj, (int, float, str, bool, type(None))):
        return obj
    if isinstance(obj, list):
        return [to_json_structure(item) for item in obj]
    if isinstance(obj, tuple):
        return [to_json_structure(item) for item in obj]
    if isinstance(obj, dict):
        return {key: to_json_structure(value) for key, value in obj.items()}
    if isinstance(obj, bytes):
        return obj.hex()

    # Check if the object has a __dict__ attribute
    if hasattr(obj, '__dict__'):
        return {key: to_json_structure(value) for key, value in vars(obj).items()}

    # Handle other cases (e.g., built-in types)
    return str(obj)

json_structure = []
for prop in properties:
    json_structure.append(to_json_structure(prop))

json_string = json.dumps(json_structure, indent=2)

# Save to a file
with open('output.json', 'w') as json_file:
    json_file.write(json_string)