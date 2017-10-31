template1 = """
Value Required Interface ([^:]+)
Value MTU (\d+)
Value State ((in)?active)
Value MAC ([\d\w:]+)
Value List Inet ([\d\.]+)
Value List Netmask (\S+)
# Don't match interface local (fe80::/10) - achieved with excluding '%'.
Value List Inet6 ([^%]+)
Value List Prefix (\d+)

Start
  # Record interface record (if we have one).
  ^\S+:.* -> Continue.Record
  # Collect data for new interface.
  ^${Interface}:.* mtu ${MTU}
  ^\s+ether ${MAC}
  ^\s+inet6 ${Inet6} prefixlen ${Prefix}
  ^\s+inet ${Inet} netmask ${Netmask}
""".strip()


template = """
Value Required Interface ([^:]+)
Value MTU (\d+)
Value State (\w+)
Value MAC ([\d\w:]+)
Value List Inet ((?:[0-9]{1,3}\.){3}[0-9]{1,3})
# Don't match interface local (fe80::/10) - achieved with excluding '%'.
Value List Inet6 ([^%]+)
Value List Prefix (\d+)

Start
  # Record interface record (if we have one).
  ^\S+:.* -> Continue.Record
  # Collect data for new interface.
  ^[1-9]: ${Interface}:.* mtu ${MTU}.* state ${State}
  ^\s+link\/ether ${MAC}
  ^\s+inet6 ${Inet6}
  ^\s+inet ${Inet}
""".strip()



result1 = """

lo0: flags=8049<UP,LOOPBACK,RUNNING,MULTICAST> mtu 16384
        inet6 ::1 prefixlen 128
        inet6 fe80::1%lo0 prefixlen 64 scopeid 0x1
        inet 127.0.0.1 netmask 0xff000000
en0: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        ether 34:15:9e:27:45:e3
        inet6 fe80::3615:9eff:fe27:45e3%en0 prefixlen 64 scopeid 0x4
        inet6 2001:db8::3615:9eff:fe27:45e3 prefixlen 64 autoconf
        inet 192.0.2.215 netmask 0xfffffe00 broadcast 192.0.2.255
        media: autoselect (1000baseT <full-duplex,flow-control>)
        status: active
en1: flags=8863<UP,BROADCAST,SMART,RUNNING,SIMPLEX,MULTICAST> mtu 1500
        ether 90:84:0d:f6:d1:55
        media: <unknown subtype> (<unknown type>)
status: inactive
""".strip()

result = """
1: lo: <LOOPBACK,UP,LOWER_UP> mtu 65536 qdisc noqueue state UNKNOWN group default
    link/loopback 00:00:00:00:00:00 brd 00:00:00:00:00:00
    inet 127.0.0.1/8 scope host lo
       valid_lft forever preferred_lft forever
    inet6 ::1/128 scope host
       valid_lft forever preferred_lft forever
2: eth0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:93:e9:07 brd ff:ff:ff:ff:ff:ff
    inet 10.0.2.15/24 brd 10.0.2.255 scope global eth0
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe93:e907/64 scope link
       valid_lft forever preferred_lft forever
3: eth1: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc pfifo_fast state UP group default qlen 1000
    link/ether 08:00:27:52:e6:a1 brd ff:ff:ff:ff:ff:ff
    inet 192.168.33.11/24 brd 192.168.33.255 scope global eth1
       valid_lft forever preferred_lft forever
    inet6 fe80::a00:27ff:fe52:e6a1/64 scope link
       valid_lft forever preferred_lft forever
""".strip()
import textfsm

from io import StringIO

t1 = textfsm.TextFSM(StringIO(template1))
a1 = t1.ParseText(result1.strip())
for i in a1:
    print(i)

t = textfsm.TextFSM(StringIO(template))
a = t.ParseText(result.strip())

for i in a:
    print(i)


