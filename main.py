import socket
import datetime
# IRC server information
server = "irc.libera.chat"
port = 6667
channel = "#HackerIdiot"
bot_name = "Helper"

# Connect to the IRC server
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))

# Send IRC commands
def send_irc_message(message):
    irc.send((message + "\n").encode("utf-8"))

send_irc_message("NICK " + bot_name)
send_irc_message("USER " + bot_name + " 0 * :" + bot_name)
send_irc_message("JOIN " + channel)

# Global variables for tracking bot status and moderation
start_time = datetime.datetime.now()
connected_users = set()

# Command handler functions
def handle_greet(user):
    response = f"Hello, {user}! How can I assist you?"
    return response

def handle_help():
    response = "I'm here to help! Available commands: !greet, !help, !status, !kick, !ban, !clear"
    return response

def handle_status():
    uptime = datetime.datetime.now() - start_time
    formatted_uptime = str(uptime).split('.')[0]  # Format uptime as HH:MM:SS
    num_users = len(connected_users)
    response = f"Bot Uptime: {formatted_uptime} | Connected Users: {num_users}"
    return response

def handle_kick(user, target, is_op):
    if is_op:
        send_irc_message("KICK " + channel + " " + target)
        response = f"{target} has been kicked from the channel."
    else:
        response = "You don't have permission to use this command."
    return response

def handle_ban(user, target, is_op):
    if is_op:
        send_irc_message("MODE " + channel + " +b " + target)
        send_irc_message("KICK " + channel + " " + target)
        response = f"{target} has been banned from the channel."
    else:
        response = "You don't have permission to use this command."
    return response

def handle_clear(user, is_op):
    if is_op:
        # Clear chat history by sending a message with null content
        send_irc_message("PRIVMSG " + channel + " :\x01ACTION clears the chat history\x01")
        response = "Chat history has been cleared."
    else:
        response = "You don't have permission to use this command."
    return response

# Main loop to receive and process messages
while True:
    data = irc.recv(2048).decode("utf-8")

    if data.startswith("PING"):
        send_irc_message("PONG" + data.split()[1])
    elif "PRIVMSG" in data:
        user = data.split('!', 1)[0][1:]
        connected_users.add(user)  # Add user to the set of connected users
        message = ":".join(data.split(':')[2:])
        
        # Check if message is a command
        if message.startswith("!"):
            command = message.split()[0][1:].lower()
            args = message.split()[1:]
            
            # Check if the user is an op
            is_op = "@" in data
            
            # Process command
            if command == "greet":
                response = handle_greet(user)
            elif command == "help":
                response = handle_help()
            elif command == "status":
                response = handle_status()
            elif command == "kick":
                if len(args) >= 1:
                    target = args[0]
                    response = handle_kick(user, target, is_op)
                else:
                    response = "Please specify a user to kick."
            elif command == "ban":
                if len(args) >= 1:
                    target = args[0]
                    response = handle_ban(user, target, is_op)
                else:
                    response = "Please specify a user to ban."
            elif command == "clear":
                response = handle_clear(user, is_op)
            # Add more command handlers here as needed
            
            # Send the response back to the channel
            send_irc_message("PRIVMSG " + channel + " :" + response)
