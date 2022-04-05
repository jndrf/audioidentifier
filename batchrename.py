#!/usr/bin/env python3
# Copyright 2022 Jonas Neundorf
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.

import argparse
import os

from mutagen.easyid3 import EasyID3
from mutagen.oggvorbis import OggVorbis

retrieve_tags = {'ogg':lambda path: OggVorbis(path).tags,
                 'mp3': EasyID3}

def flatten_tags(tags):
    '''mutagen returns a list for each tag, take only first element of it'''
    ret = {}
    for key, taglist in tags.items():
        tag = taglist[0].replace('/', '_')
        ret[key] = tag
    return ret

def rename(inputfile, pattern, dry_run):
    extension = inputfile.split('.')[-1].lower()
    tags = retrieve_tags[extension](inputfile)
    tags = flatten_tags(tags)
    tags['extension'] = extension
    pattern = pattern + '.{extension}'

    outputfile = pattern.format(**tags)

    if dry_run:
        print('{} --> {}'.format(inputfile, outputfile))
    else:
        os.renames(inputfile, outputfile)


if __name__ == '__main__':

    parser = argparse.ArgumentParser('tool to batch-rename audio files')
    parser.add_argument('files', help='files to rename', nargs='+')
    parser.add_argument('-p', '--pattern', default='{artist}/{album}/{tracknumber}_{title}',
                        help='''
Pattern for the new file names using lower-case tag names and the syntax of str.format
Default is '{artist}/{album}/{tracknumber}_{title}'.
The file extension will be copied automatically, folders will be created as needed.
''')
    parser.add_argument('-n', '--dry-run', action='store_true',
                        help='print what would be changed, but don\'t change')

    args = parser.parse_args()

    for f in args.files:
        rename(f, args.pattern, args.dry_run)
