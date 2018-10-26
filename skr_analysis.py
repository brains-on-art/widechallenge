from subprocess import call


print('Downloading SKR data')
call("curl 'https://apurahat.skr.fi/myonnot/xml_apurahat?vuosi=2018&mkr=KR&ala=Tiede' -H 'User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: https://apurahat.skr.fi/myonnot' -H 'Connection: keep-alive' -o skr.xml", shell=True)


import xmltodict

with open('./skr.xml', 'r') as fd:
    data = xmltodict.parse(fd.read())

from collections import namedtuple

Apuraha = namedtuple('Apuraha', ['saaja', 'otsikko', 'ala', 'rahasto', 'summa'])

def parse_skr(rec):
    n = len(rec)
    res = [None]*n
    for i,x in enumerate(rec):
        res[i] = Apuraha(saaja=x['aakkosnimi'], 
                         otsikko=x['kuvaus'], 
                         ala=x['tieteenala'], 
                         rahasto=x['nimikkorahasto'], 
                         summa=x['summa'])
    return res


print('Parsing SKR data')
apurahat = parse_skr(data['apurahat']['apuraha'])

for i in range(5):
    print(apurahat[i])
