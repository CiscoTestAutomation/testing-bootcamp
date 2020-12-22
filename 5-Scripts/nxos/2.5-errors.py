from genie.testbed import load
tb = load('../../testbed.yaml')

devices = (tb.devices['nx-osv-1'],)
errors = ('out_errors', 'in_errors')
summary = []

for dev in devices:
    dev.connect(via='cli')

    output = dev.parse('show interface')
    # Structure looks like
    #interface
    #  counters
    #     errors
    print('The following interfaces have in_errors greater than 0')
    print(output.q.value_operator('in_errors', '>', 0).get_values('[0]'))
    print('The following interfaces have out_errors greater than 0')
    print(output.q.value_operator('out_errors', '>', 0).get_values('[0]'))
