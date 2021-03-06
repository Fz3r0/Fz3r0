
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## Configure FHRP (First Hop Redundancy) on Cisco Routers, using HSRP (Hot Standby Router) like a Sir! 

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `FHRP` `Router Redundancy`

---
   
### Index

- < **Before anything else!!!** >

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

- < **Troubleshooting** & **show commands** for this configuration >** 

### Background Knowledge about this config:

- < **Nerd Pocket-Bible about this configuration** >

---

### Configuration of FHRP & HSRP 

- **Before anything else!**

    - Just as the redundancy in Layer 2 _(STP/Etherchannel in switches)_ you can configure redundancy on Layer 3 _(Routers)_ with **First Hop Redundancy Protocols (FHRPs)**.
    
    - This protocols use  

    - For example: 
    
        - If the gateway router (to Internet) goes down. None of your hosts can send any messages outside of the immediate network _(Internet or other VLANs)_. 
         
        - It’s going to take a while to get this default gateway router operating again, cuz you have the worst luck and the potato deosn't even turn on...RMA time... 
         
        - Tickets, calls and mails from people that doesn't even know a shit about computers are complaining because "it's you fault".
         
        - But the real problem here is that devices are not magical and sometimes shit happens... so, the solution:
         
            - We need to ask the CEO to invest in at least **other Gateway Router, so we can configure it as a "mirror" or a `Redundancy of Routers`**, that's the way we can fight back against the worst luck it can exist: _"the luck of an engineer"_ and buy some time until we can replace the faulty Router. EZ!
        
- **OK...let's keep going...**

---

### Background Knowledge

### Default Gateway Limitations

- If a router or router interface (that serves as a default gateway) fails, the hosts configured with that default gateway are isolated from outside networks. 

- A mechanism is needed to **provide alternate default gateways in switched networks where two or more routers are connected to the same VLANs**. That mechanism is provided by **first hop redundancy protocols (FHRPs).**

- In a switched network, each client receives only one default gateway. There is no way to use a secondary gateway, even if a second path exists to carry packets off the local segment.

### The problem with PCs (or other device) and unique IP config

- End devices are typically configured with a single IPv4 address for a default gateway.

- This address does not change when the network topology changes. (so, how it will "know his way" to the "mirror" router?!) 

- If that default gateway IPv4 address cannot be reached, the local device is unable to send packets off the local network segment, effectively disconnecting it from other networks.

    - **Even if a redundant router exists that could serve as a default gateway for that segment, there is no dynamic method by which these devices can determine the address of a new default gateway.** 

- _Note: IPv6 devices receive their default gateway address dynamically from the ICMPv6 Router Advertisement._

### Router Redundancy

- One way to prevent a single point of failure at the default gateway is to implement a `virtual router`.

- To implement this type of router redundancy, **multiple routers are configured to work together to present the illusion of a single router to the hosts on the LAN**, as shown in the figure.

- By sharing an IP address and a MAC address, two or more routers can act as a single virtual router: 

    - That's why I called as a **"mirror"**: devices "think" that the same router stills there, even if the original router fails, the PC just notice a little "cut" of couple seconds in the connection. 

