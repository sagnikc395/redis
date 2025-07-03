import socket  # noqa: F401


def main():
    # You can use print statements as follows for debugging, they'll be visible when running tests.
    print("Logs from your program will appear here!")

    # Uncomment this to pass the first stage
    #
    server_socket = socket.create_server(("localhost", 6379), reuse_port=True)
    conn, addr = server_socket.accept() # wait for client
    # print(f"Accepted connection from {addr}")
    # send the response to PING
    # conn.sendall(b"+PONG\r\n")
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        data = data.split("\n")
        pongs = [i for i in data if i=="+PONG"]
        for _ in pongs:
            conn.send(b"+PONG\r\n")

    conn.close()
    server_socket.close()



if __name__ == "__main__":
    main()
