'''
    Class for creating command packets from bytes in a file and sending those created packets to the pi
'''
import time

from commandParent import commandParent # pylint: disable=e0401
from command_packets.functions import ccsds_crc16 # pylint: disable=e0401
from command_packets.cmd_server_commands.cmd_aux import aux_constants as system_constants # pylint: disable=e0401

#import DTO for communicating internally
from logging_system_display_python_api.DTOs.print_message_dto import print_message_dto # pylint: disable=e0401

class cmd_AOP_config(commandParent):
    '''
        The init function goes to the cmd class and then populates its 
        self into its command dict so that it is dynamically added to the command repo
    '''
    def __init__(self, CMD, coms):
        # init the parent
        super().__init__(CMD, coms=coms, called_by_child=True)
        #CMD is the cmd class and we are using it to hold all the command class
        self.__commandName = 'command_AOPDAC_config'
        self.__args ={
            "AOPDAC_config" : self.AOPDAC_config,
            "AOPPI_config" : self.AOPPI_config,
            "AOPT_config" : self.AOPT_config,
            "AOPGS_config" : self.AOPGS_config
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
    def AOPDAC_config(self, args):
        '''
            creates a byte array for a AOPDAC config packet.
        '''

        AOP1_DAC = int(args[1])
        AOP2_DAC = int(args[2])
        RIC_DAC = int(args[3])

        packet_apid = 0x04C

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

        AOP1_DAC_bytes = AOP1_DAC.to_bytes(2, 'big')
        
        AOP2_DAC_bytes = AOP2_DAC.to_bytes(2, 'big')

        RIC_DAC_bytes = RIC_DAC.to_bytes(2, 'big')
        
        bytes_for_crc = header + AOP1_DAC_bytes + AOP2_DAC_bytes + RIC_DAC_bytes

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
            bin_file = open("packet_data.bin",  'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran AOPDAC_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command AOPDAC_config with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def AOPPI_config(self, args):
        '''
            creates a byte array for a AOPPI config packet.
        '''
        
        AOP_P = int(args[1])
        AOP_I = int(args[2])

        packet_apid = 0x04D

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

        AOP_P_bytes = AOP_P.to_bytes(3, 'big')
        
        AOP_I_bytes = AOP_I.to_bytes(3, 'big')
        
        bytes_for_crc = header + AOP_P_bytes + AOP_I_bytes

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
            bin_file = open("packet_data.bin",  'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran AOPPI_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command AOPPI_config with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def AOPT_config(self, args):
        '''
            creates a byte array for a AOPT config packet.
        '''
        
        AOP_T = int(args[1])
        AOP_Heater_en = int(args[2])

        packet_apid = 0x04E

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 4 # number of bytes after header
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        AOP_T_bytes = AOP_T.to_bytes(2, 'big')
        AOP_Heater_en = AOP_Heater_en.to_bytes(1, 'big')
        
        bytes_for_crc = header + AOP_T_bytes + AOP_Heater_en

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
            bin_file = open("packet_data.bin",  'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran AOPT_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command AOPT_config with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def AOPGS_config(self, args):
        '''
            creates a byte array for an AOPGS config packet.
        '''

        AOP1_GS = int(args[1])
        AOP2_GS = int(args[2])

        packet_apid = 0x053

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

        AOP1_GS_bytes = AOP1_GS.to_bytes(1, 'big')
        
        AOP2_GS_bytes = AOP2_GS.to_bytes(1, 'big')
        
        bytes_for_crc = header + AOP1_GS_bytes + AOP2_GS_bytes

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
            bin_file = open("packet_data.bin",  'wb+')
            bin_file.write(self.__packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran AOPGS_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command AOPGS_config with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
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
            if key == 'AOPDAC_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-AOP1_DAC-/-AOP2_DAC-/-RIC_DAC-',
                'Description' : 'Configures DAC outputs for AOP1, AOP2, RIC'    
                })
            if key == 'AOPPI_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-AOP_P-/-AOP_I-',
                'Description' : 'Configures PI constants on PI controller'    
                })
            if key == 'AOPT_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-AOP_T-/-AOP_Heater_EN-',
                'Description' : 'Configures word for desired temp for PI controller'    
                })
            if key == 'AOPGS_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-AOP1_GS-/-AOP2_GS-',
                'Description' : 'Configures the gain select bits for AOP1 and AOP2'    
                })
        return message