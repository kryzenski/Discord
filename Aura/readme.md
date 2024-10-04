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

## Explanation:
#### Tracking Points:

The bot uses a dictionary aura_points to store each member's points. The keys are Discord member objects, and the values are their corresponding points.
Positive and Negative Reactions:

You can modify positive_reactions and negative_reactions lists to include the specific emojis you want to use for positive and negative feedback. By default, common emojis like 👍, ❤️, and 👎 are used.
Reaction Events:

on_reaction_add: This event triggers whenever a reaction is added to a message. The bot checks if the reaction is positive or negative and adjusts the author's points accordingly.
on_reaction_remove: This event triggers whenever a reaction is removed. The bot adjusts the points accordingly, reversing the effect of the reaction.
Commands:

#### !points [member]: Allows a user to check their aura points or another member's points if specified.
#### !leaderboard: Displays a leaderboard of users and their points in descending order.

### Token:

Replace YOUR_BOT_TOKEN with your actual Discord bot token from the Discord Developer Portal.
Running the Bot:
Ensure you have your bot token.
Install the required libraries with pip install discord.py.
Run the Python script, and invite your bot to a server where you can start tracking and rewarding users based on reactions.
This bot will now track points based on the type of reactions users receive on their messages!

### Contributing
Contributions are welcome! If you'd like to help improve AURA, please fork this repository and submit a pull request.

### License
AURA is open source.

### Your Feedbacks are highly appreciated
