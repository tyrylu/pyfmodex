Quickstart
==========

Let's play a sample sound.
Try the following simple script:

.. code-block:: python
   :linenos:

   import pyfmodex

   system = pyfmodex.System()
   system.init()
   sound = system.create_sound("somefile.mp3")
   channel = sound.play()

   while channel.is_playing:
      pass

   sound.release()
   system.release()

Of course, `somefile.mp3` must be replaced with something that actually exists. :-)

Note that the while loop is necessary (at least in this simple example) to keep the main thread alive long enough.
You should know this if you want to use FMOD however.
If you don't, it's probably a good thing to spend some time with the `FMOD API documentation <https://fmod.com/resources/documentation-api>`_ first.
