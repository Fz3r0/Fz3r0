
---

### Fz3r0 Operations  [Networking]

### EtherChannel like a Sir (PortChannel) 

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `STP`

---
   
### Configure Etherchannel like a Sir straight to the point!

- If you want to read more, go to:

### Etherchannel with LACP (Open Standard)

- **Note: When configuring EtherChannels, it is recommended to shut down the physical ports being grouped on both devices before configuring them into channel groups. Otherwise, EtherChannel Misconfig Guard may place these ports into err-disabled state. The ports and port channels can be re-enabled after EtherChannel is configured.**

```

SW1# config t
SW1(config)# interface range FastEthernet 0/1 - 2
SW1(config-if-range)# shut

```  

- EtherChannel is disabled by default and must be configured. 

- The topology in the figure will be used to demonstrate an EtherChannel configuration example using LACP.

```
                <<---------LACP---------------->>

                            /\
========     |1------------/--\----------------1|     ========
MODE-SW1  SW1|            /    \PortChannel    +|SW2  MODE-SW2
========     |2-----------\----/---------------2|     ========
                           \  /
                            \/
```  

- Remember!...use the Fz3r0 standard for cool people! *both sides `ON`*

- Just follow 3 steps:

1. Specify the interfaces that compose the EtherChannel group using the `interface range` interface global configuration mode command.

```

SW1# config t
SW1(config)# interface range FastEthernet 0/1 - 2
 
```    

2. Create the port channel interface with the `channel-group` identifier _(like channel-group 1,2,3,4,etc)_ `mode ON` command in interface range configuration mode. 

```

SW1(config-if-range)# channel-group 666 mode on
Creating a port-channel interface Port-channel 666

SW1(config-if-range)# no shut

```     

3. If you need to change Layer 2 settings on the port channel interface, for example, making it a trunk link. Enter port channel interface configuration mode using the `interface port-channel` command, followed by the interface identifier.

```  

SW1(config)# interface port-channel 666
SW1(config-if)# switchport mode trunk
SW1(config-if)# switchport trunk allowed vlan 1,2,10,20,99

```

- In resume, the full configuration & settings changes are:

```

=-=-=-=-= Config Port-Channel =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

SW1# config t
SW1(config)# interface range FastEthernet 0/1 - 2
SW1(config-if-range)# channel-group 666 mode on
Creating a port-channel interface Port-channel 666


=-=-=-=-= Config Port-Channel Settings -=-=-=-=-=-=-=-=-=-=-=-=

SW1(config)# interface port-channel 666
SW1(config-if)# switchport mode trunk
SW1(config-if)# switchport trunk allowed vlan 1,2,10,20,99


=-=-=-=-=-=-=-=-= Copy paste -=-=-=-=-=-=-=-=-=-=-=-=

!
enable
configure terminal
interface range FastEthernet 0/1 - 2
channel-group 666 mode on
exit
exit
wr
end
!

!
enable
configure terminal
interface port-channel 666
switchport mode trunk
switchport trunk allowed vlan 1,2,10,20,99
no shut
exit
exit
wr
end
!

```

- That's all!!! easy as cake...but here's the nerd stuff:

---  

### Link Aggregation & EtherChannel

- **In resume and simple way of view it, this is Etherchannel & Link Aggregation:**

- EtherChannel is a link aggregation technology that groups multiple physical Ethernet links together into one single logical link. It means, it's used to "sumarize" 2 or more ethernet "cables" (maximum 8) into just 1 "fat cable"(PortChannel). That's it! easy...

- It is used to provide fault-tolerance, load sharing, increased bandwidth, and redundancy between switches, routers, and servers.

- Multiple links could be connected between devices to increase bandwidth. 

- A link aggregation technology is needed that allows redundant links between devices that will not be blocked by STP. That technology is known as EtherChannel.

- EtherChannel technology makes it possible to combine the number of physical links between the switches to increase the overall speed of switch-to-switch communication.

- For example:

    - If you have 2 FastEthernet cables(links) 100Mbps each one, then you will have 1 single "cable"(PortChannel) with 200Mbps! 1+1=2 (inside one)

    - Aditionally... if 1 cable fails, the other take the redundancy _(and return to only 100Mbps)_

    - There are some rules & restrictions like: all the "cables"(links) must be the same speed and type.

    - Etherchannel support Spanning-Tree or any other protocol, just like a "normal" link between network devices. Remember, is just a "fat" cable made by 2 or more cables (maximum 8 per PortChannel).

    - For better understanding, I wrote a little more about this:   

---

### EtherChannel

