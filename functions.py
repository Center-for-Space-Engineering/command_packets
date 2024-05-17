def ccsds_crc16(data : bytearray):
    '''
        Make crc16/CCITT-FALSE check sum for the CCSDS packet.
    '''
    if data is None:
        return 0
    crc = 0xFFFF
    poly = 0x1021


    for byte in data:
        # print(hex(crc & 0xFFFF))
        crc ^= byte << 8
        for _ in range(0,8):
            if (crc & 0x8000):
                crc = (crc << 1) ^ poly
            else:
                crc = crc << 1
    return crc & 0xFFFF 