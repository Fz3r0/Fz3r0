
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### Find Access Layer Issues, Output & Input Errors {Runt, Giants, CRC, Collisions, etc} (show interface)

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Troubleshooting` `Switches` `Layer 2` `Access Layer`

---

### Network Access Layer Issues  

- **Before anything!** 

    - This technique and simple command will be very useful in the whole Networking career fur sure... `show interface` _(options)_
    
    - **This can help a lot when a cable is damaged, a plug, a rat bite the wire, interferences, or something causing lose of packets or shitty transsmissions to be clear...**
     
    - The concept is very easy: if something is happening with the packets travelling throught our devices, we can identify the integrity of the transmission with a simple and mystic command `show interface`.
     
- **...OK let's move on...**

1. The output from the `show interfaces` command is useful for detecting common media issues. 
    - One of the most important parts of this output is the display of the `line` and `data link protocol` status, as shown in the example:

```

Fz3r0_Switch#
Fz3r0_Switch#
Fz3r0_Switch#show interfaces fastEthernet 0/10     <<<----------| Command

FastEthernet0/10 is up, line protocol is up (connected)  <<<----------| Interface # , UP/DOWN

Hardware is Lance, address is 00d0.badc.be0a (bia 00d0.badc.be0a)    <<<----| Interface MAC

  Description: << Testing Interface Fa 0/10 Issues >>     <<<----| Description

(more results explained in the next point!)

Fz3r0_Switch#

```

- `FastEthernet0/18 is up` refers to the hardware layer and indicates whether the interface is receiving a carrier detect signal.

- `line protocol is up` refers to the data link layer and indicates whether the data link layer protocol keepalives are being received.

    - **Troubleshoot it!:**

        - Based on the output of the `show interfaces` command, possible problems can be fixed as follows:

            - Interface `UP` / line protocol `DOWN`
                - There could be an encapsulation type mismatch, the interface on the other end could be error-disabled, or there could be a hardware problem.
    
            - Interface `DOWN` / line protocol `DOWN`
                - A cable is not attached, or some other interface problem exists. 
                - For example, in a back-to-back connection, the other end of the connection may be administratively down.
    
            - Interface `Administratively Down`
                - It has been manually disabled (the shutdown command has been issued) in the active configuration.

### The real deal

- Now I will show the full command, not just the header:
 
```

Fz3r0_Switch#
Fz3r0_Switch#show interfaces fastEthernet 0/10     <<<----------| Command

FastEthernet0/10 is up, line protocol is up (connected)              <|-------   
  Hardware is Lance, address is 00d0.badc.be0a (bia 00d0.badc.be0a)  <|  The header we just reviewed
  Description: << Testing Interface Fa 0/10 Issues >>                <|-------
 
                                                           Easy to read...
  |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||                                   
  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv 
 
 BW 100000 Kbit, DLY 1000 usec,
     reliability 255/255, txload 1/255, rxload 1/255
  Encapsulation ARPA, loopback not set
  Keepalive set (10 sec)
  Full-duplex, 100Mb/s                                  
  input flow-control is off, output flow-control is off
  ARP type: ARPA, ARP Timeout 04:00:00
  Last input 00:00:08, output 00:00:05, output hang never
  Last clearing of "show interface" counters never
  Input queue: 0/75/0/0 (size/max/drops/flushes); Total output drops: 0
  Queueing strategy: fifo
  Output queue :0/40 (size/max)
  
                                     TASTY DATA FOR TROUBLESHOOTING AND ASS SAVERS!!!
  |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||                                   
  vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv                          
  
  5 minute input rate 0 bits/sec, 0 packets/sec
  5 minute output rate 0 bits/sec, 0 packets/sec                             <| 
     345634 packets input, 3456345634563456 bytes, 0 no buffer               <| 
     Received 345645 broadcasts, 666 runts, 666 giants, 0 throttles          <|
     666 input errors, 0 CRC, 666 frame, 666 overrun, 666 ignored, 0 abort   <|
     0 watchdog, 0 multicast, 0 pause input                                  <| Holy data for Access Layer Issues
     0 input packets with dribble condition detected                         <| I changed the values to "666" to
     2357 packets output, 263570 bytes, 0 underruns                          <|   <MOST SEVERE ISSUES & ERRORS>
     666 output errors, 666 collisions, 666 interface resets                 <| 
     0 babbles, 666 late collision, 0 deferred                               <|         (see table below)
     
     0 lost carrier, 0 no carrier
     0 output buffer failures, 0 output buffers swapped out

Fz3r0_Switch#
Fz3r0_Switch# 

```

- If something of the following is more than **0**.... run!!! _(Or check the hardware, cables, config...you know...follow the troubleshooting guidelines and your heart)_

| **Error Type**  | **Description**                                                                                            |
|-----------------|------------------------------------------------------------------------------------------------------------|
| `Input Errors`    | **Total number of errors.** It includes runts, giants, no buffer, CRC, frame, overrun, and ignored counts.     |
| `Runts`           | Frames that are discarded because they are **smaller than the minimum frame size for the medium**. For instance, any Ethernet frame that is **less than 64 bytes is considered a runt**.  |
| `Giants`          | Frames that are discarded because they **exceed the maximum frame size for the medium**. For example, any Ethernet frame that is **greater than 1,518 bytes is considered a giant**.      |
| `CRC`             | **CRC errors** are generated when the calculated **checksum is not the same** as the checksum received.                                                                                   |
| `Output Errors`   | **Sum of all errors** that prevented the final transmission of datagrams out of the interface that is being examined.                                                                 |
| `Collisions`      | Number of **messages retransmitted** because of an **Ethernet collision**.                                                                                                                |
| `Late Collisions` | A **collision** that occurs **after 512 bits of the frame have been transmitted**.  |

---

### References

- https://networklessons.com/cisco/ccna-routing-switching-icnd1-100-105/cisco-ios-boot-system-image-
- https://www.cisco.com/en/US/docs/switches/lan/catalyst4000/7.5/configuration/guide/boot_support_TSD_Island_of_Content_Chapter.html
---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 

