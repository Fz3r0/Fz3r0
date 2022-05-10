
# Fz3r0 Operations: Network Security

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## Layer 2 Cisco Switches Defensive Configurations

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---
 
#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Layer 2 Attack` `Hacking` `Pentesting` `MAC Flooding` `ARP Spoofing` `Try Hack Me` `Writeup`
---
   
### Index 

- < **[Before anything else!!!]()** >

- < **Task 1**: [Network Discovery]() >

- < **Task 2**: [Passive Network Sniffing](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#passive-network-sniffing) >

- < **Task 3**: [Sniffing while MAC Flooding](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#sniffing-while-mac-flooding) >

    - < **Task 3.1**: [Mitigation of MAC Flooding Attacks on Cisco Layer 2 Devices](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#mitigation-of-mac-flooding-attacks-on-cisco-layer-2-devices) >

- < **Task 4**: [MITM Man-in-the-Middle (MITM): Intro to ARP Poisoning + Sniffing](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#man-in-the-middle-intro-to-arp-spoofing) >

- < **Task 5**: [MITM Man-in-the-Middle (MITM): ARP Posoning + MAC Spoofing + Sniffing || Reverse Shell Payload + PrivEsc](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#man-in-the-middle-sniffing) >

    - < **Task 5.1**: [Mitigation of ARP Poisoning + MAC Spoofing Attacks on Cisco Layer 2 Devices]() >

- [< **Conclusions & Proof of Concept** >]()

---

### Before anything else!!!



    
---

### Layer 2 Vulnerabilities & Mitigations Introduction

- Network administrators routinely implement security solutions to protect the elements in Layer 3 up through Layer 7. 
- They use VPNs, firewalls, and IPS devices to protect these elements. 
- However, if Layer 2 is compromised, then all the layers above it are also affected. 
- For example, if a threat actor with access to the internal network captured Layer 2 frames, then all the security implemented on the layers above would be useless. 
- The threat actor could cause a lot of damage on the Layer 2 LAN networking infrastructure.

![image](https://user-images.githubusercontent.com/94720207/167526943-63ca7fd8-325d-48b7-83d6-e82c9c481ab6.png)

### Switch Attack Categories

- Security is only as strong as the weakest link in the system, and Layer 2 is considered to be that weak link. This is because LANs were traditionally under the administrative control of a single organization. 
- We inherently trusted all persons and devices connected to our LAN. 
- Today, with BYOD and more sophisticated attacks, our LANs have become more vulnerable to penetration. 
- Therefore, in addition to protecting Layer 3 to Layer 7, network security professionals must also mitigate attacks to the Layer 2 LAN infrastructure.

- The first step in mitigating attacks on the Layer 2 infrastructure is to understand the underlying operation of Layer 2 and the threats posed by the Layer 2 infrastructure.

    - Attacks against the Layer 2 LAN infrastructure are described in the table and are discussed in more detail later in this module.

    - Layer 2 Attacks

| **Category**                 | **Examples**                            |
|------------------------------|-----------------------------------------|
| **MAC Table Attacks**        | Includes MAC address flooding attacks.  |
| **VLAN Attacks**             | Includes VLAN hopping and VLAN double-tagging attacks. It also includes attacks between devices on a common VLAN.  |
| **DHCP Attacks**             | Includes DHCP starvation and DHCP spoofing attacks.            |
| **ARP Attacks**              | Includes ARP spoofing and ARP poisoning attacks.     |
| **Address Spoofing Attacks** | Includes MAC address and IP address spoofing attacks.        |
| **STP Attacks**              | Includes Spanning Tree Protocol manipulation attacks.      |

### Switch Attack Mitigation Techniques

- The table provides an overview of Cisco solutions to help mitigate Layer 2 attacks.

   - Layer 2 Attack Mitigation

| **Solution**                     | **Description **           |
|----------------------------------|--------------------------------|
| **Port Security**                | Prevents many types of attacks including MAC address flooding attacks and DHCP starvation attacks.  |
| **DHCP Snooping**                | Prevents DHCP starvation and DHCP spoofing attacks.    |
| **Dynamic ARP Inspection (DAI)** | Prevents ARP spoofing and ARP poisoning attacks.       |
| **IP Source Guard (IPSG)**       | Prevents MAC and IP address spoofing attacks.          |

- These Layer 2 solutions will not be effective if the management protocols are not secured. 
    
    - For example:   
   
        - The management protocols Syslog, Simple Network Management Protocol (SNMP), Trivial File Transfer Protocol (TFTP), telnet, File Transfer Protocol (FTP) and most other common protocols are insecure; 
    
    - Therefore, the following strategies are recommended:

        - Always use secure variants of these protocols such as SSH, Secure Copy Protocol (SCP), Secure FTP (SFTP), and Secure Socket Layer/Transport Layer Security (SSL/TLS).
        - Consider using out-of-band management network to manage devices.
        - Use a dedicated management VLAN where nothing but management traffic resides.
        - Use ACLs to filter unwanted access.

--- 

### MAC Address Table Attack

- **Switch Operation Review**

    - In this topic, the focus is still on switches, specifically their MAC address tables and how these tables are vulnerable to attacks.
    - Recall that to make forwarding decisions, a Layer 2 LAN switch builds a table based on the source MAC addresses in received frames. 
    - Shown in the figure, this is called a MAC address table. 
    - **MAC address tables** are stored in memory and are used to more efficiently forward frames. 

```
S1# show mac address-table dynamic
          Mac Address Table
-------------------------------------------
Vlan    Mac Address       Type        Ports
----    -----------       --------    -----
   1    0001.9717.22e0    DYNAMIC     Fa0/4
   1    000a.f38e.74b3    DYNAMIC     Fa0/1
   1    0090.0c23.ceca    DYNAMIC     Fa0/3
   1    00d0.ba07.8499    DYNAMIC     Fa0/2
S1#
```

### MAC Address Table Flooding

- All MAC tables have a fixed size and consequently, a switch can run out of resources in which to store MAC addresses. 
- MAC address flooding attacks take advantage of this limitation by bombarding the switch with fake source MAC addresses until the switch MAC address table is full.
- When this occurs, the switch treats the frame as an unknown unicast and begins to flood all incoming traffic out all ports on the same VLAN without referencing the MAC table. 
- This condition now allows a threat actor to capture all of the frames sent from one host to another on the local LAN or local VLAN.

![image](https://user-images.githubusercontent.com/94720207/167533324-11527668-1974-414c-86fc-87d50bfcfdfd.png)

- Note: 
    - Traffic is flooded only within the local LAN or VLAN. 
    - The threat actor can only capture traffic within the local LAN or VLAN to which the threat actor is connected.

- The figure shows how a threat actor can easily use the network attack tool `macof` to overflow a MAC address table.

![image](https://user-images.githubusercontent.com/94720207/167533504-b6487d0a-9600-464c-bc9a-4ad6cafcca91.png)

### MAC Address Table Attack Mitigation

- What makes tools such as macof so dangerous is that an attacker can create a MAC table overflow attack very quickly. 
- For instance, a Catalyst 6500 switch can store 132,000 MAC addresses in its MAC address table. 
- A tool such as `macof` **can flood a switch with up to 8,000 bogus frames per second**; creating a MAC address table overflow attack in a matter of a few seconds. 
- The example shows a sample output of the `macof` launching a Mac Flooding attack for 15 seconds:

<span align="center"> <p align="center"> ![image](/Networking/Attacking-Cisco/MAC_Flooding_Attack.gif) </p> </span>

- **Another reason why these attack tools are dangerous is because they not only affect the local switch, they can also affect other connected Layer 2 switches:** 

    - When the MAC address table of a switch is full, it starts flooding out all ports including those connected to other Layer 2 switches.

- **To mitigate MAC address table overflow attacks, network administrators must implement `port security`.** 

    - `Port security` will only allow a specified number of source MAC addresses to be learned on the port. (Port security is further discussed in another module.)

--- 




---

### References

- https://www.cisco.com/c/en/us/products/collateral/security/email-security-appliance/data-sheet-c78-729751.html
- https://www.cisco.com/c/en/us/products/security/web-security-appliance/index.html 
 
---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_  
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 



