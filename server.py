import glob
import re
import socket
import os
import sys

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
    matching_files = os.listdir(f"{directory}")
    r = re.compile(f'{file_split[0]}-v.*{file_split[1]}')
    file_versions = sorted(list(filter(r.match, matching_files)))
    for file in os.listdir(f"{directory}"):
        if file == filename:

            if len(file_versions) == 0:
                file_split[0] += '-v1'
            else:

                last_file_version = file_versions[-1]
                last_file_version = int(last_file_version[last_file_version.index('-v') + 2]) + 1
                file_split[0] += f'-v{last_file_version:_}'
            break

    return f'{file_split[0]}.{file_split[1]}'


def execute_request(req: ServerRequest):

    try:
        s = socket.socket()

        s.bind((SERVER_HOST, req.port))

        s.listen(MAX_INCOMING_CONNECTIONS)
        print(f"[LOG] Listening as {SERVER_HOST}:{req.port}")

        accepting = True
        while accepting:
            client_socket, address = s.accept()
            print(f"[LOG] {address} has connnected.")

            received = client_socket.recv(BUFFER_SIZE).decode()
            filename, filesize = received.split(SEPARATOR)
            filename = os.path.basename(filename)

            write_to_directory = req.root_directory + f'/{address[0]}'
            create_directory(write_to_directory)

            if os.path.exists(f"{write_to_directory}/{filename}"):
                filename = generate_new_file_version(filename, write_to_directory)

            with open(f"{write_to_directory}/{filename}", "wb") as f:
                while True:
                    bytes_read = client_socket.recv(BUFFER_SIZE)
                    if not bytes_read:
                        break
                    f.write(bytes_read)

            client_socket.close()
    except FileNotFoundError:
        print("Given Directory does not exist")
        quit()
    except KeyboardInterrupt:
        quit()
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

        return req
    except Exception as e:
        print(f"An unexpected error occurred. {e}")
        quit()
    except KeyboardInterrupt:
        quit()


def main():
    request = setup_server_cmd_request()
    execute_request(request)


if __name__ == '__main__':
    main()
