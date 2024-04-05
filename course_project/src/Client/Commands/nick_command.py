from Client.Commands.command import Command

class ChangeNicknameCommand(Command):
    """
    Command class for handling the "/nick" command.
    """
    def __init__(self, irc_client, new_nickname):
        """
        Initialize the ChangeNicknameCommand.

        Parameters:
        - irc_client: The IRC client instance.
        - new_nickname: The new nickname to set.
        """
        self.irc_client = irc_client
        self.new_nickname = new_nickname

    def execute(self):
        """
        Change the user's nickname.

        Returns:
        - The IRC NICK message string.
        """
        return f"NICK {self.new_nickname}\r\n"
