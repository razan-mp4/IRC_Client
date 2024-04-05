
from multiprocessing import Process

from Client.gui import GUI
from Client.irc_client import IRCClient
from Client.server_config_validation import BasicConfigValidation, AdvancedConfigValidation

from Server.history_sever import Server, ServerConfig

def run_client():
    irc_client = IRCClient()
    irc_client.set_server_config_validator(BasicConfigValidation())
    gui = GUI(irc_client)
    gui.start()

def run_server():
    server_config = ServerConfig("127.0.0.1", 12340, 2048)
    server = Server(server_config)
    server.start()

if __name__ == "__main__":
    # Create separate processes for client and server
    client_process = Process(target=run_client)
    server_process = Process(target=run_server)

    # Start both processes
    client_process.start()
    server_process.start()

    # Wait for both processes to finish
    client_process.join()
    server_process.join()
