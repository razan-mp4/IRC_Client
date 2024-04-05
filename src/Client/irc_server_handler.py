import socket
import threading
import sys
from abc import ABC, abstractmethod

MAX_BUFFER_SIZE = 2048

class IRCConnection(ABC):
   """
   Abstract base class for IRC bridges.

   Attributes:
   - None

   Methods:
   - connect(): Connect to the IRC server.
   - disconnect(): Disconnect from the IRC server.
   - reconnect(): Reconnect to the IRC server.
   - send_data(message): Send data to the IRC server.
   - receive_data(): Receive data from the IRC server.
   """
   @abstractmethod
   def connect(self):
      pass

   @abstractmethod
   def disconnect(self):
      pass

   @abstractmethod
   def reconnect(self):
      pass

   @abstractmethod
   def send_data(self, message):
      pass

   @abstractmethod
   def receive_data(self):
      pass
    

class IRCSocketConnection(IRCConnection):
   def __init__(self, server, port, channel, nickname):
      """
      Concrete implementation of IRCBridge for socket-based IRC connection.

      Attributes:
      - server (str): IRC server address.
      - port (int): IRC server port.
      - channel (str): Initial channel to join.
      - nickname (str): User's nickname.
      - irc_socket (socket.socket): Socket object for IRC communication.

      Methods:
      - connect(): Connect to the IRC server, send initial USER and NICK commands, and join the specified channel.
      - disconnect(): Disconnect from the IRC server.
      - reconnect(): Reconnect to the IRC server.
      - send_data(message): Send data to the IRC server.
      - receive_data(): Receive data from the IRC server.
      - start(): Start the IRC client by connecting to the server.
      """
      self.server = server
      self.port = port
      self.channel = channel
      self.nickname = nickname
      self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      


   def connect(self):
      """
      Connect to the IRC server, send initial USER and NICK commands (to register user),
      and join the specified channel.

      Returns:
      - True if the connection is successful, False otherwise.
      """
      try:
         # Establish a connection to the IRC server
         self.irc_socket.connect((self.server, self.port))
         # Send initial USER and NICK commands to REGISTER the user
         self.send_data(f"USER {self.nickname} 0 * :{self.nickname}\r\n")
         self.send_data(f"NICK {self.nickname}\r\n")
         # Join the specified channel
         self.send_data(f"JOIN {self.channel}\r\n")
      except socket.error as e:
            print(f"Error connecting to the server: {e}")
            return False
      return True

   def disconnect(self):
      """
      Disconnect from the IRC server.
      """
      try:
         self.send_data("QUIT :Disconnected\r\n")
         self.irc_socket.close()
      except Exception as e:
         print(f"Error disconnecting from the server: {e}")

   def reconnect(self):
      """
      Reconnect to the IRC server.
      """
      try:
         # Reestablish a connection to the IRC server
         self.irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
         # Send initial USER and NICK commands to ReREGISTER the user
         self.irc_socket.connect((self.server, self.port))
         self.send_data(f"USER {self.nickname} 0 * :{self.nickname}\r\n")
         self.send_data(f"NICK {self.nickname}\r\n")
         self.send_data(f"JOIN {self.channel}\r\n")
      except socket.error as e:
         print(f"Error reconnecting to the server: {e}")

   def send_data(self, message):
      """
      Send data to the IRC server.

      Parameters:
      - message: The message to be sent.
      """
      try:
         self.irc_socket.send(bytes(message, 'UTF-8'))
      except socket.error as e:
         print(f"Error sending data: {e}")

   def receive_data(self):
      """
      Receive data from the IRC server.

      Returns:
      - The received data.
      """
      try:
         # Receive data from the IRC server
         data = self.irc_socket.recv(MAX_BUFFER_SIZE).decode('UTF-8')
         if not data:
            return "Connection closed by server."

         if data.startswith("PING"):
            # Respond to PING messages to keep the connection alive
            self.send_data("PONG {}\r\n".format(data.split()[1]))
         elif data:
            return data
            
      except socket.error as e:
         print(f"Socket error while receiving data: {e}")
         sys.exit(0)

      except Exception as e:
         print(f"An unexpected error occurred while receiving data: {e}")
         sys.exit(1)
   

   def start(self):
      """
      Start the IRC client by connecting to the server.
      """
      if not self.connect():
         receive_data_thread = threading.Thread(target=self.receive_data, daemon=True)
         receive_data_thread.start()
         return


class IRCWebSocketConnection(IRCConnection):
   """
   Concrete implementation of IRCBridge for WebSocket-based IRC connection.

   Attributes:
   - Implementation for WebSocket connection

   Methods:
   - connect(): Implementation for WebSocket connection.
   - disconnect(): Implementation for WebSocket disconnection.
   - reconnect(): Implementation for WebSocket reconnection.
   - send_data(message): Implementation for sending data over WebSocket.
   - receive_data(): Implementation for receiving data over WebSocket.
   """
   def __init__(self, server, port, channel, nickname):
      # Implementation for WebSocket connection
      pass

   def connect(self):
      # Implementation for WebSocket connection
      pass

   def disconnect(self):
      # Implementation for WebSocket disconnection
      pass

   def reconnect(self):
      # Implementation for WebSocket reconnection
      pass

   def send_data(self, message):
      # Implementation for sending data over WebSocket
      pass

   def receive_data(self):
      # Implementation for receiving data over WebSocket
      pass