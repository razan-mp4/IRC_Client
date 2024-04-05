from Client.Commands.command import Command

from Client.Commands.composite_command import CompositeCommand
from Client.Commands.join_command import JoinChannelCommand
from Client.Commands.leave_command import LeaveChannelCommand
from Client.Commands.list_command import ListUsersCommand
from Client.Commands.info_command import ChannelInfoCommand
from Client.Commands.nick_command import ChangeNicknameCommand
from Client.Commands.help_command import DisplayHelpCommand
from Client.Commands.quit_command import QuitCommand




class MessageHandler:
    """
    Handles the execution of IRC commands based on user input.
    """
    def __init__(self, irc_client):
        """
        Initialize the MessageHandler class.

        Parameters:
        - irc_client: The associated IRC client instance.
        """
        self.irc_client = irc_client
        self.commands = {
            "/join": JoinChannelCommand,
            "/part": LeaveChannelCommand,
            "/names": ListUsersCommand,
            "/info": ChannelInfoCommand,
            "/nick": ChangeNicknameCommand,
            "/help": DisplayHelpCommand,
            "/quit": QuitCommand
        }

    def command_choice(self, message):
        """
        Execute the IRC command based on the user input.

        Parameters:
        - message: The user input to be chosen and executed.

        Returns:
        - The generated IRC message string.
        """
        try:
            # Check if the message contains multiple commands
            if ';' in message:
                composite_command = CompositeCommand()
                command_strings = message.split(';')
                for command_string in command_strings:
                    command, *args = command_string.split()
                    command_class = self.commands.get(command.lower())
                    if command_class and issubclass(command_class, Command):
                        command_instance = command_class(self.irc_client, *args)
                        composite_command.add_command(command_instance)
                return composite_command.execute()
            else:
                # Process single command
                command, *args = message.split()
                command_class = self.commands.get(command.lower())
                if command_class and issubclass(command_class, Command):
                    command_instance = command_class(self.irc_client, *args)
                    return command_instance.execute()
                else:
                    return f"PRIVMSG {self.irc_client.channel} :{message}\r\n"
        except Exception as e:
            print(f"Error executing command: {e}")
            return ""
