from socket import *
import sys

# get server port input from user
try:
  serverPort = int(sys.argv[1])
except:
  print("Error recieving server port (did you input a port number?)")

# create server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
host = "localhost"
serverSocket.bind((host, serverPort))

# listen to connections
serverSocket.listen()
print(f"Le server is now listening on host {host}:{serverPort}")

# accept socket connection
newSocket, address = serverSocket.accept()

# while connected...
with newSocket:
  print(f"Le server is now connected to {address}")
  while True:
    message = serverSocket.recv(2028)
    print(message)