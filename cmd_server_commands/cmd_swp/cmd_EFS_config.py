'''
    Class for creating command packets from bytes in a file and sending those created packets to the pi
'''
import time

from commandParent import commandParent # pylint: disable=e0401
from command_packets.functions import ccsds_crc16 # pylint: disable=e0401
import system_constants # pylint: disable=e0401

#import DTO for communicating internally
from logging_system_display_python_api.DTOs.print_message_dto import print_message_dto # pylint: disable=e0401

class cmd_EFS_config(commandParent):
    '''
        The init function goes to the cmd class and then populates its 
        self into its command dict so that it is dynamically added to the command repo
    '''
    def __init__(self, CMD, coms):
        # init the parent
        super().__init__(CMD, coms=coms, called_by_child=True)
        #CMD is the cmd class and we are using it to hold all the command class
        self.__commandName = 'command_EFS_config'
        self.__args ={
            "EFS1_config" : self.EFS1_config,
            "EFS2_config" : self.EFS2_config,
            "EFS3_config" : self.EFS3_config
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
        try:
            message = self.__args[args[0]](args)
            dto = print_message_dto(message)
            self.__coms.print_message(dto, 2)
        except Exception as e: # pylint: disable=w0718
            message += f"<p> Not valid arg Error {e}</p>"
        return message
    

    def EFS1_config(self, args):
        '''
            creates a byte array for a EFS config packet.
        '''
        file_path = "command_packets/packets/"

        EFS1_Bins = int(args[1])
        EFS1_DG = int(args[2])

        packet_apid = 0x02C

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 34 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        EFS2_Bins_bytes = EFS1_Bins.to_bytes(32, 'big')
        
        EFS1_DG_bytes = EFS1_DG.to_bytes(1, 'big')
        
        bytes_for_crc = header + EFS1_DG_bytes + EFS2_Bins_bytes

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
            bin_file = open("host/packet_data.bin", 'a')
            bin_file.write(self.__packet_bytes)
            return_val = "successfully"
        except Exception :
            return_val = Exception        

        # print("ran create_packets")
        dto = print_message_dto("Ran EFS1_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command EFS1_config with args {str(args)}</p><p>{formatted_bytes}</p> " + return_val
    
    def EFS2_config(self, args):
        '''
            creates a byte array for a EFS config packet.
        '''
        file_path = "command_packets/packets/"

        EFS2_Bins = int(args[1])
        EFS2_DG = int(args[2])

        packet_apid = 0x02D

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 34 #length of the SIP config packet
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        EFS2_Bins_bytes = EFS2_Bins.to_bytes(32, 'big')
        
        EFS2_DG_bytes = EFS2_DG.to_bytes(1, 'big')
        
        bytes_for_crc = header + EFS2_DG_bytes + EFS2_Bins_bytes

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
            bin_file = open("host/packet_data.bin", 'a')
            bin_file.write(self.__packet_bytes)
            return_val = "successfully"
        except Exception :
            return_val = Exception

        # print("ran create_packets")
        dto = print_message_dto("Ran EFS2_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command EFS2_config with args {str(args)}</p><p>{formatted_bytes}</p> " + return_val
    
    def EFS3_config(self, args):
        '''
            creates a byte array for a EFS config packet.
        '''
        file_path = "command_packets/packets/"

        packet_apid = 0x033

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 1 # number of bytes after header
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        bytes_for_crc = header

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
            bin_file = open("host/packet_data.bin", 'a')
            bin_file.write(self.__packet_bytes)
            return_val = "successfully"
        except Exception :
            return_val = Exception

        # print("ran create_packets")
        dto = print_message_dto("Ran EFS3_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command EFS3_config with args {str(args)}</p><p>{formatted_bytes}</p> " + return_val

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
            if key == 'EFS1_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-EFS1_Bins-/-EFS1_DG-',
                'Description' : 'Configure First Electric Field Spectrometer V12 (EFS1) parameters'    
                })
            elif key == 'EFS2_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-EFS2_Bins-/-EFS2_DG-',
                'Description' : 'Configure Second Electric Field Spectrometer V34 (EFS2) parameters'    
                })
            elif key == 'EFS3_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/',
                'Description' : 'Configure Third Electric Field Spectrometer HF12 (EFS3) parameters'    
                })

        return message
