from Client.Commands.command import Command

class CompositeCommand(Command):
    """
    A command that aggregates and executes multiple commands.
    """
    def __init__(self):
        """
        Initialize an instance of CompositeCommand.
        """
        self.commands = []

    def add_command(self, command):
        """
        Add a command to the list of commands to be executed.

        Parameters:
        - command: An instance of a Command subclass.
        """
        self.commands.append(command)

    def execute(self):
        """
        Execute each command in the list and concatenate the results.

        Returns:
        - str: The concatenated result of executing each command.
        """
        result = ""
        for command in self.commands:
            result += command.execute()
        return result