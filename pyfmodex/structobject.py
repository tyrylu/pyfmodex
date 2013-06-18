#Implementation from http://benlast.livejournal.com/12301.html with removed unnecessary zope security flag
class Structobject(object):
    def __init__(self, **kw):
        """Initialize, and set attributes from all keyword arguments."""
        self.__members=[]
        for k in list(kw.keys()):
            setattr(self,k,kw[k])
            self.__remember(k)


    def __remember(self, k):
        """Add k to the list of explicitly set values."""
        if not k in self.__members:
            self.__members.append(k)


    def __getitem__(self, key):
        """Equivalent of dict access by key."""
        try:
            return getattr(self, key)
        except AttributeError:
            raise KeyError(key)


    def __setitem__(self, key, value):
        setattr(self, key, value)
        self.__remember(key)


    def has_key(self, key):
        return hasattr(self, key)


    def keys(self):
        return self.__members


    def iterkeys(self):
        return self.__members


    def __iter__(self):
        return iter(self.__members)


    def __str__(self):
        """Describe only those attributes explicitly set."""
        s = ""
        for x in self.__members:
            v = getattr(self, x)
            if s: s+=", "
            s += "%s: %s" % (x, repr(v))
        return s
