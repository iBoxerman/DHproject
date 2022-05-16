import json
import requests
import logging
import pandas as pd

logging.basicConfig(filename="./logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')
logger = logging.getLogger("crawler")
logger.setLevel(logging.DEBUG)
PAGE_SIZE = 100000
PAGE_NUMBER = 1
N_PLACES = 27239
N_VARIANTS = 102454
N_ATTESTATIONS = 236744


def getRequest(path):
    r = requests.get(path, timeout=5)
    if r.status_code != 200:
        logger.error("Status code isn't 200", r.status_code)
    return r.json()


def save(instance, n, prefix, asCSV=False):
    records = instance.getAll(page_size=n)
    filename = f"{prefix}_{n}"
    if asCSV:
        df = pd.DataFrame.from_dict(records, orient='columns')
        df.to_csv(f'{filename}.csv', index=True)
        logger.info(f"Saved {n} records to {filename}.csv")
    else:
        with open(f'{filename}.json', 'w', encoding='utf8') as fd:
            json.dump(records, fd, indent=4, ensure_ascii=False)
        logger.info(f"Saved {n} records to {filename}.json")


class KimaCrawler:
    def __init__(self):
        self.url = 'https://geo-kima.org/'
        self.attestations = Attestations(self.url)
        self.functions = Functions(self.url)
        self.places = Places(self.url)
        self.variants = Variants(self.url)
        logger.info("Crawler was created...")


class Attestations:
    def __init__(self, kima_path):
        self.path = kima_path + '/api/Attestations'


class Functions:
    def __init__(self, kima_path):
        self.path = kima_path + '/api/Function'

    def countAll(self):
        return getRequest(f'{self.path}/GeneralCounts')


class Places:
    def __init__(self, kima_path):
        self.path = kima_path + '/api/Places'
        self.toPlace = lambda json_data: json.loads(json_data, object_hook=lambda d: SimpleNamespace(**d))

    def count(self):
        return getRequest(f'{self.path}/PlacesCount')

    def getByID(self, id):
        return getRequest(f'{self.path}/Place/{id}')

    def getByVariant(self, variant_name):
        return getRequest(f'{self.path}/Place/{variant_name}')

    def getAll(self, page_size=N_PLACES, page_number=PAGE_NUMBER):
        return getRequest(f'{self.path}/Places/{page_size}/{page_number}')

    def saveAll(self, n=N_PLACES, asCSV=False):
        save(self, n, "places", asCSV)


class Variants:
    def __init__(self, kima_path):
        self.path = kima_path + '/api/Variants'

    def count(self):
        return getRequest(f'{self.path}/VariantsCount')

    def countByPlaceId(self, place_id):
        return getRequest(f'{self.path}/PlaceVariantsCount/{place_id}')

    def getByID(self, id):
        return getRequest(f'{self.path}/Variant/{id}')

    def getByPlaceId(self, place_id, page_size=PAGE_SIZE, page_number=PAGE_NUMBER):
        return getRequest(f'{self.path}/PlaceVariants/{place_id}/{page_size}/{page_number}')

    def getAll(self, page_size=N_VARIANTS, page_number=PAGE_NUMBER):
        return getRequest(f'{self.path}/Variants/{page_size}/{page_number}')

    def saveAll(self, n=N_VARIANTS, asCSV=False):
        save(self, n, "variants", asCSV)


if __name__ == '__main__':
    cr = KimaCrawler()
    cr.places.saveAll()
    cr.variants.saveAll()
