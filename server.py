import socket
import os
from request import ServerRequest
import argparse

SERVER_HOST = socket.gethostbyname(socket.gethostname())
SERVER_PORT = 5001
# receive 4096 bytes each time
BUFFER_SIZE = 4096
SEPARATOR = "<SEPARATOR>"
MAX_INCOMING_CONNECTIONS = 999
DEFAULT_PATH = './server/downloads/'


def create_directory(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print("Error Creating directory " + directory)


def generate_new_file_version(filename, directory):
    file_split = filename.split('.')
    print("LIST DIRECTORY", os.listdir(f"{directory}"))
    for file in os.listdir(f"{directory}"):
        if filename == file:
            print(filename, " = ", file)
            print("contains file")


    return f'{file_split[0]}-v{len(os.listdir(f"{directory}"))}.{file_split[1]}'


def execute_request(req: ServerRequest):
    # create the server socket
    # TCP socket
    s = socket.socket()

    # bind the socket to our local address
    s.bind((SERVER_HOST, req.port))

    s.listen(MAX_INCOMING_CONNECTIONS)
    print(f"[LOG] Listening as {SERVER_HOST}:{req.port}")

    accepting = True
    while accepting:
        # accept connection if there is any
        client_socket, address = s.accept()
        # if below code is executed, that means the sender is connected
        print(f"[LOG] {address} is connected.")

        # receive the file infos
        # receive using client socket, not server socket
        received = client_socket.recv(BUFFER_SIZE).decode()
        filename, filesize = received.split(SEPARATOR)
        # remove absolute path if there is
        filename = os.path.basename(filename)
        # convert to integer

        # start receiving the file from the socket
        # and writing to the file stream
        write_to_directory = req.root_directory + f'/{address[0]}'
        create_directory(write_to_directory)

        if os.path.exists(f"{write_to_directory}/{filename}"):
            print(f'the file {filename} exists')
            filename = generate_new_file_version(filename, write_to_directory)
            print(f'NEW FILE  {filename}')

        with open(f"{write_to_directory}/{filename}", "wb") as f:
            while True:
                # read 1024 bytes from the socket (receive)
                bytes_read = client_socket.recv(BUFFER_SIZE)
                if not bytes_read:
                    print("done")
                    # nothing is received
                    # file transmitting is done
                    break
                # write to the file the bytes we just received
                f.write(bytes_read)
                print("Incoming file " + str(bytes_read))
                # update the progress bar

        # close the client socket
        client_socket.close()
    # close the server socket
    s.close()


def setup_server_cmd_request() -> ServerRequest:
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", help="The root directory for the downloaded files. Defaults to "
                                                  "~/server/downloads", required=False, default=DEFAULT_PATH)
    parser.add_argument("-p", "--port", help="The port in which the program should run. Defaults to 8000",
                        required=False, default=SERVER_PORT, type=int)

    try:
        args = parser.parse_args()
        req = ServerRequest()
        req.root_directory = args.directory
        req.port = args.port

        print(args)
        return req
    except Exception as e:
        print(f"Error! Could not recognized arguments.\n{e}")
        quit()


def main():
    request = setup_server_cmd_request()
    print(request.root_directory)
    execute_request(request)


if __name__ == '__main__':
    main()
