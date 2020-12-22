
from genie.testbed import load
tb = load('../../testbed.yaml')
dev1 = tb.devices['xr-1']
dev1.connect(via='cli')

# Let's send a command to the device
output = dev1.parse('show interfaces')

# Structure looks like
#interface
#  counters
#     crc_errors

for interface in output:
    if 'counters' in output[interface] and\
       'in_crc_errors' in output[interface]['counters']:
        crc_error = output[interface]['counters']['in_crc_errors']
        if crc_error > 0:
            print("Interface '{intf}' has '{error}' "
                  "crc_error".format(intf=interface,
                                     error=crc_error))
            # Send
        else:
            print("Interface '{intf}' has no crc_error".format(intf=interface))

