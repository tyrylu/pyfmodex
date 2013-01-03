Pyfmodex
========
This is pyfmodex a fmod ex binding using ctypes.

Installation
------------
For installation, first make sure that you have the fmod ex library for you platform somewhere on your path, so python will be able to find it.
For download visit http://fmod.org/fmod-downloads.html. Ignore everything except the fmod ex api, there are numerous things which will try to distract you.
Next, execute: setup.py install. You might be required to add python as first think of this command. And on linux don't forget to run this command with superuser rights (sudo or su root).
Usage
-----
To verify if everythink works, open python interactive interpreter and try importing pyfmodex:
```python
import pyfmodex
```
If there is no error, good. It worked. Playing a sound is a little bit complicated, but nothing horrible:
```python
import pyfmodex
system = pyfmodex.System()
system.init()
sound = system.create_sound("somefile.mp3")
sound.play()
```
Of course, somefile.mp3 must be replaced with somethink that actually exists. Here, i used the default parameters and not used features like 3d positioning. For more info, you can using dir function and of course the source.