from tmdbv3api import TMDb, TV, Season, Episode
from parser import parse_show, parse_season, parse_episode

tmdb_session = TMDb()
tmdb_session.api_key = '58d359ae49f4cdd645c59713d20933a9'
tmdb_session.language = 'en'
tmdb_session.debug = True


def get_show(name):
    tv_api = TV()
    query = tv_api.search(name)
    for show_candidate in query:
        return parse_show(tv_api.details(show_candidate.id))


def get_seasons(show):
    season_api = Season()
    return [parse_season(season_api.details(show["id"], season))
            for season in range(1, show["seasons_number"] + 1)]


def get_episodes(show_id, season_id, season_info):
    episodes_api = Episode()
    return [parse_episode(episodes_api.details(show_id, season_id, episode, append_to_response="credits"))
            for episode in range(1, season_info["episodes_number"] + 1)]
