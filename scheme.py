from client_wikidata import get_occupations

COLUMNS = ['show_name', 'season_number', 'actor_id', 'actor_name', 'gender',
           'main_cast', 'character_name', 'character_occupation', 'year', 'month']


class Record:
    def __init__(self, credit, show_name, season_number, episode):
        self.show_name = str(show_name)
        self.season_number = int(season_number)
        self.actor_id = int(credit.id)
        self.actor_name = str(credit.name)
        self.character_name = str(credit.character)
        self.gender = int(credit.gender)
        self.main_cast = bool(credit.is_main)
        self.character_occupation = str(credit.find_occupation())
        self.year = int(episode.year)
        self.month = int(episode.month)


class Credit:
    def __init__(self, show_id, actor_id, name, character, gender, is_main):
        self.show_id = int(show_id)
        self.id = int(actor_id)
        self.name = str(name)
        self.character = str(character)
        self.gender = int(gender)
        self.is_main = bool(is_main)

    def find_occupation(self):
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

        def search_for_in_all_synonyms(x):
            for synonym in synonyms:
                for occupation in synonym:
                    if x.find(occupation) != -1:
                        return synonym[0]
            return None

        found = search_for_in_all_synonyms(character_name)
        if found:
            return found

        cross_reference_occupations = get_occupations(self.show_id, self.character)
        for other_occupation in cross_reference_occupations:
            found = search_for_in_all_synonyms(other_occupation)
            if found:
                return found
        return 'other' if not self.is_main else 'doctor (probably)'


class Episode:
    def __init__(self, show_id, episode_id, year, month, cast):
        self.show_id = int(show_id)
        self.id = int(episode_id)
        self.year = int(year)
        self.month = int(month)
        self.cast = cast

    def append_to_cast(self, another_cast):
        self.cast += another_cast


class Season:
    def __init__(self, season_id, season_number, episodes_number):
        self.id = int(season_id)
        self.number = int(season_number)
        self.episodes_number = int(episodes_number)


class Show:
    def __init__(self, show_id, name, seasons_number):
        self.id = int(show_id)
        self.name = str(name)
        self.seasons_number = int(seasons_number)
