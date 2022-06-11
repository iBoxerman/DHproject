from tmdb_client import get_show, get_episodes, get_seasons
import pandas as pd
from scheme import Record, COLUMNS


def add_or_update(df, record):
    ind = df.index[(df["actor_id"] == record.actor_id) & (df["season_number"] == record.season_number)].tolist()
    if len(ind) > 0:
        # print("double")
        old = df.at[ind[0], "actor_id"]
        if old != record.actor_id:
            print("PROMOTION")
            return df.insert(ind[0], "character_occupation", record.character_occupation)
        return df
    return df.append(record.__dict__, ignore_index=True)


def handle_episode(df, show, season_number, episode):
    for credit in episode.cast:
        record = Record(credit, show.name, season_number, episode)
        df = add_or_update(df, record)
    return df


shows = ["The Good Doctor", "ER", "Scrubs", "Grey's Anatomy"]
for show in shows:
    show_df = pd.DataFrame(columns=COLUMNS, dtype=object)
    show = get_show(show)
    seasons = get_seasons(show)
    for season in seasons:
        episodes = get_episodes(show.id, season)
        for episode in episodes:
            show_df = handle_episode(show_df, show, season.number, episode)
        print(f'done {show.name} {season.number}/{show.seasons_number}')
    show_df.to_csv(f'./data/csv/{show.name}.csv')
