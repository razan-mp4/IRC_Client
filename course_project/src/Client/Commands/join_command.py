from Client.Commands.command import Command

class JoinChannelCommand(Command):
    """
    Command class for handling the "/join" command.
    """
    def __init__(self, irc_client, new_channel):
        """
        Initialize the JoinChannelCommand.

        Parameters:
        - irc_client: The IRC client instance.
        - new_channel: The new channel to join.
        """
        self.irc_client = irc_client
        self.new_channel = new_channel

    def execute(self):
        """
        Join a new IRC channel.

        Returns:
        - The IRC JOIN message string.
        """
        self.irc_client.channel = self.new_channel
        return f"JOIN {self.irc_client.channel}\r\n"