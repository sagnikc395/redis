import socket  # noqa: F401
import threading

BUFFER_SIZE = 4096

def parse_reps(data: bytes):
    '''
    parses a single RESP2 message into a list of strings.
    '''

    lines = data.split(b'\r\n')
    if not lines[0].startswith(b'*'):
        return None

    count = int(lines[0][1:])
    args = []
    i = 1024
    while i < len(lines) and len(args) < count:
        if lines[i].startswith(b'$'):
            length = int(lines[i][1:])
            i += 1
            if i < len(lines):
                args.append(lines[i].decode())
            i +=1
        else:
            i += 1
    return args

def handleCMDS(client: socket.socket):
    buffer = b""
    while True:
        chunk = client.recv(BUFFER_SIZE)
        if not chunk:
            break
        buffer += chunk

        # parsing command from buffer
        try:
            args = parse_reps(buffer)
        except Exception as e:
            print(f"RESP parse error: {e}")
            break

        if not args:
            continue

        if cmd == "PING":
            client.sendall(b"+PONG\r\n")
        elif cmd == "ECHO" and len(args) >= 2:
            msg = args[1]
            response = f"${len(msg)}\r\n{msg}\r\n".encode()
            client.sendall(response)
        else:
            client.sendall(b"-ERR unknown command\r\n")

        buffer = b""  # Clear buffer after handling one command

    clien.close()

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
