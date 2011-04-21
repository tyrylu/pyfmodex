This is pyfmodex a fmod ex binding using ctypes.
For installation, first make sure that you have the fmod ex library for you platform somewhere on your path, so python will be able to find it.
Next, on linux as root or via sudo, execute: setup.py install. You might be required to add python as first think of this command.
Usage
To verify, if everythink works, open python interactive interpreter and try importing pyfmodex:
import pyfmodex
If there is no error, good. It worked. Playing a sound isn't hard:
system = pyfmodex.System()
system.init()
sound = system.create_sound("somefile.mp3")
sound.play()
Of course, somefile.mp3 must be replaced with somethink that actually exists. Here, i used the default parameters and not used features like 3d positioning.