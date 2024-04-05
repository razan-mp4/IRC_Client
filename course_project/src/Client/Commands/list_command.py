from Client.Commands.command import Command



class ListUsersCommand(Command):
    """
    Command class for handling the "/names" command.
    """
    def __init__(self, irc_client):
        """
        Initialize the ListUsersCommand.

        Parameters:
        - irc_client: The IRC client instance.
        """
        self.irc_client = irc_client

    def execute(self):
        """
        List users in the specified IRC channel.

        Returns:
        - The IRC NAMES message string.
        """
        return f"NAMES {self.irc_client.channel}\r\n"
