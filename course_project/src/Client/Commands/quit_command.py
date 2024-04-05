from Client.Commands.command import Command

class QuitCommand(Command):
    """
    Command class for handling the "/quit" command.
    """
    def __init__(self, irc_client):
        """
        Initialize the QuitCommand.

        Parameters:
        - irc_client: The IRC client instance.
        """
        self.irc_client = irc_client

    def execute(self):
        """
        Gracefully disconnect from the IRC server.

        Returns:
        - The IRC QUIT message string.
        """
        return f"QUIT :{self.irc_client.nickname} is disconnecting\r\n"
