from skosmos_client import SkosmosClient
from rdflib.namespace import SKOS
import joblib

memory = joblib.Memory('./cache', verbose=0)


@memory.cache
def get_branch_route(keyword, sk):

    results = sk.search(keyword, vocabs='yso')
    print('--- keyword: {} ---'.format(keyword))

    if results:
        result = results[0]
        uri = result['uri']
    else:
        print('No hits for <<{}>>'.format(keyword))
        return []

    br_list = []

    try:
        while True:
            concept = sk.get_concept('yso', uri)
            br_list.append(concept.label())
            next_label = concept.broader()[0]['prefLabel']
            uri = concept.broader()[0]['uri']

    except IndexError:
        pass

    return br_list

if __name__ == '__main__':

    sk = SkosmosClient()

    # keywords = ['rakkaus', 'makkara', 'kosmonautti', 'hevonen', 'rauta', 'taivas', 'helvetti']
    # keywords = ['love', 'sausage', 'cosmonaut', 'horse', 'iron', 'heaven', 'hell']
    keywords = ['häst', 'teknik', 'porträtt']

    for keyword in keywords:
        br = get_branch_route(keyword, sk)

        for item in br:
            print('{}\n⬇️'.format(item))
