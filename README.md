Audio Identifier
================

Uploads an audio snippet to [audiotag.info](https://audiotag.info/).
If it can be identified, it shows the user the identified sets of tags (artist, title, album and year) and asks to choose one.
The chosen set of tags is then directly applied to the file.
A second tool takes care of renaming audio files according to their tags.

Dependencies
------------
Apart from [python3](www.python.org), this program needs
- [sox](http://sox.sourceforge.net/) to truncate the audio files.
- [mutagen](https://github.com/quodlibet/mutagen) to modify the tags.

Usage
-----
```
% ./audioidentifier.py --help
usage: Tool to get audio metadata from audiotag.info [-h] -a API_KEY [-l LENGTH] files [files ...]

positional arguments:
  files                 files in need of metadata

options:
  -h, --help            show this help message and exit
  -a API_KEY, --api-key API_KEY
                        file containing the api key (and nothing else)
  -l LENGTH, --length LENGTH
                        length of audio snippet to upload in mm:ss, default is 00:20
```
You need to create a free account at [audiotag.info](https://audiotag.info/) and generate an API key.
This API key then has to be stored in a text file that is passed as argument to `audioidentifier.py`.
I recommend to name the file `apikey.txt`, since this file name will be ignored by `git`.

A second tool, `batchrename.py`, can then be used to rename the files based on their tracks.
```
% ./batchrename.py -husage: tool to batch-rename audio files [-h] [-p PATTERN] files [files ...]

positional arguments:
  files                 files to rename

options:
  -h, --help            show this help message and exit
  -p PATTERN, --pattern PATTERN
                        Pattern for the new file names using lower-case tag names and the syntax of
                        str.format Default is '{artist}/{album}/{tracknumber}_{title}'. The file
                        extension will be copied automatically, folders will be created as needed.
```

Feature Ideas
-------------

This program is working well enough for my purposes, however, there is always something that could be improved.
Some ideas, in no particular order, are
- support a different backend, e.g. [ffmpeg](https://www.ffmpeg.org).
- make the requests async.
- show tags of all files before deciding which to apply.
- support more formats than ogg vorbis and mp3.
