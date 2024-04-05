import socket
from abc import ABC, abstractmethod

class ConfigValidation(ABC):
   """
   Abstract base class for server configuration validation.
   """
   @abstractmethod
   def validate_config(self, server, port, channel, nickname):
      pass

class BasicConfigValidation(ConfigValidation):
   """
   Basic implementation of server configuration validation.
   """
   def is_valid_ip(self, ip):
      """
      Check if the given string is a valid IP address.

      Parameters:
      - ip: The string to check.

      Returns:
      - True if the string is a valid IP address, False otherwise.
      """
      try:
         socket.inet_pton(socket.AF_INET, ip)
         return True
      except socket.error:
         try:
            socket.inet_pton(socket.AF_INET6, ip)
            return True
         except socket.error:
            return False

   def is_valid_domain(self, domain):
      """
      Check if the given string is a valid domain name.

      Parameters:
      - domain: The string to check.

      Returns:
      - True if the string is a valid domain name, False otherwise.
      """
      try:
         socket.gethostbyname(domain)
         return True
      except socket.error:
            return False

   def validate_config(self, server, port, channel, nickname):
      """
      Validate the server configuration before using it in the IRC client.

      Parameters:
      - server: IRC server address
      - port: IRC server port
      - channel: Initial channel to join
      - nickname: User's nickname

      Returns:
      - A tuple containing validated server address, port, channel, and nickname.
         Returns None if the configuration is invalid.
      """
      # Check if the server is a valid IP or domain
      if not (self.is_valid_ip(server) or self.is_valid_domain(server)):
         return None

      # Check if the channel starts with #
      if not channel.startswith("#"):
         channel = "#" + channel
      
      # Check if the port is an integer
      try:
         port = int(port)
      except ValueError:
         return None

      # Check if the port is within a valid range
      if not (0 < port < 65535):
         return None

      # If no validation conditions are met, return the validated configuration
      return server, port, channel, nickname


class AdvancedConfigValidation(ConfigValidation):
   """
   Advanced implementation of server configuration validation.
   """
   def validate_config(self, server, port, channel, nickname):
      """
      Validate the server configuration using advanced logic.

      Parameters:
      - server: IRC server address
      - port: IRC server port
      - channel: Initial channel to join
      - nickname: User's nickname

      Returns:
      - A tuple containing validated server address, port, channel, and nickname.
         Returns None if the configuration is invalid.
      """
      # Advanced validation logic
      if server and port and channel and nickname and len(nickname) > 3:
         return server, port, channel, nickname
      else:
         return None

