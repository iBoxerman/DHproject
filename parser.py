import re
from validator import validate_genre, validate_credit


def if_satisfy(element_to_return, *preds):
    return element_to_return if all(preds) else None


def parse_date(yyyy_mm_dd, goal='y'):
    if goal == 'y':
        return re.search(r"(\d{4})", yyyy_mm_dd).group(0)
    elif goal == 'm':
        return re.search(r"-(\d{2})-", yyyy_mm_dd).group(1)
    else:
        return yyyy_mm_dd.split('-')[-1]


def parse_credit(credit, is_main):
    return if_satisfy({"id": credit.id,
                       "character": credit.character,
                       'name': credit.name,
                       "gender": credit.gender,
                       "is_main": is_main},
                      validate_credit(credit))


def parse_credits(credits, is_main):
    return list(filter(None, [parse_credit(credit, is_main) for credit in credits]))


def parse_episode(episode_details):
    details = {"id": episode_details.id,
               "year": parse_date(episode_details.air_date),
               "month": parse_date(episode_details.air_date, 'm'),
               "cast": parse_credits(episode_details.credits.cast, True)}
    try:
        guest_stars = parse_credits(episode_details.credits.guest_stars, False)
        if guest_stars:
            details["cast"] += guest_stars
    except RuntimeError:
        print("error")
    finally:
        return details


def parse_season(season_details):
    return {"id": season_details.id,
            "episodes_number": len(season_details.episodes)}


def parse_show(show_details):
    return if_satisfy({"id": show_details.id,
                       "name": show_details.name,
                       "seasons_number": show_details.number_of_seasons},
                      validate_genre(show_details.genres))
