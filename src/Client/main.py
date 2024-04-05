# to run this code u need to specify path in some files
# (files in Command Folder except command.py, irc_client.py, message_handler.py)
from gui import GUI
from irc_client import IRCClient
from server_config_validation import BasicConfigValidation, AdvancedConfigValidation



if __name__ == "__main__":
    # Initialize IRC client and GUI
    irc_client = IRCClient()
    irc_client.set_server_config_validator(BasicConfigValidation())
    gui = GUI(irc_client)

    # Start the GUI in the main thread
    gui.start()

