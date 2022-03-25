#!/usr/bin/env python3

import asyncio
import argparse
import os
import subprocess
import tempfile

def truncate_audio_file(inputpath, duration='00:20'):
    '''return path to temp file with first duration mm:ss'''
    handle, temppath = tempfile.mkstemp(prefix='audioidentifier', suffix='.ogg')
    os.close(handle)
    subprocess.run(['sox', inputpath, temppath, 'trim', '0', duration])
    return temppath

def main():
    p = truncate_audio_file('/home/jonas/Musik/72 Zum Laichen Und Sterben Ziehen Di.mp3')
    print(p)

if __name__ == '__main__':
    main()
