#######################################################################
# File:             client_handler.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template ClientHandler class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client handler class, and use a version of yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################
import pickle
import datetime
from menu import Menu

class ClientHandler(object):
    """
    The ClientHandler class provides methods to meet the functionality and services provided
    by a server. Examples of this are sending the menu options to the client when it connects,
    or processing the data sent by a specific client to the server.
    """
    def __init__(self, server_instance, clientsocket, addr):
        """
        Class constructor already implemented for you
        :param server_instance: normally passed as self from server object
        :param clientsocket: the socket representing the client accepted in server side
        :param addr: addr[0] = <server ip address> and addr[1] = <client id>
        """
        self.server_ip = addr[0]
        self.client_id = addr[1]
        self.server = server_instance
        self.clientsocket = clientsocket
        self.unread_messages = []

    def _sendMenu(self):
        """
        Already implemented for you.
        sends the menu options to the client after the handshake between client and server is done.
        :return: VOID
        """
        fp = open('menu.py', 'rb')

        menuFile = {
            'message': 'new file',
            'file_name': 'menu.py',
            'file_content': fp.read()
        }

        menu = Menu(self.client_id)
        menuObj = {
            'message': 'menu',
            'menu': menu
        }
        self.server.send(self.clientsocket, menuFile)
        self.server.send(self.clientsocket, menuObj)
        print('\t* Sent Menu to: {id}'.format(id=self.client_id))


    def process_options(self):
        """
        Process the option selected by the user and the data sent by the client related to that
        option. Note that validation of the option selected must be done in client and server.
        In this method, I already implemented the server validation of the option selected.
        :return:
        """
        while True:
            data = self.server.receive(self.clientsocket)

            print("(+) Received Data from: {id} --> {message}".format(id=self.client_id, message=data['option']))
            if ('option' in data.keys()) and (1 <= data['option'] <= 6): # validates a valid option selected
                option = data['option']
                if option == 1:
                    self._send_user_list()
                elif option == 2:
                    recipient_id = data['id']
                    message = data['message']
                    self._save_message(recipient_id, message)
                elif option == 3:
                    self._send_messages()
                elif option == 4:
                    room_id = data['room_id']
                    self._create_chat(room_id)
                elif option == 5:
                    room_id = data['room_id']
                    self._join_chat(room_id)
                elif option == 6:
                    self._disconnect_from_server()
            else:
                print("The option selected is invalid")

    def _send_user_list(self):
        """
        TODO: send the list of users (clients ids) that are connected to this server.
        :return: VOID
        """
        message = "Users in server:"
        for client in self.server.clients.keys():
            message += " {name}:{id},".format(name=self.server.names[client], id=client)
            message = message.rstrip(',')
        data = {
            "message": message
        }
        self.server.send(self.clientsocket, data)

    def _save_message(self, recipient_id, message):
        """
        TODO: link and save the message received to the correct recipient. handle the error if recipient was not found
        :param recipient_id:
        :param message:
        :return: VOID
        """
        # print("_save_message")
        if recipient_id in self.server.clients:
            recipient_handler = self.server.clients[recipient_id]
            recipient_handler.unread_messages.append((datetime.datetime.now(), message, self.server.names[self.client_id]))
            self.server.send(self.clientsocket, {
                'message': "(+) Message Sent"
            })
        else:
            print("(x) No user {id}".format(id=recipient_id))
            self.server.send(self.clientsocket, {
                'message': "(x) No user {id}".format(id=recipient_id)
            })

    def _send_messages(self):
        """
        TODO: send all the unread messages of this client. if non unread messages found, send an empty list.
        TODO: make sure to delete the messages from list once the client acknowledges that they were read.
        :return: VOID
        """
        message = "My messages:"
        for msg in self.unread_messages:
            message += "\n{date}: {sent} (from: {sender})".format(date=msg[0], sent=msg[1], sender=msg[2])
        try:
            self.server.send(self.clientsocket, {
                'message': message
            })
            self.unread_messages.clear()
        except Exception as e:
            print("(x) Failed to get Messages from {id}".format(id=self.client_id))


    def _create_chat(self, room_id):
        """
        TODO: Creates a new chat in this server where two or more users can share messages in real time.
        :param room_id:
        :return: VOID
        """
        print("_create_chat")

    def _join_chat(self, room_id):
        """
        TODO: join a chat in a existing room
        :param room_id:
        :return: VOID
        """
        print("_join_chat")

    def delete_client_data(self):
        """
        TODO: delete all the data related to this client from the server.
        :return: VOID
        """
        print("delete_client_data")
        self.server.clients.pop(self.client_id, None)

    def _disconnect_from_server(self):
        """
        TODO: call delete_client_data() method, and then, disconnect this client from the server.
        :return: VOID
        """
        print("_disconnect_from_server")
        self.delete_client_data()
        self.clientsocket.close()

    def run(self):
        self._sendMenu()
        self.process_options()













