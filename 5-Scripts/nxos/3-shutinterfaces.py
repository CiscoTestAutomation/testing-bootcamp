# Shut all the interfaces
# return the list of interfaces that were shut
from genie.testbed import load

def interfaces_up(device):
    up_interfaces = []
    output = device.parse('show interfaces')
    return output.q.contains_key_value('oper_status', 'up').get_values('[0]')

tb = load('../../testbed.yaml')
device = tb.devices['csr1000v-1']

# Learn which interface is up
# Connect to the device via Console; as we want to shut all the interfaces
device.connect()

interface_to_shut = interfaces_up(device)
configuration = []
un_configuration = []
print("{device}: Shutting the following interfaces"
      "'{to_shut}'".format(device=device.name, to_shut=interface_to_shut))

for interface in interface_to_shut:
    configuration.append('interface {intf}\nshut'.format(intf=interface))
    un_configuration.append('interface {intf}\nno shut'.format(intf=interface))

# Once its all collected, shut the interface
import pdb;pdb.set_trace()
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

