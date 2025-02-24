# 🎬 Movie Search Telegram Bot

A **Telegram bot** that allows users to search for movies by **actors, genres, and years**. The bot also keeps track of the most popular queries.

## 🚀 Features

- **Search by Actor** – find movies by actor's name.
- **Search by Genre & Year** – browse movies by categories and release years.
- **Random Movie** – get a random movie suggestion.
- **Top Queries Tracking** – displays the most searched terms.
- **Multilingual Support** – switch between Russian, English, and German languages.

## 🛠️ Installation

### 1️⃣ Clone the repository

git clone https://github.com/yourusername/your-repo-name
cd your-repo-name

### 2️⃣ Install dependencies
Install the required dependencies:


pip install -r requirements.txt
### 3️⃣ Configure the bot
Copy the example configuration file and update it with your Telegram bot token and MySQL database credentials:


cp config_example.ini config.ini
Edit config.ini:


[TELEGRAM]
TOKEN = YOUR_TELEGRAM_BOT_TOKEN

[DATABASE]
HOST = YOUR_DATABASE_HOST
USER = YOUR_DATABASE_USER
PASSWORD = YOUR_DATABASE_PASSWORD
DBNAME = YOUR_DATABASE_NAME
### 4️⃣ Run the bot

python main.py
## 📌 Usage
Start the bot by sending the /start command. The bot will present a menu with several options:

🎲 Random Movie – Get a random movie suggestion.
🔎 Search by Actor – Enter an actor's name to find movies they starred in.
🎭 Search by Genre – Select a genre to browse movies.
📅 Search by Year – Enter a year to find movies released in that year.
📊 Popular Queries – View the most searched queries.
🌐 Change Language – Switch the bot's language between Russian, English, and German.
## 📄 License
MIT License. Feel free to use and modify.
