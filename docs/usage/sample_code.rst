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
