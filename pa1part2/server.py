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
  host = "127.0.0.1"
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
      setupMessage = False
      while True:
        message = newSocket.recv(2028)
        # no msg means client dc'd
        if not message:
          print("Client dc'd")
          break
        decodedMessage = message.decode('utf-8')
        invalid = False

        print(decodedMessage)
        # CSP
        # check if we recieved setup message yet
        if setupMessage == False:
          # if not, then assume it's the current message
          parsedMessage = decodedMessage.split(" ")
          if parsedMessage[0] != "s":
            # if the current message is not setup, then this is invalid
            invalid = True
          else:
            # it's a setup connection, as it should be

            empty = False
            # content is not empty check
            for item in parsedMessage:
              if item == " " or "\n":
                empty = True
            # check validity (length check)
            if (empty) or (not(len(parsedMessage) == 5)):
              invalid = True
            else:
              # send OK status
              newSocket.send(("200 OK: Ready").encode())
              continue
        # if setup message is invalidated (should have been setup msg but is not or incorrect parsing format)
        if invalid:
          newSocket.send(("404 ERROR: Invalid Connetion SetupMessage").encode())
          break
        
        # send back the same data
        newSocket.send(decodedMessage.encode())
except Exception as e:
  print(f"Error listening/communicating with client socket: {e}")
  sys.exit(1)