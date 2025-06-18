'''
    Class for creating command packets from bytes in a file and sending those created packets to the pi
'''
import time

from commandParent import commandParent # pylint: disable=e0401
from command_packets.functions import ccsds_crc16 # pylint: disable=e0401
from command_packets.cmd_server_commands.cmd_aux import aux_constants as system_constants # pylint: disable=e0401

#import DTO for communicating internally
from logging_system_display_python_api.DTOs.print_message_dto import print_message_dto # pylint: disable=e0401

class cmd_AUX_config(commandParent):
    '''
        The init function goes to the cmd class and then populates its 
        self into its command dict so that it is dynamically added to the command repo
    '''
    def __init__(self, CMD, coms):
        # init the parent
        super().__init__(CMD, coms=coms, called_by_child=True)
        #CMD is the cmd class and we are using it to hold all the command class
        self.__commandName = 'command_AUX_config'
        self.__args ={
            "PPS" : self.PPS,
            "REGA" : self.REGA,
            "TKA" : self.TKA
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
        dto = print_message_dto("Ran command")
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
    def PPS(self, args):
        '''
            creates a byte array for a PPS packet.
        '''

        PPS_W = int(args[1])
        PPS_M = int(args[2])

        packet_apid = 0x021

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 7 # number of bytes after header
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        PPS_W_bytes = PPS_W.to_bytes(2, 'big')
        
        PPS_M_bytes = PPS_M.to_bytes(4, 'big')
        
        bytes_for_crc = header + PPS_W_bytes + PPS_M_bytes

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
        dto = print_message_dto("Ran PPS")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command PPS with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def REGA(self, args):
        '''
            creates a byte array for a REGA packet.
        '''

        S_5VREG = int(args[1])

        packet_apid = 0x04A

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 7 # number of bytes after header
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        S_5VREG_bytes = S_5VREG.to_bytes(1, 'big')
        
        bytes_for_crc = header + S_5VREG_bytes

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
        dto = print_message_dto("Ran REGA")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command REGA with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def TKA(self, args):
        '''
            creates a byte array for a TKA packet.
        '''

        TK1_R1 = int(args[1])
        TK1_R2 = int(args[2])
        TK2_R1 = int(args[3])
        TK2_R2 = int(args[4])
        TK3_R1 = int(args[5])
        TK3_R2 = int(args[6])
        TK4_R1 = int(args[7])
        TK4_R2 = int(args[8])
        TK5_R1 = int(args[9])
        TK5_R2 = int(args[10])
        TK6_R1 = int(args[11])
        TK6_R2 = int(args[12])

        packet_apid = 0x04B

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 3 # number of bytes after header
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])
        
        TK1_R1_bytes = TK1_R1.to_bytes(1, 'big')
        TK1_R2_bytes = TK1_R2.to_bytes(1, 'big')
        TK2_R1_bytes = TK2_R1.to_bytes(1, 'big')
        TK2_R2_bytes = TK2_R2.to_bytes(1, 'big')
        TK3_R1_bytes = TK3_R1.to_bytes(1, 'big')
        TK3_R2_bytes = TK3_R2.to_bytes(1, 'big')
        TK4_R1_bytes = TK4_R1.to_bytes(1, 'big')
        TK4_R2_bytes = TK4_R2.to_bytes(1, 'big')
        TK5_R1_bytes = TK5_R1.to_bytes(1, 'big')
        TK5_R2_bytes = TK5_R2.to_bytes(1, 'big')
        TK6_R1_bytes = TK6_R1.to_bytes(1, 'big')
        TK6_R2_bytes = TK6_R2.to_bytes(1, 'big')
        
        bytes_for_crc = header + TK1_R1_bytes + TK1_R2_bytes + TK2_R1_bytes + TK2_R2_bytes + TK3_R1_bytes + TK3_R2_bytes + TK4_R1_bytes + TK4_R2_bytes + TK5_R1_bytes + TK5_R2_bytes + TK6_R1_bytes + TK6_R2_bytes

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
        dto = print_message_dto("Ran TKA")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command TKA with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
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
            if key == 'PPS':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-PPS_W-/-PPS_M-',
                'Description' : 'PPS Timing Packet'    
                })
            if key == 'REGA':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-S_5VREG-',
                'Description' : 'Turns on/off the 5V regulator to the thermal knives and hinges'    
                })
            if key == 'TKA':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-TK1_R1-/-TK1_R2-/-TK2_R1-/-TK2_R2-/-TK3_R1-/-TK3_R2-/-TK4_R1-/-TK4_R2-/-TK5_R1-/-TK5_R2-/-TK6_R1-/-TK6_R2-',
                'Description' : 'Turns on/off the thermal knife resistors (for hinge release)'    
                })
        return message