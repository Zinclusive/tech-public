
def assert_equals(expected, actual, desc=""):
    if expected == actual: return
    if expected is actual: return
    e = repr(expected)
    a = repr(actual)
    s = f"""
ASSERT ERROR: {desc}
EXPECT: [{e}] len={len(e)}
ACTUAL: [{a}] len={len(a)}
"""
    raise AssertionError(s)
    