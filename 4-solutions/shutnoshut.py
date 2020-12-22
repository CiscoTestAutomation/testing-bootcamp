import time
import logging
from ats import aetest

from genie.harness.base import Trigger

log = logging.getLogger()

class ShutNoShutInterface(Trigger):
    '''Shut and unshut Interface'''

    @aetest.setup
    def prerequisites(self, uut, interface):
        '''Verify interface is non shut'''

        # To verify if the interface is up
        output = uut.parse('show interfaces {interface}'.format(interface=interface))

        # Check if interface is up
        if output[interface]['oper_status'] != 'up':
            self.failed('Interface {} is not up'.format(interface))

        self.passed('Interface {} is up'.format(interface))

    @aetest.test
    def shut(self, uut, interface):
        '''Shut interface'''
        uut.configure('''\
interface {interface}
shutdown'''.format(interface=interface))

    @aetest.test
    def verify(self, uut, interface):
        '''Verify if the shut worked'''
        # To verify if the interface is down
        output = uut.parse('show interfaces {interface}'.format(interface=interface))

        # Check if interface is down
        if output[interface]['oper_status'] != 'down':
            self.failed('Interface {} is not down'.format(interface))

        self.passed('Interface {} is down'.format(interface))

    @aetest.test
    def unshut(self, uut, interface):
        '''Un Shut interface'''
        uut.configure('''\
interface {interface}
no shutdown'''.format(interface=interface))

    @aetest.test
    def verify_recover(self, uut, interface):
        '''Figure out if interface is recovered'''
        # To verify if the interface is down
        output = uut.parse('show interfaces {interface}'.format(interface=interface))

        # Check if interface is up
        if output[interface]['oper_status'] != 'up':
            self.failed('Interface {} is not up'.format(interface))

        self.passed('Interface {} is up'.format(interface))
