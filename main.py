import socket
import datetime
# IRC server information
server = "irc.libera.chat"
port = 6667
channel = "#HackerIdiot"
bot_name = "HackerIdiot_bot"

# Connect to the IRC server
irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
irc.connect((server, port))

# Send IRC commands
def send_irc_message(message):
    irc.send((message + "\n").encode("utf-8"))

send_irc_message("NICK " + bot_name)
send_irc_message("USER " + bot_name + " 0 * :" + bot_name)
send_irc_message("JOIN " + channel)

# Global variables for tracking bot status
start_time = datetime.datetime.now()
connected_users = set()

# Command handler functions
def handle_greet(user):
    response = f"Hello, {user}! How can I assist you?"
    return response

def handle_help():
    response = "I'm here to help! Available commands: !greet, !help, !status"
    return response

def handle_status():
    uptime = datetime.datetime.now() - start_time
    formatted_uptime = str(uptime).split('.')[0]  # Format uptime as HH:MM:SS
    num_users = len(connected_users)
    response = f"Bot Uptime: {formatted_uptime} | Connected Users: {num_users}"
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
            
            # Process command
            if command == "greet":
                response = handle_greet(user)
            elif command == "help":
                response = handle_help()
            elif command == "status":
                response = handle_status()
            # Add more command handlers here as needed
            
            # Send the response back to the channel
            send_irc_message("PRIVMSG " + channel + " :" + response)
