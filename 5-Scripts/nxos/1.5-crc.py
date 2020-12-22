
from genie.testbed import load
tb = load('../../testbed.yaml')
dev1 = tb.devices['nx-osv-1']
dev1.connect(via='cli')

# Let's send a command to the device
output = dev1.parse('show interface')

# Structure looks like
#interface
#  counters
#     in_crc_errors
import pdb;pdb.set_trace()

print('The following interfaces have in_crc_errors greater than 0')
print(output.q.value_operator('in_crc_errors', '>', 0).get_values('[0]'))
