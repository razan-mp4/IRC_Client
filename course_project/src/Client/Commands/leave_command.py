from Client.Commands.command import Command


class LeaveChannelCommand(Command):
    """
    Command class for handling the "/part" command.
    """
    def __init__(self, irc_client):
        """
        Initialize the LeaveChannelCommand.

        Parameters:
        - irc_client: The IRC client instance.
        """
        self.irc_client = irc_client

    def execute(self):
        """
        Leave the current IRC channel.

        Returns:
        - The IRC PART message string.
        """
        return f"PART {self.irc_client.channel}\r\n"
