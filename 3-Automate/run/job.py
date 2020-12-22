import os

from ats.datastructures.logic import And, Not, Or
from genie.harness.main import gRun

def main():
    test_path = os.path.dirname(os.path.abspath(__file__))

    gRun(trigger_uids=['TriggerDemoShutNoShutBgp'],
         trigger_datafile='trigger_datafile.yaml')

#gRun(verification_uids=['Verify_BgpProcessVrfAll.uut'],
#     trigger_uids=['TriggerDemoShutNoShutBgp'],
#     trigger_datafile='trigger_datafile.yaml')

#gRun(verification_uids=['Verify_Bgp.uut'],
#     trigger_uids=['TriggerDemoShutNoShutBgp'],
#     verification_datafile='verification_datafile.yaml',
#     trigger_datafile='trigger_datafile.yaml')
