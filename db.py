# ======================================================================
# File: db.py
# Description: This file initializes an SQLite database to track an anime watchlist
# and provides CRUD operations for users, anime, watchlist, and releases.
# It also exposes a CLI command (using click) to initialize the database via the Database class.
# ======================================================================

import sqlite3
import os
import click
from rich.console import Console

# Database file name
DB_NAME = "anime_watchlist.db"

# Rich console for colored output
console = Console()

# ----------------------------------------------------------------------
# Database Operations Class (CRUD operations and initialization)
# ----------------------------------------------------------------------

class Database:
    """Class that encapsulates CRUD operations and initialization for the database."""
    def __init__(self, db_name=DB_NAME):
        self.db_name = db_name

    def _connect(self):
        """Create and return a new database connection."""
        return sqlite3.connect(self.db_name)

    def init_db(self):
        """Create and initialize all necessary tables in the database if they do not exist."""
        conn = self._connect()
        cursor = conn.cursor()

        # Create 'users' table
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mal_user_id TEXT UNIQUE NOT NULL
        )
        ''')

        # Create 'anime' table with details from the Jikan API
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS anime (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mal_id INTEGER UNIQUE NOT NULL,
            title TEXT NOT NULL,
            synopsis TEXT,
            episodes INTEGER,
            status TEXT,
            aired_from TEXT,
            aired_to TEXT,
            broadcast TEXT
        )
        ''')

        # Create 'watchlist' table to link users and anime
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS watchlist (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            anime_id INTEGER,
            added_on TEXT DEFAULT CURRENT_TIMESTAMP,
            last_watched_episode INTEGER DEFAULT 0,
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(anime_id) REFERENCES anime(id)
        )
        ''')

        # Create 'releases' table to track episode release dates
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS releases (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            anime_id INTEGER,
            episode_number INTEGER,
            release_date TEXT,
            broadcast TEXT,
            FOREIGN KEY(anime_id) REFERENCES anime(id),
            FOREIGN KEY (broadcast) REFERENCES anime(broadcast)
        )
        ''')

        conn.commit()
        conn.close()
        console.print("[green]Database initialized successfully.[/green]")

    # ---------------------
    # Users Table Operations
    # ---------------------
    def create_user(self, mal_user_id):
        """Create a new user with the given mal_user_id. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (mal_user_id) VALUES (?)", (mal_user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def get_user(self, user_id):
        """Retrieve a user by id. Returns the user record or False if there is an error."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            return False

    def update_user(self, user_id, new_mal_user_id):
        """Update a user's mal_user_id. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET mal_user_id = ? WHERE id = ?", (new_mal_user_id, user_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def delete_user(self, user_id):
        """Delete a user by id. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    # ---------------------
    # Anime Table Operations
    # ---------------------
    def create_anime(self, mal_id, title, synopsis, episodes, status, aired_from, aired_to, broadcast):
        """Create a new anime entry. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO anime (mal_id, title, synopsis, episodes, status, aired_from, aired_to, broadcast) VALUES (?,?,?,?,?,?,?,?)", 
                           (mal_id, title, synopsis, episodes, status, aired_from, aired_to, broadcast))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def get_anime(self, anime_id):
        """Retrieve an anime record by id. Returns the record or False if there is an error."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM anime WHERE id = ?", (anime_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            return False

    def update_anime(self, anime_id, **kwargs): # TO REDO
        """Update an anime record using keyword arguments for fields to update. Returns True if successful."""
        try:
            columns = []
            values = []
            for key, value in kwargs.items():
                columns.append(f"{key} = ?")
                values.append(value)
            if not columns:
                return False
            values.append(anime_id)
            sql = f"UPDATE anime SET {', '.join(columns)} WHERE id = ?"
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(sql, tuple(values))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def delete_anime(self, anime_id):
        """Delete an anime record by id. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM anime WHERE id = ?", (anime_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    # --------------------------
    # Watchlist Table Operations
    # --------------------------
    def add_to_watchlist(self, user_id, anime_id, last_watched_episode=0):
        """Add an anime to a user's watchlist. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO watchlist (user_id, anime_id, last_watched_episode) VALUES (?,?,?)", 
                           (user_id, anime_id, last_watched_episode))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def get_watchlist(self, user_id):
        """Retrieve all watchlist entries for a given user. Returns a list of records or False if there is an error."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM watchlist WHERE user_id = ?", (user_id,))
            results = cursor.fetchall()
            conn.close()
            return results
        except Exception as e:
            return False

    def update_watchlist(self, watchlist_id, last_watched_episode):
        """Update a watchlist entry's last watched episode. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("UPDATE watchlist SET last_watched_episode = ? WHERE id = ?", (last_watched_episode, watchlist_id))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def delete_from_watchlist(self, watchlist_id):
        """Delete a watchlist entry by id. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM watchlist WHERE id = ?", (watchlist_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    # -------------------------
    # Releases Table Operations
    # -------------------------
    def add_release(self, anime_id, episode_number, release_date, broadcast):
        """Add a new release entry for an anime. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO releases (anime_id, episode_number, release_date, broadcast) VALUES (?,?,?,?)", 
                           (anime_id, episode_number, release_date, broadcast))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def get_release(self, release_id):
        """Retrieve a release record by id. Returns the record or False if there is an error."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM releases WHERE id = ?", (release_id,))
            result = cursor.fetchone()
            conn.close()
            return result
        except Exception as e:
            return False

    def update_release(self, release_id, **kwargs):
        """Update a release record using keyword arguments for fields to update. Returns True if successful."""
        try:
            columns = []
            values = []
            for key, value in kwargs.items():
                columns.append(f"{key} = ?")
                values.append(value)
            if not columns:
                return False
            values.append(release_id)
            sql = f"UPDATE releases SET {', '.join(columns)} WHERE id = ?"
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute(sql, tuple(values))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False

    def delete_release(self, release_id):
        """Delete a release record by id. Returns True if successful."""
        try:
            conn = self._connect()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM releases WHERE id = ?", (release_id,))
            conn.commit()
            conn.close()
            return True
        except Exception as e:
            return False


# ----------------------------------------------------------------------
# If file ran directly, initialize the database                        
# ----------------------------------------------------------------------

@click.command()
def init_db():
    """CLI command to initialize the SQLite database via the Database class."""
    if os.path.exists(DB_NAME):
        console.print(f"[yellow]Database {DB_NAME} already exists.[/yellow]")
    else:
        db = Database()
        db.init_db()


if __name__ == '__main__':
    init_db()
    