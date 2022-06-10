def handle_validation(pred, msg):
    if pred:
        print('Validation Error: ' + msg)
        return False
    return True


def validate_genre(show_candidate):
    allowed_genres_id = [18, 35]  # 18 = Drama
    return handle_validation(any(genre_id in show_candidate for genre_id in allowed_genres_id), "genre not allowed")


def validate_credit(credit_candidate):
    credit = credit_candidate.known_for_department
    return handle_validation(credit != 'Acting', f"credit is not for actor - {credit}")
