from socket import *
import sys
import time

# get server host name/ipaddr and server port input from user
try:
  host = sys.argv[1]
  serverPort = int(sys.argv[2])
except:
  print("Error recieving host & server port (did you input a host & port number?)")
  sys.exit(1)

# size in bytes for message content
sizes = [1, 100, 200, 400, 800, 1000]
#sizes = [1000, 2000, 4000, 8000, 16000, 32000]
# probes used for iterating
probes = 10
# buffer size for recieving
buffer_size = 33000
# server delay 
delay = 0 # 0, 0.1, 0.2
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
    csp_message = f"s rtt {probes} {size} {delay}\n"
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
      print(mp_message)
      clientSocket.send(mp_message.encode("utf-8"))
      message = clientSocket.recv(buffer_size).decode()
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
    print(f"Average RTT: {avg_rtt}ms")
    print(f"Average Throughput: {avg_throughput}Mbps")
    
    #print("MP done, now moving onto CTP")

    # CTP
    ctp_message = f"t\n"
    clientSocket.send(ctp_message.encode("utf-8"))
    # get status from server
    status = clientSocket.recv(buffer_size).decode()
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