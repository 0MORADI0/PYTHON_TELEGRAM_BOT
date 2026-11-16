# Telegram Task Manager Bot

A Telegram bot built with Python that helps users organize and manage their daily tasks.

## Features

- Add new tasks through Telegram.
- Display personal task lists.
- Mark tasks as completed.
- Delete existing tasks.
- Interactive inline keyboard buttons.
- Individual task management for each Telegram user.
- Persistent data storage using SQLite.
- Asynchronous message and callback handling.
- Automatic database initialization.

## Technologies

- Python
- python-telegram-bot
- SQLite
- SQL
- Async Programming
- Telegram Bot API

## Project Structure

```text
PYTHON_TELEGRAM_BOT/
│
├── main.py
└── database.py
```

## Installation

Install the required dependency:

```bash
pip install python-telegram-bot
```

## Configuration

Create a Telegram bot using BotFather.

Set your bot token in `main.py`:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN"
```

**Important:** Never publish your real bot token or upload it to GitHub.

## How to Run

Start the bot:

```bash
python main.py
```

Open your bot in Telegram and send:

```text
/start
```

Use the interactive buttons to manage your daily tasks.

## Database

The application automatically creates an SQLite database named `tasks.db`.

Each task is associated with its Telegram user ID, ensuring that users manage their own tasks independently.

## Author

0MORADI0

GitHub: https://github.com/0MORADI0
