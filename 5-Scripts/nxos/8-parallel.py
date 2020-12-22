from pyats.async_ import pcall
from genie.testbed import load

def admin_vs_oper(device):
    # How many up interfaces?
    # Let's send a command to the device
    output = device.parse('show interface', regex=True)
    oper_up = output.q.contains_key_value('oper_status', 'up').get_values('[0]')
    admin_up = output.q.contains_key_value('admin_state', 'up').get_values('[0]')

    # Not equal, let's find which one
    return set(admin_up) - set(oper_up)

tb = load('../../testbed.yaml')
tb.connect()
result = pcall(admin_vs_oper, device=tb.devices.values())

# Connect to all devices in parallel
import pdb;pdb.set_trace()

if result:
    print("These interfaces are adminstratively up but aren't "
          "operationally up\n{}".format(difference))
