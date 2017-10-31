template = """
Value Required Size (\S*)
Value Used (\S*)
Value Available (\S*)
Value Used_prec (\S*)

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

result1 = """
Filesystem                   Size  Used Avail Use% Mounted on
/dev/mapper/vgroot-lv_root   8.0G  3.1G  5.0G  39% /
devtmpfs                     7.8G     0  7.8G   0% /dev
tmpfs                        7.8G     0  7.8G   0% /dev/shm
tmpfs                        7.8G  824M  7.0G  11% /run
tmpfs                        7.8G     0  7.8G   0% /sys/fs/cgroup
/dev/mapper/vgroot-lv_tmp   1014M   33M  982M   4% /tmp
/dev/mapper/vgapp-lv_app      20G   72M   19G   1% /app
/dev/mapper/vgroot-lv_home   125M   21M  104M  17% /export/home
/dev/mapper/vgroot-lv_var    2.0G  644M  1.4G  32% /var
/dev/mapper/vgroot-lv_log    2.0G  1.5G  551M  73% /var/log
/dev/sda1                    497M  253M  245M  51% /boot
/dev/mapper/vgroot-lv_audit   97M   43M   54M  45% /var/log/audit
tmpfs                        1.6G     0  1.6G   0% /run/user/47042
tmpfs                        1.6G     0  1.6G   0% /run/user/35939
total                         68G  6.4G   60G  10% -
"""

import textfsm
from io import StringIO

t = textfsm.TextFSM(StringIO(template))
a = t.ParseText(result.strip())

for i in a:
    print(i)


