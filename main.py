import socket

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

# User class
class User:
    def __init__(self, username, password, permissions=[]):
        self.username = username
        self.password = password
        self.permissions = permissions

# List of registered users
registered_users = [
    User("user1", "password1", ["greet"]),
    User("user2", "password2", ["greet", "help"])
]

# Command handler functions
def handle_register(user, args):
    if len(args) != 2:
        return "Invalid usage. Please provide a username and password."
    
    username = args[0]
    password = args[1]
    
    # Check if the username is already taken
    for registered_user in registered_users:
        if registered_user.username == username:
            return f"The username '{username}' is already taken."
    
    # Register the user
    registered_users.append(User(username, password))
    return f"Registration successful. Welcome, {username}!"

def handle_login(user, args):
    if len(args) != 2:
        return "Invalid usage. Please provide your username and password."
    
    username = args[0]
    password = args[1]
    
    # Check if the user exists and the password is correct
    for registered_user in registered_users:
        if registered_user.username == username:
            if registered_user.password == password:
                return f"Authentication successful. Welcome back, {username}!"
            else:
                return "Incorrect password. Please try again."
    
    return f"The username '{username}' is not registered."

def handle_greet(user):
    if "greet" in user.permissions:
        response = f"Hello, {user.username}! How can I assist you?"
    else:
        response = "You don't have permission to use this command."
    return response

def handle_help(user):
    if "help" in user.permissions:
        response = "I'm here to help! Available commands: !greet, !help"
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
        message = ":".join(data.split(':')[2:])
        
        # Check if message is a command
        if message.startswith("!"):
            command = message.split()[0][1:].lower()
            args = message.split()[1:]
            
            # Find the user object
            current_user = None
            for registered_user in registered_users:
                if registered_user.username == user:
                    current_user = registered_user
                    break
            
            if not current_user:
                current_user = User(user, "", [])
                registered_users.append(current_user)
            
            # Process command
            if command == "register":
                response = handle_register(current_user, args)
            elif command == "login":
                response = handle_login(current_user, args)
            elif command == "greet":
                response = handle_greet(current_user)
            elif command == "help":
                response = handle_help(current_user)
            # Add more command handlers here as needed
            
            # Send the response back to the channel
            send_irc_message("PRIVMSG " + channel + " :" + response)
