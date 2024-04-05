class InputValidation:

   def validate_input(user_input):
      """
      Validate user input before sending it to the server.

      Parameters:
      - user_input: The user input to be validated.

      Returns:
      - The validated user input or None if input is invalid.
      """
      # Remove leading and trailing whitespaces
      user_input = user_input.strip()

      # Check if the input is None
      if user_input is None:
         return None
      
      # Modify user input based on specific commands
      if user_input[0:5].lower() == "/join":
         new_channel = user_input.split()[1]
         if new_channel.startswith("#"):
            pass
         else:
            new_channel = "#" + new_channel
         user_input = "/join " + new_channel
      elif user_input[0:5].lower() == "/part":
         user_input = user_input.split()[0]
      elif user_input[0:6].lower() == "/names":
         user_input = user_input.split()[0]
      elif user_input[0:5].lower() == "/info":
         user_input = user_input.split()[0]
      elif user_input.lower().startswith("/nick"):
         new_nickname = ""
         if user_input != "/nick":
            new_nickname = user_input.split()[1]
         if new_nickname is None:
            new_nickname = "not_given"
         user_input = "/nick " + new_nickname
      elif user_input[0:5].lower() == "/help":
         # Help Messages
         help_messages = {
            "join": "Join a channel/create new channel",
            "part": "Leave the current channel",
            "names": "List users in the current channel",
            "info": "Display information about the current channel",
            "nick": "Change your nickname. Usage: /nick <new_nickname>",
            "quit": "Gracefully disconnect from the server",
            "help": "Display this help message"
         }
         helping = "__________Available commands:_________\n"
         for command, description in help_messages.items():
            helping += f"/{command} - {description}\n"
         helping += "\n"
         user_input = helping

      elif user_input[0:5].lower() == "/quit":
         user_input = user_input.split()[0]
      return user_input
