
import textfsm


TEXTFSM_TEMPLATES = {
        "linux": {
            "`which ip` addr show": """
Value Required Interface ([^:]+)
Value MTU (\d+)
Value State (\w+)
Value MAC ([\d\w:]+)
Value List Inet ((?:[0-9]{1,3}\.){3}[0-9]{1,3})
# Don't match interface local (fe80::/10) - achieved with excluding '%'.
Value List Inet6 ([^/]*)

Start
  # Record interface record (if we have one).
  ^\S+:.* -> Continue.Record
  # Collect data for new interface.
  ^[1-9]: ${Interface}:.* mtu ${MTU}.* state ${State}
  ^\s+link\/ether ${MAC}
  ^\s+inet6 ${Inet6}
  ^\s+inet ${Inet}
""",
        "free -m": """
Value Required Mem (\d+)
Value Free (\d+)
Value Swap (\d+)

Start
  ^Mem:[\s]*${Mem}
  ^-\/\+ buffers\/cache:[\s]*(\d+)[\s]*${Free}
  ^Swap:[\s]*${Swap} -> Record
        """,
        "df -h --total": """
Value Required Size (\S*)
Value Used (\S*)
Value Available (\S*)
Value Used_prec (\S*)

Start
  ^total[\s]*${Size}[\s]*${Used}[\s]*${Available}[\s]*${Used_prec}
""",
        }
}



def parse_network(result, results):
    return result.strip()


PARSING = {
    "linux": {
        "hostname": lambda x, y: f'{str(x)[:-1]}',
        "hostname -I": lambda x, y: x.strip().split(' '),

        #"cat /etc/*-release": clean_cat_release,

        }
    }

import textfsm

from io import StringIO

def parse_textfsm(result, template):
    t = textfsm.TextFSM(StringIO(template))
    a = t.ParseText(result.strip())
    return a
    

raw_output = lambda x, y: ' '.join(x.replace('\t', ' ').split())

def parse(device, command, result, results):
    if command in TEXTFSM_TEMPLATES.get(device, {}):
        template = TEXTFSM_TEMPLATES[device][command].strip()
        return parse_textfsm(result, template)
    func = PARSING[device].get(command)
    if func is None:
        return result
    return func(result, results)
