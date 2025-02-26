# 🎬 Movie Search Telegram Bot

A **Telegram bot** that allows users to search for movies by **actors, genres, and years**. The bot also keeps track of the most popular queries.

## 🚀 Features

- **Search by Actor** – find movies by actor's name.
- **Search by Genre & Year** – browse movies by categories and release years.
- **Random Movie** – get a random movie suggestion.
- **Top Queries Tracking** – displays the most searched terms.
- **Multilingual Support** – switch between Russian, English, and German languages.

## 🛠️ Installation

## 1️⃣ Clone the repository

## git clone https://github.com/gasanovdominik/bot
## cd bot

## 2️⃣ Install dependencies
### Install the required dependencies:
### pip install -r requirements.txt
### pip install python-telegram-bot
### pip install mysql-connector-python
### pip install requests
### pip install python-dotenv

## 3️⃣ Configure the bot
### Copy the example configuration file and update it with your Telegram bot token and MySQL database credentials:
### cp config_example.ini config.ini
### Edit config.ini:


## [TELEGRAM]
### TOKEN = 7903480173:AAHGN_WGifcJDawEFKMafGyyfieHybLIxoo

## [DATABASE]
### HOST = ich-db.ccegls0svc9m.eu-central-1.rds.amazonaws.com
### USER = ich1
### PASSWORD = password
### DBNAME = sakila

## 4️⃣ Run the bot

### python main.py

## 📌 Usage
Start the bot by sending the /start command. The bot will present a menu with several options:

### 🎲 Random Movie – Get a random movie suggestion.
### 🔎 Search by Actor – Enter an actor's name to find movies they starred in.
### 🎭 Search by Genre – Select a genre to browse movies.
### 📅 Search by Year – Enter a year to find movies released in that year.
### 📊 Popular Queries – View the most searched queries.
### 🌐 Change Language – Switch the bot's language between Russian, English, and German.
## 📄 License
### MIT License. Feel free to use and modify.
