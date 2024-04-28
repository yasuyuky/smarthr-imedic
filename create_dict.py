#!/usr/bin/env python

import argparse
import os
import xml.dom.minidom as minidom

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
    if not s: return ''
    return ''.join(KATA_HIRA.get(c, c) for c in s)


def create_argapaser():
    parser = argparse.ArgumentParser()
    ftchoices = ['plist', 'csv', 'tsv']
    parser.add_argument('filetype', choices=ftchoices)
    nchoices = ['full', 'last', 'first', 'email']
    parser.add_argument('key', nargs='?', choices=nchoices, default='full')
    parser.add_argument('value', nargs='?', choices=nchoices, default='full')
    parser.add_argument('comment', nargs='?', default=os.getenv('SMARTHR_TENANT'))
    eschoices = ['employed', 'absent', 'retired']
    parser.add_argument('--sep', default=' ')
    parser.add_argument('--emp-status', choices=eschoices, default="employed")
    parser.add_argument('--business-name', action='store_true', default=False)
    return parser


def get_pages(url, headers, params, page, per_page):
    params['page'] = page
    params['per_page'] = per_page
    r = requests.get(url, headers=headers, params=params)
    if r.status_code >= 400:
        print(r.json())
        quit(2)
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


def create_pairs(names, key, value, business_name, sep):
    namepairs = []
    for name in names:
        pfx = 'business_' if all(name[k] for k in BNAME_FIELDS) and business_name else ''
        d = {}
        if name['email']:
            d['email'] = (name['email'][:name['email'].index('@')], name['email'])
        for order in ['last', 'first']:
            k = pfx + order + '_name'
            d[order] = (kata2hira(name[k + '_yomi']), name[k])
        full_yomi = d['last'][0] + d['first'][0]
        full = d['last'][1] + sep + d['first'][1]
        d['full'] = (full_yomi, full)
        namepairs.append((d[key][0], d[value][1]))
    return namepairs


def create_xml_child(dom, tag, text):
    el = dom.createElement(tag)
    el.appendChild(dom.createTextNode(text))
    return el


def output_plist(namepairs):
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


def output_csv(namepairs, comment):
    for shortcut, phrase in namepairs:
        print(','.join([shortcut, phrase, '人名', '', '', comment]))


def output_tsv(namepairs, comment):
    for shortcut, phrase in namepairs:
        print('\t'.join([shortcut, phrase, '人名', comment]))


if __name__ == "__main__":
    parser = create_argapaser()
    args = parser.parse_args()
    allnames = get_names(args.emp_status)
    namepairs = create_pairs(allnames, args.key, args.value, args.business_name, args.sep)
    if args.filetype == 'plist':
        output_plist(namepairs)
    elif args.filetype == 'csv':
        output_csv(namepairs, args.comment)
    elif args.filetype == 'tsv':
        output_tsv(namepairs, args.comment)
