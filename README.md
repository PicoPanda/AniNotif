# 📺 AniNoti - Anime Watchlist & Notification System

A personal project to track anime watchlists and receive notifications for new episode releases, built with Python.

## 🌟 Features

- 🗃️ **Database Management**
  - SQLite database for storing anime, users, watchlists, and release information
  - Integration with Jikan API (MyAnimeList)
  - CRUD operations for all entities

- 🖥️ **CLI Interface**
  - Interactive menu-driven interface
  - Direct commands for quick actions
  - User-friendly prompts and confirmations
  - Colored output for better readability

- 📱 **Notifications**
  - Desktop notifications for new episode releases
  - Customizable notification settings
  - macOS notification support

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- pip (Python package manager)

### Installation

1. Clone the repository
```bash
git clone <repository-url>
cd AniNoti
```

2. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate  # On Unix/macOS
# or
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

### 🎮 Usage

1. Initialize the database:
```bash
python cli.py init-db
```

2. Start the interactive interface:
```bash
python cli.py interactive
```

3. Or use direct commands:
```bash
# Add a new user
python cli.py add-user

# Add an anime by MAL ID
python cli.py add-anime --mal_id <id>

# Add to watchlist
python cli.py add-to-watchlist
```

## 🛠️ Project Structure

```
AniNoti/
├── db.py           # Database operations and initialization
├── cli.py          # Command-line interface
├── api_requests.py # Jikan API integration
├── notifications.py # Notification system
└── requirements.txt # Project dependencies
```

## 📚 API Reference

This project uses the [Jikan API v4](https://docs.api.jikan.moe/) for fetching anime information from MyAnimeList.

## 🤝 Contributing

This is a personal project, but suggestions and feedback are welcome! Feel free to:
1. Report bugs
2. Suggest new features
3. Improve documentation

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- [Jikan API](https://jikan.moe/) for providing MyAnimeList data
- [Click](https://click.palletsprojects.com/) for the CLI framework
- [Rich](https://rich.readthedocs.io/) for beautiful terminal formatting 