'''
    Class for creating command packets from bytes in a file and sending those created packets to the pi
'''
import time

from commandParent import commandParent # pylint: disable=e0401
from command_packets.functions import ccsds_crc16 # pylint: disable=e0401
from command_packets.cmd_server_commands.cmd_aux import aux_constants as system_constants # pylint: disable=e0401

#import DTO for communicating internally
from logging_system_display_python_api.DTOs.print_message_dto import print_message_dto # pylint: disable=e0401

class cmd_command_from_file_aux(commandParent):
    '''
        The init function goes to the cmd class and then populates its 
        self into its command dict so that it is dynamically added to the command repo
    '''
    def __init__(self, CMD, coms):
        # init the parent
        super().__init__(CMD, coms=coms, called_by_child=True)
        #CMD is the cmd class and we are using it to hold all the command class
        self.__commandName = 'command_from_file_aux'
        self.__args ={
            "create_packet_aux" : self.create_packet_aux,
            "send_packet_aux" : self.send_packet_aux,
            "create_and_send_packet_aux" : self.create_and_send_packet_aux,
            "send_mode_packet_aux" : self.send_mode_packet_aux,
            "send_idle_packet_aux" : self.send_idle_packet_aux,
            "request_status_packet_aux" : self.request_status_packet_aux
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
    def create_packet_aux(self, args):
        '''
            creates a byte array for a packet given a byte array with the packet contents and an APID.
        '''
        file_path = "command_packets/packets/"

        bytes_filename = file_path + args[1] + ".bin"
        packet_apid = int(args[2])

        #Import bytearray from file
        try:
            with open(bytes_filename, 'rb') as file:
                data = file.read()
            byte_data = bytearray(data)
        except FileNotFoundError:
            return f"Error: File '{bytes_filename}' not found."
        except IOError:
            return f"Error: Unable to read file '{bytes_filename}'."

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = len(byte_data) + 1 #Has to be the total number of data bytes (not including crc) plus one for ccsds standard ¯\_(ツ)_/¯
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        bytes_for_crc = header + byte_data

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

        self.__packet_bytes = packet_bytes

        formatted_bytes = [f'\\x{byte:02x}' for byte in packet_bytes]
        formatted_bytes =  ''.join(formatted_bytes)


        # print("ran create_packets")
        dto = print_message_dto("Ran create_packet")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command create_packet with args {str(args)}</p><p>{formatted_bytes}</p>"
    def send_packet_aux(self, _):
        '''
            Sends the created packet to a binary file.
        '''
        # serial_writer = system_constants.swp_board_writer
        # request_id = self.__coms.send_request(serial_writer, ["write_to_serial_port_bytes", self.__packet_bytes])
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
        
        dto = print_message_dto("Ran send_packet")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command send_packet</p><p>{return_val}</p>"
    
    def create_and_send_packet_aux(self, args):
        '''
            creates and sends a byte array for a packet given a byte array with the packet contents and an APID.
        '''
        file_path = "command_packets/packets/"

        bytes_filename = file_path + args[1] + ".bin"
        packet_apid = int(args[2])

        #Import bytearray from file
        try:
            with open(bytes_filename, 'rb') as file:
                data = file.read()
            byte_data = bytearray(data)
        except FileNotFoundError:
            return f"Error: File '{bytes_filename}' not found."
        except IOError:
            return f"Error: Unable to read file '{bytes_filename}'."

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = len(byte_data) + 1 #Has to be the total number of data bytes (not including crc) plus one for ccsds standard ¯\_(ツ)_/¯
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        bytes_for_crc = header + byte_data

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

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
            bin_file.write(packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran create_and_send_packet")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command create_and_send_packet with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def send_mode_packet_aux(self, args):
        '''
            sends a mode packet with the mode given by the 16 bits in args[1].
        '''

        packet_apid = system_constants.APID_Mode #0x24
        byte_data = int(args[1], 16)
        byte_data = byte_data.to_bytes(1, byteorder='big')

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = len(byte_data) + 1 #Has to be the total number of data bytes (not including crc) plus one for ccsds standard ¯\_(ツ)_/¯

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        bytes_for_crc = header + byte_data

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

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
            bin_file.write(packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran send_mode_packet")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command end_mode_packet with args {str(args)}</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def send_idle_packet_aux(self, _):
        '''
            sends an idle packet.
        '''

        packet_apid = system_constants.APID_Idle # 0x22
        byte_data = 0
        byte_data = byte_data.to_bytes(1, byteorder='big')

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = len(byte_data) + 1 #Has to be the total number of data bytes (not including crc) plus one for ccsds standard ¯\_(ツ)_/¯
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        bytes_for_crc = header + byte_data

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

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
            bin_file.write(packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran send_idle_packet")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command send_idle_packet</p><p>{formatted_bytes}</p><p>{return_val}</p>"
    
    def request_status_packet_aux(self, _):
        '''
            requests an status packet.
        '''

        packet_apid = system_constants.APID_Stat # 0x23
        byte_data = 0
        byte_data = byte_data.to_bytes(1, byteorder='big')

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = len(byte_data) + 1 #Has to be the total number of data bytes (not including crc) plus one for ccsds standard ¯\_(ツ)_/¯
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        bytes_for_crc = header + byte_data

        crc = ccsds_crc16(data=bytes_for_crc)
        
        crc_bytes = crc.to_bytes(2, byteorder='big')

        packet_bytes = bytes_for_crc + crc_bytes

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
            bin_file.write(packet_bytes)
            return_val = "successful"
        except Exception as e:
            return_val = str(e)

        # print("ran create_packets")
        dto = print_message_dto("Ran request_status_packet")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command request_status_packet</p><p>{formatted_bytes}</p><p>{return_val}</p>"

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
            if key == 'create_packet_aux':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-filename-/-APID-',
                'Description' : 'Creates a packet header and crc for bytes in file'    
                })
            elif key == 'send_packet_aux':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/',
                'Description' : 'Saves the created packet as packet_data.bin'    
                })
            elif key == 'create_and_send_packet_aux':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-filename-/-APID-',
                'Description' : 'Runs both create and send packet'    
                })
            elif key == 'send_mode_packet_aux':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-bytes[hex]-',
                'Description' : 'Saves a mode packet with given bytes as packet_data.bin'    
                })
            elif key == 'send_idle_packet_aux':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/',
                'Description' : 'Saves an idle packet as packet_data.bin'    
                })
            elif key == 'request_status_packet_aux':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/',
                'Description' : 'Saves a status request packet as packet_data.bin'    
                })
        return message
