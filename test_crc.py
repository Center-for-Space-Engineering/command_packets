from functions import ccsds_crc16

byte_array = bytearray([65, 66, 67, 68])  # ASCII values for 'A', 'B', 'C', 'D'
# byte_array = bytearray([1, 2, 3, 4])  
print(byte_array)

crc = ccsds_crc16(data=byte_array)
print(hex(crc))
