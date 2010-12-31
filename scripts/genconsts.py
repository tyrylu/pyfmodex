#This script analyzes the fmod header file and generates structures.py, enums.py and callbackprototypes.py.
#We're going to parse the xml output from gccxml's work.
#We are using following mapping from c types to ctypes equivalents
import os
import xml.etree.ElementTree as et
types_map = {"int": "c_int", "float": "c_float", "char*": "c_char_p", "void*": "c_void_p", "unsigned short": "c_ushort", "unsigned int": "c_uint", "enum":"c_int", "short unsigned int":"c_ushort", "unsigned char":"c_ubyte","char":"c_char","void":"c_void"}
#Which types are function types?
function_types = []
initial_lines = "from ctypes import *\n"
enums = initial_lines
structures = initial_lines + "\nfrom callbackprototypes import *\n"
callbackprototypes = initial_lines + "\nimport os\nfunc = WINFUNCTYPE if os.name == \"nt\" else CFUNCTYPE"

def create_enum_code(enum_elem):
    global enums, types_map
    name = enum_elem.attrib["name"]
    #We know about new type, so we're going to add it to our mapping
    types_map[name] = "c_int"
    enums += "#%s enumeration.\n"%name
    for enum_val in enum_elem.getchildren():
        enums += "%s = %s\n"%(enum_val.attrib["name"], enum_val.attrib["init"])
    enums += "\n"

def create_function_type_code(func_name, func_elem):
    global callbackprototypes
    print func_name + " - generating."
    callbackprototypes += "%s = func(%s,"%(func_name,get_type(elems_by_id[func_elem.attrib["returns"]]))
    for arg in func_elem.getchildren():
        callbackprototypes += " %s,"%get_type(elems_by_id[arg.attrib["type"]], func_name)
    callbackprototypes += callbackprototypes[:-1] + ")\n"

def create_struct_code(struct_elem):
    global structures
    if struct_elem.attrib.has_key("incomplete"): return #Skip all incomplete structures, we have dealed with them earlier.
    structures += "class %s(Structure):\n"%struct_elem.attrib["name"]
    structures += " " * 4 + "_fields_ = [\n"
    for mid in struct_elem.attrib["members"].split():
        m = elems_by_id[mid]
        if m.tag == "Field": #Structure field.
            structures += " " * 8 + "(\"%s\", %s)\n"%(m.attrib["name"], get_type(elems_by_id[m.attrib["type"]]))
    structures += " " * 4 + "]\n"

def get_type(type_elem, type_name=""):
    global types_map, function_types
    #If we don't hawe name of the type, we're going to handle new type.
    if not type_name:
        print "Name not known from param, tag %s"%type_elem.tag
        type_name = type_elem.attrib.get("name", "unknown")
    #We could have seen this type in some other call, so we'll try it.
    if types_map.has_key(type_name):
        return types_map[type_name]
    #Then, we should check if this isn't only a reference for somethink else.
    if type_elem.attrib.has_key("type"):
        t = get_type(elems_by_id[type_elem.attrib["type"]], type_name)
        #Add it for later time.
        types_map[type_name] = t
        return t
    #If this is a fundamental type, we already know about the right definition.
    if type_elem.tag == "FundamentalType":
        return types_map[type_elem.attrib["name"]]
    #Or, it might be a function type definition?
    elif type_elem.tag == "FunctionType":
        function_types.append(type_name)
        create_function_type_code(type_name, type_elem)
        return type_name #We can return same name, because we're really referencing function prototype object later.
doc = et.parse("fmodout.xml")
root = doc.getroot()
#generate enumerations
print "Generating enumerations..."
for enum in root.findall("Enumeration"):
    create_enum_code(enum)
#Now, before we continue, we'll introduce some types as c_ints. These types are incomplete structures for c compilers.
print "Adding incomplete structures as c_ints..."
for st in root.findall("Struct"):
    if st.attrib.has_key("incomplete"):
       types_map[st.attrib["name"]] = "c_int"
#Now, we'll introduce mapping from ids to etree elements.
elems_by_id = {}
print "Generating elems_by_id dict..."
for el in root.getchildren():
    elems_by_id[el.attrib["id"]] = el
#Now, add all remaining unknown types.
print "Adding remaining type declarations and generating callback prototypes."
for td in root.findall("Typedef"):
    t = get_type(td)
#After this, structures are waiting for us.
print "Generating structures..."
for st in root.findall("Struct"):
    create_struct_code(st)
#Final part, write the results.
f = open("enums.py", "w")
f.write(enums)
f.close()
f = open("structures.py", "w")
f.write(structures)
f.close()
f = open("callbackprototypes.py", "w")
f.write(callbackprototypes)
f.close()