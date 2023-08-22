from struct import pack

def write_int16(value):
    return pack('<h', value)

def write_int32(value):
    return pack('<i', value)

def write_uint32(value):
    return pack('<I', value)

def write_float32(value):
    return pack('<f', value)

from datetime import datetime

def write_string(string):
    string_size = write_uint32(len(string) + 1)
    string_array = string.encode()
    return bytes([*string_size, *string_array, 0x00])

def write_date_time(date_time_string):
    date = datetime.fromisoformat(date_time_string)
    ticks = int(date.timestamp() * 10000) + 621355968000000000
    return pack('<Q', ticks)

def write_bytes(hex_string):
    return bytes.fromhex(hex_string)