import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
def process_data(input,output):
    files = os.listdir(input)
    for f in tqdm(files):

        data = pd.read_csv(input+"/"+f)
        data.columns = [str.strip(i) for i in data.columns]
        data.columns = ['PM2', 'PM10', 'SO2', 'NO2', 'CO', 'O3', 'U', 'V', 'TEMP', 'RH', 'PSFC', 'lat', 'lon', '']
        out_path = str(output)+"/"+f
        if not os.path.exists(output):
            os.mkdir(output)
        data.to_csv(out_path)


def download_data(target_fie):

    r = requests.get("http://naq.cicidata.top:10443/chinavis/opendata")
    soup = BeautifulSoup(r.text, 'html.parser')
    l = []
    for k in soup.find_all({'a'}):
        l.append(k['href'])
    l = l[2:]

    _l = []
    for i in l:
        site = "http://naq.cicidata.top:10443/" + i
        _l.append(site)
    f = open(target_fie+'/target.txt', 'a+w')
    for i in _l:
        f.write(str(i))
        f.write('\n')
    f.close()

if __name__ == '__main__':
    process_data(input='H:/desktop/CN-Reanalysis201301/201301',output='H:/desktop/CN-Reanalysis201301/201301tmp')