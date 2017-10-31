template = """
Value Required Size (\w+)
Value Used (\w+)
Value Available (\w+)
Value Used_prec ([\d]+%)

Start
  ^total[\s]*${Size}[\s]*${Used}[\s]*${Available}[\s]*${Used_prec}
""".strip()

result = """
Filesystem      Size  Used Avail Use% Mounted on
/dev/sda1       9.2G  7.7G 1022M  89% /
udev             10M     0   10M   0% /dev
tmpfs           215M  4.4M  210M   3% /run
tmpfs           536M     0  536M   0% /dev/shm
tmpfs           5.0M     0  5.0M   0% /run/lock
tmpfs           536M     0  536M   0% /sys/fs/cgroup
none            233G  221G   13G  95% /vagrant
tmpfs           108M     0  108M   0% /run/user/1000
total           244G  229G   15G  94% -
""".strip()

import textfsm
from io import StringIO

t = textfsm.TextFSM(StringIO(template))
a = t.ParseText(result.strip())

for i in a:
    print(i)


