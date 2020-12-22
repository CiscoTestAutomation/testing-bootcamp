# Shut all the interfaces
# return the list of interfaces that were shut
from genie.testbed import load

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

# Learn which interface is up
# Connect to the device via Console; as we want to shut all the interfaces
device.connect(via='cli')

interface_to_shut = interfaces_up(device)
configuration = []
un_configuration = []
print("{device}: Shutting the following interfaces"
      "'{to_shut}'".format(device=device.name, to_shut=interface_to_shut))

for interface in interface_to_shut:
    configuration.append('interface {intf}\nshut'.format(intf=interface))
    un_configuration.append('interface {intf}\nno shut'.format(intf=interface))

# Once its all collected, shut the interface
device.configure(configuration)

# Verify they are all down
interfaces_up = interfaces_up(device)
if interfaces_up:
    raise Exception("{device}: Has shut the following interfaces "
                    "'{to_shut}' but '{intf}' are still up".format(device=device.name,
                                                                   to_shut=interface_to_shut,
                                                                   intf=interfaces_up))

print('---Summary---')
print("{device}: Has shut the following interfaces "
      "'{to_shut}'".format(device=device.name, to_shut=interface_to_shut))
print('Configuration to undo these changes')
print('\n'.join(un_configuration))

