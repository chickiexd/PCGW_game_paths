# PCGW Parser

A CLI tool to fetch and parse game configuration and save directory paths from PCGamingWiki into a local SQLite database.

## Acknowledgements

This project makes use of data from [PCGamingWiki](https://www.pcgamingwiki.com/), a community-driven resource that documents PC games, their settings, configuration files, and save data locations.
All game path and configuration information is sourced from PCGamingWiki contributors.

## Features

- Fetches game list and game data (config and saves paths) using the PCGamingWiki API.
- Parses "Game data" sections to extract config and save directory information.
- Stores game and directory mappings in an SQLite database.

## Requirements

- Python 3.6 or higher
- requests
- tqdm

## Installation

```bash
pip install requests tqdm
```

Fetch and process new games:

```bash
python main.py
```

## Project Structure

- `main.py`: Entry point that triggers game data fetching.
- `games.py`: Contains the `GameData` class for database and API interactions.
- `games.txt`: Sample list of game titles.
- `pcgw_games.db`: SQLite database file (generated after initialization).
- `LICENSE`: MIT License for this project.

## Database Schema

```mermaid
erDiagram
    games {
        INTEGER id PK
        TEXT name UNIQUE
    }
    directory_paths {
        INTEGER id PK
        TEXT path UNIQUE
    }
    game_paths {
        INTEGER game_id FK
        INTEGER path_id FK
        TEXT type
        TEXT os
    }
    games ||--o{ game_paths : has
    directory_paths ||--o{ game_paths : has
```

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
