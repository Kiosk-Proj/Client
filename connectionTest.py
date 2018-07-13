from connection import *

myConnection = Connection("96.225.21.203", 25565)
myConnection.connect()
print(myConnection.message_protocol(Message(MessageType.CONNECTION, 0, b'\00\00')))
print(myConnection.message_protocol(Message(MessageType.INPUT, 0, 15415)))
myConnection.close()
