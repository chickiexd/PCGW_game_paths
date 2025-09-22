import requests
import sqlite3
import re

from tqdm import tqdm


class GameData:
    def __init__(self, url=None, db_path=None):
        self.url = "https://www.pcgamingwiki.com/w/api.php"
        self.db_path = db_path if db_path else "./pcgw_games.db"
        self.games_list = self.get_current_games()
        self.init_db()

    def init_db(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.executescript(
            """
            CREATE TABLE IF NOT EXISTS games (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS directory_paths (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                path TEXT UNIQUE
            );

            CREATE TABLE IF NOT EXISTS game_paths (
                game_id INTEGER,
                path_id INTEGER,
                type TEXT,
                os TEXT,
                FOREIGN KEY (game_id) REFERENCES games(id),
                FOREIGN KEY (path_id) REFERENCES directory_paths(id),
                UNIQUE(game_id, path_id, type)
            );
            """
        )
        conn.commit()
        conn.close()

    def get_current_games(self):
        conn = sqlite3.connect(self.db_path)
        cur = conn.cursor()
        cur.execute("SELECT name FROM games")
        games = [row[0] for row in cur.fetchall()]
        conn.close()
        return games

    def fetch_new_games(self):
        params = {
            "action": "cargoquery",
            "format": "json",
            "tables": "Infobox_game",
            "fields": "_pageName=Name",
            "limit": "500",
            "offset": "0",
        }
        games = []
        offset = 0

        pbar = tqdm(desc="Fetching Game List", unit="games")
        while True:
            params["offset"] = str(offset)
            r = requests.get(self.url, params=params)
            data = r.json()
            results = data.get("cargoquery", [])
            if not results:
                break
            for entry in results:
                games.append(entry["title"]["Name"])
            offset += len(results)
            pbar.update(len(results))
        pbar.close()

        new_games = list(set(games) - set(self.games_list))
        print(f"Found {len(new_games)} new games.")
        if new_games:
            self.update_games_list(new_games)

    def update_games_list(self, new_games):
        for game in tqdm(new_games, desc="Processing New Games", unit="games"):
            self.insert_game_name_only(game)
            game_data = self.get_game_data(game)
            if not game_data:
                continue
            for path_type in game_data:
                for os in game_data.get(path_type):
                    if not game_data[path_type][os]:
                        continue
                    self.insert_game_data(game, path_type, os, game_data[path_type][os])
                    self.games_list.append(game)

    def insert_game_name_only(self, game):
        conn = sqlite3.connect(self.db_path)
        try:
            with conn:
                conn.execute("INSERT OR IGNORE INTO games (name) VALUES (?)", (game,))
        except Exception as e:
            print(f"Error inserting game name {game}: {e}")
        finally:
            conn.close()

    def insert_game_data(self, game, path_type, os, path):
        conn = sqlite3.connect(self.db_path)
        try:
            with conn:
                conn.execute("INSERT OR IGNORE INTO games (name) VALUES (?)", (game,))
                conn.execute(
                    "INSERT OR IGNORE INTO directory_paths (path) VALUES (?)", (path,)
                )
                game_id = conn.execute(
                    "SELECT id FROM games WHERE name = ?", (game,)
                ).fetchone()[0]
                path_id = conn.execute(
                    "SELECT id FROM directory_paths WHERE path = ?", (path,)
                ).fetchone()[0]
                conn.execute(
                    "INSERT OR IGNORE INTO game_paths (game_id, path_id, type, os) VALUES (?, ?, ?, ?)",
                    (game_id, path_id, path_type, os),
                )
        except Exception as e:
            print(f"Error inserting data for {game}: {e}")
        finally:
            conn.close()

    def get_game_data(self, game):
        params = {
            "action": "parse",
            "page": game,
            "prop": "wikitext",
            "format": "json",
        }

        try:
            data = requests.get(self.url, params=params).json()
        except Exception:
            return None
        wikitext = data["parse"]["wikitext"]["*"]

        match = re.search(r"==Game data==.*?(?=\n==[^=])", wikitext, flags=re.S)
        game_data_block = ""
        if match:
            game_data_block = match.group(0)
        if not game_data_block:
            print(f"No game data found for {game}")
            return None

        game_data_block = game_data_block.split("\n")
        game_data = {}
        config_locations = {}
        save_locations = {}
        game_data["config"] = config_locations
        game_data["saves"] = save_locations
        for b in game_data_block:
            if "Game data/config" in b:
                splits = b.split("|")
                if len(splits) > 2:
                    config_locations[splits[1]] = "".join(b.split("|")[2:])[:-2]
            if "Game data/saves" in b:
                splits = b.split("|")
                if len(splits) > 2:
                    save_locations[splits[1]] = "".join(b.split("|")[2:])[:-2]

        return game_data
