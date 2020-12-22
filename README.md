# Welcome to pyATS testing bootcamp about executing Tests!

This bootcamp is focused towards Testing scenarios and how it can help to save
you time. It can be used for: 

* Sanity / Regression 
* Verify configuration has been pushed correctly on your devices
* Verify device configuration
* Certification testing
* ...

You can either use the .virl file provided or use the mocked devices which are provided.

The CML (VIRL) devices is the recommended format.

## Install pyATS

1. Make sure you go through our [getting-started guide](https://developer.cisco.com/docs/pyats-getting-started/).
2. Internal Cisco users can also use our Install scripts.

## Format

The bootcamp is divided in:

[1-TestPlan](1-TestPlan/) - Go over the test plan

[2-Manual](2-Manual/) - Give it a try manually and use the library to make it easier

[3-Automate](3-Automate/) - Automate the test plan

[4-Solution](4-Solutions/) - Similar as #3 but with Tons of features

[5-Scripts](5-Scripts/) - Small extra scripts

[tb.yaml](tb.yaml) - an example of a testbed file


## Reference

* pyATS documentation: https://pubhub.devnetcloud.com/media/pyats/docs/
* pyATS library (Genie) documentation: https://developer.cisco.com/docs/genie-docs/
* Api Browser: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/

* Quick Getting Started Guide: https://developer.cisco.com/docs/pyats-getting-started/
* Quick Development Guide: https://developer.cisco.com/docs/pyats-development-guide/


## Mocked Device

Most examples have mock devices available to run, in case you do not have any
device. It is a Python script which acts the same way as a device. Here's an
example:

```
mock_device_cli --os nxos --mock_data_dir $VIRTUAL_ENV/genie-bootcamp/mocked_devices/2-manual/initial/playback/nxos --state execute
```

**Ctrl + D to get out**

Mocked devices are fantastic for training purposes:

* Focus on the training instead of the device
* The devices are always ready!
* Workshop can be replayed at any time without the need to get devices!

They can also be used to run scripts, the script run the same way as if a real
device was there.

More information on [unicon documentation](https://pubhub.devnetcloud.com/media/unicon/docs/playback/index.html).
