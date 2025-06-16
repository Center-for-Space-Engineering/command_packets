'''
    This file contains all the constants that the whole system needs. 
'''
interface_listener_list = []
interface_writer_list = []
sensors_config = {}

swp_board_writer = ""

# Command packet constants
APID_pps = 0x021
APID_Idle = 0x047 #Aux
APID_Stat = 0x048 #Aux
APID_Mode = 0x049 #Aux

pvn = 0
pck_type = 1
sec_header = 0
seq_flags = 3

mask_pvn = 0b111
mask_pck_type = 0b1
mask_sec_header = 0b1
mask_APID_1 = 0b11100000000
mask_APID_2 = 0b00011111111
mask_seq_flags = 0b11
mask_packet_count_1 = 0b11111100000000
mask_packet_count_2 = 0b00000011111111
mask_packet_len_1 = 0xFF00
mask_packet_len_2 = 0x00FF