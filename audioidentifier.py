#!/usr/bin/env python3
# Copyright 2022 Jonas Neundorf
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import argparse
import os
import subprocess
import sys
import tempfile
import time

import json
from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis
import requests

API_URL = 'https://audiotag.info/api'
API_KEY = ''

def truncate_audio_file(inputpath, duration='00:20'):
    '''return path to temp file with first duration mm:ss'''
    handle, temppath = tempfile.mkstemp(prefix='audioidentifier', suffix='.ogg')
    os.close(handle)
    subprocess.run(['sox', inputpath, temppath, 'trim', '0', duration], check=True)
    return temppath

def upload_for_identification(path, apikey):
    payload = {'action':'identify', 'apikey':apikey}
    with open(path, 'rb') as handle:
        result = requests.post(API_URL, payload, files={'file':handle})
    reply = json.loads(result.text)
    if reply['success']:
        return reply['token']

    raise RuntimeError(reply['error'])

def retrieve_result(token, apikey):
    payload = {'action':'get_result', 'token':token, 'apikey':apikey}

    while True:
        result = requests.post(API_URL, payload)
        reply = json.loads(result.text)
        if not reply['success']:
            raise RuntimeError(reply['error'])
        if reply['result'] == 'wait':
            time.sleep(1)
        elif reply['result'] == 'found':
            return reply['data']
        else:
            return False

def apply_tags_mp3(path, **kwargs): #title='', artist='', album='', year=''):
    id3tags = EasyID3(path)
    for tag, value in kwargs.items():
        if not tag in EasyID3.valid_keys.keys():
            continue
        id3tags[tag] = value

    id3tags.save()

def apply_tags_ogg(path, **kwargs):
    oggfile = OggVorbis(path)
    for tag, value in kwargs.items():
        if not tag in EasyID3.valid_keys.keys():
            continue
        oggfile.tags[tag.upper()] = value

    oggfile.save()

TAGGING_FUNCTIONS = {'mp3':apply_tags_mp3,
                     'ogg':apply_tags_ogg}

def pick_and_apply_tags(path, all_data):
    # find tagging function
    filetype = path.split('.')[-1].lower()
    try:
        apply_tags = TAGGING_FUNCTIONS[filetype]
    except KeyError:
        print('only {} are supported'.format(', '.join(TAGGING_FUNCTIONS.keys())))
        sys.exit(1)
        
    print('\n** {}'.format(path))
    choice_template = '\t'.join(['({index})', 'ARTIST={artist}',
                                 'TITLE={title}', 'ALBUM={album}', 'YEAR={year}'])
    for index, ds in enumerate(all_data):
        tags = ds['tracks'][0]
        print(choice_template.format(index=index, artist=tags[1],
                                     title=tags[0], album=tags[2], year=tags[3]))

    invalid_reply = True
    while invalid_reply:
        reply = input('type number to pick suggestion, s to skip, q to quit. ').lower().strip()
        print(reply)
        if reply == 'q':
            sys.exit()
        elif reply == 's':
            return
        try:
            index = int(reply)
            tags = all_data[index]['tracks'][0]
            apply_tags(path, artist=tags[0], title=tags[1], album=tags[2], year=tags[3])
            invalid_reply = False
        except (ValueError, IndexError):
            invalid_reply = True


def main(path, length):
    idsnippet = truncate_audio_file(path, length)
    token = upload_for_identification(idsnippet, API_KEY)
    all_data = retrieve_result(token, API_KEY)
    if all_data:
        pick_and_apply_tags(path, all_data)
    os.remove(idsnippet)

if __name__ == '__main__':
    parser = argparse.ArgumentParser('Tool to get audio metadata from audiotag.info')
    parser.add_argument('-a', '--api-key', help='file containing the api key (and nothing else)',
                        required=True)
    parser.add_argument('files', help='files in need of metadata', nargs='+')
    parser.add_argument('-l', '--length', default='00:20',
                        help='length of audio snippet to upload in mm:ss, default is 00:20')
    args = parser.parse_args()

    with open(args.api_key) as tokenfile:
        API_KEY = tokenfile.read().strip()

    for path in args.files:
        main(path, args.length)
