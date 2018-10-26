from collections import namedtuple
from finna_client import FinnaClient

ImageRecord = namedtuple('ImageRecord', ['id', 'subject', 'url'])

class FinnaImageFinder:
    def __init__(self):
        #self.monkeypatch()
        self.client = FinnaClient()        
    
    def __call__(self, year):
        a = int(year)
        b = a+1
        res = self.client.search('',
                                 fields=['id', 'subjects', 'images'],
                                 filters=['format:0/Image/', 
                                          'online_boolean:1', 
                                          'search_daterange_mv:"[{} TO {}]"'.format(a,b)], 
                                 other={'search_daterange_mv_type':'within'},
                                 limit=100)
        records = res['records']
        print(records[0])
        ids = [x['id'] for x in records]
        subjects = [x['subjects'][0][0] if len(x['subjects'])>0 else [] for x in records]
        images = [x['images'][0] if len(x['images'])>0 else [] for x in records]
        return [ImageRecord(id_, subj, img) for id_, subj, img in zip(ids, subjects, images)]
