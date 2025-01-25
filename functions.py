'''
    This modules contains function to help us procerss packets.
'''
def ccsds_crc16(data : bytearray):
    '''
        Make crc16/CCITT-FALSE check sum for the CCSDS packet.
    '''
    if data is None:
        return 0
    crc = 0xFFFF
    poly = 0x1021


    for byte in data:
        crc ^= byte << 8
        for _ in range(0,8):
            if crc & 0x8000:
                crc = (crc << 1) ^ poly
            else:
                crc = crc << 1
    return crc & 0xFFFF

def FBP_calibrated_dac_code(voltage : float):
    '''
        Converts desired voltage to a calibrated DAC word for the FBP
    '''
    FBP_Gain = 8009.947863209321
    FBP_offset = 32772.41705613722
    calibrated_dac_code = int(round(voltage*FBP_Gain + FBP_offset,0))
    calibrated_dac_code = max(0,min(calibrated_dac_code,(2**(16))-1))
    
    return calibrated_dac_code

def SLP_calibrated_dac_code(voltage : float):
    '''
        Converts desired voltage to a calibrated SLP word for the FBP
    '''
    SLP_Gain = 8007.254939956971
    SLP_offset = 32767.59380278144
    calibrated_dac_code = int(round(voltage*SLP_Gain + SLP_offset,0))
    calibrated_dac_code = max(0,min(calibrated_dac_code,(2**(16))-1))

    return calibrated_dac_code
