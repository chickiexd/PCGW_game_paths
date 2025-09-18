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

**Games**

| Column | Type    | Notes  |
| ------ | ------- | ------ |
| id     | INTEGER | PK     |
| name   | TEXT    | Unique |

**Directory Paths**

| Column | Type    | Notes  |
| ------ | ------- | ------ |
| id     | INTEGER | PK     |
| path   | TEXT    | Unique |

**Game Paths**

| Column   | Type    | Notes                    |
| -------- | ------- | ------------------------ |
| game\_id | INTEGER | FK → games.id            |
| path\_id | INTEGER | FK → directory\_paths.id |
| type     | TEXT    | e.g., 'config' or 'save' |
| os       | TEXT    | Windows/Linux/etc        |


## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
