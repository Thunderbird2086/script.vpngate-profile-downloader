# -*-coding: utf-8 -*-

import base64
import csv
import os
import sys

def url_req2x(url):
    import urllib2
    http = urllib2.urlopen(url)

    csv_data = ""
    while True:
        buffer = http.read(8192)
        if not buffer:
            break

        csv_data += str(buffer)

    return csv_data


def url_req(url):
    import urllib.request
    http = urllib.request.urlopen(url)

    csv_data = ""
    while True:
        buffer = http.read(8192)
        if not buffer:
            break

        csv_data += buffer.decode("utf-8")

    return csv_data


def download_profile():
    url = "http://www.vpngate.net/api/iphone/"

    if sys.version_info.major >2:
        return url_req(url)

    return url_req2x(url)


def get_dict(csv_data):
    orig_csv = csv.DictReader(csv_data)
    ks = orig_csv.fieldnames
    res_dict = {k:[] for k in [k[1:] if k[0] == '#' else k for k in ks]}

    for row in orig_csv:
        for k, v in row.items():
            if k[0] == '#':
                k=k[1:]
            res_dict[k].append(v)

    return res_dict


def get_dump_dir():
    dump_dir = os.path.join(os.path.expanduser('~'), 'VPN')

    if os.path.isdir(dump_dir):
        for f_name in os.listdir(dump_dir):
            if f_name.endswith('.ovpn'):
                os.unlink(os.path.join(dump_dir, f_name))
        os.rmdir(dump_dir)

    if os.path.exists(dump_dir):
        os.remove(dump_dir)

    os.makedirs(dump_dir)

    return dump_dir

def dump_profile(dump_dir, csv_dict, idx):
    o_name = 'vpngate'
    o_name += '_{:03d}M'.format(int(int(csv_dict['Speed'][idx])/1024/1024))
    o_name += '_' + csv_dict['CountryShort'][idx]
    o_name += '_' + csv_dict['HostName'][idx]

    b64 = csv_dict['OpenVPN_ConfigData_Base64'][idx]
    conf = base64.b64decode(b64).decode("utf-8")

    for line in conf.splitlines():
        if line.startswith('proto'):
            o_name += '_' + line.split()[1].strip()
        elif line.startswith('remote'):
            o_name += '_' + line.split()[2].strip()

    o_name += '.ovpn'

    o_path = os.path.join(dump_dir, o_name)
    with open(o_path, 'w') as fo:
        fo.write(conf)

    return o_name

def get(filter):
    profiles = download_profile()

    csv_dict = get_dict(profiles.splitlines()[1:-1])

    index = []
    for idx, country in enumerate(csv_dict['CountryShort']):
        if country not in filter:
            continue
        index.append(idx)    

    dump_dir = get_dump_dir()
    for idx in index:
        dump_profile(dump_dir, csv_dict, idx)

    return len(index)

if __name__ == "__main__":
    no_of_files = get(['KR', 'US'])

    print("dumped {} profiles".format(no_of_files))
