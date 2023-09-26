import socket

# Construct HTML request string to fetch the page '/'
request = b"GET / HTTP/1.0\r\n\r\n"

# Create an INET, STREAMing socket
mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # AF_INET = IPv4 address and SOCK_STREAM is TCP

# timeout after 10 seconds
mysocket.settimeout(10)

# Connect to the google server on Port 80
mysocket.connect(("www.google.com", 80))
mysocket.sendall(request)

# while loop to recieve data of unknown buffer size
response = b""
while(True):
    part = mysocket.recv(4096)
    if len(part) == 0:  # If no more data is recieved, quit
        break
    response = response + part

# Close the socket
mysocket.close()

# decode the response
decoded_data = response.decode()

# split the http response into 2 parts - header and body
response_parts = decoded_data.split("\r\n\r\n")

# split the header part by newline into response and header values
http_header = response_parts[0].split("\r\n")

# split the http response into 3 parts - protocol, response code and response message
http_response = http_header[0].split()

# extract the http response code
response_code = http_response[1] #200

# extract the response message
response_message = http_response[2] #OK

#
http_header_response = response_parts[0]

# Initialize an empty dicitionary
header_content = {}

# Split the http header content by new line
lines = http_header_response.split("\n")

# Loop through each line and split it by ':' to get key and value
for l in lines:
    parts = l.split(":", 1) # limit spliting by ':' to one time
    if len(parts) == 2: 
        key = parts[0].strip() # remove any trailing or leading spaces
        value = parts[1].strip() # remove any trailing or leading spaces
        header_content[key] = value

# Print the HTTP Response code
print("Response Code:")
print(response_code)

# Print the HTTP Response Message
print("\nResponse Message:")
print(response_message)

# Print the header contents(parameters and values)
print("\nHeader Content:")
for key, value in header_content.items():
    print(f"{key}: {value}")

# If the HTTP response is NOT 200, display an error message, otherwise print the HTML contents to the screen
if response_code == "200":
    print("\nHTML Content:")
    print(response_parts[1])
else:
    print("Error: 404 Not Found!")


