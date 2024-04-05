from Client.Commands.command import Command

class ChannelInfoCommand(Command):
    """
    Command class for handling the "/info" command.
    """
    def __init__(self, irc_client):
        """
        Initialize the ChannelInfoCommand.

        Parameters:
        - irc_client: The IRC client instance.
        """
        self.irc_client = irc_client

    def execute(self):
        """
        Display information about the specified IRC channel.

        Returns:
        - The IRC LIST message string.
        """
        return f"LIST {self.irc_client.channel}\r\n"
