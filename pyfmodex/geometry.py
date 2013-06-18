from .fmodobject import *
from .globalvars import dll as _dll
from .structures import VECTOR

class PolygonAttributes(object):
    def __init__(self, gptr, index):
        self._gptr = gptr
        self.index = index
        self._directocclusion = c_float()
        self._reverbocclusion = c_float()
        self._doublesided = c_bool()
        ckresult(_dll.FMOD_Geometry_GetPolygonAttributes(self._ptr, self.index, byref(self._directocclusion), byref(self._reverbocclusion), byref(self._doublesided)))

    @property
    def direct_occlusion(self):
        return self._directocclusion.value
    @direct_occlusion.setter
    def direct_occlusion(self, occ):
                ckresult(_dll.FMOD_Geometry_SetPolygonAttributes(self._gptr, self.index, occ, self._reverbocclusion, self._doublesided))

    @property
    def reverb_occlusion(self):
        return self._reverbocclusion.value
    @reverb_occlusion.setter
    def reverb_occlusion(self, occ):
                ckresult(_dll.FMOD_Geometry_SetPolygonAttributes(self._gptr, self.index, self._directocclusion, occ, self._doublesided))

    @property
    def double_sided(self):
        return self._doublesided
    @double_sided.setter
    def double_sided(self, dval):
                ckresult(_dll.FMOD_Geometry_SetPolygonAttributes(self._gptr, self.index, occ, self._reverbocclusion, dval))

    @property
    def num_vertices(self):
        num = c_int()
        ckresult(_dll.FMOD_Geometry_GetPolygonNumVertices(self._gptr, self.index, byref(num)))
        return num.value

    def get_vertex(self, index):
        vertex = VECTOR()
        ckresult(_dll.FMOD_Geometry_GetPolygonVertex(self._gptr, self.index, index, byref(vertex)))
        return vertex.to_list()

    def set_vertex(self, index, vertex):
        vvec = VECTOR.from_list(vertex)
        ckresult(_dll.FMOD_Geometry_SetPolygonVertex(self._gptr, self.index, index, vvec))


class Geometry(FmodObject):

    def add_polygon(self, directocclusion, reverbocclusion, doublesided, *vertices):
        va = VECTOR * len(vertices)
        varray = va(*vertices)
        idx = c_int()
        self._call_fmod("FMOD_Geometry_AddPolyGon", directocclusion, reverbocclusion, doublesided, len(vertices), byref(varray), byref(idx))
        return idx.value

    @property
    def active(self):
        active = c_bool()
        self._call_fmod("FMOD_Geometry_GetActive", byref(active))
        return active.value
    @active.setter
    def active(self, ac):
        self._call_fmod("FMOD_Geometry_SetActive", ac)

    @property
    def _creation_limits(self):
        maxpols, maxverts = (c_int(), c_int())
        self._call_fmod("FMOD_Geometry_GetMaxPolygons", byref(maxpols), byref(maxverts))
        return (maxpols.value, maxverts.value)


    @property
    def max_polygons(self):
        return self._creation_limits[0]
    @property
    def max_vertices(self):
        return self._creation_limits[1]
    
    @property
    def num_polygons(self):
        num = c_int()
        self._call_fmod("FMOD_Geometry_GetNumPolygons", byref(num))
        return num.value

    def get_polygon(self, index):
        return PolygonAttributes(self._ptr, index)

    @property
    def position(self):
        pos = VECTOR()
        self._call_fmod("FMOD_Geometry_GetPosition", byref(pos))
        return pos.to_list()
    @position.setter
    def position(self, pos):
        posv = VECTOR.from_list(pos)
        self._call_fmod("FMOD_Geometry_SetPosition", posv)

    @property
    def _rotation(self):
        fwd = VECTOR()
        up = VECTOR()
        self._call_fmod("FMOD_Geometry_GetRotation", byref(fwd), byref(up))
        return [fwd.to_list(), up.to_list()]
    @_rotation.setter
    def _rotation(self, rot):
        fwd = VECTOR.from_list(rot[0])
        up = VECTOR.from_list(rot[1])
        self._call_fmod("Geometry_SetRotation", fwd, up)

    @property
    def forward_rotation(self):
        return self._rotation[0]
    @forward_rotation.setter
    def forward_rotation(self, rot):
        r = self._rotation
        r[0] = rot
        self._rotation = r

    @property
    def up_rotation(self):
        return self._rotation[1]
    @up_rotation.setter
    def up_rotation(self, rot):
        r = self._rotation
        r[1] = rot
        self._rotation = r

    @property
    def scale(self):
        scale = VECTOR()
        self._call_fmod("FMOD_Geometry_GetScale", byref(scale))
        return scale.to_list()
    @scale.setter
    def position(self, scale):
        scalev = VECTOR.from_list(scale)
        self._call_fmod("FMOD_Geometry_SetScale", scalev)

    def release(self):
        self._call_fmod("FMOD_Geometry_Release")

    def save(self):
        size = c_int()
        ptr = c_void_p()
        self._call_fmod("FMOD_Geometry_Save", 0, byref(size))
        self._call_fmod("FMOD_Geometry_Save", ptr, byref(size))
        return ptr.value
        return string_at(ptr, size)