- EtherChannel technology is as a `LAN switch-to-switch technique` of grouping several Fast Ethernet or Gigabit Ethernet ports into one logical channel.

- When an EtherChannel is configured, the resulting virtual interface is called a `port channel`. 

- The physical interfaces are bundled together into a port channel interface:

```
        ----------->
     |1----100mbps--------------------------1|
  SW1|         PortChannel = 200mbps ====>> +|SW2
     |2----100mbps--------------------------2|
        ----------->

```

### Advantages of EtherChannel

- EtherChannel technology has many advantages, including the following:

    - Most configuration tasks can be done on the EtherChannel interface instead of on each individual port, ensuring configuration consistency throughout the links.

    - EtherChannel relies on existing switch ports. There is no need to upgrade the link to a faster and more expensive connection to have more bandwidth.

    - Load balancing takes place between links that are part of the same EtherChannel. Depending on the hardware platform, one or more load-balancing methods can be implemented. These methods include: 

        - **Source MAC and destination MAC load balancing**
        - **Source IP and destination IP load balancing.**

    - EtherChannel creates an aggregation that is seen as one logical link. When several EtherChannel bundles exist between two switches, STP may block one of the bundles to prevent switching loops. 

    - When STP blocks one of the redundant links, it blocks the entire EtherChannel. Again... just like one "fat" cable...that's all!!!

    - EtherChannel provides redundancy because the overall link is seen as one logical connection. Additionally, the loss of one physical link within the channel does not create a change in the topology. 

    -Therefore, a **spanning tree recalculation is not required. Assuming at least one physical link is present; the EtherChannel remains functional, even if its overall throughput decreases because of a lost link within the EtherChannel.**

### Restrictions in the Implementation of Etherchannel

- EtherChannel has certain implementation restrictions, including the following:

    - Interface types cannot be mixed. For example, Fast Ethernet and Gigabit Ethernet cannot be mixed within a single EtherChannel.

    - Currently, each EtherChannel can consist of up to `**eight compatibly-configured Ethernet ports**`. 

    - **EtherChannel provides full-duplex bandwidth up to 800 Mbps (Fast EtherChannel) or 8 Gbps (Gigabit EtherChannel) between one switch and another switch or host.**

    - _The Cisco Catalyst 2960 Layer 2 switch currently supports up to six EtherChannels. However, as new IOSs are developed and platforms change, some cards and platforms may support increased numbers of ports within an EtherChannel link, as well as support an increased number of Gigabit EtherChannels. Always chack the manual of the switch_

    - The individual EtherChannel group member port configuration must be consistent on both devices: 

        - If the physical ports of one side are configured as trunks, the physical ports of the other side must also be configured as trunks within the same native VLAN. 

        - **Additionally, all ports in each EtherChannel link must be configured as Layer 2 ports.**

    - **A configuration applied to the port channel interface affects all physical interfaces that are assigned to that interface.**

---     

### AutoNegotiation Protocols

- EtherChannels can be formed through negotiation using one of two protocols:

    - **Port Aggregation Protocol (PAgP)**

    - **Link Aggregation Control Protocol (LACP)** 

- **Note: It is also possible to configure a static or unconditional EtherChannel without PAgP or LACP.** 

---   

### PAgP Operation

- **PAgP is a Cisco-proprietary protocol**

- When an EtherChannel link is configured using `PAgP`, PAgP packets are sent between EtherChannel-capable ports to negotiate the forming of a channel. 

- When PAgP identifies matched Ethernet links, it groups the links into an EtherChannel. The EtherChannel is then added to the spanning tree as a single port.

- When enabled, PAgP also manages the EtherChannel. 

- **PAgP packets are sent every 30 seconds.** 

- PAgP checks for configuration consistency and manages link additions and failures between two switches. It ensures that when an EtherChannel is created, all ports have the same type of configuration.

- **Note: In EtherChannel, it is mandatory that all ports have the same speed, duplex setting, and VLAN information. Any port-channel modification after the creation of the channel also changes the aggregated channel ports.**

### PAgP Modes

- **On**
    - This mode forces the interface to channel without PAgP. 
    - Interfaces configured in the on mode do not exchange PAgP packets.

- **PAgP desirable**
    - This PAgP mode places an interface in an active negotiating state in which the interface initiates negotiations with other interfaces by sending PAgP packets.

- **PAgP auto**
    - This PAgP mode places an interface in a passive negotiating state in which the interface responds to the PAgP packets that it receives but does not initiate PAgP negotiation.

- The modes must be compatible on each side.

- Consider the two switches in the figure. Whether SW1 and SW2 establish an EtherChannel using PAgP depends on the mode settings on each side of the channel:

