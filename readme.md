Pyfmodex
========
This is pyfmodex, an [FMOD](https://fmod.com) Python binding using [ctypes](https://docs.python.org/3/library/ctypes.html).

Installation
------------
To install, first make sure that you have the FMOD Engine library for you platform somewhere in your path, so Python will be able to find it.
On Linux, libraries are searched for in `LD_LIBRARY_PATH`.
To download the FMOD Engine library, visit http://www.fmod.org/download. The library is free to download, but requires a free account to be made first.

Then, install pyfmodex via `pip`, `easy_install` or the `setup.py` way.

Usage
-----
To verify if everything works, open a Python REPL and try importing pyfmodex:

```python
import pyfmodex
```

If there is no error: good, it worked. :-)

Playing a sound is a little bit more complicated than the import, but nothing horrible.
Try the following simple script:

```python
import pyfmodex

system = pyfmodex.System()
system.init()
sound = system.create_sound("somefile.mp3")
channel = sound.play()

while channel.is_playing:
    pass
```

Of course, `somefile.mp3` must be replaced with something that actually exists. :-)

Note that the while loop is necessary (at least in this simple example) to keep the main thread alive long enough.
