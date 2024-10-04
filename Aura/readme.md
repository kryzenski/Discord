# AURA - Discord Bot

Overview
AURA is a Discord bot that rewards server members with points based on the reactions they receive on their messages. The more reactions a message gets, the more points the member earns. Positive reactions increase the member's aura points, while negative reactions decrease them.

## Features
Reaction-based point system: Members earn points based on the reactions they receive on their messages.
Positive and negative reactions: Positive reactions (e.g. 👍) increase aura points, while negative reactions (e.g. 👎) decrease them.
Configurable reaction types: Server administrators can customize the reaction types that affect aura points.
## Getting Started
### Prerequisites
A Discord server with the necessary permissions to create and manage roles.
A Discord bot token (obtained through the Discord Developer Portal).

### Installation
Clone this repository to your local machine.
Install the required dependencies using npm install or yarn install.
Create a config.json file with your bot token and other configuration options.
Run the bot using node index.js or npm start.

### Configuration
The bot can be configured through the config.json file. The following options are available:

token: Your Discord bot token.

#### reactionTypes: An object mapping reaction emojis to their point values (e.g. { '👍': 1, '👎': -1 }).
#### pointsPerReaction: The number of points awarded per reaction (default: +10 and -5).

### Contributing
Contributions are welcome! If you'd like to help improve AURA, please fork this repository and submit a pull request.

### License
AURA is open source.

### Your Feedbacks are highly appreciated
