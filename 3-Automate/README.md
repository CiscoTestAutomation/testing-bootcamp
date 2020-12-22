# Automation

Let's automate it now!

Before we go ahead and code anything, let's re-iterate our goal:

* Make it independent on specific device, topology, or hostname
* Make it independent on the device configuration
* Make the log readable - easy to understand the failures
    * divide the actions
    * log useful information
* Be able to re-use this test in combination with other test

Grow our libraries and make all future automation much easier!

Here are the steps:

1. Create a Trigger
2. Hook it up in the Yaml files
3. Run it


## 1. Create a Trigger

The trigger is already pre-created for you, let's go through it.
Open `triggers/shutnoshut/bgp/nxos/shutnoshut.py`.

This is the "trigger" that performs a modify action. It looks the same as 
any other pyATS Testcase, however not tied to a script. It can be re-used time
and time again in any test scripts.

Yes, triggers are independent pyATS testcases that can be loaded and used where
needed. We build a consistent library of testcases so whenever 
some testing is needed, just pull out and use it!

We want a library of testcase for the same reason that we want library in programing.

**Re-use them.**

## 2. Hook it up in the YAML files

Now that the trigger has been created, lets run it. In this concept of 
"pool/library of testcases", because everything is reusable, and all you need to to is "pick and choose" the testcases you want to run, it means that:

- there is no testscript
- we define all the available "testcases" we can run in a YAML file

Check both `3-Automate/run/verification_datafile.yaml` and `3-Automate/run/Trigger_datafile.yaml`

The framework knows how to read the syntax of these YAML file. For all intents, think of these YAML files as your "test library database"

## 3. Run it

It runs the same way as another pyATS script: using the job file. It can also be run with the `pyats run genie` command, which removes the need of a job file.

```bash
cd run
cat job.py
```

Open up the file to see the content and how we mention what we want to execute.

```python
gRun(trigger_uids=['TriggerDemoShutNoShutBgp'],
     trigger_datafile='trigger_datafile.yaml')
```

> `gRun()` API effectively tells the engine to run "these testcases" from 
> "that pool of test cases as a suite"

And to run it

```bash
pyats run job job.py --testbed-file ../../tb.yaml --liveview --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/3-automate/one/ 
```

That's it! Our re-usable testcase is now running. With the ``--liveview`` field, a logviewer will pop up at runtime.

Right now our trigger verify only what is expected. The next step is - how do we verify also the unexpected as we've seen in the previous manual step?

Try this by uncommenting the comments in the trigger code.

And this is also a perfect place to introduce our Verification concept:

```python
# in job file
gRun(verification_uids=['Verify_BgpProcessVrfAll.uut'],
     trigger_uids=['TriggerDemoShutNoShutBgp'],
     trigger_datafile='trigger_datafile.yaml')
```

The code that was uncommented works, instead of just verifying the shut/no shut
of Bgp it will verify the other keys in that same show command, to make sure
they are the same as initially.

However, what if tomorrow you want to verify Ospf? Or 5 new commands. You
always need to go back and modify your Testcase, which is NOT what we want to
do. 

By adding these checks within your testcase, your testcase becomes less and less re-usable.

Go back and comment out the uncommented code from earlier.

Instead, we can use the power of Verification.

A verification is another Testcase which is ran AROUND a Trigger. It runs before and after.

They are to be added dynamically either a Global Verification or Local verification.

- Global: Run before and after every Trigger
- Local: Run before and after specific Trigger

Let's modify our job file to now call Verify_Bgp

| Note: Any of the verification defined on this page can be used: https://pubhub.devnetcloud.com/media/testing-feature-browser/docs/#/verifications

```python
# in job file
gRun(verification_uids=['Verify_Bgp.uut'],
     trigger_uids=['TriggerDemoShutNoShutBgp'],
     verification_datafile='verification_datafile.yaml',
     trigger_datafile='trigger_datafile.yaml')
```

```bash
pyats run job job.py --testbed-file ../../tb.yaml --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/3-automate/three/
```

We've seen a few ways to run this trigger, all are accomplished using only libraries:
- pick and choose what we need
- and create test suite using `gRun()`

Nothing is hard-coded, everything is reusable, and the flow is exactly as
we've determined.
