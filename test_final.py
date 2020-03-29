def assertEqualPrint(a, b):
    try: assert a == b; print(f"{a} equals {b}")
    except AssertionError: print(f"{a} does not equal {b}")
    finally: print("do this last")

def assertEqualReturn(a, b):
    try: assert a == b; return f"{a} equals {b}"
    except AssertionError: return f"{a} does not equal {b}"
    finally: return "You thought the 'finally'-block would run AFTER try/except? lol u big dumdum"

assertEqualPrint(True, False)
print(assertEqualReturn(True, False))