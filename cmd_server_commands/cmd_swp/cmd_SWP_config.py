'''
    Class for creating command packets from bytes in a file and sending those created packets to the pi
'''
import time

from commandParent import commandParent # pylint: disable=e0401
from command_packets.functions import ccsds_crc16 # pylint: disable=e0401
from command_packets.cmd_server_commands.cmd_swp import swp_constants as system_constants # pylint: disable=e0401

#import DTO for communicating internally
from logging_system_display_python_api.DTOs.print_message_dto import print_message_dto # pylint: disable=e0401

class cmd_SWP_config(commandParent):
    '''
        The init function goes to the cmd class and then populates its 
        self into its command dict so that it is dynamically added to the command repo
    '''
    def __init__(self, CMD, coms):
        # init the parent
        super().__init__(CMD, coms=coms, called_by_child=True)
        #CMD is the cmd class and we are using it to hold all the command class
        self.__commandName = 'command_SWP_config'
        self.__args ={
            "manSIP" : self.manSIP,
            "manSLP" : self.manSLP,
            "cfgFPP" : self.cfgFPP,
            "cfgFBP" : self.cfgFBP,
            "cfgSLP" : self.cfgSLP,
            # "cfgSIP" : self.cfgSIP,
            "cfgTIP" : self.cfgTIP,
            "cfgQIP" : self.cfgQIP
        }
        dictCmd = CMD.get_command_dict()
        dictCmd[self.__commandName] = self #this is the name the web server will see, so to call the command send a request for this command. 
        CMD.setCommandDict(dictCmd)
        self.__coms = coms
        self.__packet_count = 0
        self.__packet_bytes = b''

    def run(self):
        '''
            Runs a call from the server, with no args!
        '''
        print("Ran command")
        dto  = print_message_dto("Ran command")
        self.__coms.print_message(dto, 2) 
        return f"<p>ran command {self.__commandName}<p>"
    def run_args(self, args):
        '''
            This function is what allows the server to call function in this class
            ARGS:
                [0] : function name
                [1:] ARGS that the function needs. NOTE: can be blank
        '''
        # print(f"ran command {str(args[0])} with args {str(args[1:])}")
        message = ""
        try:
            message = self.__args[args[0]](args)
            dto = print_message_dto(message)
            self.__coms.print_message(dto, 2)
        except Exception as e: # pylint: disable=w0718
            message += f"<p> Not valid arg Error {e}</p>"
        return message
    def manSIP(self, args):
        '''
            creates a byte array for a sip calibration config packet.
        '''
        file_path = "command_packets/packets/"

        manual_mode = int(args[1])
        NCO_step = int(args[2])
        NCO_frequency = int(args[3])
        coarse_delay = int(args[4])
        amplitude = int(args[5])
        fine_delay = int(args[6])

        packet_apid = 0x027

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 13+1 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        if(manual_mode == 0):
            manual_mode_byte = 0x00
        else:
            manual_mode_byte = 0xFF
        
        manual_mode_byte = bytearray([manual_mode_byte])

        NCO_step_bytes = NCO_step.to_bytes(2, 'big')
        
        NCO_frequency_bytes = NCO_frequency.to_bytes(3, 'big')
        
        coarse_delay_bytes = coarse_delay.to_bytes(1, 'big')

        amplitude_bytes = amplitude.to_bytes(2, 'big')

        fine_delay_bytes = fine_delay.to_bytes(4, 'big')

        bytes_for_crc = header + manual_mode_byte + NCO_step_bytes + NCO_frequency_bytes + coarse_delay_bytes + amplitude_bytes + fine_delay_bytes

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)

        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
        # return_val = self.__coms.get_return(serial_writer, request_id)

        # while return_val is None:
        #     time.sleep(0.001)
        #     return_val = self.__coms.get_return(serial_writer, request_id)
        # self.__packet_count += 1

        try:
            bin_file = open("packet_data.bin", 'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran manSIP")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command manSIP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def manSLP(self, args):
        '''
            creates a byte array for a slp calibration config packet.
        '''
        file_path = "command_packets/packets/"

        manual_mode = int(args[1])
        DAC_word = int(args[2])
        Manual_step = int(args[3])
        Gain_Select = int(args[4])

        packet_apid = 0x026
        # packet_apid = system_constants.APID_manSLP

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 7 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        
        manual_mode_byte = bytearray([manual_mode])

        DAC_word_bytes = DAC_word.to_bytes(2, 'big')
        
        Manual_step_bytes = Manual_step.to_bytes(2, 'big')
        
        Gain_Select_bytes = Gain_Select.to_bytes(1, 'big')

        bytes_for_crc = header + manual_mode_byte + DAC_word_bytes + Manual_step_bytes + Gain_Select_bytes

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)

        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
        # return_val = self.__coms.get_return(serial_writer, request_id)

        # while return_val is None:
        #     time.sleep(0.001)
        #     return_val = self.__coms.get_return(serial_writer, request_id)
        # self.__packet_count += 1

        try:
            bin_file = open("packet_data.bin", 'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran manSLP")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command manSLP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def cfgFPP(self, args):
        '''
            creates a byte array for a fpp config packet.
        '''
        file_path = "command_packets/packets/"

        digital_gain = int(args[1])

        packet_apid = 0x02B

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 8 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])
        
        digital_gain_bytes = digital_gain.to_bytes(1, 'big')

        bytes_for_crc = header + digital_gain_bytes

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)

        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
        # return_val = self.__coms.get_return(serial_writer, request_id)

        # while return_val is None:
        #     time.sleep(0.001)
        #     return_val = self.__coms.get_return(serial_writer, request_id)
        # self.__packet_count += 1

        try:
            bin_file = open("packet_data.bin", 'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran cfgFPP")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command cfgFPP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def cfgFBP(self, args):
        '''
            creates a byte array for a fbp config packet.
        '''
        file_path = "command_packets/packets/"

        digital_gain = int(args[1])
        DAC_word = int(args[2])

        # packet_apid = 0x028
        packet_apid = system_constants.APID_cfgFBP

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 4 #length of the FBP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])
        
        digital_gain_bytes = digital_gain.to_bytes(1, 'big')
        
        DAC_word_bytes = DAC_word.to_bytes(2, 'big')

        bytes_for_crc = header + digital_gain_bytes + DAC_word_bytes

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)

        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
        # return_val = self.__coms.get_return(serial_writer, request_id)

        # while return_val is None:
        #     time.sleep(0.001)
        #     return_val = self.__coms.get_return(serial_writer, request_id)
        # self.__packet_count += 1

        try:
            bin_file = open("packet_data.bin", 'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran cfgFBP")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command cfgFBP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def cfgSLP(self, args):
        '''
            creates a byte array for a slp config packet.
        '''
        file_path = "command_packets/packets/"

        slp_rate = int(args[1])

        packet_apid = 0x029

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 8 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])
        
        slp_rate_bytes = slp_rate.to_bytes(1, 'big')

        bytes_for_crc = header + slp_rate_bytes

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)

        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
        # return_val = self.__coms.get_return(serial_writer, request_id)

        # while return_val is None:
        #     time.sleep(0.001)
        #     return_val = self.__coms.get_return(serial_writer, request_id)
        # self.__packet_count += 1

        try:
            bin_file = open("packet_data.bin", 'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran cfgSLP")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command cfgSLP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
        
    # def cfgSIP(self, args):
    #     '''
    #         creates a byte array for a sip config packet.
    #     '''
    #     file_path = "command_packets/packets/"

    #     sip_sweep_rate = int(args[1])
    #     lip_sweep_rate = int(args[2])

    #     packet_apid = 0x030

    #     packet_version_number = system_constants.pvn
    #     packet_type = system_constants.pck_type
    #     secondary_header = system_constants.sec_header
    #     sequence_flags = system_constants.seq_flags
    #     packet_count = self.__packet_count
    #     packet_length = 8 #length of the SIP config packet
    #     # self.__packet_count += 1

    #     header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
    #     header_byte2 = packet_apid & system_constants.mask_APID_2
    #     header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
    #     header_byte4 = packet_count & system_constants.mask_packet_count_2
    #     header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
    #     header_byte6 = packet_length & system_constants.mask_packet_len_2

    #     header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])
        
    #     sip_sweep_rate_bytes = sip_sweep_rate.to_bytes(1, 'big')
        
    #     lip_sweep_rate_bytes = lip_sweep_rate.to_bytes(1, 'big')

    #     bytes_for_crc = header + sip_sweep_rate_bytes + lip_sweep_rate_bytes

    #     crc = ccsds_crc16(data=bytes_for_crc)
        
    #     crc_bytes = crc.to_bytes(2, byteorder='big')

    #     packet_bytes = bytes_for_crc + crc_bytes

    #     self.__packet_bytes = packet_bytes

    #     formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
    #     formatted_bytes =  ''.join(formatted_bytes)

    #     # serial_writer = system_constants.swp_board_writer
    #     # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
    #     # return_val = self.__coms.get_return(serial_writer, request_id)

    #     # while return_val is None:
    #     #     time.sleep(0.001)
    #     #     return_val = self.__coms.get_return(serial_writer, request_id)
    #     # self.__packet_count += 1

        # try:
        #     bin_file = open("packet_data.bin", 'wb+')
        #     bin_file.write(self.__packet_bytes)
        #     return_val = "successful"
        # except Exception as e:
        #     return_val = str(e)

        # # print("ran create_packets")
        # dto = print_message_dto("Ran cfgSIP")
        # self.__coms.print_message(dto, 2)
        # return f"<p>ran command cfgSIP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def cfgTIP(self, args):
        '''
            creates a byte array for a tip config packet.
        '''
        file_path = "command_packets/packets/"

        freq_lim1 = int(args[1])
        freq_lim2 = int(args[2])
        freq_init = int(args[3])
        freq_gain1 = int(args[4])
        freq_gain2 = int(args[5])

        packet_apid = 0x031

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 8 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])
        
        freq_lim1_bytes = freq_lim1.to_bytes(3, 'big')
        freq_lim2_bytes = freq_lim2.to_bytes(3, 'big')
        freq_init_bytes = freq_init.to_bytes(3, 'big')
        freq_gain1_bytes = freq_gain1.to_bytes(4, 'big')
        freq_gain2_bytes = freq_gain2.to_bytes(4, 'big')

        bytes_for_crc = header + freq_lim1_bytes + freq_lim2_bytes + freq_init_bytes + freq_gain1_bytes + freq_gain2_bytes

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)

        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
        # return_val = self.__coms.get_return(serial_writer, request_id)

        # while return_val is None:
        #     time.sleep(0.001)
        #     return_val = self.__coms.get_return(serial_writer, request_id)
        # self.__packet_count += 1

        try:
            bin_file = open("packet_data.bin", 'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran cfgTIP")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command cfgTIP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"

    def cfgQIP(self, args):
        '''
            creates a byte array for a qip config packet.
        '''
        file_path = "command_packets/packets/"

        qip_rate = int(args[1])

        packet_apid = 0x032

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 8 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])
        
        qip_rate_bytes = qip_rate.to_bytes(1, 'big')

        bytes_for_crc = header + qip_rate_bytes

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)

        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", packet_bytes])
        # return_val = self.__coms.get_return(serial_writer, request_id)

        # while return_val is None:
        #     time.sleep(0.001)
        #     return_val = self.__coms.get_return(serial_writer, request_id)
        # self.__packet_count += 1

        try:
            bin_file = open("packet_data.bin", 'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran cfgQIP")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command cfgQIP with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"

    def get_args(self):
        '''
            This function returns an html obj that explains the args for all the internal
            function calls. 
        '''
        message = ""
        for key in self.__args:
            message += f"<url>/{self.__commandName}/{key}</url><p></p>" #NOTE: by adding the url tag, the client knows this is a something it can call, the <p></p> is basically a new line for html
        return message

    def __str__(self):
        return self.__commandName
    def get_args_server(self):
        '''
            This function returns an html obj that explains the args for all the internal
            function calls. 
        '''
        message = []
        for key in self.__args:
            if key == 'manSIP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-manual mode-/-NCO step-/-NCO frequency-/-coarse delay-/-amplitude-/fine delay-',
                'Description' : 'Creates an sip calibration config packet and saves it as packet_data.bin'    
                })
            if key == 'manSLP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-manual mode-/-DAC word-/-manual step-/-gain select-',
                'Description' : 'Creates an slp calibration config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgFPP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-Digital Gain-',
                'Description' : 'Creates an fpp config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgFBP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-Digital Gain-/-DAC word-',
                'Description' : 'Creates an fbp config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgSLP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-SLP_Rate-',
                'Description' : 'Creates an slp config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgFLP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-FLP_Rate-',
                'Description' : 'Creates an flp config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgPDS':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-PDS_Bins-/-PDS_DG-',
                'Description' : 'Creates an pds config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgEFS1':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-EFS1_Bins-/-EFS1_DG-',
                'Description' : 'Creates an efs1 config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgEFS2':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-EFS2_Bins-/-EFS2_DG-',
                'Description' : 'Creates an efs2 config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgSIP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-SIP sweep rate-/-LIP sweep rate-',
                'Description' : 'Creates an sip config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgTIP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-freq limit 1-/-freq limit 2-/-initial freq-/-TIP gain 1-/-TIP gain 2-',
                'Description' : 'Creates an tip config packet and saves it as packet_data.bin'    
                })
            if key == 'cfgQIP':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-QIP rate-',
                'Description' : 'Creates an qip config packet and saves it as packet_data.bin'    
                })
        return message
