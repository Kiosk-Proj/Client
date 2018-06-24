from connection import *

myConnection = Connection()
myConnection.connect()
print(myConnection.message_protocol(Message(MessageType.INPUT, 0, 15415)))
myConnection.close()