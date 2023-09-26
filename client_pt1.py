import socket

# Construct HTML request string to fetch the page '/'
request = b"GET / HTTP/1.0\r\n\r\n"

# AF_INET = IPv4 address and SOCK_STREAM is TCP
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# timeout after 10 seconds
mysocket.settimeout(10)

# Connect to the google server
mysocket.connect(("www.google.com", 80))
mysocket.sendall(request)

# while loop to recieve data of unknown buffer size
response = b""
while(True):
    part = mysocket.recv(4096)
    if len(part) == 0:  # If no more data is recieved, quit
        break
    response = response + part;

# Close the socket
mysocket.close()

# print downloaded response to screen
print(response.decode())
