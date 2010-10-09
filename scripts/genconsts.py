#This script analyzes the fmod header file and generates structures.py and constants.py.
#We're using pygccxml for our hard parsing job.
#We are using following mapping from c types to ctypes equivalents
import os
from pygccxml import parser, declarations
types_map = {"int": "c_int", "float": "c_float", "char*": "c_char_p", "void*": "c_void_p", "unsigned short": "c_ushort", "unsigned int": "c_uint", "enum":"c_int", "short unsigned int":"c_ushort", "unsigned char":"c_ubyte","char":"c_char","void":"c_void"}
initial_lines = "from ctypes import *\n"
constants = initial_lines
structures = initial_lines + "\nfrom callbackprototypes import *\n"
callbackprototypes = initial_lines + "\nimport os\nfunc = WINFUNCTYPE if os.name == \"nt\" else CFUNCTYPE"
gc_path = r"c:\gccxml\bin"
fmod_h_path = r"c:\gccxml\bin\fmod.h"
cfg = parser.config_t(gccxml_path=gc_path)
ns_list = parser.parse([fmod_h_path], cfg)
ns = ns_list[0]

def get_type(type):
    print "Request for type %s"%type
    if isinstance(type, declarations.fundamental_t): return types_map[str(type)]
    if isinstance(type, declarations.enumeration_t): return "enum"
    if isinstance(type, declarations.array_t):
        basetype = get_type(type.base)
        return "%s * %i"%(basetype,type.size)
    if isinstance(type, declarations.pointer_t):
        if isinstance(type.base, declarations.const_t): return types_map["%s*"%str(type.base.base)]

def gen_callback(name, func):
    global callbackprototypes
    print "generating callback %s"%name
    callbackprototypes += "\n%s = func("%name
    if hasattr(func.return_type, "declaration"):
        rdec = func.return_type.declaration
    else:
        rdec = func.return_type
    rettype = get_type(rdec)
    if not rettype: introduce_type(rdec)
    callbackprototypes += "%s,"%get_type(func.return_type)
    for argtype in func.arguments_types:
        at = get_type(argtype)
        if not at: introduce_type(argtype)
        callbackprototypes += "%s,"%get_type(argtype)
    callbackprototypes = callbackprototypes[:-1]
    callbackprototypes += ")\n"
   
def introduce_type(t):
    print "introducing type %s of class %s"%(t,str(type(t)))
    if hasattr(t, "type"):
        tvar = t.type
    else:
        tvar = t
    guess = get_type(tvar)
    if guess:
        types_map[t.name] = guess    
    else:
        if isinstance(tvar, declarations.pointer_t):
            p = tvar
            if isinstance(p.base, declarations.free_function_type_t):
                gen_callback(t.name, p.base)
                types_map[t.name] = t.name

def gen_enum(enum):
    global constants
    """Appends code for one enumeration type."""
    constants += "\n#Definition for %s enumeration.\n"%enum.name
    for name, value in enum.values:
        constants += "%s = %s\n"%(name, value)

def gen_struct(s):
    global structures    
    structures += "\nclass %s(Structure):\n"%s.name
    structures += "    _fields_ = [\n"
    fields = [f for f in s.public_members if type(f) == declarations.variable_t]
    currfield = 1
    for f in fields:
        if currfield != len(fields):
            tpl = "        (\"%s\", %s),\n"
        else:
            tpl = "        (\"%s\", %s)\n"
        structures += tpl%(f.name, get_type(f.type))
        currfield += 1
    structures += "    ]\n"
    fnames = [f.name for f in fields]
    if "cbsize" in fnames:
        structures += "\n    def __init__(self, *args, **kwargs):\n        super(%s, self).__init__(self, *args, **kwargs)\n        self.cbsize = sizeof(self)\n"%s.name

#Introduce custom fmod ex types for next time reference
for t in ns.typedefs():
    introduce_type(t)    
#Enumerations
for e in ns.enums():
    gen_enum(e)
#structures
for c in ns.classes():
    gen_struct(c)
cur_dir = os.path.dirname(__file__)
sf = open(os.path.join(cur_dir, "../structures.py"), "w")
sf.write(structures)
sf.close()
cf = open(os.path.join(cur_dir, "../constants.py"), "w")
cf.write(constants)
cf.close()
cf = open(os.path.join(cur_dir, "../callbackprototypes.py"), "w")
cf.write(callbackprototypes)
cf.close()