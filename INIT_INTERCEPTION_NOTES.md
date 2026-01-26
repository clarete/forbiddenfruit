# Intercepting set.__init__() Calls

## Summary

Built-in types like `set`, `dict`, and `list` use highly optimized constructors in CPython that bypass the normal `__new__` + `__init__` flow. This document explains the limitations and available workarounds.

## What Works ✅

### 1. Set Subclasses
Cursing `__init__` works perfectly on subclasses of built-in types:

```python
from forbiddenfruit import curse, reverse

class MySet(set):
    pass

def custom_init(self, args, kwargs):
    # Call original init to populate the set
    if args and hasattr(type(self), '_c___init__'):
        type(self)._c___init__(self, *args, **kwargs)
    self.custom_attr = 'initialized'
    return 0

curse(MySet, '__init__', custom_init)

s = MySet([1, 2, 3])  # custom_init is called!
assert s.custom_attr == 'initialized'
assert s == {1, 2, 3}
```

### 2. Explicit __init__ Calls
Direct calls to `__init__()` are intercepted:

```python
curse(set, '__init__', custom_init)

s = set.__new__(set)
s.__init__([1, 2, 3])  # custom_init is called!
```

### 3. Builtins Replacement
For read-only interception of `set()` constructor calls, replace `set` in builtins:

```python
import builtins

original_set = builtins.set
intercept_log = []

class SetInterceptor:
    def __new__(cls, iterable=None):
        intercept_log.append(('constructor_called', iterable))
        if iterable is None:
            return original_set()
        return original_set(iterable)

builtins.set = SetInterceptor

s = set([1, 2, 3])  # Intercepted!
# But note: s is still a real set, not a SetInterceptor instance
```

## What Doesn't Work ❌

### Direct Constructor Interception
Cursing `set.__init__` does NOT intercept `set([1,2,3])` calls:

```python
curse(set, '__init__', custom_init)

s = set([1, 2, 3])  # custom_init is NOT called (CPython optimization)
```

## Why This Happens

### CPython Optimizations
Built-in types like `set`, `dict`, `list` use vectorcall or similar optimizations that:
1. Create and initialize objects in a single C function call
2. Bypass the normal Python-level `__new__` + `__init__` sequence
3. Don't call `tp_init` from the type structure

### Investigation Results

We tested multiple interception approaches:

| Approach | Result | Notes |
|----------|--------|-------|
| Curse `set.__init__` | ❌ Doesn't intercept constructor | Only works for explicit calls |
| Curse `set.__new__` | ❌ Not called | Constructor bypasses it |
| Curse `type.__call__` | ❌ Not supported | Would affect all types |
| Hook `tp_call` | ❌ Not invoked | Optimization bypasses it |
| `sys.settrace` | ❌ C code invisible | Can't trace C functions |
| `sys.audit` | ❌ No relevant events | No object creation events |
| Replace in `builtins` | ✅ Works | Best option for read-only monitoring |

## Recommendations

1. **For custom functionality**: Use subclasses of `set`/`dict`/`list`
2. **For monitoring**: Replace the type in `builtins` module
3. **For testing**: Use explicit `__init__` calls or subclasses
4. **For production**: Accept that direct constructor calls can't be intercepted

## Technical Details

### tp_init Slot
The `tp_init` slot in `PyTypeObject` is properly set when cursing `__init__`, but CPython's optimized constructors don't call it:

```c
// Simplified CPython code for set()
static PyObject *
set_new(PyTypeObject *type, PyObject *args, PyObject *kwds)
{
    // Creates AND initializes the set in one go
    // Does NOT call tp_init!
    return setobject;
}
```

### Type Dictionary
We update both:
1. The `tp_init` slot (for explicit `__init__()` calls)
2. The type's `__dict__` (for Python-level attribute access)

This ensures cursing works for all supported use cases.

## See Also

- Test: `test_dunder_init_on_set_subclass()` - Demonstrates working subclass approach
- Test: `test_dunder_init_on_builtin_set_explicit_call()` - Shows explicit call behavior
- Test: `test_intercepting_set_via_builtins_replacement()` - Builtins replacement example
