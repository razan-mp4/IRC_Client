from Client.Commands.command import Command

class DisplayHelpCommand(Command):
    """
    Command class for handling the "/help" command.
    """
    def __init__(self, irc_client):
        """
        Initialize the DisplayHelpCommand.

        Parameters:
        - irc_client: The IRC client instance.
        """
        self.irc_client = irc_client

    def execute(self):
        """
        Display available commands and their descriptions.

        Returns:
        - Help message string.
        """
        return "Available commands:\n/join - Join a channel/create a new channel\n/part - Leave the current channel\n/names - List users in the current channel\n/info - Display information about the current channel\n/nick - Change your nickname. Usage: /nick <new_nickname>\n/quit - Gracefully disconnect from the server\n/help - Display this help message\n"
