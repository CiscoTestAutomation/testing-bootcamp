# Manual

Before starting with our automation, let's test it on the device manually.

## The Typical... Way

Telnet to the device and issue these commands

```text
Step 1.
show bgp process vrf all

Step 2.
router bgp <bgp id>
   shutdown 

Step 3.
show bgp process vrf all

Step 4.
router bgp <bgp id>
   no shutdown 

Step 5.
show bgp process vrf all
```

The nature of these commands shows that you are trying to accomplish the 
following:

- **Step 1:** study what was there before

- **Step 2:** perform the action

- **Step 3:** verify what has changed and is it expected

- **Step 4:** perform second action

- **Step 5:** Make sure it recovered as expected

These steps requires human interaction and expertise to determine what has 
changed and not just look to what is expected. 

> What if something else changes that was not anticipated by these steps?

As engineers, we write automated scripts for a few reasons:

* Make sure our features react as expected
* Make sure there are no unexpected changes
* We don't want to manually test the samething every day: it's too slow and 
  too repetitive
* We need to go fast!
* We want the machine to analyze the data and tell us what has changed
* Find bugs
* etc

We should not be looking only at the expected (typical scenario). Rather,
also consider the surrounding aspects as well: the unexpected.

As an exercise, let's see what has changed:

We have three snapshot here

- First one is the initial state
- Second one is the modified state with Bgp shutdown
- Third one is the reverted state with Bgp unshut

**Can you send the show command to see what has changed and verify that nothing else has changed.**

```
# Initial
mock_device_cli --os nxos --mock_data_dir $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/initial/playback/nxos --state execute
# Bgp Shutdown
mock_device_cli --os nxos --mock_data_dir $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/modified/playback/nxos --state execute
# Bgp Unshut
mock_device_cli --os nxos --mock_data_dir $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/reverted/playback/nxos --state execute
```

Even though is a 1 line change, there can be many operation to verify.


# pyATS Cli | Manual Automation way

| Note: As we are using a mock device, no need to perform the action on the device, just skip Step 2 and 5.

- **Step 1:** take a snapshot
  ```bash
  pyats parse "show bgp process vrf all" --testbed-file $VIRTUAL_ENV/testing-bootcamp/tb.yaml --output initial --device nx-osv-1 --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/initial/record/
  ```

- **Step 2:** perform the action
  ```text
  router bgp <bgp id>
     shutdown 
  ```

- **Step 3:** take a snapshot
  ```bash
  pyats parse "show bgp process vrf all" --testbed-file $VIRTUAL_ENV/testing-bootcamp/tb.yaml --output modified --device nx-osv-1  --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/modified/record/
  ```

- **Step 4:** compare the snapshot
  ```bash
  pyats diff initial modified --output modified_diff
  ```

- **Step 5:** perform second action
  ```text
  router bgp <bgp id>
     no shutdown 
  ```

- **Step 6:** take a snapshot
  ```bash
  pyats parse "show bgp process vrf all" --testbed-file $VIRTUAL_ENV/testing-bootcamp/tb.yaml --output recovered --device nx-osv-1 --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/reverted/record/
  ```

- **Step 7:** compare the snapshot
  ```bash
  pyats diff initial recovered --output recovered_diff
  ```

| Note: The `--replay` is only needed as we are using mocked devices


With pyATS cli, you are being told what has changed at each step: instead of relying
on human expertise (the probablity of error) on finding the issues, you can
make educated decisions based on the automation output instead: focus your
attention where it matters.

You are being told of all the changes that has happened, so that we can
revert to the original output and ensure nothing else was modified!

Take a look in the `output/output.txt` directory for the flow and all the log!

We can see all the values which changed; this is more than expected! Would we
have though about all of those?

```text
> cat modified_diff/diff_nx-osv-1_show-bgp-process-vrf-all_parsed.txt
--- initial/nx-osv-1_show-bgp-process-vrf-all_parsed.txt
+++ modified/nx-osv-1_show-bgp-process-vrf-all_parsed.txt
+bgp_protocol_state: shutdown
-bgp_protocol_state: running
+bytes_used: 100
-bytes_used: 200
+num_attr_entries: 1
-num_attr_entries: 2
vrf:
 default:
  address_family:
   ipv4 unicast:
    peers:
     1:
+      active_peers: 0
-      active_peers: 1
+      paths: 1
-      paths: 2
+      routes: 1
-      routes: 2
+  num_established_peers: 0
-  num_established_peers: 1
```

You can also parse multiple commands to see this action affect the operation
state of the device.


Can we go one level deeper?

```
1. pyats learn bgp --testbed-file $VIRTUAL_ENV/testing-bootcamp/tb.yaml --output bgp_initial --device nx-osv-1 --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/initial_bgp/

2. router bgp <bgp id>
      shutdown 

3 pyats learn bgp --testbed-file $VIRTUAL_ENV/testing-bootcamp/tb.yaml --output bgp_modified --device nx-osv-1 --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/modified_bgp

4. pyats diff bgp_initial bgp_modified --output bgp_modified_diff

5. router bgp <bgp id>
      no shutdown 

6. pyats learn bgp --testbed-file $VIRTUAL_ENV/testing-bootcamp/tb.yaml --output bgp_recovered --device nx-osv-1 --replay $VIRTUAL_ENV/testing-bootcamp/mocked_devices/2-manual/recovered_bgp//

7. pyats diff bgp_initial bgp_recovered --output bgp_recovered_diff

```

Now instead of just focusing on only 1 command, it learns BGP and related commands, and compare these.

https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/#/models
