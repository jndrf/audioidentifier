#!/usr/bin/env python3

import asyncio
import argparse
import os
import subprocess
import tempfile
import time

import json
import requests

API_URL = 'https://audiotag.info/api'

def truncate_audio_file(inputpath, duration='00:20'):
    '''return path to temp file with first duration mm:ss'''
    handle, temppath = tempfile.mkstemp(prefix='audioidentifier', suffix='.wav')
    os.close(handle)
    subprocess.run(['sox', inputpath, temppath, 'trim', '0', duration], check=True)
    return temppath

def upload_for_identification(path, apikey):
    payload = {'action':'identify', 'apikey':apikey}
    with open(path, 'rb') as handle:
        result = requests.post(API_URL, payload, files={'file':handle})
    print(result.text)
    reply = json.loads(result.text)
    if reply['success']:
        return reply['token']

    raise RuntimeError(reply['error'])

def retrieve_result(token, apikey):
    payload = {'action':'get_result', 'token':token, 'apikey':apikey}

    while True:
        result = requests.post(API_URL, payload)
        reply = json.loads(result.text)
        print(reply)
        if not reply['success']:
            raise RuntimeError(reply['error'])
        if reply['result'] == 'wait':
            time.sleep(1)
        else:
            break

    
def main():
    p = truncate_audio_file('/home/jonas/Musik/72 Zum Laichen Und Sterben Ziehen Di.mp3')
    print(p)
    t = upload_for_identification(p, API_KEY)
    retrieve_result(t, API_KEY)

if __name__ == '__main__':
    main()
