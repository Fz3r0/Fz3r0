
---

### Fz3r0 Operations  [Networking]

### Spaning Tree Protocol (STP) 

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `STP`

---

### Fz3r0 RSTP & Rapid PVST+ guide for dummies

- _Forget the acronym "STP" we are in 2022 and we use RSTP & Rapid PVST+, period. We will use "STP" & "PVST+" only for concept (cuz' it's the same shit but those are more oldies) so...anyways let's begin:_ 

- _This is my "Fz3r0 STP easy guide for dummies all in one!" Precise info about STP(ehmehm now RSTP!) is shown below the guide_

- **Before everything, we only need to select our Root Bridge(Switch), it will be the center of the network, easy! that will be our `STP/RSTP Root Bridge` (by default Cisco config chooses the switch with lowest MAC, it don't cares about the location like us).** 

- _If there are 2 switches in the same "level" and centered (for example 2 switches at distribution layer), take the switch with less charge of work, or newest, or shiny!...if everything is the same...usually engineers choose "left center" switch, the other switch could be used as a backup root bridge_ 

- Set the BIDs for each switch, where **Root Bridge will be 0 (or lowest)**

    - Remember (0,1,2,3,4,5,6...) but in spanning tree we use "different" numbers:
        - Priority Values of STP are **0 to 61440 in increments of 4096**. Default 32768
        - 0,1,2,3,4,5 = 0,4096,8192,12288,16384
        - 4096+4096+4096+4096+4096+4096+4096+4096 (8 times = 32768 = default)
        - 4096*15 = 61440 (max)

    - Just set an order, usually the priority goes:
        - Distribution Layer (Center Switches) - 0,1,2...
        - Core Layer (Up/Core Switches) - 7,8,9...
        - Access Layer (Down/Access Switches to Hosts) - 13,14,15  

- **Very important:** If you are using VLANs, then STP should be configured on each VLAN! it works independent, and that's automatically called PVST, it could be the same config and paths, or different, that's your choice for specific scenarios. 

- Set the Port-Fast and BPDU guard on all access ports (to hosts and end devices):

```

spanning-tree bpduguard enable
spanning-tree portfast

```

- Do the opposite for all the links between switches or trunks:

```

spanning-tree bpduguard disable
spanning-tree portfast disable

```  

- And actually...that's all! That's RSTP & Rapid PVST+ AKA "STP" and all the fancy stuff!! so, in resume, from 0 to hero:

---

### All-in-One from zero to hero by Fz3r0:

- **For Root Bridge** (Root Switch "0"): 

```

spanning-tree mode rapid-pvst

spanning-tree vlan 10 root primary

spanning-tree bpduguard disable
spanning-tree portfast disable

```

- _Optional:_ **For Root Bridge Backup** _(the backup "1" if root dies, another centered switch)_: 

```

spanning-tree mode rapid-pvst

spanning-tree vlan 10 root secondary

spanning-tree bpduguard disable
spanning-tree portfast disable

```

- For the other Bridges **BETWEEN SWITCHES OR TRUNKS** (example: core switches) in the order you want or need (All the other switches except Root, only will change the BID for each one):

- Switch 2 (non-root switch "2" trunks & switches)

```

spanning-tree mode rapid-pvst

spanning-tree vlan 10 root secondary

spanning-tree bpduguard disable
spanning-tree portfast disable

```

- For the other Bridges **BETWEEN HOSTS & ACCESS SWITCHES** (example: access switches) in the order you want or need (All the other switches except Root, only will change the BID for each one):

- Switch 3 (non-root switch "3" access to hosts & end-devices)

```

spanning-tree mode rapid-pvst

spanning-tree vlan 10 priority 4096

spanning-tree bpduguard enable
spanning-tree portfast

```

- Switch 4 (non-root switch "4") _access or trunk_ priority: [2]8192  
- Switch 5 (non-root switch "5") _access or trunk_ priority: [3]12288
- Switch 6 (non-root switch "6") _access or trunk_ priority: [4]16384
- Switch 7 (non-root switch "7") _access or trunk_ priority: [5]20480
.
.
.
.
etc

- From 7 chained switched, set more seconds on timers STP timers ;) 

- We only need to set the Root, BIDs, bpduguard and portfast! easy huh?! byebye!! :D 

- Well, well, well here you go:

---    

- We are set with the "initial" config, let's start...        

- STP is very easy if you remember just 2 things:

