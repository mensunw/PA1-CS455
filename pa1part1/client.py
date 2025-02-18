from socket import *
import sys

# get server host name/ipaddr and server port input from user
try:
  host = sys.argv[1]
  serverPort = int(sys.argv[2])
except:
  print("Error recieving host & server port (did you input a host & port number?)")
  sys.exit(1)

try:
  # create client socket
  clientSocket = socket(AF_INET, SOCK_STREAM)

  # connect socket
  clientSocket.connect((host, serverPort))
  print(f"Connected to {host}:{serverPort}")
except Exception as e:
  print(f"Error connecting client socket to server: {e}")
  sys.exit(1)

try:
  # send from client socket to server's socket
  message = "Hello on the other side"
  encodedData = message.encode("utf-8")
  clientSocket.send(encodedData)
  echoMessage = clientSocket.recv(2048)
  print(f"Recieved from server: {echoMessage.decode("utf-8")}")

  clientSocket.close()
except Exception as e:
  print(f"Error sending/receiving from server socket: {e}")
  sys.exit(1)