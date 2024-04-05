import socket
import threading

class ServerConfig:
    """
    Configuration class for the Server.

    Attributes:
    - address (str): The IP address to bind the server to.
    - port (int): The port number to bind the server to.
    - max_buffer_size (int): The maximum buffer size for receiving data.
    """
    def __init__(self, address, port, max_buffer_size):
        self.address = address
        self.port = port
        self.max_buffer_size = max_buffer_size

class Server:
    """
    Simple server class that handles communication with a single client.
    """
    def __init__(self, config):
        """
        Initialize the server with the provided configuration.

        Parameters:
        - config (ServerConfig): The configuration for the server.
        """
        self.config = config
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((config.address, config.port))
        self.server_socket.listen(1)
        print(f"Server listening on {config.address}:{config.port}")

        self.client_socket = None
        self.chat_history = []

    def start(self):
        """
        Start the server and continuously accept incoming client connections.
        """
        try:
            while True:
                self.client_socket, client_address = self.server_socket.accept()
                print(f"Accepted connection from {client_address}")

                # Start a thread to handle the client
                client_handler_thread = threading.Thread(target=self.handle_client)
                client_handler_thread.start()

        except Exception as e:
            print(f"Server error: {e}")

    def handle_client(self):
        """
        Handle communication with a connected client.
        Receive data from the client, update the chat history,
        and send back the updated history to the client.
        """
        try:
            while True:
                data = self.client_socket.recv(self.config.max_buffer_size).decode('utf-8')
                if not data:
                    break

                # Store received data in chat_history
                self.chat_history.append(data)

                # Send back the updated chat_history to the client
                history_data = '\n'.join(self.chat_history)
                self.client_socket.sendall(history_data.encode('utf-8'))

        except Exception as e:
            print(f"Error handling client: {e}")

        finally:
            # Close the client socket when the client disconnects
            self.client_socket.close()
            print("Client disconnected")
