from history_sever import Server, ServerConfig

if __name__ == "__main__":
    server_config = ServerConfig("127.0.0.1", 12340, 2048)
    server = Server(server_config)
    server.start()