**1- Triforce of STP rules** _1-Lowest Hop | 2-Lowest BID | 3-Lowest Port#_
**2- Triforce of STP steps** _1-Select Root Port | 2-Select FWD/Designated Port | 3-Block everything else

- **This are the Trifoce of STP rules (3 rules):**

    1. Try Lowest cost by hop 
        - It will count every "hop" and chooses shortest path with less hops = (hop=4)
        - If all hops cost 4 or 8 or 16 or 32...etc is a tie! then:

    2. Try lowest BID = It will choose the SW with less BID (like 1)
        - If all BIDs are the same, like "32768"(default) is a tie! then:

    3. Lowest port # or MAC = It will choose the lowest port ID # on the switch.
        - The lowest Port on the switch, Fa0/1 = lowest, Fa0/24 = highest
        - Lowest port will be the winner!

- **This are the Triforce of STP steps (3 steps):**

1. Select **just one `Root Port` in every switch**

    - **All the ports pointing to Root Switch are Root Ports** "like zombies".
    - Direct paths will always cost less
    - Unclear direct paths will choose the way with less costs, using the `triforce of STP rules`

        1. Try Lowest cost by hop 
            - It will count every "hop" and chooses shortest path with less hops = (hop=4)
            - If all hops cost 4 or 8 or 16 or 32...etc is a tie! then:

        2. Try lowest BID = It will choose the SW with less BID (like 1)
            - If all BIDs are the same, like "32768"(default) is a tie! then:

        3. Port # = It will choose the lowest port # on the switch.
            - It's supposed it never reach this part, because it's suposed we need to set the BID for all the switches on the network! So go back, and set the BIDs!!!            

2. Select Forward (also known as Designated) Port, **one per sergment**

    - **All the ports in Root Switch are Forward Ports** pointing to "the zombies"
    - The **segment** means the link between 2 switches. Think about it as `side A` & `side B` of the cable.
    - We need to choose one side of the segment (ethernet cable), that's it! we have all the ports on the root already:

        1. **Root Switch - All ports are designated ports.**

        2. **The other side of all `root ports` that we found on `step 1` will be designated ports.**

        3. Switches wehre already have `root ports` selected but still other empty port, those empty ports are automatically designated ports! (usually access switches on 3 tier)         

        4. Segments where both sides are empty and don't have root ports will choose the way with less costs, using the `triforce of STP rules`:

            1. Try Lowest cost by hop 
                - It will count every "hop" and chooses shortest path with less hops = (hop=4)
                - If all hops cost 4 or 8 or 16 or 32...etc is a tie! then

            2. Try lowest BID = It will choose the SW with less BID (like 1)
                - If all BIDs are the same, like "32768"(default) is a tie! then:

            3. Port # = It will choose the lowest port # on the switch.
                - It's supposed it never reach this part, because it's suposed we need to set the BID for all the switches on the network! So go back, and set the BIDs!!!

3. Select Alternate (Blocked) Ports. Easiest step on the Triforce...Block all the ports left! that's it! 

    - All ports that still empty in the topology will be blocked, and that's it! Full STP!.     

---     

### Spanning Tree Protocol

-  **Spanning Tree Protocol (STP)** is a loop-prevention network protocol that allows for redundancy while creating a loop-free Layer 2 topology. 

- `IEEE 802.1D` is the original IEEE MAC Bridging standard for STP.

- For example, if there's a redundancy between 3 switches STP will always block 1 way to prevent loops:


```

     SW1---------SW2
        \       /
         \     x  <--- STP will block this path 
          \   /        everytime PC send traffic to SW1
           \ /
           SW3
            |
            |
           PC1                              

```

- But if the connection between SW1 & SW3 fails due to a cable fail, port or any kind of issue, STP will unblock the other way!


```

     SW1---------SW2
        \       /
FAIL!--> x     o   <--- STP will un-block this path 
          \   /         creating redundancy! :D 
           \ /
           SW3
            |
            |
           PC1                                

```

- That's it! now we have `Redundant Switch Links`

### Issues with Redundant Switch Links

- Path redundancy provides multiple network services by eliminating the possibility of a single point of failure. 

- When multiple paths exist between two devices on an Ethernet network, and there is no spanning tree implementation on the switches, a Layer 2 loop occurs. 

- A Layer 2 loop can result in MAC address table instability, link saturation, and high CPU utilization on switches and end-devices, resulting in the network becoming unusable.

- In easy words: **We need to prevent loops when using redundant links, how? using STP!**

### Layer 2 Loops

