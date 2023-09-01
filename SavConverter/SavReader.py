from .SavProperties import *
from struct import pack, unpack
from datetime import datetime

class SavReader:
    def __init__(self, file_array_buffer = None):
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

    def read_int64(self):
        value = unpack('<q', self.file_array_buffer[self.offset:self.offset + 8])[0]
        self.offset += 8
        return value

    def read_string(self):
        length = self.read_int32()
        raw_bytes = self.file_array_buffer[self.offset:self.offset + length - 1] # Exclude the null terminator
        result = raw_bytes.decode('utf-8')
        self.offset += length
        return result
    
    def read_string_special(self):
        length = self.read_int32()
        wide = False
        encoding = "utf-8"
        null = 1
        if length < 0:
            length = abs(length)*2
            wide = True
            encoding = 'utf-16-le'
            null = 2
        raw_bytes = self.file_array_buffer[self.offset:self.offset + length - null] # Exclude the null terminator
        result = raw_bytes.decode(encoding)
        self.offset += length
        return result, wide

    def read_boolean(self):
        result = bool(self.file_array_buffer[self.offset])
        self.offset += 1
        return result

    def read_date_time(self):
        ticks = int.from_bytes(self.file_array_buffer[self.offset:self.offset + 8], 'little')
        self.offset += 8
        try:
            calculated_time = datetime.utcfromtimestamp((ticks // 10000 - 62135596800000) / 1000.0)
        except:
            calculated_time = ticks
        return calculated_time

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
        elif property_type == "Int64Property":
            return Int64Property(property_name, self)
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
        elif property_type == "SetProperty":
            return SetProperty(property_name, self)
        elif property_type == "ArrayProperty":
            return ArrayProperty(property_name, self)
        elif property_type == "ObjectProperty":
            return ObjectProperty(property_name, self)
        elif property_type == "SoftObjectProperty":
            return SoftObjectProperty(property_name, self)
        elif property_type == "MulticastInlineDelegateProperty":
            return MulticastInlineDelegateProperty(property_name, self)
        elif property_type == "MapProperty":
            return MapProperty(property_name, self)
        else:
            raise Exception(f"Unknown property type: {property_type}")

    def read_whole_buffer(self):
        output = []
        try:
            header_property = HeaderProperty(self)
        except:
            raise Exception('Failed to read HeaderProperty due to invalid or obfuscated GVAS .sav format.\nPlease provide a path to a valid uncompressed Unreal Engine GVAS .sav file.')
        output.append(header_property)

        while not self.has_finished():
            next_property = self.read_property()
            output.append(next_property)
        return output

def read_sav(file_path):
    if file_path[-4:] != '.sav':
        raise ValueError("Please provide a path to a valid Unreal Engine GVAS .sav file.")
    with open(file_path, 'rb') as f:
        file = f.read()
    sav_reader = SavReader(file)
    properties = sav_reader.read_whole_buffer()
    return properties