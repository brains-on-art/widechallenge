import random
from collections import namedtuple
import joblib
from finna_client import FinnaClient

ImageRecord = namedtuple('ImageRecord', ['id', 'subject', 'url'])

memory = joblib.Memory('./cache', verbose=1)

@memory.cache(ignore=['client'])
def finna_search(year_a, year_b, client):
    res = client.search('',
                        fields=['id', 'subjects', 'images'],
                        filters=['format:0/Image/', 
                                 'online_boolean:1', 
                                 'search_daterange_mv:"[{} TO {}]"'.format(year_a, year_b)], 
                        other={'search_daterange_mv_type':'within'},
                        limit=100)
    records = res['records']
    ids = [x['id'] for x in records]
    subjects = [x['subjects'][0][0] if len(x['subjects'])>0 else [] for x in records]
    images = [x['images'][0] if len(x['images'])>0 else [] for x in records]
    base_url = 'https://finna.fi'
    return [ImageRecord(id_, subj, base_url+img) for id_, subj, img in zip(ids, subjects, images) if subj != [] and img != []]
    

class FinnaImageFinder:
    def __init__(self):
        self.client = FinnaClient()        
    
    def __call__(self, year, n=50):
        a = int(year)
        b = a+1
        res = finna_search(a, b, self.client)
        random.seed(42)
        return random.sample(res, k=n)
        
if __name__ == '__main__':
    finder = FinnaImageFinder()
    print(finder(1900))

    print(len(finna_search(1900,1901,finder.client)))
