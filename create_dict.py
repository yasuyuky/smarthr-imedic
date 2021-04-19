import argparse
import os
import xml.dom.minidom as minidom
from itertools import product

import requests

NAME_FIELDS = [
    'last_name',
    'first_name',
    'last_name_yomi',
    'first_name_yomi',
]
BNAME_FIELDS = [
    'business_last_name',
    'business_first_name',
    'business_last_name_yomi',
    'business_first_name_yomi',
]
EMAIL = ['email']
PLIST_TEMPLATE = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<array>
</array>
</plist>
'''
KATA = map(chr, range(ord('ァ'), ord('ヶ')))
HIRA = map(chr, range(ord('ぁ'), ord('ゖ')))
KATA_HIRA = dict(zip(KATA, HIRA))


def kata2hira(s):
    return ''.join(KATA_HIRA.get(c, c) for c in s)


def create_argapaser():
    parser = argparse.ArgumentParser()
    imechoices = ['mac', 'csv', 'win']
    parser.add_argument('ime', choices=imechoices)
    nchoices = ['full', 'last', 'first', 'email']
    parser.add_argument('-k', '--key', choices=nchoices, action='append')
    parser.add_argument('-v', '--value', choices=nchoices, action='append')
    eschoices = ['employed', 'absent', 'retired']
    parser.add_argument('--emp-status', choices=eschoices, default="employed")
    return parser


def get_pages(url, headers, params, page, per_page):
    params['page'] = page
    params['per_page'] = per_page
    r = requests.get(url, headers=headers, params=params)
    if 'Link' in r.headers and 'next' in r.headers['Link']:
        return r.json() + get_pages(url, headers, params, page + 1, per_page)
    else:
        return r.json()


def get_names(emp_status):
    tenant = os.getenv('SMARTHR_TENANT')
    endpoint = f'https://{tenant}.smarthr.jp/api/v1'
    url = f'{endpoint}/crews'
    token = os.getenv('SMARTHR_TOKEN')
    headers = {'Authorization': f'Bearer {token}'}
    fields = NAME_FIELDS + BNAME_FIELDS + EMAIL
    params = {'fields': ','.join(fields), 'sort': 'emp_code'}
    if emp_status: params['emp_status'] = emp_status
    allnames = get_pages(url, headers, params, 1, 100)
    return allnames


def create_pairs(names, keys, values):
    if not keys: keys = ['full']
    if not values: values = ['full']
    namepairs = []
    for name in names:
        pfx = 'business_' if all(name[k] for k in BNAME_FIELDS) else ''
        d = {}
        if name['email']:
            d['email'] = (name['email'][:name['email'].index('@')], name['email'])
        for order in ['last', 'first']:
            k = pfx + order + '_name'
            d[order] = (kata2hira(name[k + '_yomi']), name[k])
        full_yomi = d['last'][0] + d['first'][0]
        full = d['last'][1] + ' ' + d['first'][1]
        d['full'] = (full_yomi, full)
        for k, v in product(keys, values):
            namepairs.append((d[k][0], d[v][1]))
    return namepairs


def create_xml_child(dom, tag, text):
    el = dom.createElement(tag)
    el.appendChild(dom.createTextNode(text))
    return el


def output_mac(namepairs):
    dom = minidom.parseString(PLIST_TEMPLATE)
    array_el = dom.getElementsByTagName("array")[0]
    for shortcut, phrase in namepairs:
        dict_el = dom.createElement('dict')
        for tag, text in [
            ('key', 'phrase'),
            ('string', phrase),
            ('key', 'shortcut'),
            ('string', shortcut),
        ]:
            dict_el.appendChild(create_xml_child(dom, tag, text))
        array_el.appendChild(dict_el)
    print(dom.toprettyxml())


def output_csv(namepairs):
    for shortcut, phrase in namepairs:
        print(','.join([shortcut, phrase, '人名', '', '']))


def output_win(namepairs):
    for shortcut, phrase in namepairs:
        print('\t'.join([shortcut, phrase, '人名']))


if __name__ == "__main__":
    parser = create_argapaser()
    args = parser.parse_args()
    allnames = get_names(args.emp_status)
    namepairs = create_pairs(allnames, args.key, args.value)
    if args.ime == 'mac':
        output_mac(namepairs)
    elif args.ime == 'csv':
        output_csv(namepairs)
    elif args.ime == 'win':
        output_win(namepairs)
