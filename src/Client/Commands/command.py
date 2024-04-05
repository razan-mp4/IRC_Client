from abc import ABC, abstractmethod

class Command(ABC):
    """
    Abstract base class for IRC command classes.
    """
    @abstractmethod
    def execute(self):
        """
        Execute the IRC command.
        """
        pass