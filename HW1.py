import socket
import threading

def handle_client(clientS):
    requestedData = clientS.recv(1024).decode()

    # 4. Parsing HTTP GET Request
    htmlFile = requestedData.split()[1]
    if htmlFile == "/":
        htmlFile = "/index.html"

    #5.	Preparing Response
    try:
        with open("webFile" + htmlFile, "rb") as file:
            responseBody = file.read()
        response = """HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nContent-Length: {}\r\n\r\n{}""".format(
            len(responseBody), responseBody.decode())
    
    except FileNotFoundError:
        response = "HTTP/1.1 404 Not Found\r\n\r\n404 Not Found"

    # 6. Sending Response to Client
    clientS.send(response.encode())
    clientS.close()

def main():
    serverS = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 1. Opening Port 80
    serverS.bind(("localhost", 80))

    # 2. Accepting Connection Requests
    serverS.listen(5)
    print("[*] Listening on port 80")
    while True:
        clientS, addr = serverS.accept()
        print("[*] Accepted connection from: %s:%d" % (addr[0], addr[1]))

        handler = threading.Thread(target=handle_client, args=(clientS,))
        handler.start()

if __name__ == "__main__":
    main()