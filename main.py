from get_data import get_show, get_episodes, get_seasons
import pandas as pd

columns = ['show_name', 'season_number', 'actor_id', 'actor_name', 'gender',
           'main_cast', 'character_name', 'character_occupation', 'year', 'month']


def find_occ(character_name):
    doctor_synonym = ['doctor', 'doc', 'dr', 'dr.', 'physician', 'surgeon', 'specialist']
    nurse_synonym = ['nurse']
    intern_synonym = ['intern']
    medic_synonym = ['medic', 'emt', 'assistant']
    character_name = character_name.lower()
    for synonym in [doctor_synonym, nurse_synonym, intern_synonym, medic_synonym]:
        for occ in synonym:
            if character_name.find(occ) != -1:
                return synonym[0]
    return 'other'


def add_or_update(df, credit):
    ind = df.index[(df["actor_id"] == credit["actor_id"])&(df["season_number"] == credit["season_number"])].tolist()
    if len(ind) > 0:
        # print("double")
        old = df.at[ind[0], "actor_id"]
        if old != credit["actor_id"]:
            print("PROMOTION")
        return df
    return df.append(credit, ignore_index=True)


def handle_episode(df, show, season_number, episode):
    for i, credit in enumerate(episode["cast"]):
        row = {"show_name": show["name"], "season_number": int(season_number),
               "actor_id": credit["id"], "actor_name": credit["name"], "gender": credit["gender"],
               "main_cast": bool(credit["is_main"]), "character_name": credit["character"],
               "character_occupation": find_occ(credit["character"]),
               "year": int(episode["year"]), "month": int(episode["month"])}
        df = add_or_update(df, row)
    return df


shows = ["The Good Doctor", "ER", "Scrubs", "Grey's Anatomy"]
for show in shows:
    show_df = pd.DataFrame(columns=columns, dtype=object)
    show = get_show(show)
    seasons = get_seasons(show)
    for season_number, season_info in enumerate(seasons, start=1):
        episodes = get_episodes(show["id"], season_number, season_info)
        for _, episode in enumerate(episodes, start=1):
            show_df = handle_episode(show_df, show, season_number, episode)
        print(f'done {show["name"]} {season_number}/{show["seasons_number"]}')
    show_df.to_csv(f'./data/{show["name"]}')
