import sqlite3
import pygame
from player import Player
from enemy import Enemy
from platform_module import Platform

# Connect to the SQLite database
CONNECTION = sqlite3.connect('save_file.db')
CURSOR = CONNECTION.cursor()

def create_save(player: Player, enemies: list[Enemy], platforms: list[Platform]) -> None:
    """Creates the save file with tables and inserts data."""
    # Create the Player table
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS player (
            player_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            level INTEGER, 
            health INTEGER
        )
    """)

    # Create the Enemies table
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS enemies (
            enemy_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            location_x INTEGER, 
            location_y INTEGER
        )
    """)

    # Create the Platforms table
    CURSOR.execute("""
        CREATE TABLE IF NOT EXISTS platforms (
            platform_id INTEGER PRIMARY KEY AUTOINCREMENT, 
            location_x INTEGER, 
            location_y INTEGER, 
            width INTEGER, 
            height INTEGER
        )
    """)

    # Insert player data
    CURSOR.execute("""
        INSERT INTO player (level, health) 
        VALUES (?, ?)
    """, (player.level, player.health))

    # Insert enemies data
    for enemy in enemies:
        CURSOR.execute("""
            INSERT INTO enemies (location_x, location_y) 
            VALUES (?, ?)
        """, (enemy.rect.x, enemy.rect.y))

    # Insert platforms data
    for platform in platforms:
        CURSOR.execute("""
            INSERT INTO platforms (location_x, location_y, width, height) 
            VALUES (?, ?, ?, ?)
        """, (platform.rect.x, platform.rect.y, platform.rect.width, platform.rect.height))

    # Commit changes to the database
    CONNECTION.commit()


def load_player_save() -> Player:
    """Loads the player data from the save file and returns a Player object."""
    # Check if the player table exists
    CURSOR.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='player'
    """)
    table_exists = CURSOR.fetchone()

    if not table_exists:
        raise ValueError("Player table does not exist in the database.")

    # Retrieve the player data
    CURSOR.execute("SELECT * FROM player")
    player_data = CURSOR.fetchone()  # Fetch the first row

    if not player_data:
        raise ValueError("No player data found in the save file.")

    player = Player(health=player_data[2])
    player.level = player_data[1]

    return player


def load_enemies_save() -> list[Enemy]:
    """Loads the enemies data from the save file and returns a list of Enemy objects."""
    # Check if the enemies table exists
    CURSOR.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='enemies'
    """)
    table_exists = CURSOR.fetchone()

    if not table_exists:
        raise ValueError("Enemies table does not exist in the database.")

    # Retrieve all enemy data
    CURSOR.execute("SELECT * FROM enemies")
    enemies_data = CURSOR.fetchall()

    enemies = []
    for enemy in enemies_data:
        new_enemy = Enemy()  # Create an Enemy object
        new_enemy.set_xy(enemy[1], enemy[2])  # Set x and y positions
        enemies.append(new_enemy)

    return enemies


def load_platforms_save() -> list[Platform]:
    """Loads the platforms data from the save file and returns a list of Platform objects."""
    # Check if the platforms table exists
    CURSOR.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name='platforms'
    """)
    table_exists = CURSOR.fetchone()

    if not table_exists:
        raise ValueError("Platforms table does not exist in the database.")

    # Retrieve all platform data
    CURSOR.execute("SELECT * FROM platforms")
    platforms_data = CURSOR.fetchall()

    platforms = pygame.sprite.Group()
    for platform in platforms_data:
        # Assuming platform columns are (platform_id, location_x, location_y, width, height)
        new_platform = Platform(platform[1], platform[2], platform[3], platform[4])
        platforms.add(new_platform)

    return platforms


def delete_save() -> None:
    """Deletes all tables from the save file."""
    try:
        # Drop the tables if they exist
        CURSOR.execute("DROP TABLE IF EXISTS player")
        CURSOR.execute("DROP TABLE IF EXISTS enemies")
        CURSOR.execute("DROP TABLE IF EXISTS platforms")

        # Commit the changes
        CONNECTION.commit()
        print("Save file deleted successfully.")
    except sqlite3.Error as e:
        print(f"An error occurred while deleting the save file: {e}")
