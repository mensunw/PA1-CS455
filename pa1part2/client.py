from socket import *
import sys
import time

def recv_full_message(sock):
    '''
    creating this lil helper function to help with retrieving ENTIRE message from server
    in cases where the msg too big
    '''
    msg = ""
    while True:
        msg_chunk = sock.recv(buffer_size).decode("utf-8")
        # nothing being received means connection is closed
        if not msg_chunk:  
          break
        msg += msg_chunk
        # once \n is recieved, we know it's end of message
        if "\n" in msg_chunk:  
          break
    return msg

# get server host name/ipaddr and server port input from user
try:
  host = sys.argv[1]
  serverPort = int(sys.argv[2])
  # get measurement type (0 = rtt, 1 = tput)
  measurementNum = int(sys.argv[3])
  # get server delay
  delay = float(sys.argv[4])
  if(measurementNum != 0 and measurementNum != 1):
    print("Error: measure must must be 0 or 1")
    sys.exit(1)
except:
  print("Error recieving host & server port (did you input a host & port number?)")
  sys.exit(1)

# size in bytes for message content
sizes = []
# probes used for iterating
probes = 10
# buffer size for recieving
buffer_size = 33000
# measurement type
measurement = ""
if(measurementNum == 0):
  measurement = "rtt"
  sizes = [1, 100, 200, 400, 800, 1000]
else:
  measurement = "tput"
  sizes = [1000, 2000, 4000, 8000, 16000, 32000]
for size in sizes:
  # for EACH size generate content of that size
  print("----------------------------------------")
  print(f"Size: {size}")
  content = "C" * size
  try:
    # create client socket
    clientSocket = socket(AF_INET, SOCK_STREAM)

    # connect socket
    clientSocket.connect((host, serverPort))
    #print(f"Connected to {host}:{serverPort}")
  except Exception as e:
    print(f"Error connecting client socket to server: {e}")
    sys.exit(1)

  try:
    # CSP
    # get the byte size of the data
    csp_message = f"s {measurement} {probes} {size} {delay}\n"
    clientSocket.send(csp_message.encode("utf-8"))
    # get status from server
    status = clientSocket.recv(buffer_size).decode()
    # if error status, close and exit
    if "200" not in status:
      print(f"Recieved error from server: {status}")
      clientSocket.close()
      sys.exit(1)
    
    #print("CSP done, now moving onto MP")

    # MP
    # for each probe, send the message along with the increasing seq number
    total_rtt = 0
    total_time = 0
    for probe in range(1, probes+1):
      # note starting time
      starting_time = time.time()
      mp_message = f"m {probe} {content}\n"
      #print(mp_message)
      clientSocket.send(mp_message.encode("utf-8"))
      # call helper function for recieving full msg (thanks bu server limiter -_-)
      message = recv_full_message(clientSocket)
      # note ending time
      ending_time = time.time()

      # if error contained in message, then close and exit
      if "404" in message:
        print(f"Recieved error from server: {message}")
        clientSocket.close()
        sys.exit(1)
      # note the rtt for this probe (multiplying it by 1000 to conver to ms for easier read)
      rtt = (ending_time - starting_time) * 1000
      total_rtt += rtt
      # note time passed
      passed_time = ending_time - starting_time
      total_time += passed_time
    avg_rtt = total_rtt / probes
    avg_throughput = 0
    # incase barely any change
    if((total_time / probes) == 0):
      avg_throughput = 0
    else:
      # divide at the end to convert to mb/ps for easier reading
      avg_throughput = (size / (total_time / probes) / (1024 * 1024)) 
    if(measurement == "rtt"):
      print(f"Average RTT: {avg_rtt}ms")
    if(measurement == "tput"):
      print(f"Average Throughput: {avg_throughput}Mbps")
    
    #print("MP done, now moving onto CTP")

    # CTP
    ctp_message = f"t\n"
    clientSocket.send(ctp_message.encode("utf-8"))
    # get status from server
    status = clientSocket.recv(buffer_size).decode()
    #print("status for termination:", status)
    # close either way
    if "200" not in status:
      print(f"Recieved error from server: {status}")
      clientSocket.close()
      sys.exit(1)
    #print("CTP successfully terminated")
    clientSocket.close()
  except Exception as e:
    print(f"Error sending/receiving from server socket: {e}")
    sys.exit(1)