# pip install sparqlwrapper
# https://rdflib.github.io/sparqlwrapper/

import sys
from SPARQLWrapper import SPARQLWrapper, JSON

endpoint_url = "https://query.wikidata.org/sparql"

tv_show_data = {}

def get_results(endpoint_url, id):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(
        """SELECT ?tv_showLabel ?actorLabel ?characterLabel ?roleLabel
        WHERE
        {
        ?tv_show p:P4983 ?tmdb_tv_id.
        ?tmdb_tv_id (ps:P4983) "%s". # 1416 grey's anatomy,  "1408" house, "918" mesh, "18053" nurse jacky
        
        ?tv_show p:P161 [
                ps:P161 ?actor;
                pq:P453 ?character;
            ].
        ?character wdt:P106 ?role.
        
        # ?character wdt:P106 wd:Q774306. # surgeon
        # ?character wdt:P106 wd:Q186360. # nurse
        # ?character wdt:P21 wd:Q6581072. # female

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }"""
    %id)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()

def get_tv_show_roles(id):
    if id in tv_show_data:
        return {}
    results = get_results(endpoint_url,id)["results"]["bindings"]
    dict = {}
    for result in results:
        char_name = result["characterLabel"]["value"]
        role = result["roleLabel"]["value"]
        if char_name in dict:
            dict[char_name].append(role)
        else:
            dict[char_name] = [role]
    tv_show_data[id] = dict
    return dict

def get_occupations(id,name):
    if id in tv_show_data:
        return tv_show_data[id][name]
    else:
        return []






