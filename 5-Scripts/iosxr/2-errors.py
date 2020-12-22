from genie.testbed import load
tb = load('../../testbed.yaml')

devices = (tb.devices['xr-1'],)
#devices = (tb.devices['iosxrv9000-1'], tb.devices['iosxrv9000-2'])
errors = ('out_errors', 'in_errors')
summary = []

for dev in devices:
    dev.connect(via='cli')

    output = dev.parse('show interfaces')
    # Structure looks like
    #interface
    #  counters
    #     errors

    for error in errors:
        for interface in output:
            if 'counters' in output[interface] and\
               error in output[interface]['counters']:
                count = output[interface]['counters'][error]
                if count > 0:
                    msg = "{device}: Interface '{intf}' has '{count}' "\
                          "{error}".format(device=dev.name,
                                           intf=interface,
                                           count=count,
                                           error=error)
                    summary.append(msg)
                else:
                    msg = "{device}: Interface '{intf}' has '{count}' "\
                          "{error}".format(device=dev.name,
                                           intf=interface,
                                           count=count,
                                           error=error)
                    summary.append(msg)

print('---Errors Summary---')
print('\n'.join(summary))
