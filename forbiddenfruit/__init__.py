import ctypes


class PyObject(ctypes.Structure):
    pass


Py_ssize_t = \
    hasattr(ctypes.pythonapi, 'Py_InitModule4_64') \
    and ctypes.c_int64 or ctypes.c_int


PyObject._fields_ = [
    ('ob_refcnt', Py_ssize_t),
    ('ob_type', ctypes.POINTER(PyObject)),
]


class SlotsProxy(PyObject):
    _fields_ = [('dict', ctypes.POINTER(PyObject))]


def patchable_builtin(klass):
    name = klass.__name__
    target = getattr(klass, '__dict__', name)

    proxy_dict = SlotsProxy.from_address(id(target))
    namespace = {}

    ctypes.pythonapi.PyDict_SetItem(
        ctypes.py_object(namespace),
        ctypes.py_object(name),
        proxy_dict.dict,
    )

    return namespace[name]


def curse(klass, attr, value):
    dikt = patchable_builtin(klass)
    dikt[attr] = value
