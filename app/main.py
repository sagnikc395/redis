import socket  # noqa: F401
import threading

BUFFER_SIZE = 4096

# walrus operator
def handleCMDS(client: socket.socket):
    while chunk := client.recv(BUFFER_SIZE):
        if chunk == b"":
            break
        lines = chunk.decode().split("\n")
        for line in lines:
            cmd = line.strip()
            if not cmd:
                continue

            if "PING" in cmd:
                client.sendall(b"+PONG\r\n")
                continue

            args = cmd.split(" ")
            if args[0] == "ECHO" and len(args) > 1:
                res = args[1]
                client.sendall(f"${len(res)}\r\n{res}\r\n".encode())

    client.close()


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    # conn, addr = server_socket.accept() # wait for client
    # print(f"Accepted connection from {addr}")
    # send the response to PING
    # conn.sendall(b"+PONG\r\n")
    # while True:
    #     data = conn.recv(1024)
    #     if not data:
    #         break
    #     lines = data.decode().split("\n")
    #     for line in lines:
    #         cmd = line.strip().upper()
    #         if cmd == "PING":
    #             conn.sendall(b"+PONG\r\n")
    while True:
        client_socket, client_addr = server_socket.accept()
        threading.Thread(target=handleCMDS,args=(client_socket,)).start()





if __name__ == "__main__":
    main()
