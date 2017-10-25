def parse_network(stdout, stderr, results):
    return stdout.strip()

PARSING = {
    "linux": {
        "hostname": lambda x, y, z: f'hostname: {str(x)[:-1]}',
        "ip addr show": parse_network
        }
    }

raw_output = lambda x, y, z: ' '.join(x.replace('\t', ' ').split())

def parse(device, command, stdout, stderr, results):
    func = PARSING[device].get(command, raw_output)
    return func(stdout, stderr, results)
