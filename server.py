from socket import *
import sys

# get server port input from user
try:
  serverPort = int(sys.argv[1])
except Exception as e:
  print("Error recieving server port (did you input a port number?)")
  print("Error:", e)
  sys.exit(1)

# create server socket
serverSocket = socket(AF_INET, SOCK_STREAM)
host = "127.0.0.1"
serverSocket.bind((host, serverPort))

# listen to connections
serverSocket.listen(1)
print(f"Le server is now listening on host {host}:{serverPort}")
while True:

  # accept socket connection
  newSocket, address = serverSocket.accept()

  # use connection to recieve data ('with' handles socket closure)
  with newSocket:
    print(f"Le server is now connected to {address}")
    while True:
      message = newSocket.recv(2028)
      # no msg means client dc'd
      if not message:
        print("Client dc'd")
        break
      decodedMessage = message.decode('utf-8')
      newSocket.send(decodedMessage.encode())