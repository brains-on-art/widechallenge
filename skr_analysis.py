import os
from collections import namedtuple
from subprocess import call
import xmltodict
from annif_client import AnnifClient
import joblib

if not os.path.exists('skr.xml'):
    print('Downloading SKR data')
    call("curl 'https://apurahat.skr.fi/myonnot/xml_apurahat?vuosi=2018&mkr=KR&ala=Tiede' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://apurahat.skr.fi/myonnot' -H 'Connection: keep-alive' -o skr.xml", shell=True)

with open('./skr.xml', 'r') as fd:
    data = xmltodict.parse(fd.read())

Apuraha = namedtuple('Apuraha', ['saaja', 'otsikko', 'ala', 'rahasto', 'summa', 'annif'])

client = AnnifClient()

memory = joblib.Memory('./cache', verbose=0)

@memory.cache
def parse_skr(rec):
    annif_res = client.analyze(project_id='yso-fi', text=x['kuvaus'], limit=5)
    return Apuraha(saaja=x['aakkosnimi'], 
                   otsikko=x['kuvaus'], 
                   ala=x['tieteenala'], 
                   rahasto=x['nimikkorahasto'], 
                   summa=x['summa'],
                   annif=annif_res)

recs = data['apurahat']['apuraha']
n = len(recs)
res = [None]*n
print('Parsing SKR data')
for i,x in enumerate(recs[:50]):
    res[i] = parse_skr(x)

for i in range(5):
    print(res[i].otsikko, [x['label'] for x in res[i].annif])


