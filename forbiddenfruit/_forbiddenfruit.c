#include "Python.h"

typedef struct {
  _PyObject_HEAD_EXTRA
} ExtraHeadStruct;

/*
    Use this method to determine offset of refcnt of a PyObject
    on python debug builds
*/
PyObject* get_extra_head_size(PyObject* self, PyObject* args) {
    return PyLong_FromLong(sizeof(ExtraHeadStruct));
}

PyObject* get_not_implemented(PyObject* self, PyObject* args) {
    Py_INCREF(Py_NotImplemented);
    return Py_NotImplemented;
}

static PyMethodDef FFruitMethods[] = {
  {"get_extra_head_size",  get_extra_head_size, METH_NOARGS, "xo size of the PyObject_HEAD macro."},
  {"get_not_implemented",  get_not_implemented, METH_NOARGS, "Get the Py_NotImplemented object."},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef ffruitmodule = {
  PyModuleDef_HEAD_INIT,
  "_forbiddenfruit",
  "Helpers for forbidden fruit",
  -1,
  FFruitMethods
};

#endif

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
# define PyMODINIT_FUNC void
#endif

#if PY_MAJOR_VERSION < 3
# define FUNC_NAME init_forbiddenfruit
#else
# define FUNC_NAME PyInit__forbiddenfruit
#endif

PyMODINIT_FUNC
FUNC_NAME(void)
{
  PyObject *m = NULL;

#if PY_MAJOR_VERSION < 3
  m = Py_InitModule("_forbiddenfruit", FFruitMethods);
#else
  m = PyModule_Create(&ffruitmodule);
#endif
  if (m == NULL)
    goto end;

 end:
#if PY_MAJOR_VERSION < 3
  return;
#else
  return m;
#endif
}
