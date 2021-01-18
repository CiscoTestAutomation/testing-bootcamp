# Testplan

We've just received our new test plan, it goes like this:

## Testcase - Shut no shut BGP 

1. Have BGP configuration on your devices
2. Shut BGP
3. Verify it has been shut
4. Unshut it
5. Verify it is back to its original state

We want to automate this test plan following these guidelines:

* Make it independent on specific device, topology, or hostname
* Make it independent on the device configuration
* Make the log readable - easy to understand the failures
    * divide the actions
    * log useful information
* Be able to re-use this test in combination with other test

> Good design and coding practices pays off big time in the long run.
