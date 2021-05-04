Examples
========

While we strive to keep the number of external dependencies required to run the examples below small (ideally: zero), many of the examples require the :py:mod:`curses` library.
On Windows, this unfortunately requires the installation of an extra module, for example `windows-curses <https://pypi.org/project/windows-curses/>`_.

Device detection
----------------

This is a sample script pretty printing the audio and recording devices detected by the FMOD Engine on your system.

.. literalinclude:: ../sample_code/detect_devices.py
   :linenos:
   :language: python

3D sound positioning
--------------------

This is a sample script demonstrating the very basics of 3D sound positioning.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/threed.py
   :linenos:
   :language: python

Channel groups
--------------

This is sample script showing how to put channels into channel groups.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/channel_groups.py
   :linenos:
   :language: python

Convolution reverb
------------------

This is a sample script showing how to set up a convolution reverb DSP and work with it.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/convolution_reverb.py
   :linenos:
   :language: python

DSP effect per speaker
----------------------

This is a sample script showing how to manipulate a DSP network and as an
example, creating two DSP effects, splitting a single sound into two audio
paths, which then gets filtered seperately.

To only have each audio path come out of one speaker each,
:py:meth:`~pyfmodex.dsp_connection.DSPConnection.set_mix_matrix` is used just
before the two branches merge back together again.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/dsp_effect_per_speaker.py
   :linenos:
   :language: python

Effects
-------

This is a sample script showing how to apply some of the built in software
effects to sounds by applying them to the master channel group. All software
sounds played here would be filtered in the same way. To filter per channel,
and not have other channels affected, simply aply the same function to the
:py:class:`~pyfmodex.channel.Channel` instead of the
:py:class:`~pyfmodex.channel_group.ChannelGroup`.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/effects.py
   :linenos:
   :language: python

Gapless playback
----------------

This is a sample script showing how to schedule channel playback into the
future with sample accuracy. It uses several scheduled channels to synchronize
two or more sounds.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/gapless_playback.py
   :linenos:
   :language: python

Generate tone
-------------

This is a sample script showing how to play generated tones using
:py:meth:`~pyfmodex.system.System.play_dsp` instead of manually connecting and
disconnecting DSP units.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/generate_tone.py
   :linenos:
   :language: python

Granular synthesis
------------------

This is a sample script showing how to play a string of sounds together without
gaps, using :py:attr:`~pyfmodex.channel_control.ChannelControl.delay` to
produce a granular synthesis style truck engine effect.

The basic operation is:

 #. Play two sounds initially at the same time, the first sound immediately,
    and the second sound with a delay calculated by the length of the first
    sound.
 #. Set `delay` to initiate the delayed playback. The `delay` is sample
    accurate and uses output samples as the time frame, not source samples.
    These samples are a fixed amount per second regardless of the source sound
    format, for example 48000 samples per second if FMOD is initialized to
    48khz output.
 #. Output samples are calculated from source samples with a simple
    source-to-output sample rate conversion.
 #. When the first sound finishes, the second one should have automatically
    started. This is a good oppurtunity to queue up the next sound. Repeat step
    two.
 #. Make sure the framerate is high enough to queue up a new sound before the
    other one finishes otherwise you will get gaps.

These sounds are not limited by format, channel count or bit depth and can also
be modified to allow for overlap, by reducing the `delay` from the first sound
playing to the second by the overlap amount.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/granular_synth.py
   :linenos:
   :language: python

Load from memory
----------------

This is a sample script showing how to use the
:py:attr:`~pyfmodex.flags.MODE.OPENMEMORY` mode flag whe creating sounds to
load the data into memory.

This example is simply a variant of the :ref:`play_sound` example, but it loads
the data into memory and then uses the `load from memory` feature of
:py:meth:`~pyfmodex.system.create_sound`.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/load_from_memory.py
   :linenos:
   :language: python

Multiple speakers
-----------------

This is a sample script showing how to play sounds on multiple speakers, and
also how to assign sound subchannels (like in stereo sound) to different,
individual speakers.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/multiple_speaker.py
   :linenos:
   :language: python

Multiple systems
----------------

This example shows how to play sounds on two different output devices from the
same application. It creates two :py:class:`~pyfmodex.system.System` objects,
selects a different sound device for each, then allows the user to play one
sound on each device.

Note that sounds created on device A cannot be played on device B and vice
versa.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/multiple_system.py
   :linenos:
   :language: python

Net stream
----------

This example shows how to play streaming audio from an Internet source.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/net_stream.py
   :linenos:
   :language: python

.. _play_sound:

Play sound
----------

This example shows how to simply load and play multiple sounds, the simplest
usage of FMOD. By default FMOD will decode the entire file into memory when it
loads. If the sounds are big and possibly take up a lot of RAM it would be
better to use the :py:attr:`~pyfmodex.flags.MODE.CREATESTREAM` flag, as this
will stream the file in realtime as it plays (see :ref:`play_stream`).

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/play_sound.py
   :linenos:
   :language: python

.. _play_stream:

Play stream
-----------

This example shows how to simply play a stream such as an MP3 or WAV. The
stream behaviour is achieved by specifying
:py:attr:`~pyfmodex.flags.MODE.CREATESTREAM` in the call to
:py:meth:`~pyfmodex.system.System.create_sound`. This makes FMOD decode the
file in realtime as it plays, instead of loading it all at once which uses far
less memory in exchange for a small runtime CPU hit.

Note that `pyfmodex` does this automatically through the convenience method
:py:meth:`~pyfmodex.system.System.create_stream`.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/play_stream.py
   :linenos:
   :language: python

Record enumeration
------------------

This example shows how to enumerate the available recording drivers on a
device. It demonstrates how the enumerated list changes as microphones are
attached and detached. It also shows that you can record from multi mics at the
same time (if your audio subsystem supports that).

Please note: to minimize latency, care should be taken to control the number of
samples between the record position and the play position. Check :ref:`record`
for details on this process.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/record_enumeration.py
   :linenos:
   :language: python

.. _record:

Record
------

This example shows how to record continuously and play back the same data while
keeping a specified latency between the two. This is achieved by delaying the
start of playback until the specified number of milliseconds has been recorded.
At runtime the playback speed will be slightly altered to compensate for any
drift in either play or record drivers.

(Adapted from sample code shipped with FMOD Engine.)

.. literalinclude:: ../sample_code/record.py
   :linenos:
   :language: python
