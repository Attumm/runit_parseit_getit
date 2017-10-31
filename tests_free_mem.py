template = """
Value Required Mem (\d+)
Value Free (\d+)
Value Swap (\d+)

Start
  ^Mem:[\s]*${Mem}
  ^-\/\+ buffers\/cache:[\s]*(\d+)[\s]*${Free}
  ^Swap:[\s]*${Swap} -> Record
""".strip()

result = """
 total       used       free     shared    buffers     cached
Mem:          1070        289        780          4         18        128
-/+ buffers/cache:        142        927
Swap:          461          0        461
""".strip()

import textfsm
from io import StringIO

t = textfsm.TextFSM(StringIO(template))
a = t.ParseText(result.strip())

for i in a:
    print(i)


