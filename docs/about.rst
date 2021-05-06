About
=====

FMOD
----

`FMOD <https://fmod.com/>`_ is a solution of adaptive audio, mostly used for games.
The software suite consists of two components:

FMOD Studio:
   A GUI to build adaptive audio.

FMOD Engine:
   An API to play adaptive audio.

The FMOD Engine API consists of

Studio API:
   Plays back content created within the FMOD Studio authoring tool. 
   Studio's data-driven approach means audio behaviors remain easily accessible and editable to sound designers.

Core API:
   Allows for custom requirements that go beyond what the FMOD Studio API offers, providing fast and flexible access to low-level audio primitives.

The documentation for these components can be found at https://fmod.com/resources/documentation-api.

pyfmodex
--------

The FMOD APIs have officiale bindings for C, C++, C# and Javascript.
`pyfmodex` provides unofficial bindings for Python.

Goal of the project
^^^^^^^^^^^^^^^^^^^

The goal of the `pyfmodex` project - ran by volunteers in the Open Source community - is to provide a first class package to allow users to interface with FMOD from within their Python programs without needing to worry about the internals.

The intention is to

 - support the last three stable minor releases of Python
 - support Linux x86 and Windows platforms
 - keep documentation and code quality consistently high

Given the portable nature of both Python and the FMOD libraries, this ought to mean that `pyfmodex` works just fine on other platforms (Mac OS) or architectures (Raspberry Pi, ...).

This concerted effort can be found on the `Github page <https://github.com/tyrylu/pyfmodex/>`_ of the project's founder Lukáš Tyrychtr.

The name
^^^^^^^^

The name `pyfmodex` comes from the legacy name "FMOD Ex" that was used by FMOD in the past.
