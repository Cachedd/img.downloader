import socket

# A function which accepts a path and returns a http response
def fetch_http_response(url_path): 
    
    # Construct HTML request string to fetch the page 'given page'
    request = f"GET {url_path} HTTP/1.0\r\n\r\n"

    # Create an INET, STREAMing socket
    mysocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # timeout after 10 seconds
    mysocket.settimeout(10)

    # Connect to the google server
    mysocket.connect(("www.google.com", 80))
    mysocket.sendall(request.encode())

    # while loop to recieve to recieve data of unknown buffer size
    response = b""
    while(True):
        part = mysocket.recv(4096)
        if len(part) == 0: # if no data is recieved then quit
            break
        response = response + part

    # Close the socket
    mysocket.close() 

    # returns the http response given by the url
    return response

# split the response into 2 parts - header and body
response_parts =  fetch_http_response("/").decode().split("\r\n\r\n")

# split the header part into response and header values
http_header = response_parts[0].split("\r\n")

# split the http response into 3 parts - protocol, response code, response message
_, response_code, response_message = http_header[0].split()

# extract the header data
http_header_response = response_parts[0]

# extract the html data
html_data = response_parts[1]

# Initialize an empty dicitionary
header_content = {}

# Split the http header content by new line
lines = http_header_response.split("\n")

# Loop through each line and separate it by ':' to get key and value
for line in lines:
    parts = line.split(":", 1) # limit spliting to one time
    if len(parts) == 2:
        key = parts[0].strip() # remove any trailing or leading spaces
        value = parts[1].strip() # remove any trailing or leading spaces
        header_content[key] = value

# Parse HTML data and search for any embedded HTML tags
def find_tags(html, start_param, end_param, last_element):
    start = 0
    img_string = ""
    while True:
        start = html.find(start_param, start)
        if start == -1:
            break # -1 means <img does not exist
        end = html.find(end_param, start)
        if end == -1:
            break
        img_tag = html[start:end + last_element] # +1 to take the last element too
        img_string += (img_tag) + " "
        start = end + 1
    img_string = img_string[:-1]
    return img_string

def find_imgs(img_tags):
    result_list = []
    for img_srcs in img_tags.split(" "):
        if img_srcs.find("src=") != -1:
            result_list.append(img_srcs[5:-1])
    return result_list

# extract the source paths from the image tags
src_path_parts = find_imgs(find_tags(html_data, "<img", ">", 1))

# Function to create a new file and save image to the file
def create_file(img_name, img):
    with open(img_name, "wb") as f:
        f.write(img)

# function to download the image and save it 
def download_image(response, image_name):
    response_parts = response.split(b'\r\n\r\n')
    create_file(image_name, response_parts[1])

# iterate through the images paths to download the images
for img_path in src_path_parts:
    download_image(fetch_http_response(img_path), img_path.split("/").pop())
