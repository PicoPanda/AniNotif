# ======================================================================
# File: cli.py
# Description: This file contains the CLI for the anime watchlist.
# ======================================================================

import click
from rich.console import Console
from rich.table import Table
from db import Database
from api_requests import get_full_anime_info, parse_anime_info

console = Console()

@click.group()
def cli():
    """Anime Watchlist CLI - Track your favorite anime and get notifications for new episodes!"""
    pass

# -------------------------
# Interactive Mode
# -------------------------
@cli.command()
def interactive():
    """Start interactive mode with guided prompts."""
    while True:
        console.print("\n[bold cyan]What would you like to do?[/bold cyan]")
        table = Table(show_header=False, box=None)
        table.add_row("[1] Initialize database")
        table.add_row("[2] Manage users")
        table.add_row("[3] Manage anime")
        table.add_row("[4] Manage watchlist")
        table.add_row("[5] Manage releases")
        table.add_row("[q] Quit")
        console.print(table)
        
        choice = click.prompt("Enter your choice", type=str)
        
        if choice == 'q':
            break
        elif choice == '1':
            db = Database()
            if click.confirm("Initialize/reset the database?"):
                db.init_db()
        elif choice == '2':
            _handle_user_menu()
        elif choice == '3':
            _handle_anime_menu()
        elif choice == '4':
            _handle_watchlist_menu()
        elif choice == '5':
            _handle_release_menu()

def _handle_user_menu():
    """Handle user management menu."""
    while True:
        console.print("\n[bold cyan]User Management[/bold cyan]")
        table = Table(show_header=False, box=None)
        table.add_row("[1] Add new user")
        table.add_row("[2] View user")
        table.add_row("[3] Update user")
        table.add_row("[4] Delete user")
        table.add_row("[b] Back")
        console.print(table)
        
        choice = click.prompt("Enter your choice", type=str)
        
        if choice == 'b':
            break
        elif choice == '1':
            mal_user_id = click.prompt("Enter MAL user ID", type=str)
            db = Database()
            if db.create_user(mal_user_id):
                console.print("[green]User added successfully![/green]")
            else:
                console.print("[red]Failed to add user.[/red]")
        elif choice == '2':
            user_id = click.prompt("Enter user ID", type=int)
            db = Database()
            user = db.get_user(user_id)
            if user:
                console.print(f"[green]User found:[/green] {user}")
            else:
                console.print("[red]User not found.[/red]")

def _handle_anime_menu():
    """Handle anime management menu."""
    while True:
        console.print("\n[bold cyan]Anime Management[/bold cyan]")
        table = Table(show_header=False, box=None)
        table.add_row("[1] Add anime by MAL ID")
        table.add_row("[2] View anime")
        table.add_row("[3] Update anime")
        table.add_row("[4] Delete anime")
        table.add_row("[b] Back")
        console.print(table)
        
        choice = click.prompt("Enter your choice", type=str)
        
        if choice == 'b':
            break
        elif choice == '1':
            mal_id = click.prompt("Enter MAL ID", type=int)
            try:
                anime_info = get_full_anime_info(mal_id)
                parsed_info = parse_anime_info(anime_info)
                
                # Show fetched information
                console.print("\n[bold cyan]Fetched Anime Information:[/bold cyan]")
                for key, value in parsed_info.items():
                    console.print(f"[green]{key}:[/green] {value}")
                
                if click.confirm("\nAdd this anime to database?"):
                    db = Database()
                    if db.create_anime(**parsed_info):
                        console.print("[green]Anime added successfully![/green]")
                        
                        # Prompt to add to watchlist
                        if click.confirm("\nWould you like to add this anime to your watchlist?"):
                            user_id = click.prompt("Enter your user ID", type=int)
                            # Get the anime ID (it should be 1 if it's the first anime, but better to search for it)
                            cursor = db._connect().cursor()
                            cursor.execute("SELECT id FROM anime WHERE mal_id = ?", (parsed_info['mal_id'],))
                            anime_id = cursor.fetchone()[0]
                            
                            last_watched = click.prompt("How many episodes have you watched?", type=int, default=0)
                            
                            if db.add_to_watchlist(user_id, anime_id, last_watched):
                                console.print("[green]Added to watchlist![/green]")
                            else:
                                console.print("[red]Failed to add to watchlist.[/red]")
                    else:
                        console.print("[red]Failed to add anime.[/red]")
            except Exception as e:
                console.print(f"[red]Error fetching anime info: {str(e)}[/red]")