- Without STP enabled, Layer 2 loops can form, causing broadcast, multicast and unknown unicast frames to loop endlessly.

- **This can bring down a network within a very short amount of time, sometimes in just a few seconds.**

### Broadcast Storm

- A broadcast storm is an abnormally high number of broadcasts overwhelming the network during a specific amount of time.

- Broadcast storms can disable a network within seconds by overwhelming switches and end devices. 

- Broadcast storms can be caused by a hardware problem such as a faulty NIC or from a Layer 2 loop in the network... Or maybe by an attack of Broadcast Storm! ;) 

- To prevent these issues from occurring in a redundant network, some type of spanning tree must be enabled on the switches. 

- **Spanning tree is enabled, by default, on Cisco switches to prevent Layer 2 loops from occurring.**

---

### Steps to a Loop-Free Topology

- Using the STA (Spanning Tree Algorythm), STP builds a loop-free topology in a four-step process:

    1- Elect the root bridge.
    2- Elect the root ports.
    3- Elect designated ports.
    4- Elect alternate (blocked) ports.

- During STA and STP functions, switches use Bridge Protocol Data Units (BPDUs) to share information about themselves and their connections.

- **Each BPDU contains a bridge ID `BID` that identifies which switch sent the BPDU.**

- The `BID` is involved in making many of the STA decisions including root bridge and port roles.    

- The BID contains a priority value, an extended system ID, and the MAC address of the switch. The lowest BID value is determined by the combination of these three fields:

    1- Priority - If the Priority is the same then compares the Extended System ID:
    2- Extended System ID - If the Priority is the same then compares the MAC Address
    3- MAC Address - The MACs are unique smart boy ;) dead end. 

### Bridge Priority   

- **The default priority value for all Cisco switches is the decimal value `32768`**

- The range is 0 to 61440 in increments of **4096**.

- A bridge priority of 0 takes precedence over all other bridge priorities.

### Elect the Root Bridge

- The switch with the lowest BID will become the root bridge.

- At first, all switches declare themselves as the root bridge with their own BID set as the Root ID. 

- Eventually, the switches learn through the exchange of BPDUs which switch has the lowest BID and will agree on one root bridge.

- **To ensure that the root bridge decision best meets network requirements, it is recommended that the administrator configure the desired root bridge switch with a lower priority.**

---

### STP Timers

- STP convergence requires three timers, as follows:

    1- Hello Timer:
        - The hello time is the interval between BPDUs. 
        - The default is 2 seconds but can be modified to between 1 and 10 seconds.

    2- Forward Delay Timer:
        - The forward delay is the time that is spent in the listening and learning state. 
        - The default is 15 seconds but can be modified to between 4 and 30 seconds.

    3- Max Age Timer: 
        - The max age is the maximum length of time that a switch waits before attempting to change the STP topology. 
        - The default is 20 seconds but be modified to between 6 and 40 seconds.
        - Remember, STP is waiting for a fail and de redundant! So when Max Age timer is reached, boom! STP change the paths to the "blocked" ports, now are forward ports!!!

- **Note: The default times can be changed on the root bridge, which dictates the value of these timers for the STP domain.**

- **Note2: To avoid problems with STP, IEEE recommends a maximum diameter of seven switches when using the default STP timers.
    - So, form more than 7 chained switches would be good to increment those timers and five some room to STP!!

### STP Port States 

- Dont' worry so much about this...just remember the 7 switch rule in Note2.

- Everytime a switch is turned on the port states changes in STP to determine the root and all the topology automatically so... these are the states:

- Link comes up -> Blocking(All are root) -> Listening(listen to neighbors) -> Learning(learn from bpdus from neighbors) -> Forwarding (STP topology ready)

- Port States: 

    - **Blocking:**    
        - The port is an alternate port and does not participate in frame forwarding. 
        - The port receives BPDU frames to determine the location and root ID of the root bridge.
        - BPDU frames also determine which port roles each switch port should assume in the final active STP topology. 
        - With a Max Age timer of 20 seconds, a switch port that has not received an expected BPDU from a neighbor switch will go into the blocking state.

    - **Listening:**
        - After the blocking state, a port will move to the listening state. 
        - The port receives BPDUs to determine the path to the root. 
        - The switch port also transmits its own BPDU frames and informs adjacent switches that the switch port is preparing to participate in the active topology.

    - **Learning:**
        - A switch port transitions to the learning state after the listening state. 
        - During the learning state, the switch port receives and processes BPDUs and prepares to participate in frame forwarding. 
        - It also begins to populate the MAC address table. 
        - However, in the learning state, user frames are not forwarded to the destination.

    - **Forwarding:** 
        - In the forwarding state, a switch port is considered part of the active topology. 
        - The switch port forwards user traffic and sends and receives BPDU frames.

    - **Disabled**    
        - A switch port in the disabled state does not participate in spanning tree and does not forward frames. 
        - The disabled state is set when the switch port is administratively disabled     

