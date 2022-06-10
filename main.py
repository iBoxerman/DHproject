from get_data import get_show, get_episodes, get_seasons
import pandas as pd


def find_occ(credit):
    allowed_occupations = ['nurse', 'dr']  # lower case only


def build_row(data, ):
    pass


def handle_episode(show, season, episode):
    pass


shows = ["ER", "Scrubs", "Grey's Anatomy", "The Good Doctor"]
for show in shows:
    show = get_show(show)
    seasons = get_seasons(show)
    for season_number, season_info in enumerate(seasons, start=1):
        episodes = get_episodes(show["id"], season_number, season_info)
        for _, episode in enumerate(episodes, start=1):
            handle_episode(show, season_info, episode)
        print(f'done {show["name"]}/{season_number}')
