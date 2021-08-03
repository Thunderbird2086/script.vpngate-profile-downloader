# -*-coding: utf-8 -*-
# Auther: Theunderbird2086
"""
   downloader script
"""

import base64
import csv
import os
import sys

from .const import FILTER_COUNTRY, FILTER_SPEED, PROFILE_URL

def url_req2x(url):
    """URL request for python 2.x
    """
    import urllib2
    http = urllib2.urlopen(url)

    csv_data = ""
    while True:
        csv_buffer = http.read(8192)
        if not csv_buffer:
            break

        csv_data += str(csv_buffer)

    return csv_data


def url_req(url):
    """URL request for python 3.x
    """
    import urllib.request
    http = urllib.request.urlopen(url)

    csv_data = ""
    while True:
        csv_buffer = http.read(8192)
        if not csv_buffer:
            break

        csv_data += csv_buffer.decode("utf-8")

    return csv_data


def download_profile():
    """download profile csv
    """
    if sys.version_info.major > 2:
        return url_req(PROFILE_URL)

    return url_req2x(PROFILE_URL)


def get_dict(csv_data):
    """reconstuct CSV data
    """
    orig_csv = csv.DictReader(csv_data)
    ks = orig_csv.fieldnames
    res_dict = {k:[] for k in [k[1:] if k[0] == '#' else k for k in ks]}

    for row in orig_csv:
        for k, v in row.items():
            if k[0] == '#':
                k = k[1:]
            res_dict[k].append(v)

    return res_dict


def prepare_storage(storage_path):
    """remove *.ovpn files under 'storage_path'.
       Also, creates the directory if not exist.
    """
    if os.path.isdir(storage_path):
        for f_name in os.listdir(storage_path):
            if f_name.endswith('.ovpn'):
                os.unlink(os.path.join(storage_path, f_name))
        return

    if os.path.exists(storage_path):
        os.remove(storage_path)

    os.makedirs(storage_path)


def dump_profile(dump_dir, csv_dict, idx, min_speed):
    """dump OpenVPN profiles based on the give filter(min speed)
    """
    speed = int(int(csv_dict['Speed'][idx])/1024/1024)
    if min_speed != 0 and speed < min_speed:
        return False

    o_name = 'vpngate'
    o_name += '_{:03d}Mbps'.format(speed)
    if csv_dict['Ping'][idx] != '-':
        o_name += '_{:03d}ms'.format(int(csv_dict['Ping'][idx]))
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

    return True


def get(profile_filter, storage_path):
    """download and dump OpenVPN profiles.
       program entry point"""
    profiles = download_profile()

    csv_dict = get_dict(profiles.splitlines()[1:-1])

    filter_countries = [cn.strip()
                        for cn in profile_filter[FILTER_COUNTRY].split(',')]

    index = []
    for idx, country in enumerate(csv_dict['CountryShort']):
        if filter_countries and country not in filter_countries:
            continue
        index.append(idx)

    prepare_storage(storage_path)
    min_speed = profile_filter[FILTER_SPEED]
    cnt = 0
    for idx in index:
        if dump_profile(storage_path, csv_dict, idx, min_speed):
            cnt += 1

    return cnt


if __name__ == "__main__":
    TEST_FILTER = {
        FILTER_COUNTRY: "KR, US",
        FILTER_SPEED: 50
    }

    STORAGE_PATH = os.path.join(os.path.expanduser('~'), 'VPN')
    NO_OF_FILES = get(TEST_FILTER, STORAGE_PATH)

    print("dumped {} profiles".format(NO_OF_FILES))
