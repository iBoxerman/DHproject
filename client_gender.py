import requests as r
import gender_guesser.detector as gender_detector

CERTAINTY = 0.7
NOT_FOUND = -9

switcher = {"unknown": 0,
            "female": 1,
            "mostly_female": 1,
            "male": 2,
            "mostly_male": 2,
            "andy": 3}
cache = {}


def is_in_cache(name):
    # print("Cache hit!")
    return cache.get(name, NOT_FOUND) != NOT_FOUND


def convert_and_update(gender_str, name):
    gender = switcher.get(gender_str, NOT_FOUND)
    cache[name] = gender
    return gender


class First:
    def __init__(self):
        self.url = "https://api.genderize.io"

    def get_gender(self, name):
        try:
            if is_in_cache(name):
                return cache[name]
            res = r.get(self.url, {"name": name}).json()
            if res['probability'] > CERTAINTY:
                return convert_and_update(res["gender"], name)
            return NOT_FOUND
        except:
            # print("ERROR - first api fail")
            return NOT_FOUND


class Second:
    def __init__(self):
        self.detector = gender_detector.Detector(case_sensitive=False)

    def get_gender(self, name):
        try:
            if is_in_cache(name):
                return cache[name]
            return convert_and_update(self.detector.get_gender(name), name)
        except:
            # print("ERROR - second api fail")
            return NOT_FOUND


def get_gender(gender, name):
    if gender != 0:
        return gender
    if is_in_cache(name):
        return cache[name]
    first = First().get_gender(name)
    if first != NOT_FOUND:
        return first
    second = Second().get_gender(name)
    if second != NOT_FOUND:
        return second
    return 0
