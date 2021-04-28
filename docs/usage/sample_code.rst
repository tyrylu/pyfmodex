Examples
========

While we strive to keep the number of external dependencies required to run the examples below (ideally, to zero), many of the examples require the `curses` library.
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
