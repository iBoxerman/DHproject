import sys
from SPARQLWrapper import SPARQLWrapper, JSON

TV_SHOW_DATA = {}


def get_results(show_id, endpoint_url="https://query.wikidata.org/sparql"):
    user_agent = "WDQS-example Python/%s.%s" % (sys.version_info[0], sys.version_info[1])
    sparql = SPARQLWrapper(endpoint_url, agent=user_agent)
    sparql.setQuery(
        """SELECT ?tv_showLabel ?actorLabel ?characterLabel ?roleLabel
        WHERE
        {
        ?tv_show p:P4983 ?tmdb_tv_id.
        ?tmdb_tv_id (ps:P4983) "%s".
        
        ?tv_show p:P161 [
                ps:P161 ?actor;
                pq:P453 ?character;
            ].
        ?character wdt:P106 ?role.

        SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
        }"""
        % show_id)
    sparql.setReturnFormat(JSON)
    return sparql.query().convert()


def update_tv_show_by_id(show_id):
    if show_id in TV_SHOW_DATA:
        return TV_SHOW_DATA[show_id]
    results = get_results(show_id)["results"]["bindings"]
    show_dict = {}
    for result in results:
        char_name = result["characterLabel"]["value"]
        role = result["roleLabel"]["value"]
        if char_name in show_dict:
            show_dict[char_name].append(role)
        else:
            show_dict[char_name] = [role]
    TV_SHOW_DATA[show_id] = show_dict
    return show_dict


def get_occupations(show_id, name):
    update_tv_show_by_id(show_id)
    if show_id in TV_SHOW_DATA:
        try:
            return TV_SHOW_DATA[show_id][name]
        except KeyError:
            return []
    else:
        return []
