########################################################################################################################
# Class: Computer Networks
# Date: 02/03/2020
# Lab3: Server support for multiple clients
# Goal: Learning Networking in Python with TCP sockets
# Student Name: Robert Clarkson
# Student ID: 915433914
# Student Github Username: robertIanClarkson
# Lab Instructions: No partial credit will be given. Labs must be completed in class, and must be committed to your
#               personal repository by 9:45 pm.
# Running instructions: This program needs the server to run. The server creates an object of this class.
#
########################################################################################################################
import threading
import pickle

class ClientHandler:
    """
    The client handler class receives and process client requests
    and sends responses back to the client linked to this handler.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you.
        :param server_instance: passed as 'self' when the object of this class is created in the server object
        :param clientsocket: the accepted client on server side. this handler, by itself, can send and receive data
                             from/to the client that is linked to.
        :param addr: addr[0] = server ip address, addr[1] = client id assigned buy the server
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.handler = clientsocket
        self.print_lock = threading.Lock() # creates the print lock

    def process_client_data(self):
        """
        TODO: receives the data from the client
        TODO: prepares the data to be printed in console
        TODO: acquire the print lock
        TODO: prints the data in server console
        TODO: release the print lock
        TODO: keep this handler object listening for more incoming data from the client
        :return: VOID
        """
        data = self.receive()
        self.print_lock.acquire()
        print(data)
        self.print_lock.release()


    def send(self, data):
        serialized_data = pickle.dumps(data)
        self.handler.send(serialized_data)

    def receive(self, max_mem_alloc=4096):
        raw_data = self.handler.recv(max_mem_alloc)
        data = pickle.loads(raw_data)
        return data

    def run(self):
        self.process_client_data()