```
                <<---------PAgp---------------->>

                            /\
========     |1------------/--\----------------1|     ========
MODE-SW1  SW1|            /    \PortChannel    +|SW2  MODE-SW2
========     |2-----------\----/---------------2|     ========
                           \  /
                            \/
```        

### PAgP Modes

| SW1         | SW2            | Channel Establishment  |
|:-----------:|:--------------:|:----------------------:|
| `On`        | `On`           | `Yes`                  |
| On          | Desirable/Auto | No                     |
| `Desirable` | `Desirable`    | `Yes`                  |
| `Desirable` | `Auto`         | `Yes`                  |
| `Auto`      | `Desirable`    | `Yes`                  |
| Auto        | Auto           | No                     |

- **Just follow the fz3r0 International-Standard for cool people and set both sides `ON`...easy!**

- _Or be a hater and use other combinations..._

---

### LACP Operation

- **LACP is part of an IEEE specification (802.3ad)**

- LACP allows a switch to negotiate an automatic bundle by sending LACP packets to the other switch.

- It performs a function similar to PAgP with Cisco EtherChannel.

- Because LACP is an IEEE standard, it can be used to facilitate EtherChannels in multivendor environments. 

- On Cisco devices, both protocols are supported.

- LACP provides the same negotiation benefits as PAgP:

    - LACP helps create the EtherChannel link by detecting the configuration of each side and making sure that they are compatible so that the EtherChannel link can be enabled when needed.

- The modes for LACP are as follows:

- **On**
    - This mode forces the interface to channel without LACP. 
    - Interfaces configured in the on mode do not exchange LACP packets.

- **LACP active**
    - This LACP mode places a port in an active negotiating state. 
    - In this state, the port initiates negotiations with other ports by sending LACP packets.

- **LACP passive**
    - This LACP mode places a port in a passive negotiating state. 
    - In this state, the port responds to the LACP packets that it receives but does not initiate LACP packet negotiation.

- Just as with PAgP, modes must be compatible on both sides for the EtherChannel link to form. 

- The on mode is repeated, because it creates the EtherChannel configuration unconditionally, without PAgP or LACP dynamic negotiation.

- LACP allows for eight active links, and also eight standby links. A standby link will become active should one of the current active links fail.    

### LACP Modes

| SW1         | SW2            | Channel Establishment  |
|:-----------:|:--------------:|:----------------------:|
| `On`        | `On`           | `Yes`                  |
| On          | Active/Passive | No                     |
| `Active`    | `Active`       | `Yes`                  |
| `Active`    | `Passive`      | `Yes`                  |
| `Passive`   | `Active`       | `Yes`                  |
| Passive     | Passive        | No                     |

- **Just follow the fz3r0 International-Standard for cool people and set both sides `ON`...easy!**

- _Or be a hater and use other combinations..._

---

### Configuration Guidelines

- The following guidelines and restrictions are useful for configuring EtherChannel:

    - EtherChannel support
        - All Ethernet interfaces must support EtherChannel with no requirement that interfaces be physically contiguous.

    - Speed and duplex
        - Configure all interfaces in an EtherChannel to operate at the same speed and in the same duplex mode.

    - VLAN match
        - All interfaces in the EtherChannel bundle must be assigned to the same VLAN or be configured as a trunk (shown in the figure).

    - Range of VLANs
        - An EtherChannel supports the same allowed range of VLANs on all the interfaces in a trunking EtherChannel. 
        - If the allowed range of VLANs is not the same, the interfaces do not form an EtherChannel, even when they are set to auto or desirable mode. 

- **Very important to remember!** 

    - Use the same speed on cable and ports of the devices used on the etherchannel link (PortChannel). 

    - Basically, use identical cables, identical ports, even use same colors and plugs!

    - Use the same config in Speed, Duplex, VLAN #, trunk/access and any port configuration. SAME CONFIG, SAME CABLES, SAME SPEED, SAME INTERFACES... 

- Very important to remember II!

    - If you need to change the settings of the ChannelPort (the "fat cable"), even the description, vlan, or something... **configure them in port channel interface configuration mode.** 

        - Any configuration that is applied to the port channel interface also affects individual interfaces. 

        - However, configurations that are applied to the individual interfaces do not affect the port channel interface. 

        - **Therefore, making configuration changes to an interface that is part of an EtherChannel link may cause interface compatibility issues.**

- **The port channel can be configured in access mode, trunk mode (most common), or on a routed port.**      

---

### References

- https://contenthub.netacad.com/srwe-dl/6.2.3

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
