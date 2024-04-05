import threading
import tkinter as tk
from tkinter import messagebox
from tkinter import scrolledtext


class GUI:
   def __init__(self, irc_client):
      """
      Initialize the GUI for the IRC client.

      Parameters:
      - irc_client (IRCClient): An instance of the IRCClient class.
      """
      self.irc_client = irc_client
      self.root = tk.Tk()
      self.root.title("IRC Client")
      self.root.geometry("380x525")
      self.current_frame = None
      self.registration_frame()

   def registration_frame(self):
      """
      Show the first frame of the GUI, allowing users to input server details.
      """
      if self.current_frame:
         self.current_frame.destroy()  # Destroy the current frame

      self.current_frame = tk.Frame(self.root)
      # Labels and entry widgets for server details
      self.server_label = tk.Label(self.current_frame, text="Server Address:")
      self.server_entry = tk.Entry(self.current_frame, width=30)
      self.server_entry.insert(tk.END, "lead.libera.chat")  # Set default value

      self.port_label = tk.Label(self.current_frame, text="Server Port:")
      self.port_entry = tk.Entry(self.current_frame, width=30)
      self.port_entry.insert(tk.END, "6667")  # Set default value

      self.channel_label = tk.Label(self.current_frame, text="Channel to Join:")
      self.channel_entry = tk.Entry(self.current_frame, width=30)
      self.channel_entry.insert(tk.END, "#your_channel")  # Set default value

      self.nickname_label = tk.Label(self.current_frame, text="Your Nickname:")
      self.nickname_entry = tk.Entry(self.current_frame, width=30)
      self.nickname_entry.insert(tk.END, "your_name")  # Set default value

      self.connect_button = tk.Button(self.current_frame, text="Connect", command=self.send_server_info)

      self.server_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")
      self.server_entry.grid(row=0, column=1, padx=5, pady=5)
      self.port_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
      self.port_entry.grid(row=1, column=1, padx=5, pady=5)
      self.channel_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
      self.channel_entry.grid(row=2, column=1, padx=5, pady=5)
      self.nickname_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
      self.nickname_entry.grid(row=3, column=1, padx=5, pady=5)
      self.connect_button.grid(row=4, column=0, columnspan=2, pady=10)
      # Center the frame within the root window
      self.current_frame.pack(expand=True, fill="both", padx=20, pady=150)
      self.current_frame.pack()

   def send_server_info(self):
      """
      Validate server details, connect to the server, and switch to the second frame.
      Display error messages for invalid configurations or connection issues.
      """
      server = self.server_entry.get().strip()
      port = self.port_entry.get().strip()
      channel = self.channel_entry.get().strip()
      nickname = self.nickname_entry.get().strip()

      validated_config = self.irc_client.connect_to_server(server, port, channel, nickname)
      if validated_config is not None:
         self.chatting_frame()
      else:
         messagebox.showerror("Error", "Invalid configuration. Please enter valid details.")

   def chatting_frame(self):
      """
      Show the second frame of the GUI, displaying chat functionality.
      """
      if self.current_frame:
         self.current_frame.destroy()  # Destroy the current frame
      self.current_frame = tk.Frame(self.root)

      # Button to disconnect from the server
      disconnect_button = tk.Button(self.current_frame, text="Disconnect from server", command=self.disconnect_from_server, width=29)
      disconnect_button.grid(row=0, column=0, pady=0, sticky="w")
      
      # Button to get chat history
      history_button = tk.Button(self.current_frame, text="History", command=self.get_chat_history)
      history_button.grid(row=0, column=0, pady=0, sticky="e")

      # Scrollable text area for displaying messages
      self.text_area = scrolledtext.ScrolledText(self.current_frame, wrap=tk.WORD, width=50, height=35)
      self.text_area.grid(row=1, column=0, padx=0, pady=0)
      self.text_area.configure(state="disabled")

      # Entry widget for typing messages
      self.message_entry = tk.Entry(self.current_frame, width=35)
      self.message_entry.grid(row=2, column=0, padx=1, pady=0, sticky="w")

      # Button to send messages
      send_button = tk.Button(self.current_frame, text="Send", command=self.send_message, width=3, height=1)
      send_button.grid(row=2, column=0, padx=0, pady=0, sticky="e")

      self.current_frame.pack()
      # Start a thread to continuously receive data and update the text area
      output_thread = threading.Thread(target=self.give_output)
      output_thread.start()
    
   def disconnect_from_server(self):
      """
      Disconnect from the IRC server and show a message to the user.
      """
      try:
         if self.irc_client:
            self.irc_client.disconnect_from_server()
            messagebox.showinfo("Disconnected", "Disconnected from the server.")
            self.registration_frame()
      except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred: {e}")

   def send_message(self):
      """
      Send a message to the IRC server based on user input.
      Validate the message, delegate it to the message handler, and update the text area.
      Display an error message for unexpected issues during message handling.
      """
      try:
         message = self.message_entry.get().strip()
         if message:
            validated_message = self.irc_client.send_message(message)
            if validated_message is not None:
               # Set the text area to normal to enable insertion
               self.text_area.configure(state="normal")
               self.text_area.insert(tk.END, f"You: {validated_message}\n")
               self.text_area.yview(tk.END)  # Ensure the text_area is scrolled to the end
               # Set the text area back to disabled
               self.text_area.configure(state="disabled")
               self.message_entry.delete(0, tk.END)
      except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred: {e}")

   
   def give_output(self):
      """
      Continuously receive data from the server and display it in the text area.
      Handle disconnection events and attempt to reconnect.
      """
      try:
         while True:
            # Receive and display output from the server
            output = self.irc_client.receive_data()
            self.text_area.configure(state="normal")
            self.text_area.insert(tk.END, output)
            self.text_area.yview(tk.END)  # Ensure the text_area is scrolled to the end
            self.text_area.configure(state="disabled")
            if "Connection closed by server." in output:
               # Handle disconnection by showing a message and reconnecting
               messagebox.showinfo("Disconnected", "Disconnected from the server.")
               self.reconnect_to_server()
      except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    
   def reconnect_to_server(self):
      """
      Attempt to reconnect to the IRC server and show a message to the user.
      """
      try:
         if self.irc_client:
            self.irc_client.reconnect_to_server()
            messagebox.showinfo("Reconnecting", "Reconnecting to the server...")
            self.chatting_frame(self.irc_client.validated_config)
      except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred: {e}")

   

   def chat_history_frame(self, chat_history):
      """
      Show a frame with a scrolled text area to display chat history.
      """
      if self.current_frame:
         self.current_frame.destroy()  # Destroy the current frame
      self.current_frame = tk.Frame(self.root)

      # Button to go back to the chatting frame
      back_button = tk.Button(self.current_frame, text="Back to Chat", command=self.chatting_frame, width=38)
      back_button.grid(row=0, column=0, pady=0, sticky="w")

      # Scrollable text area for displaying chat history
      history_text_area = scrolledtext.ScrolledText(self.current_frame, wrap=tk.WORD, width=50, height=35)
      history_text_area.grid(row=1, column=0, padx=0, pady=0)
      history_text_area.insert(tk.END, chat_history)
      history_text_area.configure(state="disabled")

      self.current_frame.pack()

   def get_chat_history(self):
      """
      Retrieve and display chat history.
      """
      try:
         chat_history = self.irc_client.get_chat_history()
         self.chat_history_frame(chat_history)
      except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred: {e}")

   def start(self):
      """
      Start the Tkinter main loop for the GUI.
      """
      try:
         self.root.mainloop()
      except Exception as e:
         messagebox.showerror("Error", f"An unexpected error occurred: {e}")
      finally:
         # Ensure proper cleanup when the application is closed
         if hasattr(self, 'irc_client'):
            self.irc_client.disconnect_from_server()


    