![image](https://user-images.githubusercontent.com/94720207/166187133-11bfdda5-1822-45ee-a2cb-f6a618d5f95f.png)

- The IPv4 address of the virtual router _(Center Router)_ is configured as the default gateway for the workstations on a specific IPv4 segment.

- In a "normal" setup, when frames are sent from host devices to the default gateway, the hosts use ARP to resolve the MAC address that is associated with the IPv4 address of the default gateway _(MAC of the interface like Gi 0/1)_

- **But! with a virtual router is configured like a sir: the ARP resolution returns the `MAC address of the virtual router`.** _(NOT the physical interface, like MAC of Gi 0/1)_ 

### But how it works?!

- A redundancy protocol provides the mechanism for determining which router should take the active role in forwarding traffic. 

- It also determines when the forwarding role must be taken over by a standby router. 

- **The transition from one forwarding router to another is transparent to the end devices.**

- **The ability of a network to dynamically recover from the failure of a device acting as a default gateway is known as first-hop redundancy.**

---

### Steps for Router Failover

- When the `active router` fails, the redundancy protocol transitions the `standby router` to the `new active router` role, as shown in the figure. These are the steps that take place when the active router fails:

    1. The `standby router` **stops seeing Hello messages** from the `forwarding router`.

    2. The `standby router` **assumes the role** of the `forwarding router`.

    3. Because the `new forwarding router` **assumes both the IPv4 and MAC addresses of the virtual router**, the host devices see no disruption in service _(or maybe just a little micro tiny tiny cut)_.

![image](https://user-images.githubusercontent.com/94720207/166187812-f5eef0b4-67f2-48d3-b086-cc0855b37ece.png)

---

### FHRP Options

- The FHRP used in a production environment largely depends on the equipment and needs of the network. 

- This are all the options available for First Hop Redundancy Protocols `FHRPs`.

1. **Hot Standby Router Protocol (`HSRP`)** 
2. **HSRP for IPv6 (`HSRP-IPv6`)**
3. **Virtual Router Redundancy Protocol v2 (`VRRPv2`)**
4. **Virtual Router Redundancy Protocol v3 (`VRRPv3`)**
5. **Gateway Load Balancing Protocol (`GLBP`)**
6. **GLBP for IPv6 (`GLBP-IPv6`)**
7. **ICMP Router Discovery Protocol (`IRDP`)**

### 1. Hot Standby Router Protocol (`HSRP`)

- HRSP is a Cisco-proprietary First Hop Redundancy Protocol (FHRP) that is designed to allow for transparent failover of a first-hop IPv4 device.

- HSRP provides high network availability by providing first-hop routing redundancy for IPv4 hosts on networks configured with an IPv4 default gateway address. 

- HSRP is used in a group of routers for selecting an active device and a standby device. 

- In a group of device interfaces, the active device is the device that is used for routing packets; the standby device is the device that takes over when the active device fails, or when pre-set conditions are met.

- The function of the HSRP standby router is to monitor the operational status of the First Hop Redundancy Protocols (HSRP) group and to quickly assume packet-forwarding responsibility if the active router fails.

### 2. HSRP for IPv6 (`HSRP-IPv6`)

- This is a Cisco-proprietary FHRP that provides the same functionality of HSRP, but in an IPv6 environment. 

- An HSRP IPv6 group has a virtual MAC address derived from the HSRP group number and a virtual IPv6 link-local address derived from the HSRP virtual MAC address. 

- Periodic router advertisements (RAs) are sent for the HSRP virtual IPv6 link-local address when the HSRP group is active. 

    - When the group becomes inactive, these RAs stop after a final RA is sent.

### 3. Virtual Router Redundancy Protocol v2 (`VRRPv2`)

- This is a non-proprietary election protocol that dynamically assigns responsibility for one or more virtual routers to the VRRP routers on an IPv4 LAN. 
- This allows several routers on a multiaccess link to use the same virtual IPv4 address.

### 4. VRRPv3

- This provides the capability to support IPv4 and IPv6 addresses. 
- VRRPv3 works in multi-vendor environments and is more scalable than VRRPv2.

### 5. Gateway Load Balancing Protocol (GLBP)

- This is a Cisco-proprietary FHRP that protects data traffic from a failed router or circuit, like HSRP and VRRP, while also allowing load balancing (also called load sharing) between a group of redundant routers.

### 6. GLBP for IPv6

- This is a Cisco-proprietary FHRP that provides the same functionality of GLBP, but in an IPv6 environment. 
- GLBP for IPv6 provides automatic router backup for IPv6 hosts configured with a single default gateway on a LAN. 
- Multiple first-hop routers on the LAN combine to offer a single virtual first-hop IPv6 router while sharing the IPv6 packet forwarding load.

### 7. ICMP Router Discovery Protocol (IRDP)

- Specified in RFC 1256, IRDP is a legacy FHRP solution. IRDP allows IPv4 hosts to locate routers that provide IPv4 connectivity to other (nonlocal) IP networks.

---

### HSRP Overview

- Cisco provides HSRP and HSRP for IPv6 as a way to avoid losing outside network access if your default router fails.

- HSRP is a Cisco-proprietary FHRP that is designed to allow for transparent failover of a first-hop IP device.

- HSRP ensures high network availability by providing first-hop routing redundancy for IP hosts on networks configured with an IP default gateway address. HSRP is used in a group of routers for selecting an active device and a standby device. 

    - In a group of device interfaces, the active device is the device that is used for routing packets; 
    - the standby device is the device that takes over when the active device fails, or when pre-set conditions are met. 
    - The function of the HSRP standby router is to monitor the operational status of the HSRP group and to quickly assume packet-forwarding responsibility if the active router fails.

### HSRP Priority & Preemprion

- The role of the active and standby routers is determined during the HSRP election process. 
- By default, the router with the numerically highest IPv4 address is elected as the active router. 
- However, it is always better to control how your network will operate under normal conditions rather than leaving it to chance.

    - **HSRP Priority**
    
        - HSRP priority can be used to determine the active router. 
        - The router with the highest HSRP priority will become the active router. 
        - By default, the HSRP priority is 100. 
        - If the priorities are equal, the router with the numerically highest IPv4 address is elected as the active router.
            
            - **To configure a router to be the active router, use the standby priority interface command.**
            - **The range of the HSRP priority is 0 to 255.**

    - **HSRP Preemption**
    
        - By default, after a router becomes the active router, it will remain the active router even if another router comes online with a higher HSRP priority.
        - To force a new HSRP election process to take place when a higher priority router comes online, preemption must be enabled using the standby preempt interface command. 
        - Preemption is the ability of an HSRP router to trigger the re-election process. 
        - With preemption enabled, a router that comes online with a higher HSRP priority will assume the role of the active router.
        
            - Preemption only allows a router to become the active router if it has a higher priority. 
            - A router enabled for preemption, with equal priority but a higher IPv4 address will not preempt an active router. _Refer to the topology in the figure._ 

![image](https://user-images.githubusercontent.com/94720207/167488452-4122bedc-b0b4-4ac2-b330-0bb82e3f1d53.png)

- R1 has been configured with the HSRP priority of 150 while R2 has the default HSRP priority of 100. 
- Preemption has been enabled on R1. 
- With a higher priority, R1 is the active router and R2 is the standby router. 
    
    - Due to a power failure affecting only R1, the active router is no longer available and the standby router, R2, assumes the role of the active router. 
    - After power is restored, R1 comes back online. 
    - **Because R1 has a higher priority and preemption is enabled, it will force a new election process.** 
    - **R1 will re-assume the role of the active router and R2 will fall back to the role of the standby router.**

**Note: With preemption disabled, the router that boots up first will become the active router if there are no other routers online during the election process.**

### HSRP States and Timers

- A router can either be the active HSRP router responsible for forwarding traffic for the segment, or it can be a passive HSRP router on standby, ready to assume the active role if the active router fails. 
- When an interface is configured with HSRP or is first activated with an existing HSRP configuration, the router sends and receives HSRP hello packets to begin the process of determining which state it will assume in the HSRP group.

    - The table summarizes the HSRP states.

| **HSRP State** | **Description**                          |
|----------------|-------------------------------------------------------|
| **Initial**    | This state is entered through a configuration change or when an interface first becomes available.    |
| **Learn**      | The router has not determined the virtual IP address and has not yet seen a hello message from the active router. In this state, the router waits to hear from the active router.  |
| **Listen**     | The router knows the virtual IP address, but the router is neither the active router nor the standby router. It listens for hello messages from those routers.       |
| **Speak**      | The router sends periodic hello messages and actively participates in the election of the active and/or standby router.   |
| **Standby**    | The router is a candidate to become the next active router and sends periodic hello messages.    |
| **Active**     | The router won the election.    |

- The active and standby HSRP routers send hello packets to the HSRP group multicast address every 3 seconds by default. 
- The standby router will become active if it does not receive a hello message from the active router after 10 seconds. 
- You can lower these timer settings to speed up the failover or preemption. 
- However, to avoid increased CPU usage and unnecessary standby state changes, do not set the hello timer below 1 second or the hold timer below 4 seconds.

---

### References

- https://contenthub.netacad.com/srwe-dl/1.3.6

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
