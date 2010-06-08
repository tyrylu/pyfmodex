#This script analyzes the fmod header file and generates structures.py and constants.py.
#Enum values start from 0 and increase in every step by 1
#We are using following mapping from c types to ctypes equivalents
types_map = {"int": "c_int", "float": "c_float", "string": "c_char_p", "intptr": "c_void_p", "ushort": "c_ushort", "uint": "c_uint"}
initial_lines = "from ctypes import *\n"
constants = initial_lines
structures = initial_lines
callbackprototypes = initial_lines
infile = open("fmod.cs", "r")
in_block = False
for line in infile:
    line = line.trim()
    lineparts = line.split(" ")
    #Beginning of anything interesting?
