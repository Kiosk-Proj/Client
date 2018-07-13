from connection import *

myConnection = Connection("96.225.21.203", 25565)
myConnection.connect()
print(myConnection.send(Message(MessageType.CONNECTION, 0, b'\00\00')))
name = myConnection.message_protocol(Message(MessageType.INPUT, 0, 12598)).messageValue[4:]
print(name[1::2].decode('utf-8'))
myConnection.close()
