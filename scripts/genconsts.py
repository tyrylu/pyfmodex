#This script analyzes the fmod header file and generates structures.py and constants.py.
#We're using pygccxml for our hard parsing job.
#We are using following mapping from c types to ctypes equivalents
import os
from pygccxml import parser, declarations
types_map = {"int": "c_int", "float": "c_float", "char*": "c_char_p", "void*": "c_void_p", "unsigned short": "c_ushort", "unsigned int": "c_uint"}
initial_lines = "from ctypes import *\n"
constants = initial_lines
structures = initial_lines
callbackprototypes = initial_lines
gc_path = r"c:\gccxml\bin"
fmod_h_path = r"c:\gccxml\bin\fmod.h"
cfg = parser.config_t(gccxml_path=gc_path)
ns_list = parser.parse([fmod_h_path], cfg)
ns = ns_list[0]
def gen_enum(enum):
    """Appends code for one enumeration type."""
    constants += "#Definition for %s enumeration.\n"%enum.name
    for name, value in enum.values:
        constants += "%s = %s\n"(name, value)

def gen_struct(s):
    structures += "class %s(Structure):"%s.name
    structures += "    _fields_ = ["
    fields = [f for f in s.public_members() if type(f) == declarations.variable_t]
    for f in fields:
        structures += "        (%s, \"%s\")\n"%(f.name, get_type(f.type))
    structures += "    ]\n"

#Enumerations
for e in ns.enums():
    gen_enum(e)
#structures
for c in n.classes():
    gen_struct(c)
callbacks = [t for t in n.typedefs() if t.name.endswith("CALLBACK")
for c in callbacks:
    gen_callback(c)
cur_dir = os.path.dirname(__file__)
sf = open(os.path.join(cur_dir, "../structures.py", "w")
sf.write(structures)
sf.close()