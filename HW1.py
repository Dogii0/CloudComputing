import socket
import threading

# Function to handle client connections
def handle_client(client_socket):
    request_data = client_socket.recv(1024).decode()

    # Extracting the requested file name from the HTTP GET request
    requested_file = request_data.split()[1]

    # If no file is requested, default to index.html
    if requested_file == "/":
        requested_file = "/index.html"

    try:
        # Open the requested file
        with open("webFile" + requested_file, "rb") as file:
            # Read file contents
            response_body = file.read()

        # Prepare HTTP response
        response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}""".format(
            len(response_body), response_body.decode())

    except FileNotFoundError:
        # If the requested file does not exist, return a 404 Not Found response
        response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"

    # Send the HTTP response to the client
    client_socket.send(response.encode())
    client_socket.close()

# Main function to run the server
def main():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to localhost and port 80
    server_socket.bind(("localhost", 80))

    # Enable the server to accept connections
    server_socket.listen(5)
    print("[*] Listening on port 80")

    while True:
        # Accept connections from clients
        client_socket, addr = server_socket.accept()
        print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

        # Create a thread to handle the client
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == "__main__":
    main()