Audio Identifier
================

Uploads an audio snippet to [audiotag.info](https://audiotag.info/).
If it can be identified, it shows the user the identified sets of tags (artist, title, album and year) and asks to choose one.
The chosen set of tags is then directly applied to the file.

Dependencies
------------
Apart from [python3](www.python.org), this program needs
- [sox](http://sox.sourceforge.net/) to truncate the audio files.
- [mutagen](https://github.com/quodlibet/mutagen) to modify the tags.

Feature Ideas
-------------

This program is working well enough for my purposes, however, there is always something that could be improved.
Some ideas, in no particular order, are
- support a different backend, e.g. [ffmpeg](https://www.ffmpeg.org).
- make the requests async.
- show tags of all files before deciding which to apply.
