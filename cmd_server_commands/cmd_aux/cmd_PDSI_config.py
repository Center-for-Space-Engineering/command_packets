'''
    Class for creating command packets from bytes in a file and sending those created packets to the pi
'''
import time

from commandParent import commandParent # pylint: disable=e0401
from command_packets.functions import ccsds_crc16 # pylint: disable=e0401
import system_constants # pylint: disable=e0401

#import DTO for communicating internally
from logging_system_display_python_api.DTOs.print_message_dto import print_message_dto # pylint: disable=e0401

class cmd_PDSI_config(commandParent):
    '''
        The init function goes to the cmd class and then populates its 
        self into its command dict so that it is dynamically added to the command repo
    '''
    def __init__(self, CMD, coms):
        # init the parent
        super().__init__(CMD, coms=coms, called_by_child=True)
        #CMD is the cmd class and we are using it to hold all the command class
        self.__commandName = 'command_PDSI_config'
        self.__args ={
            "pdsi_config" : self.pdsi_config
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
    def pdsi_config(self, args):
        '''
            creates a byte array for a pds config packet.
        '''
        file_path = "command_packets/packets/"

        PDSI_Bin0 = int(args[1])
        PDSI_Bin1 = int(args[2])
        PDSI_Bin2 = int(args[3])
        PDSI_Bin3 = int(args[4])
        PDSI_Bin4 = int(args[5])
        PDSI_Bin5 = int(args[6])
        PDSI_Bin6 = int(args[7])
        PDSI_Bin7 = int(args[8])
        PDSI_Bin8 = int(args[9])
        PDSI_Bin9 = int(args[10])
        PDSI_Bin10 = int(args[11])
        PDSI_Bin11= int(args[12])
        PDSI_Bin12 = int(args[13])
        PDSI_Bin13 = int(args[14])
        PDSI_Bin14 = int(args[15])
        PDSI_Bin15 = int(args[16])
        PDSI_DG = int(args[17])

        packet_apid = 0x051

        packet_version_number = system_constants.pvn
        packet_type = system_constants.pck_type
        secondary_header = system_constants.sec_header
        sequence_flags = system_constants.seq_flags
        packet_count = self.__packet_count
        packet_length = 34 # number of bytes after header
        # self.__packet_count += 1

        header_byte1 = ((packet_version_number & system_constants.mask_pvn) << 5) | ((packet_type & system_constants.mask_pck_type) << 4) | ((secondary_header & system_constants.mask_sec_header) << 3) | ((packet_apid & system_constants.mask_APID_1) >> 8)
        header_byte2 = packet_apid & system_constants.mask_APID_2
        header_byte3 = ((sequence_flags & system_constants.mask_seq_flags) << 6) | ((packet_count & system_constants.mask_packet_count_1) >> 8)
        header_byte4 = packet_count & system_constants.mask_packet_count_2
        header_byte5 = (packet_length & system_constants.mask_packet_len_1) >> 8
        header_byte6 = packet_length & system_constants.mask_packet_len_2

        header = bytearray([header_byte1, header_byte2, header_byte3, header_byte4, header_byte5, header_byte6])

        PDSI_Bin0_bytes  = PDSI_Bin0.to_bytes(2, 'big')
        PDSI_Bin1_bytes  = PDSI_Bin1.to_bytes(2, 'big')
        PDSI_Bin2_bytes  = PDSI_Bin2.to_bytes(2, 'big')
        PDSI_Bin3_bytes  = PDSI_Bin3.to_bytes(2, 'big')
        PDSI_Bin4_bytes  = PDSI_Bin4.to_bytes(2, 'big')
        PDSI_Bin5_bytes  = PDSI_Bin5.to_bytes(2, 'big')
        PDSI_Bin6_bytes  = PDSI_Bin6.to_bytes(2, 'big')
        PDSI_Bin7_bytes  = PDSI_Bin7.to_bytes(2, 'big')
        PDSI_Bin8_bytes  = PDSI_Bin8.to_bytes(2, 'big')
        PDSI_Bin9_bytes  = PDSI_Bin9.to_bytes(2, 'big')
        PDSI_Bin10_bytes = PDSI_Bin10.to_bytes(2, 'big')
        PDSI_Bin11_bytes = PDSI_Bin11.to_bytes(2, 'big')
        PDSI_Bin12_bytes = PDSI_Bin12.to_bytes(2, 'big')
        PDSI_Bin13_bytes = PDSI_Bin13.to_bytes(2, 'big')
        PDSI_Bin14_bytes = PDSI_Bin14.to_bytes(2, 'big')
        PDSI_Bin15_bytes = PDSI_Bin15.to_bytes(2, 'big')
        
        PDSI_DG_bytes = PDSI_DG.to_bytes(1, 'big')
        
        bytes_for_crc = header +  PDSI_Bin0_bytes + PDSI_Bin1_bytes + PDSI_Bin2_bytes \
            + PDSI_Bin3_bytes + PDSI_Bin4_bytes + PDSI_Bin5_bytes + PDSI_Bin6_bytes \
            + PDSI_Bin7_bytes + PDSI_Bin8_bytes + PDSI_Bin9_bytes + PDSI_Bin10_bytes \
            + PDSI_Bin11_bytes + PDSI_Bin12_bytes + PDSI_Bin13_bytes + PDSI_Bin14_bytes \
            + PDSI_Bin15_bytes +  PDSI_DG_bytes

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
        dto = print_message_dto("Ran pdsi_config")
        self.__coms.print_message(dto, 2)
        return f"<p>ran command pdsi_config with args {str(args)}</p><p>{formatted_bytes}</p> " + return_val
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
            if key == 'pdsi_config':
                message.append({ 
                'Name' : key,
                'Path' : f'/{self.__commandName}/{key}/-PDSI_Bin0_bytes-/-PDSI_Bin1_bytes-/-PDSI_Bin2_bytes-/-PDSI_Bin3_bytes-/-PDSI_Bin4_bytes-/-PDSI_Bin5_bytes-/-PDSI_Bin6_bytes-/-PDSI_Bin7_bytes-/-PDSI_Bin8_bytes-/-PDSI_Bin9_bytes-/-PDSI_Bin10_bytes-/-PDSI_Bin11_bytes-/-PDSI_Bin12_bytes-/-PDSI_Bin13_bytes-/-PDSI_Bin14_bytes-/-PDSI_Bin15_bytes-/-PDSI_DG-',
                'Description' : 'Configures the 16 bin sizes and digital gain for PDSI'    
                })
        
        return message