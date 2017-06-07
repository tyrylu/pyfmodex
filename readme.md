Pyfmodex
========
This is pyfmodex a fmod ex binding using ctypes.

Installation
------------
For installation, first make sure that you have the fmod stuio library for you platform somewhere on your path, so python will be able to find it.
For download visit http://www.fmod.org/download/. For some reason, the API download requires a free account.
Then, install it via pip or easy_install, or, you can always use the setup.py way. Don't forget superuser rights, if they're needed.
Usage
-----
To verify if everything works, open python interactive interpreter and try importing pyfmodex:
```python
import pyfmodex
```
If there is no error, good. It worked. Playing a sound is a little bit more complicated, than the import, but nothing horrible:
```python
import pyfmodex
system = pyfmodex.System()
system.init()
sound = system.create_sound("somefile.mp3")
sound.play()
```
Of course, somefile.mp3 must be replaced with somethink that actually exists. Here, i used the default parameters and not used features like 3d positioning. For more info, you can use dir function and of course the source.
Python 3 compatibility
----------------------
Pyfmodex works with python 3 (tested on version 3.5, older versions than python 3.4 will not work, because the library depends on the enum module.
If you pass as a file name str on py3 or unicode on py2, make sure that they're encodable by the encoding retuned by sys.getfilesystemencoding. Channel Group names and other identifiers are supposed to be ascii only.