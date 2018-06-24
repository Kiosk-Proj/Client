from enum import Enum
import socket

class DeviceType(Enum):
    KIOSK = 0
    TABLET = 1


class MessageType(Enum):
    FAIL = -1
    CONNECTION = 0
    INPUT = 1
    INPUT_RESPONSE = 2
    NUMBER_CONFIRM = 3
    TABLET_UPDATE = 4
    TABLET_CONFIRM = 5
    TABLET_CHANGE = 6
    ACK = 7


class Message:
    def __init__(self, messageType, transactionID, messageValue):
        self.messageType = messageType
        self.transactionID = transactionID
        if type(messageValue) == type(b''):
            self.messageValue = messageValue
        else:
            self.messageValue = messageValue.to_bytes((len(bin(messageValue))+5)//8, 'big')

    @staticmethod
    def pad(string, length, pad='0'):
        return pad*(length-len(string)) + string

    @staticmethod
    def chunk(string, chunk_size):
        return list((string[i:i + chunk_size] for i in range(0, len(string), chunk_size)))

    def get_binary(self):
        message_type_binary  = self.pad(bin(self.messageType.value)[2:], 32)
        transaction_id_binary = self.pad(bin(self.transactionID)[2:], 64)

        message_binary = [bin(i)[2:].rjust(8,'0') for i in self.messageValue]
        message_length = len(message_binary)
        message_binary = "".join(message_binary)
        message_length_binary = Message.pad(bin(message_length)[2:], 32, '0')

        full_message_bitstring = message_type_binary+transaction_id_binary+message_length_binary+message_binary
        bytes = b''
        for i in Message.chunk(full_message_bitstring, 8):
            bytes = bytes + int(i,2).to_bytes(1,'big')
        return bytes

    @staticmethod
    def message_from_bytes(bytestring):
        x = Message(0,0,0)
        x.messageType = MessageType(int.from_bytes(bytestring[0:4], byteorder='big'))
        x.transactionID = int.from_bytes(bytestring[4:12], byteorder='big')
        x.messageValue = bytestring[16:]
        return x

    def __str__(self):
        return str(self.messageType) + " " + str(self.transactionID) + " " + str(self.messageValue)


class Connection:
    connection = None

    def __init__(self, ip, port):
        self.ip_address = ip
        self.port = port

    def connect(self):
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection.connect((self.ip_address, self.port))
        print("CONNECTED TO SERVER", self.ip_address, self.port)

    def close(self):
        self.connection.close()
        print("CLOSED CONNECTION TO SERVER", self.ip_address, self.port)

    def send(self, message):
        self.connection.sendall(message.get_binary())
        print("SEND", self.ip_address, self.port, message.get_binary(), len(message.get_binary())) # convert binary string to hex

    def recieve(self):
        data = self.connection.recv(4096)
        return Message.message_from_bytes(data)

    def ack(self):
        self.send(Message(MessageType.ACK, 0, 0))

    def message_protocol(self, message):
        self.send(message)
        data = self.recieve()
        self.ack()
        return data


