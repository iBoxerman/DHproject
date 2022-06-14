import re
from validator import validate_genre, validate_credit
from scheme import Show, Season, Episode, Credit


def if_satisfy(element_to_return, *preds):
    return element_to_return if all(preds) else None


def parse_date(yyyy_mm_dd, goal='y'):
    if goal == 'y':
        return re.search(r"(\d{4})", yyyy_mm_dd).group(0)
    elif goal == 'm':
        return re.search(r"-(\d{2})-", yyyy_mm_dd).group(1)
    else:
        return yyyy_mm_dd.split('-')[-1]


def parse_credit(show_id, credit, is_main):
    return if_satisfy(Credit(show_id,
                             credit.id,
                             credit.name,
                             credit.character,
                             credit.gender,
                             is_main),
                      validate_credit(credit))


def parse_credits(show_id, credits, is_main):
    return list(filter(None, [parse_credit(show_id, credit, is_main) for credit in credits]))


def parse_episode(show_id, episode_details):
    episode = Episode(show_id,
                      episode_details.id,
                      parse_date(episode_details.air_date),
                      parse_date(episode_details.air_date, 'm'),
                      parse_credits(show_id, episode_details.credits.cast, True))
    try:
        guest_stars = parse_credits(show_id, episode_details.credits.guest_stars, False)
        if guest_stars:
            episode.append_to_cast(guest_stars)
    except RuntimeError:
        print("error")
    finally:
        return episode


def parse_season(season_details):
    return Season(season_details.id,
                  season_details.season_number,
                  len(season_details.episodes))


def parse_show(show_details):
    return if_satisfy(Show(show_details.id,
                           show_details.name,
                           show_details.number_of_seasons),
                      validate_genre(show_details.genres))
