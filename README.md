

# IRC Bot

This is a simple IRC bot written in Python. The bot connects to an IRC server, joins a specified channel, and responds to various commands. It provides basic moderation features such as greeting users, kicking and banning users, clearing chat history, and displaying bot status.

## Prerequisites

- Python 3.x
- socket module

## Usage

1. Clone the repository:

   ```shell
   git clone https://github.com/mrfoxie/ircbot.git
   ```

2. Navigate to the project directory:

   ```shell
   cd ircbot
   ```

3. Open `main.py` and modify the following variables according to your desired IRC server and channel:

   ```python
   server = "irc.libera.chat"
   port = 6667
   channel = "#HackerIdiot"
   bot_name = "HackerIdiot_bot"
   ```

4. Run the bot:

   ```shell
   python main.py
   ```

5. The bot will connect to the IRC server, join the specified channel, and start listening for commands.

## Available Commands

- `!greet`: Greets the user with a welcome message.
- `!help`: Displays a list of available commands.
- `!status`: Shows the bot's uptime and the number of connected users.
- `!kick <user>`: Kicks the specified user from the channel (requires operator privileges).
- `!ban <user>`: Bans the specified user from the channel (requires operator privileges).
- `!clear`: Clears the chat history (requires operator privileges).

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-new-feature`
3. Make your changes and commit them: `git commit -am 'Add some feature'`
4. Push to the branch: `git push origin my-new-feature`
5. Submit a pull request.

## License

This project is licensed under the [MIT License](LICENSE).

You can copy the above Markdown content and save it as `README.md` in the root directory of your "mrfoxie/ircbot" repository. Feel free to customize it further based on your specific needs and provide additional information about your project if desired.
