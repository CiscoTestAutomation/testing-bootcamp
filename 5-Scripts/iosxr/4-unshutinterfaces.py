# Shut all the interfaces
# return the list of interfaces that were shut
from genie.testbed import load
import argparse

# Provide argument at runtime
parser = argparse.ArgumentParser(description='')
parser.add_argument('--interfaces',
                    nargs='*',
                    type=str,
                    help='Interface to shut')
parser.add_argument('--unshut',
                    action='store_true',
                    help='If selected, then it will unshut the interfaces')

custom_args = parser.parse_known_args()[0]

def interfaces_up(device):
    up_interfaces = []
    output = device.parse('show interfaces')
    for interface in output:
        if interface == 'Null0':
            continue
        # status
        if 'enabled' in output[interface] and\
           output[interface]['enabled'] is True:
            up_interfaces.append(interface)
    return  up_interfaces

tb = load('../../testbed.yaml')


device = tb.devices['xr-1']
#devices = (tb.devices['iosxrv9000-1'], tb.devices['iosxrv9000-2'])

# Connect to the device via Console; as we want to shut all the interfaces
device.connect(via='cli')

if custom_args.interfaces:
    interface_to_modify = custom_args.interfaces
else:
    interface_to_modify = interfaces_up(device)

configuration = []
un_configuration = []
print("{device}: modifying the following interfaces"
      "'{to_shut}'".format(device=device.name, to_shut=interface_to_modify))

for interface in interface_to_modify:
    configuration.append('interface {intf}\nshut'.format(intf=interface))
    un_configuration.append('interface {intf}\nno shut'.format(intf=interface))

# Once its all collected, shut the interface
if custom_args.unshut:
    device.configure(un_configuration)
else:
    device.configure(configuration)

# Verify they are all down
interfaces_up = interfaces_up(device)
if interfaces_up and not custom_args.unshut:
    raise Exception("{device}: Have shut the following interfaces "
                    "'{to_shut}' but '{intf}' are still up".format(device=device.name,
                                                                   to_shut=interface_to_modify,
                                                                   intf=interfaces_up))
elif custom_args.unshut:
    # Verify they are all up
    if not set(interface_to_modify).issubset(interfaces_up):
        missing = set(interface_to_modify) - set(interfaces_up)
        raise Exception("{device}: Have unshut the following interfaces "
                        "'{to_shut}' but '{missing}' are still down".format(device=device.name,
                                                                       to_shut=interface_to_modify,
                                                                       missing=missing))


print('---Summary---')
print("{device}: Have modified the following interfaces "
      "'{to_shut}'".format(device=device.name, to_shut=' '.join(interface_to_modify)))
if not custom_args.unshut:
    print('Configuration to undo these changes')
    print('\n'.join(un_configuration))
