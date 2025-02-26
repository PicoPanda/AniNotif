# CLI Guide for Anime Watchlist Application

This document explains how the command-line interface (CLI) will interact with the database through the cli.py file using click.

## Overview

The CLI application will serve as the primary interface for users to interact with the anime watchlist database. It leverages the [click](https://click.palletsprojects.com/) library to provide an organized, user-friendly command set. The commands will internally call methods from the `Database` class (in db.py) to perform CRUD operations.

## CLI Command Structure

The CLI will be organized into several main commands, including (but not limited to):

1. **Initialization Command**
   - **Command:** `init-db`
   - **Description:** Initializes the SQLite database by creating necessary tables. Calls the `init_db()` method of the `Database` class.

2. **User Commands**
   - **add-user**: Create a new user with a given identifier (e.g., MAL username).
   - **get-user**: Retrieve information about a user using the user ID.
   - **update-user**: Update a user's details.
   - **delete-user**: Delete a user from the database.

3. **Anime Commands**
   - **add-anime**: Add a new anime entry into the database. This command will integrate with the Jikan API to fetch additional anime details if necessary.
   - **get-anime**: Retrieve details of an anime by its database ID.
   - **update-anime**: Update details of an existing anime record.
   - **delete-anime**: Remove an anime record from the database.

4. **Watchlist Commands**
   - **add-watchlist**: Add an anime to a user's watchlist.
   - **get-watchlist**: View a user's watchlist.
   - **update-watchlist**: Update watchlist details such as last watched episode
   - **delete-watchlist**: Remove an entry from the watchlist.

5. **Release Commands**
   - **add-release**: Record a new anime episode release with details like episode number and release time.
   - **get-release**: Retrieve details of a specific release.
   - **update-release**: Update release details.
   - **delete-release**: Remove a release record.

## Interaction Flow

- **Initialization**: The user first runs the `init-db` command to set up the database tables. If the database file already exists, an informational message is displayed.

- **User Management**: Commands under user management allow the creation and modification of user records. For instance, `add-user` will prompt the user for details and then call `Database.create_user()`.

- **Anime Management**: Similar to user management, anime management commands will provide a way to add and modify anime records. These commands may integrate with functions like `get_full_anime_info` from api_requests.py to retrieve data from the Jikan API before adding an entry.

- **Watchlist**: Users can maintain their watchlist by adding, viewing, and updating the status of anime via the watchlist commands. This includes tracking the latest episode watched.

- **Releases**: Release commands handle operations related to recording when a new episode is out. For example, `add-release` will add a new release record which could be used in conjunction with notifications.

## CLI Implementation Guidelines

- **Modular Command Functions:** Organize your CLI commands into functions within cli.py. Group commands by their domain (users, anime, watchlist, releases).

- **Use Click Groups:** Consider using click's group functionality to create a main CLI group, under which subcommands (like user, anime, etc.) are registered. This improves organization and usability.

- **Error Handling:** Each command should gracefully handle errors, providing clear messages if something goes wrong (e.g., database connection issues, validation errors).

- **Feedback:** Make use of rich console outputs to provide colored feedback on the success or failure of operations.

- **Integration with Database:** Each CLI command should instantiate the `Database` class and call appropriate methods to perform operations.

## Example Command Usage

- Initialization:
  ```
  python cli.py init-db
  ```

- Adding a user:
  ```
  python cli.py add-user --mal_user_id john_doe
  ```

- Adding an anime:
  ```
  python cli.py add-anime --mal_id 123 --title "My Anime" --synopsis "An awesome anime." --episodes 12 --status "Finished" --aired_from "2020-01-01" --aired_to "2020-03-01" --broadcast "Sundays at 8 PM"
  ```

This guide should serve as a blueprint for implementing the CLI in cli.py. Use it to define the commands, their arguments, and how each command communicates with the backend Database class. 