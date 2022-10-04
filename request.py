class ServerRequest:

    def __init__(self):
        self.root_directory = None
        self.port = None


    def __str__(self):
        return f"ServerRequest: port: {self.port}, root_directory: {self.root_directory}"


class ClientRequest:

    def __init__(self):
        self.ip_address = None
        self.files = None
        self.port = None


    def __str__(self):
        return f"ClientRequest: ip_address: {self.ip_address}, files: {self.files}, port {self.port}"
