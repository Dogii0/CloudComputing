import socket
import threading

# Function to handle client connections
def handle_client(clientS):
    requestedData = clientS.recv(1024).decode()

    # Extracting the requested file name from the HTTP GET request
    htmlFile = requestedData.split()[1]

    # If no file is requested, default to index.html
    if htmlFile == "/":
        htmlFile = "/index.html"

    try:
        # Open the requested file
        with open("webFile" + htmlFile, "rb") as file:
            # Read file contents
            responseBody = file.read()

        # Prepare HTTP response
        response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}""".format(
            len(responseBody), responseBody.decode())

    except FileNotFoundError:
        # If the requested file does not exist, return a 404 Not Found response
        response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"

    # Send the HTTP response to the client
    clientS.send(response.encode())
    clientS.close()

def main():
    serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to localhost and port 80
    serverS.bind(("localhost", 80))

    # Enable the server to accept connections
    serverS.listen(5)
    print("[*] Listening on port 80")

    while True:
        # Accept connections from clients
        clientS, addr = serverS.accept()
        print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

        # Create a thread to handle the client
        handler = threading.Thread(target=handle_client, args=(clientS,))
        handler.start()

if __name__ == "__main__":
    main()