Installation
============

To install, first make sure that you have the FMOD Engine library for you platform somewhere in your path, so Python will be able to find it.
On Linux, libraries are searched for in `LD_LIBRARY_PATH`.
Alternatively, you can set ``PYFMODEX_DLL_PATH`` or  ``PYFMODEX_STUDIO_DLL_PATH`` as an environment variable to specify the library path. This can also be done inside Python setting ``os.environ["PYFMODEX_DLL_PATH"]`` or ``os.environ["PYFMODEX_STUDIO_DLL_PATH"]`` before importing pyfmodex. 

.. todo:: Add instructions for library paths on Mac OS X and Windows

To download the FMOD Engine library, visit http://www.fmod.org/download. The library is free to download, but requires a free account to be made first.

Then, install pyfmodex via `pip`, `easy_install` or the `setup.py` way.

To verify if everything works, open a Python REPL and try importing pyfmodex:

.. code-block:: python

   import pyfmodex

If there is no error: good, it worked. :-)
