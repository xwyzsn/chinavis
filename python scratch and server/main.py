import os
import pandas as pd
from bs4 import BeautifulSoup
import requests
import json
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

def convert_to_json():
    path = "H:/desktop/CN-Reanalysis201301/201301tmp/"
    _data = pd.DataFrame()
    for i in tqdm(os.listdir(path)):
        data = pd.read_csv(path + i)
        data.drop(['Unnamed: 0', 'Unnamed: 14'], axis=1, inplace=True)
        data['date'] = i.split('-')[-1]
        _data = pd.concat([_data, data], axis=0)
    _data = _data.reset_index()
    d = dict()
    res = _data.groupby(by=['lat', 'lon'])
    l = dict()
    for i in tqdm(res.groups.keys()):  # j经纬度坐标
        d = dict()
        _d = dict()
        for j in res.groups[i]:  # 每一个点得 所有 日期

            tmp = ""
            out = dict()
            for k in _data:
                out.setdefault(k, "0")
                out[k] = str(_data.loc[j, k])
                tmp = _data.loc[j, "date"]

            _d.setdefault(tmp, out)
            _d[tmp] = out

            key = str(i[0]) + "," + str(i[1])
        l.setdefault(key, dict())
        l[key] = _d
    j = json.dumps(l)
    f = open("H:/desktop/j_test.json", "w")
    f.write(j)
    f.close()


if __name__ == '__main__':
    process_data(input='H:/desktop/CN-Reanalysis201301/201301',output='H:/desktop/CN-Reanalysis201301/201301tmp')
