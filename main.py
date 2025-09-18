import requests
import re
from games import GameData


def get_game_data(game):
    url = "https://www.pcgamingwiki.com/w/api.php"
    params = {
        "action": "parse",
        "page": game,
        "prop": "wikitext",
        "format": "json",
    }

    data = requests.get(url, params=params).json()
    wikitext = data["parse"]["wikitext"]["*"]

    # extract the blocktext starting at "==Game data==" and ending before the next "=="
    match = re.search(r"==Game data==.*?(?=\n==[^=])", wikitext, flags=re.S)
    if match:
        game_data_block = match.group(0)

    game_data_block = game_data_block.split("\n")
    game_data = {}
    config_locations = {}
    save_locations = {}
    game_data["config"] = config_locations
    game_data["saves"] = save_locations
    # print(game_data_block)
    for b in game_data_block:
        if "Game data/config" in b:
            splits = b.split("|")
            config_locations[splits[1]] = "".join(b.split("|")[2:]).strip("}")
        if "Game data/saves" in b:
            splits = b.split("|")
            save_locations[splits[1]] = "".join(b.split("|")[2:]).strip("}")

    result = [config_locations, save_locations]

    return game_data


# conn = sqlite3.connect("pcgw_games.db")
# cur = conn.cursor()
#
# # Create table (if it doesn't exist)
# cur.execute(
#     """
# CREATE TABLE IF NOT EXISTS games (
#     id INTEGER PRIMARY KEY AUTOINCREMENT,
#     name TEXT UNIQUE
# )
# """
# )
#
# # Insert games
# for game in games:
#     try:
#         cur.execute("INSERT OR IGNORE INTO games (name) VALUES (?)", (game,))
#     except sqlite3.Error as e:
#         print(f"Error inserting {game}: {e}")
#
# conn.commit()
# conn.close()


def main():
    # game = "Counter-Strike"
    # result = get_game_data(game)
    # print(result)
    # game = "Elden Ring"
    # result = get_game_data(game)
    # print(result)
    # update_games_list()
    # update_db_with_new_game_data()
    # get
    game_data = GameData()
    game_data.fetch_new_games()
    # game_data.get_current_games()
    # game_data.init_db()
    # game_data.update_games_list(["Counter-Strike", "Elden Ring"])


if __name__ == "__main__":
    main()
