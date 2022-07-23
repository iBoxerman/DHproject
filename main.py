import pandas as pd
from scheme import Record, COLUMNS
from client_tmdb import get_show, get_show_by_id, get_episodes, get_seasons


def add_or_update(df, record):
    ind = df.index[(df["actor_id"] == record.actor_id) & (df["season_number"] == record.season_number)].tolist()
    if len(ind) > 0:
        old = df.at[ind[0], "actor_id"]
        if old != record.actor_id:
            print("PROMOTION")
            return df.insert(ind[0], "character_occupation", record.character_occupation)
        return df
    return df.append(record.__dict__, ignore_index=True)


def handle_episode(df, show, season_number, episode):
    for credit in episode.cast:
        record = Record(credit, show.name, show.origin, season_number, episode)
        df = add_or_update(df, record)
    return df


us_shows = ["Grey's Anatomy", "The Good Doctor", "ER", "Scrubs", "House", "Private Practice", "Nurse Jackie",
            "New Amsterdam", "The Resident", "Code Black", "Chicago Med", "St. Elsewhere", "Doogie Howser, M.D.",
            "M*A*S*H", "Nurses", "Medical Center", "Quincy, M.E.", "Northern Exposure", "Third Watch", "Virgin River"]
korean_shows = ["Hospital Playlist", "Descendants of the Sun", "Romantic Doctor, Teacher Kim", "Yong Pal",
                "Doctor Stranger", "It’s Okay, That’s Love", "Kill Me, Heal Me"]
british_shows = ["Doctors", "Casualty", "Holby City", "Bodies", "Doc Martin", "Monroe", "Call the Midwife", "Critical",
                 "A Young Doctor's Notebook & Other Stories", "Doctor Foster: A Woman Scorned"]
germany_shows = ["Der Landarzt", "Hallo, Onkel Doc!", "Für alle Fälle Stefanie", "Familie Dr. Kleist",
                 "Dr. Sommerfeld – Neues vom Bülowbogen", "In aller Freundschaft",
                 "St. Angela", "Die Rettungsflieger", "Der Bergdoktor", "Doktor Martin", "Add a Friend"]
czech_shows = ["Ordinace v růžové zahradě", "Doktor Martin", "Sestřičky"]
spanish_shows = ["Hospital Central", "Médico de familia"]
australian_shows = ["Shortland Street", "Doctor Doctor", "All Saints", "The Flying Doctors", "Offspring"]
canadian_shows = ["Keeping Canada Alive", "Coroner", "Hard Rock Medical", "Trauma", "Saving Hope"]
latin_shows = ["A Corazón Abierto", "Mentiras perfectas", "A Corazón Abierto", "Sob Pressão"]

special_shows = [79983, 83211]

# us_shows + korean_shows + british_shows + germany_shows +czech_shows + spanish_shows + australian_shows + canadian_shows + latin_shows+special_shows
shows = us_shows + korean_shows + british_shows + germany_shows + czech_shows + spanish_shows + australian_shows + canadian_shows + latin_shows + special_shows
# special_shows
for show in shows:
    show_df = pd.DataFrame(columns=COLUMNS, dtype=object)
    show = get_show(show) if type(show) == str else get_show_by_id(show)
    if not show:
        continue
    seasons = get_seasons(show)
    if not seasons:
        continue
    for season in seasons:
        episodes = get_episodes(show.id, season)
        if not episodes:
            continue
        for episode in episodes:
            show_df = handle_episode(show_df, show, season.number, episode)
        print(f'done {show.name} {season.number}/{show.seasons_number}')
    show_df.to_csv(f'./data/csv/{show.name}.csv')
