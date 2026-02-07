# PR Review Response

## Review Comments Addressed

### 1. ✅ PyType_Modified() Call Ordering (MAIN COMMENT)

**Review Comment:** "PyType_Modified() should be called AFTER all mutations are done, not before."

**What Was Done:**
- **Commit b629729:** Moved `PyType_Modified()` call to the END of `_curse_special()`, after both:
  1. Setting the `tp_hash` slot
  2. Updating the type's `__dict__`

**Why This Matters:**
- Calling `PyType_Modified()` in the middle of mutations could lead to inconsistent cache states
- Python might access the type between operations and cache inconsistent state
- Now Python's internal caches are invalidated AFTER all state is consistent

**Code Change:**
```python
# Before (in _curse_special):
setattr(tyobj, impl_method, cfunc)
ctypes.pythonapi.PyType_Modified(ctypes.py_object(klass))  # Called in middle
dikt[attr] = func

# After:
setattr(tyobj, impl_method, cfunc)
dikt[attr] = func
ctypes.pythonapi.PyType_Modified(ctypes.py_object(klass))  # Called at end
```

### 2. ✅ Missing PyType_Modified() in _revert_special

**What Was Done:**
- **Commit b629729:** Added `PyType_Modified()` call to `_revert_special()`
- This was completely missing before

**Why This Matters:**
- When reversing a curse, Python's caches need to be invalidated
- Without this, Python might continue using cached information about the cursed method

### 3. ✅ Dict Value Preservation Bug (DISCOVERED DURING REVIEW)

**Bug Found:** After calling `reverse(object, '__hash__')`, any newly defined classes would become unhashable with `TypeError: unhashable type`.

**Root Cause Analysis:**
1. `_curse_special()` was overwriting `__dict__` entries without saving the original
2. `_revert_special()` was deleting the entry instead of restoring the original
3. For built-in types like `object`, `__hash__` is a slot wrapper in `__dict__`
4. Deleting it made Python unable to find `__hash__` via attribute lookup
5. Even though `tp_hash` slot was correctly restored, new classes couldn't find it

**What Was Done:**
- **Commit a417c29:** Fixed both functions to match regular `curse()`/`reverse()` behavior:
  - `_curse_special()`: Save original dict value with `_c_` prefix (e.g., `_c___hash__`)
  - `_revert_special()`: Restore original value instead of deleting

**Code Changes:**
```python
# In _curse_special:
dikt = patchable_builtin(klass)
# NEW: Save original value (like regular curse does)
old_value = dikt.get(attr, None)
old_name = '_c_%s' % attr
if old_value:
    dikt[old_name] = old_value
dikt[attr] = func

# In _revert_special:
dikt = patchable_builtin(klass)
old_name = '_c_%s' % attr
if old_name in dikt:
    # NEW: Restore original instead of deleting
    dikt[attr] = dikt[old_name]
    del dikt[old_name]
elif attr in dikt:
    del dikt[attr]
```

## Review Comments NOT Addressed

None. All review feedback was addressed.

The PR review specifically mentioned:
> "for comments about nontrivial potential bugs (like other than missing finally, etc), always ensure it is actually a bug (through test cases) before fixing it"

The dict preservation bug was verified through extensive testing before fixing (see commits for test traces).

## Tests Added

### Test 1: `test_dunder_hash()` (Line 383-401)
**Purpose:** Test basic `__hash__` cursing on custom classes

**What It Tests:**
- Custom hash function returns expected value
- Dict operations work with cursed hash
- Reverse properly restores functionality

**Code:**
```python
def test_dunder_hash():
    "Test that __hash__ can be cursed on custom classes"
    def custom_hash(self):
        return 12345
    
    curse(ffruit.Dummy, '__hash__', custom_hash)
    obj = ffruit.Dummy()
    assert hash(obj) == 12345
    
    d = {obj: 'value'}
    assert d[obj] == 'value'
    
    reverse(ffruit.Dummy, '__hash__')
```

### Test 2: `test_dunder_hash_on_object()` (Line 405-443)
**Purpose:** Test cursing `object.__hash__` (the original problem statement)

**What It Tests:**
- Cursing base `object` class works
- Classes defined AFTER curse inherit the cursed hash
- Custom hash is called when creating sets/dicts
- Reverse properly cleans up

**Code:**
```python
def test_dunder_hash_on_object():
    "Test that __hash__ can be cursed on object base class"
    call_log = []
    _orig_hash = object.__hash__
    
    def custom_hash(self):
        call_log.append(repr(self))
        return _orig_hash(self)
    
    # Curse BEFORE defining class
    curse(object, '__hash__', custom_hash)
    
    # Define class after curse
    class TestClass():
        def __init__(self, x):
            self.x = x
        def __repr__(self):
            return f"TestClass({self.x})"
    
    # Create set triggers hashing
    obj1 = TestClass(1)
    obj2 = TestClass(2)
    obj3 = TestClass(3)
    s = {obj1, obj2, obj3}
    
    # Verify custom hash was called
    assert len(call_log) >= 3
    assert "TestClass(1)" in str(call_log)
    assert "TestClass(2)" in str(call_log)
    assert "TestClass(3)" in str(call_log)
    assert len(s) == 3
    
    reverse(object, '__hash__')
```

### Additional Manual Testing (Not in Test Suite)

During development, extensive manual testing was performed:

1. **Reverse Functionality Test:**
   - Verified classes defined before curse work after reverse
   - Verified classes defined after reverse are not cursed
   - Verified classes defined during curse keep cursed hash (expected Python behavior)

2. **Context Manager Test:**
   - Verified `cursed()` context manager works with `__hash__`
   - Verified cleanup happens automatically

3. **Multiple Curse/Reverse Cycles:**
   - Verified multiple curse→reverse cycles work correctly
   - No memory leaks or state corruption

## Expected Behavior Notes

### Class Creation Timing Matters

**Expected Python Behavior:**
- Classes copy slot values at creation time
- Classes defined BEFORE curse: Have original hash (won't be affected)
- Classes defined DURING curse: Have cursed hash (keep it even after reverse)
- Classes defined AFTER reverse: Have restored hash

**Example:**
```python
class Before: pass  # Has original hash

curse(object, '__hash__', custom_hash)
class During: pass  # Has cursed hash

reverse(object, '__hash__')
class After: pass   # Has original hash

# After reverse:
hash(Before())  # ✓ Works (original)
hash(During())  # ✓ Works but still uses cursed hash (copied slot)
hash(After())   # ✓ Works (restored)
```

This is expected behavior because Python copies `tp_hash` pointers when creating type objects. The curse/reverse only affects the base type and future classes.

## Summary

**All review comments were addressed:**
1. ✅ Fixed PyType_Modified() call ordering 
2. ✅ Added missing PyType_Modified() to _revert_special
3. ✅ Fixed critical dict preservation bug (discovered during review)

**Tests added:**
1. ✅ test_dunder_hash() - Basic custom class hash cursing
2. ✅ test_dunder_hash_on_object() - Original problem statement test

**No comments were left unaddressed.**
