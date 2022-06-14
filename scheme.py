COLUMNS = ['show_name', 'season_number', 'actor_id', 'actor_name', 'gender',
           'main_cast', 'character_name', 'character_occupation', 'year', 'month']


def ext(show_id, name):
    return ["surgeon"]


class Record:
    def __init__(self, credit, show_name, season_number, episode):
        self.show_name = str(show_name)
        self.season_number = int(season_number)
        self.actor_id = int(credit.id)
        self.actor_name = str(credit.name)
        self.character_name = str(credit.character)
        self.gender = int(credit.gender)
        self.main_cast = bool(credit.is_main)
        self.character_occupation = str(credit.find_occ())
        self.year = int(episode.year)
        self.month = int(episode.month)


class Credit:
    def __init__(self, show_id, id, name, character, gender, is_main):
        self.show_id = int(show_id)
        self.id = int(id)
        self.name = str(name)
        self.character = str(character)
        self.gender = int(gender)
        self.is_main = bool(is_main)

    def find_occ(self):
        doctor_synonym = ['doctor', 'doc',
                          'dr', 'dr.', 'dr ', 'dr. ',
                          'physician', 'surgeon', 'specialist',
                          'neurosurgeon', 'pediatrician', 'gynaecologist',
                          'internist', 'obstetrician']
        nurse_synonym = ['nurse', 'midwife']
        intern_synonym = ['intern']
        medic_synonym = ['medic', 'emt', 'assistant', 'psychiatrist', 'anesthesiologist']
        character_name = self.character.lower()
        synonyms = [doctor_synonym, nurse_synonym, intern_synonym, medic_synonym]
        for synonym in synonyms:
            for occ in synonym:
                if character_name.find(occ) != -1:
                    return synonym[0]
        other_occs = ext(self.show_id, self.character)
        for other_occ in other_occs:
            for synonym in synonyms:
                for occ in synonym:
                    if other_occ.find(occ) != -1:
                        return synonym[0]
        return 'other'


class Episode:
    def __init__(self, show_id, id, year, month, cast):
        self.show_id = int(show_id)
        self.id = int(id)
        self.year = int(year)
        self.month = int(month)
        self.cast = cast

    def append_to_cast(self, another_cast):
        self.cast += another_cast


class Season:
    def __init__(self, id, season_number, episodes_number):
        self.id = int(id)
        self.number = int(season_number)
        self.episodes_number = int(episodes_number)


class Show:
    def __init__(self, id, name, seasons_number):
        self.id = int(id)
        self.name = str(name)
        self.seasons_number = int(seasons_number)
