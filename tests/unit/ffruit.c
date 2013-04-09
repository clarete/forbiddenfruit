#include <Python.h>
#include "structmember.h"


static PyObject *
ffruit_sum(PyObject *self, PyObject *args)
{
  int a, b;
  if (!PyArg_ParseTuple(args, "ii", &a, &b))
    return NULL;
  return Py_BuildValue("i", a + b);
}


typedef struct {
  PyObject_HEAD
  PyObject *args;
  PyObject *kwargs;
  int my_attr;
} Dummy;


static void
Dummy_dealloc(Dummy *self)
{
  Py_XDECREF(self->args);
  Py_XDECREF(self->kwargs);

#if PY_MAJOR_VERSION < 3
  self->ob_type->tp_free((PyObject *) self);
#else
  Py_TYPE(self)->tp_free((PyObject*)self);
#endif
}


static PyObject *
Dummy_new(PyTypeObject *type, PyObject *args, PyObject *kwargs)
{
  Dummy *self;

  self = (Dummy *) type->tp_alloc(type, 0);
  if (self != NULL) {
    self->args = Py_None;
    Py_INCREF(Py_None);

    self->kwargs = Py_None;
    Py_INCREF(Py_None);
  }
  self->my_attr = 0;

  return (PyObject *) self;
}


static PyObject *
Dummy_my_method(Dummy *self, PyObject *args, PyObject *kwargs)
{
  kwargs = (kwargs == NULL) ? PyDict_New() : kwargs;
  return Py_BuildValue("(OO)", args, kwargs);
}


static PyMemberDef Dummy_members[] = {
  {"args", T_OBJECT_EX, offsetof(Dummy, args), 0,
   "Argument list passed to the __init__ method"},
  {"kwargs", T_OBJECT_EX, offsetof(Dummy, kwargs), 0,
   "Keyword arguments passed to the __init__ method"},
  {"my_attr", T_INT, offsetof(Dummy, my_attr), 0,
   "An instance attribute"},
  {NULL}                        /* Sentinel */
};


static PyMethodDef Dummy_methods[] = {
  {"my_method", (PyCFunction) Dummy_my_method, METH_VARARGS | METH_KEYWORDS,
   "Return its argument list and keyword arguments"},
  {NULL}                        /* Sentinel */
};


static PyTypeObject DummyType = {
#if PY_MAJOR_VERSION < 3
  PyObject_HEAD_INIT(NULL)
  0,                         /*ob_size*/
#else
  PyVarObject_HEAD_INIT(NULL, 0)
#endif
  "ffruit.Dummy",            /*tp_name*/
  sizeof(Dummy),             /*tp_basicsize*/
  0,                         /*tp_itemsize*/
  (destructor) Dummy_dealloc,/*tp_dealloc*/
  0,                         /*tp_print*/
  0,                         /*tp_getattr*/
  0,                         /*tp_setattr*/
  0,                         /*tp_compare*/
  0,                         /*tp_repr*/
  0,                         /*tp_as_number*/
  0,                         /*tp_as_sequence*/
  0,                         /*tp_as_mapping*/
  0,                         /*tp_hash */
  0,                         /*tp_call*/
  0,                         /*tp_str*/
  0,                         /*tp_getattro*/
  0,                         /*tp_setattro*/
  0,                         /*tp_as_buffer*/
  Py_TPFLAGS_DEFAULT | Py_TPFLAGS_BASETYPE, /*tp_flags*/
  "Dummy forbidden fruits",  /*tp_doc*/
  0,                         /* tp_traverse */
  0,                         /* tp_clear */
  0,                         /* tp_richcompare */
  0,                         /* tp_weaklistoffset */
  0,                         /* tp_iter */
  0,                         /* tp_iternext */
  Dummy_methods,             /* tp_methods */
  Dummy_members,             /* tp_members */
  0,                         /* tp_getset */
  0,                         /* tp_base */
  0,                         /* tp_dict */
  0,                         /* tp_descr_get */
  0,                         /* tp_descr_set */
  0,                         /* tp_dictoffset */
  (initproc) 0,              /* tp_init */
  0,                         /* tp_alloc */
  Dummy_new,                 /* tp_new */
};


static PyMethodDef FFruitMethods[] = {
  {"sum",  ffruit_sum, METH_VARARGS, "sum two numbers."},
  {NULL, NULL, 0, NULL}
};

#if PY_MAJOR_VERSION >= 3
static struct PyModuleDef ffruitmodule = {
  PyModuleDef_HEAD_INIT,
  "ffruit",
  "Toy module",
  -1,
  FFruitMethods
};

#endif

#ifndef PyMODINIT_FUNC	/* declarations for DLL import/export */
# define PyMODINIT_FUNC void
#endif

#if PY_MAJOR_VERSION < 3
# define FUNC_NAME initffruit
#else
# define FUNC_NAME PyInit_ffruit
#endif

PyMODINIT_FUNC
FUNC_NAME(void)
{
  PyObject *m = NULL;

  if (PyType_Ready(&DummyType) < 0)
    goto end;

#if PY_MAJOR_VERSION < 3
  m = Py_InitModule("ffruit", FFruitMethods);
#else
  m = PyModule_Create(&ffruitmodule);
#endif
  if (m == NULL)
    goto end;

  Py_INCREF(&DummyType);
  PyModule_AddObject(m, "Dummy", (PyObject *)&DummyType);

 end:
#if PY_MAJOR_VERSION < 3
  return;
#else
  return m;
#endif
}