---        

### PVST - Per-VLAN Spanning Tree

- Up until now, we have discussed STP in an environment where there is only one VLAN. 

- However, STP can be configured to operate in an environment with multiple VLANs.

- **In Per-VLAN Spanning Tree (PVST) versions of STP, there is a root bridge elected for each spanning tree instance.** 

- **This makes it possible to have different root bridges for different sets of VLANs.**

- **STP operates a separate instance of STP for each individual VLAN. If all ports on all switches are members of VLAN 1, then there is only one spanning tree instance.**

- In resume...if you have VLANs in your network then: configure STP on each VLAN!!! that's PVST!!!

---

### Different Versions of STP

- Spanning Tree Protocol and the acronym STP, which can be misleading. Many professionals generically use these to refer to the various implementations of spanning tree, such as **Rapid Spanning Tree Protocol (RSTP) and Multiple Spanning Tree Protocol (MSTP).** 

- RSTP (IEEE 802.1w) supersedes the original 802.1D while retaining backward compatibility. The 802.1w STP terminology remains primarily the same as the original IEEE 802.1D STP terminology. Most parameters have been left unchanged. Users that are familiar with the original STP standard can easily configure RSTP. The same spanning tree algorithm is used for both STP and RSTP to determine port roles and topology.

- Rapid PVST+ is the Cisco implementation of RSTP on a per-VLAN basis. With Rapid PVST+ an independent instance of RSTP runs for each VLAN.

| STP Variety    | Description                                                                                  |
|:--------------:|:--------------------------------------------------------------------------------------------:|
| STP            | This is the original IEEE 802.1D version (802.1D-1998 and earlier) that provides a loop-free topology in a network with redundant links. Also called Common Spanning Tree (CST), it assumes one spanning tree instance for the entire bridged network, regardless of the number of VLANs.
| PVST+          | Per-VLAN Spanning Tree (PVST+) is a Cisco enhancement of STP that provides a separate 802.1D spanning tree instance for each VLAN configured in the network. PVST+ supports PortFast, UplinkFast, BackboneFast, BPDU guard, BPDU filter, root guard, and loop guard.
| RSTP           | Rapid Spanning Tree Protocol (RSTP) or IEEE 802.1w is an evolution of STP that provides faster convergence than STP. |
| 802.1D-2004    | This is an updated version of the STP standard, incorporating IEEE 802.1w. |
| Rapid PVST+    | This is a Cisco enhancement of RSTP that uses PVST+ and provides a separate instance of 802.1w per VLAN. Each separate instance supports PortFast, BPDU guard, BPDU filter, root guard, and loop guard.
| MSTP           | Multiple Spanning Tree Protocol (MSTP) is an IEEE standard inspired by the earlier Cisco proprietary Multiple Instance STP (MISTP) implementation. MSTP maps multiple VLANs into the same spanning tree instance. |
| MST            | Multiple Spanning Tree (MST) is the Cisco implementation of MSTP, which provides up to 16 instances of RSTP and combines many VLANs with the same physical and logical topology into a common RSTP instance. Each instance supports PortFast, BPDU guard, BPDU filter, root guard, and loop guard. |

### PortFast & BPDU Guard

- Portfast: Could always be enabled in access ports (to Hosts or End Users).
    - When a switch port is configured with PortFast, that port transitions from blocking to forwarding state immediately, bypassing the usual 802.1D STP transition states (the listening and learning states) and avoiding a 30 second delay. 

- BPDU guard: Always disabled in access ports (to Hosts or End Users). This are "messages" (BPDUs) used by STP between switches. 
    - This must be un-set always in access ports for security!       
    - BPDUs should never be received on PortFast-enabled switch ports because that would indicate that another bridge or switch is connected to the port.

---

### References

https://www.youtube.com/watch?v=1RPMCnJStec
https://contenthub.netacad.com/srwe-dl/7.0.2
https://www.youtube.com/watch?v=Y5BXVvTnTjE&list=PLwAU7bA502wGio6Pi2RgpSY7sP7OWT_dz&index=2

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
