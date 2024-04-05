import socket
import time
import threading

MAX_BUFFER_SIZE = 2048
# Global variable to store chat history
chat_history = []

class HistoryServerHandler:
    def __init__(self, server_address, server_port):
        self.server_address = server_address
        self.server_port = server_port
        self.history_socket = None

    def connect_to_server(self):
        """
        Connect to the server to establish a socket for history communication.
        """
        try:
            self.history_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.history_socket.connect((self.server_address, self.server_port))
            self.start_history_thread()
            return True
        except Exception as e:
            print(f"Error connecting to history server: {e}")
            return False

    def post_history(self, history_data):
        """
        Send chat history data to the server.
        """
        try:
            if self.history_socket:
                self.history_socket.sendall(history_data.encode('utf-8'))
        except Exception as e:
            print(f"Error posting history to server: {e}")

    def get_history_from_server(self):
        """
        Continiously receive chat history data from the server.
        """
        while True:
            try:
                if self.history_socket:
                    data = self.history_socket.recv(MAX_BUFFER_SIZE).decode('utf-8')
                    chat_history.append(data)

                time.sleep(1)  # Add a short delay to avoid excessive CPU usage
            except Exception as e:
                print(f"Error getting history from server: {e}")


    def get_history(self):
        """
        Give history to the Client.
        """
        return chat_history
    
    def start_history_thread(self):
        """
        Start a thread to continuously get information from the server.
        """
        history_thread = threading.Thread(target=self.get_history_from_server)
        history_thread.daemon = True  # Set the thread as a daemon so it will exit when the main program exits.
        history_thread.start()

    def close_connection(self):
        """
        Close the socket connection to the server.
        """
        try:
            if self.history_socket:
                self.history_socket.close()
        except Exception as e:
            print(f"Error closing history socket: {e}")