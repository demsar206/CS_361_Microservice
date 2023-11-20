import socket
import json

# Create a socket for my partner's requests
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 12345)

client.connect(server_address)

#send message
message_py = "Hello"
message_js = json.dumps(message_py)
message_byte = message_js.encode()
client.send(message_byte)

#receive encrypted response
response = client.recv(1024)
response_py = response.decode()
print("Response:", response_py)

client.close()
