import logging
from ats import aetest

from genie.harness.base import Trigger
### Code replaced by using Verification!
#from genie.utils.diff import Diff
###

log = logging.getLogger()

class ShutNoShutBgp(Trigger):
    '''Shut and unshut bgp'''

    @aetest.setup
    def prerequisites(self, uut, abstract):
        '''Figure out if bgp is configured and up'''

        # To verify if bgp is configured, we can use the Bgp Ops object
        ops = uut.learn('bgp')

        if not hasattr(ops, 'info'):
            # No Bgp! So can't do
            self.skipped("No Bgp is configured for "\
                         "device '{d}'".format(d=uut.name))

        # Now see if its up
        for instance_key, instance in ops.info['instance'].items():
            if instance['protocol_state'] == 'running':
                self.bgp_id = instance['bgp_id']
                break
        else:
            self.skipped("Bgp is not operational on "
                         "device '{d}'".format(d=uut.name))
### Code replaced by using Verification!
#        self.initial = ops
###

    @aetest.test
    def shut(self, uut, abstract):
        '''Shut bgp'''
        uut.configure('''\
router bgp {id}
shutdown'''.format(id=self.bgp_id))

    @aetest.test
    def verify(self, uut, abstract):
        '''Verify if the shut worked'''
        # Learn bgp object
        ops = uut.learn('bgp')

        for instance_key, instance  in ops.info['instance'].items():
            if instance['protocol_state'] == 'shutdown':
                break
        else:
            self.failed("Shut on Bgp did not work as it is still up "
                         "device '{d}'".format(d=uut.name))

    @aetest.test
    def unshut(self, uut, abstract):
        '''Shut bgp'''
        uut.configure('''\
router bgp {id}
no shutdown'''.format(id=self.bgp_id))

    @aetest.test
    def verify_recover(self, uut, abstract):
        '''Figure out if bgp is configured and up'''

        # Learn bgp object
        ops = uut.learn('bgp')

        if not hasattr(ops, 'info'):
            # No Bgp! So can't do
            self.skipped("No Bgp is configured for "\
                         "device '{d}'".format(d=uut.name))

        # Now see if its up
        for instance_key, instance in ops.info['instance'].items():
            if instance['protocol_state'] == 'running':
                break
        else:
            self.skipped("Bgp is not operational on "
                         "device '{d}'".format(d=uut.name))

### Code replaced by using Verification!
#        diff = Diff(self.initial, ops)
#        diff.findDiff()
#        if diff:
#            self.failed('Unexpected change has happened to our device state '
#                        '\n{d}'.format(d=diff))
#
###
