import socket
import os
import argparse
import sys

from request import ClientRequest
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 4096
DEFAULT_PORT = 5001
def setup_client_cmd_request() -> ClientRequest:

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--ip",help="The IP address the client sends the request for. "
                                  "Must be set to a valid IP Address", required=True)
    parser.add_argument('files', nargs='*')
    parser.add_argument("-p", "--port",help="The port in which the client runs on "
                                  "Defaults to 5001", required=False, default=DEFAULT_PORT, type=int)
    try:
        args = parser.parse_args()
        req = ClientRequest()

        # req.files = args.revs
        # req.port = args.port
        # req.root_directory = args.directory
        req.ip_address = args.ip
        req.port = args.port
        req.files = args.files
        if (len(args.files) == 0):
            raise Exception("Need to specify files")

        print(req)
        return req
    except Exception as e:
        print(f"Error! Could not recognized arguments.\n{e}")
        quit()





def execute_request(req : ClientRequest):

    # the port, let's use 5001
    # the name of file we want to send, make sure it exists
    for file in req.files:
        filename = file
        # get the file size
        filesize = os.path.getsize(filename)

        s = socket.socket()
        print(f"[+] Connecting to {req.ip_address}:{req.port}")
        s.connect((req.ip_address, req.port))
        print("[+] Connected.")

        # send the filename and filesize
        s.send(f"{filename}{SEPARATOR}{filesize}".encode())

        # start sending the file
        with open(filename, "rb") as f:
            while True:
                # read the bytes from the file
                bytes_read = f.read(BUFFER_SIZE)
                if not bytes_read:
                    # file transmitting is done
                    break
                # we use sendall to assure transimission in
                # busy networks
                s.sendall(bytes_read)
                # update the progress bar
    # close the socket
    s.close()

def main():
    request = setup_client_cmd_request()
    execute_request(request)

if __name__ == '__main__':
    main()


