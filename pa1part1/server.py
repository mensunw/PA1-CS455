from socket import *
import sys

# get server port input from user
try:
  serverPort = int(sys.argv[1])
except Exception as e:
  print("Error recieving server port (did you input a port number?)")
  print("Error:", e)
  sys.exit(1)

try:
  # create server socket
  serverSocket = socket(AF_INET, SOCK_STREAM)
  host = "csa2.bu.edu"
  serverSocket.bind((host, serverPort))
except Exception as e:
  print(f"Error creating server socket: {e}")
  sys.exit(1)

try:
  # listen to connections
  serverSocket.listen(5)
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
        # send back the same data
        newSocket.send(decodedMessage.encode())
except Exception as e:
  print(f"Error listening/communicating with client socket: {e}")
  sys.exit(1)