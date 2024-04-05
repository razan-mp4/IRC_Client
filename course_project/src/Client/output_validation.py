import datetime
class OutputValidation:
   def validate_output(server_message):
      """
      Validate messages received from the server before displaying them to the user.

      Parameters:
      - server_message: The message received from the server.

      Returns:
      - The validated server message or None if the message is invalid.
      """

     
      if "ERROR" in server_message:
         return None  # Discard messages containing "ERROR"
      

      # Add a timestamp to the received data for display
      if server_message is not None:
         timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
         server_message = f"{timestamp} {server_message}"
      
      # If no validation conditions are met, timestamp + the original message is returned
      return server_message
