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
        msg_chunk = sock.recv(buffer_size).decode('utf-8')
        # nothing being received means connection is closed
        if not msg_chunk:  
          print("Client dc'd (1)")
          break
        msg += msg_chunk
        # once \n is recieved, we know it's end of message
        if "\n" in msg_chunk:  
          break
    return msg

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

# buffer size for recieving
buffer_size = 33000
try:
  # listen to connections
  serverSocket.listen(1)
  print(f"Le server is now listening on host {host}:{serverPort}")
  while True:

    # accept socket connection
    newSocket, address = serverSocket.accept()

    # use connection to recieve data ('with' handles socket closure)
    with newSocket:
      print(f"Le server is now connected to {address}")
      setupMessage = False
      seqNum = 1
      delay = 0
      while True:
        decodedMessage = recv_full_message(newSocket)
        # no msg means client dc'd
        if not decodedMessage:
          print("Client dc'd (2)")
          break
        parsedMessage = decodedMessage.split(" ")
        invalid = False

        #print("msg: ", decodedMessage)
        # CSP
        # check if we recieved setup message yet
        if setupMessage == False:
          # if not, then it has to be the current message
          if parsedMessage[0] != "s":
            # if the current message is not setup, then this is invalid
            invalid = True
          else:
            # it's a setup connection, as it should be

            # content is not empty check
            for item in parsedMessage:
              if item == " " or item == "\n":
                invalid = True
            # check validity (length check)
            if not(len(parsedMessage) == 5):
              invalid = True
            
            # made it all the way here and it's valid, then good to go
            if not invalid:
              # send OK status and set setup to true and set delay
              setupMessage = True
              # remove the \n
              delay = float(parsedMessage[4].strip())
              newSocket.send(("200 OK: Ready").encode())
              continue
            # if setup message is invalidated (should have been setup msg but is not or incorrect parsing format)
            else:
              newSocket.send(("404 ERROR: Invalid Connection SetupMessage").encode())
              break
        
        # MP
        if parsedMessage[0] == "m":
          # check validity 
          invalid = False
          # content is not empty check
          for item in parsedMessage:
            if item == " " or item == "\n":
              invalid = True
          # check validity (length check)
          if not(len(parsedMessage) == 3):
            invalid = True

          # check sequence number
          if int(parsedMessage[1]) == seqNum:
            seqNum += 1
          else:
            invalid = True

          # if invalidated send back error
          if invalid:
            newSocket.send(("404 ERROR: Invalid Measurement Message").encode())
            break
          
          # echo back message after sleeping the delay
          time.sleep(delay)
          #print("sent: ", parsedMessage[2])
          newSocket.send(parsedMessage[2].encode())
        # CTP
        elif parsedMessage[0] == "t\n":
          # check validity
          invalid = False
          # content is not empty check
          for item in parsedMessage:
            if item == " " or item == "\n":
              invalid = True
          # check validity (length check)
          if not(len(parsedMessage) == 1):
            invalid = True

          # if invalidated send back error
          if invalid:
            newSocket.send(("404 ERROR: Invalid Connection Termination Message").encode())
            break

          # if valid, send back success and then close
          newSocket.send(("200 OK: Closing Connection").encode())
          break
        # not CSP with setUp = False, MP, or CTP
        else:
          newSocket.send(("404 ERROR").encode())
          break
    # temp
    #print("temp exit")
    #sys.exit(0)
except Exception as e:
  print(f"Error listening/communicating with client socket: {e}")
  sys.exit(1)