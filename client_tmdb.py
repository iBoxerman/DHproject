from tmdbv3api import TMDb, TV, Season, Episode
from parser import parse_show, parse_season, parse_episode

tmdb_session = TMDb()
tmdb_session.api_key = '58d359ae49f4cdd645c59713d20933a9'
tmdb_session.language = 'en'
tmdb_session.debug = True


def get_show(name):
    try:
        tv_api = TV()
        query = tv_api.search(name)
        for show_candidate in query:
            return parse_show(tv_api.details(show_candidate.id))
    except:
        print("No such show on TMDB")
        return None


def get_show_by_id(id):
    try:
        tv_api = TV()
        return parse_show(tv_api.details(id))
    except:
        print("No such show on TMDB")
        return None


def get_seasons(show):
    try:
        season_api = Season()
        details = [parse_season(season_api.details(show.id, season))
                   for season in range(1, show.seasons_number + 1)]
        return details
    except:
        print("No such season on TMDB")
        return None


def get_episodes(show_id, season):
    try:
        episodes_api = Episode()
        details = [
            parse_episode(show_id, episodes_api.details(show_id, season.number, episode, append_to_response="credits"))
            for episode in range(1, season.episodes_number + 1)]
        return details
    except:
        print("No episodes on TMDB")
        return None
