
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### Boot from a Binary .bin or config.text & Recover from a System Crash like a Sir!

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Initial Settings` `Reset` `Flash`

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

