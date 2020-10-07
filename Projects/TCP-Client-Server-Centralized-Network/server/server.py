#######################################################################
# File:             server.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################

from builtins import object
import socket
from threading import Thread
import pickle


from client_handler import ClientHandler


class Server(object):
    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=13000):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}  # dictionary of clients handlers objects handling clients. format {clientid:client_handler_object}
        # TODO: bind the socket to a public host, and a well-known port
        self.host = ip_address
        self.port = port
        self._bind()

    def _bind(self):
        try:
            self.serversocket.bind((self.host, self.port))
        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: _bind --> {exception}".format(exception=e))

    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        # TODO: your code here
        try:
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server listening at {host}/{port}".format(host=self.host, port=self.port))
        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: _listen --> {exception}".format(exception=e))

    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                # TODO: Accept a client
                # TODO: Create a thread of this client using the client_handler_threaded class
                clienthandler, addr = self.serversocket.accept()
                Thread(target=self.client_handler_thread, args=(clienthandler, addr)).start()
            except Exception as e:
                # TODO: Handle exceptions
                self.serversocket.close()
                raise Exception("ERROR: _accept_clients --> {exception}".format(exception=e))

    def send(self, clientsocket, data):
        """
        TODO: Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        try:
            # print(data)
            serialized_data = pickle.dumps(data)
            clientsocket.send(serialized_data)
        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: send --> {exception}".format(exception=e))

    def receive(self, clientsocket, MAX_BUFFER_SIZE=8192):
        """
        TODO: Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        try:
            data_from_client = clientsocket.recv(MAX_BUFFER_SIZE)
            data = pickle.loads(data_from_client)
            return data
        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: receive --> {exception}".format(exception=e))

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """
        try:
            # TODO: create a new client handler object and return it

            # strip the data out of address
            server_ip = address[0]
            client_id = address[1]
            print("\n(+) Accept Client: {id}".format(id=client_id))

            # create the client handler
            client_handler = ClientHandler(self, clientsocket, address)

            # notify the server user
            if client_id not in self.clients:
                print("\t* New Client")
            else:
                print("\t* Old Client")
            self.clients[client_id] = client_handler
            print("\t* Client List:")
            for client in self.clients:
                print("\t\t- {client}".format(client=client))

            # run the client handler
            client_handler.run()
        except Exception as e:
            self.serversocket.close()
            raise Exception("ERROR: client_handler_thread --> ", e)

    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()
