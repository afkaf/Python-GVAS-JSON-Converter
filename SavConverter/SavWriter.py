from struct import pack
from datetime import datetime

def write_int16(value):
    return pack('<h', value)

def write_int32(value):
    return pack('<i', value)

def write_uint32(value):
    return pack('<I', value)

def write_float32(value):
    return pack('<f', value)

def write_int64(value):
    return pack('<q', value)

def write_string(string, wide = False):
    if string == '':
        return bytes([0x00,0x00,0x00,0x00])
    null = 1
    length = len(string) + 1
    encoding = 'utf-8'
    if wide:
        null = 2
        length = -length
        encoding = 'utf-16-le'
    string_size = write_int32(length)
    string_array = string.encode(encoding)
    return bytes([*string_size, *string_array] + [0x00]*null)

def write_date_time(date_time_string):
    if isinstance(date_time_string, int):
        ticks = date_time_string
    else:
        dt_object = datetime.strptime(date_time_string, '%Y-%m-%d %H:%M:%S.%f')
        timestamp_ms = int((dt_object - datetime(1970, 1, 1)).total_seconds() * 1000)
        ticks = (timestamp_ms + 62135596800000) * 10000    
    return pack('<Q', ticks)

def write_bytes(hex_string):
    return bytes.fromhex(hex_string)

def write_int_bytes(x):
    if x == 0:
        return b'\x00'
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')
