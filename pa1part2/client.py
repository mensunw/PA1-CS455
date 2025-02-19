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
  # CSP
  # get the size of the data
  csp_message = "s rtt 10 1024 0\n"
  clientSocket.send(csp_message.encode("utf-8"))

  status = clientSocket.recv(2048).decode()
  
  if "200" not in status:
    print(f"Recieved status 404 from server: {status}")
    clientSocket.close()
    sys.exit(1)
  
  print("CSP done, now moving onto MP")

  # MP
  probes = 10
  for probe in range(probes):
    mp_message = f"m {probe} testing\n"
    clientSocket.send(mp_message.encode("utf-8"))
    message = clientSocket.recv(2048).decode()
    if "404" in message:
      print(f"Recieved status 404 from server: {message}")
      clientSocket.close()
      sys.exit(1)
    print("recieved: ", message)

  clientSocket.close()
except Exception as e:
  print(f"Error sending/receiving from server socket: {e}")
  sys.exit(1)