from genie.testbed import load
tb = load('../../testbed.yaml')
dev1 = tb.devices['nx-osv-1']
dev1.connect()

# Let's send a command to the device
output = dev1.parse('show module')

# Let's get all the rp which are actived
print(output.q.contains('active').get_values('rp'))
print(output.q.contains('ok').get_values('lc'))

