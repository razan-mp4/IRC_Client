from Client.irc_server_handler import IRCSocketConnection
from Client.input_validation import InputValidation
from Client.output_validation import OutputValidation
from Client.message_handler import MessageHandler
from Client.history_server_handler import HistoryServerHandler

# to improve:
# 
# “/help” command fix
# 
# fix bug when input validation don't allow to execute multiple commands with parameters
# 
# split registration and chatting windows from gui class
# 
# implement “factory method” pattern to each validation
# 
# solve bug when after registration can’t request “/info”, ”/names” command because channel is not initialized in IRCClient class only in SocketBridge class
# 
# when oppening chat_history_frame in gui "history_text_area.insert(tk.END, chat_history)" cannot be performed
# bcs "history_text_area.configure(state="disabled
# ")" and it show error in message box (as i think)

class IRCClient:
    def __init__(self):
        """
        Initialize the IRCClient class.

        Attributes:
        - validated_config (tuple): A tuple containing validated server configuration.
        - server_connection (ServerHandler): An instance of the ServerHandler class for server communication.
        """
        self.server_config_validator = None
        self.validated_config = None
        self.bridge = None
        self.command_handler = None
        self.history_manager = HistoryServerHandler('127.0.0.1', 12340) 
        # Connect to the history server
        history_connected = self.history_manager.connect_to_server()
        if not history_connected:
            print("Failed to connect to the history server.")

    def set_server_config_validator(self, server_config_validator):
        """
        Set the server configuration validator for the IRC client.

        Parameters:
        - server_config_validator (InputValidation): An instance of the InputValidation class for server configuration validation.
        """
        self.server_config_validator = server_config_validator
    
    def connect_to_server(self, server, port, channel, nickname):
        """
        Connect to the IRC server with the provided configuration.

        Parameters:
        - server (str): The server address.
        - port (str): The server port.
        - channel (str): The channel to join.
        - nickname (str): The client's nickname.

        Returns:
        - validated_config (tuple): Validated server configuration if successful, otherwise None.
        """
        validated_config = self.server_config_validator.validate_config(server, port, channel, nickname)
        if validated_config is not None:
            self.bridge = IRCSocketConnection(*validated_config)
            self.bridge.start()
            self.command_handler = MessageHandler(self)
            self.validated_config = validated_config
        return validated_config

    def disconnect_from_server(self):
        """
        Disconnect from the IRC server.
        """
        if self.bridge:
            self.bridge.disconnect()
    
    def reconnect_to_server(self):
        """
        Attempt to reconnect to the IRC server.
        """
        if self.bridge:
            self.bridge.reconnect()

    def send_message(self, message):
        """
        Send a message to the IRC server.

        Parameters:
        - message (str): The message to send.

        Returns:
        - validated_message (str): Validated message if successful, otherwise None.
        """
        validated_message = InputValidation.validate_input(message)
        if validated_message is not None and self.bridge:
            self.message_handler(validated_message)
            self.post_chat_history(validated_message)
        return validated_message

    def receive_data(self):
        """
        Receive and validate data from the IRC server.

        Returns:
        - validated_data (str): Data received from the server, or an empty string if no data.
        """
        if self.bridge:
            data = self.bridge.receive_data()
            validated_data = OutputValidation.validate_output(data)
            if data is not None:
                self.post_chat_history(validated_data)
                return validated_data
        return ""
    
    def message_handler(self, message):
        """
        Delegate message handling to the MessageHandler.

        Parameters:
        - message: The message to be handled.
        """
        # Choose and execute IRC commands
        message_to_send = self.command_handler.command_choice(message)
        # Send the processed message to the IRC server
        if message_to_send:
            self.bridge.send_data(message_to_send)

    def post_chat_history(self, history_data):
        """
        Send chat history to the history server.
        """
        self.history_manager.post_history(history_data)

    def get_chat_history(self):
        """
        Request chat history from the history_server instance.
        """
        history_data = self.history_manager.get_history()
        # Process the received history data as needed
        if history_data:
            return history_data
        
    def disconnect_from_history_server(self):
        # Close the connection to the history server
        self.history_manager.close_connection()