def _handle_watchlist_menu():
    """Handle watchlist management menu."""
    while True:
        console.print("\n[bold cyan]Watchlist Management[/bold cyan]")
        table = Table(show_header=False, box=None)
        table.add_row("[1] Add anime to watchlist")
        table.add_row("[2] View watchlist")
        table.add_row("[3] Update watched episodes")
        table.add_row("[4] Remove from watchlist")
        table.add_row("[b] Back")
        console.print(table)
        
        choice = click.prompt("Enter your choice", type=str)
        
        if choice == 'b':
            break
        elif choice == '1':
            user_id = click.prompt("Enter user ID", type=int)
            anime_id = click.prompt("Enter anime ID", type=int)
            last_watched = click.prompt("Last watched episode", type=int, default=0)
            
            db = Database()
            if db.add_to_watchlist(user_id, anime_id, last_watched):
                console.print("[green]Added to watchlist![/green]")
            else:
                console.print("[red]Failed to add to watchlist.[/red]")

def _handle_release_menu():
    """Handle release management menu."""
    while True:
        console.print("\n[bold cyan]Release Management[/bold cyan]")
        table = Table(show_header=False, box=None)
        table.add_row("[1] Add new release")
        table.add_row("[2] View release")
        table.add_row("[3] Update release")
        table.add_row("[4] Delete release")
        table.add_row("[b] Back")
        console.print(table)
        
        choice = click.prompt("Enter your choice", type=str)
        
        if choice == 'b':
            break

# -------------------------
# Simplified Direct Commands
# -------------------------
@cli.command('init-db')
def init_db_command():
    """Initialize the SQLite database."""
    if click.confirm("Initialize/reset the database?"):
        db = Database()
        db.init_db()

@cli.command('add-anime')
@click.option('--mal_id', type=int, prompt='Enter MAL ID', help='MAL ID for the anime')
def add_anime_command(mal_id):
    """Add a new anime by MAL ID."""
    try:
        anime_info = get_full_anime_info(mal_id)
        parsed_info = parse_anime_info(anime_info)
        
        # Show fetched information
        console.print("\n[bold cyan]Fetched Anime Information:[/bold cyan]")
        for key, value in parsed_info.items():
            console.print(f"[green]{key}:[/green] {value}")
        
        if click.confirm("\nAdd this anime to database?"):
            db = Database()
            if db.create_anime(**parsed_info):
                console.print("[green]Anime added successfully![/green]")
                
                # Prompt to add to watchlist
                if click.confirm("\nWould you like to add this anime to your watchlist?"):
                    user_id = click.prompt("Enter your user ID", type=int)
                    # Get the anime ID
                    cursor = db._connect().cursor()
                    cursor.execute("SELECT id FROM anime WHERE mal_id = ?", (parsed_info['mal_id'],))
                    anime_id = cursor.fetchone()[0]
                    
                    last_watched = click.prompt("How many episodes have you watched?", type=int, default=0)
                    
                    if db.add_to_watchlist(user_id, anime_id, last_watched):
                        console.print("[green]Added to watchlist![/green]")
                    else:
                        console.print("[red]Failed to add to watchlist.[/red]")
            else:
                console.print("[red]Failed to add anime.[/red]")
    except Exception as e:
        console.print(f"[red]Error fetching anime info: {str(e)}[/red]")

@cli.command('add-user')
@click.option('--mal_user_id', prompt='Enter MAL username', help='MAL user identifier')
def add_user(mal_user_id):
    """Create a new user."""
    db = Database()
    if db.create_user(mal_user_id):
        console.print(f"[green]User {mal_user_id} added successfully.[/green]")
    else:
        console.print("[red]Failed to add user.[/red]")

@cli.command('add-to-watchlist')
@click.option('--user_id', type=int, prompt='Enter user ID', help='User ID')
@click.option('--anime_id', type=int, prompt='Enter anime ID', help='Anime ID')
@click.option('--last_watched_episode', type=int, prompt='Last watched episode', default=0, help='Last watched episode')
def add_watchlist(user_id, anime_id, last_watched_episode):
    """Add an anime to a user's watchlist."""
    db = Database()
    if db.add_to_watchlist(user_id, anime_id, last_watched_episode):
        console.print(f"[green]Anime ID {anime_id} added to user ID {user_id} watchlist.[/green]")
    else:
        console.print("[red]Failed to add to watchlist.[/red]")

if __name__ == '__main__':
    cli()