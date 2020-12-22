from genie.testbed import load
tb = load('../../testbed.yaml')
dev = tb.devices['nx-osv-1']
dev.connect()

# How many up interfaces?
# Let's send a command to the device
output = dev.parse('show interface')
oper_up = output.q.contains_key_value('oper_status', 'up').get_values('[0]')
admin_up = output.q.contains_key_value('admin_state', 'up').get_values('[0]')

# Not equal, let's find which one
difference = set(admin_up) - set(oper_up)

if difference:
    print("These interfaces are adminstratively up but aren't "
          "operationally up\n{}".format(difference))
