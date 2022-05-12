
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

### Implement Port Security

1. **Secure Unused Ports**

### 1. Secure Unused Ports - `shutdown`

- Layer 2 devices are considered to be the weakest link in a company’s security infrastructure. 
- Layer 2 attacks are some of the easiest for hackers to deploy but these threats can also be mitigated with some common Layer 2 solutions.
    
    - All **switch ports (interfaces)** should be secured **before the switch is deployed for production use.** 
    - **How a port is secured depends on its function.**

- A simple method that many administrators use to help secure the network from unauthorized access is to disable all unused ports on a switch. 
        
    - For example: 
        
        - If a Catalyst 2960 switch has 24 ports and there are three Fast Ethernet connections in use, it is good practice to disable the 21 unused ports!!! 
        - Navigate to each unused port and issue the Cisco IOS `shutdown` command. 
        - If a port must be reactivated at a later time, it can be enabled with the `no shutdown` command.

- To configure a range of ports, use the interface range command:

```
Fz3r0_Switch(config)# interface range type module/first-number – last-number
```

- For example: 

    - To `shutdown` ports for `Fa0/8 through Fa0/24` on `S1`, you would enter the following command:

```
Fz3r0_Switch(config)# interface range fa0/8 - 24      <<<-----| Selecting range of Switchports
Fz3r0_Switch(config-if-range)# shutdown               <<<-----| Shutdown

%LINK-5-CHANGED: Interface FastEthernet0/8, changed state to administratively down
(output omitted)
%LINK-5-CHANGED: Interface FastEthernet0/24, changed state to administratively down

Fz3r0_Switch(config-if-range)#
```

### 2. Mitigate MAC Address Table Attacks - `port security` 

- The simplest and most effective method to prevent `MAC address table overflow attacks` is to enable `port security`.
- `port security` **limits the number of valid MAC addresses allowed on a port.** 
- It allows an administrator to manually configure `MAC addresses` for a port or to permit the switch to dynamically learn a **limited number of `MAC addresses`**. 

    - **When a port configured with port security receives a frame, the source MAC address of the frame is compared to the list of secure source MAC addresses that were manually configured or dynamically learned on the port.**
    - **By limiting the number of permitted MAC addresses on a port to one, port security can be used to control unauthorized access to the network, as shown in the figure.**

![image](https://user-images.githubusercontent.com/94720207/167964079-8ffb76d7-73df-4864-8e2b-8864633ff929.png)

- **Enable Port Security:**

    - Notice in the example, the switchport port-security command was rejected. 
    - This is because port security can only be configured on manually configured access ports or manually configured trunk ports. 

        - **By default, Layer 2 switch ports are set to dynamic auto (trunking on).** 
        - **Therefore, in the example, the port is configured with the `switchport mode access` interface configuration command.**

            - Note: Trunk port security is beyond the scope of CCNA.

```
Fz3r0_Switch(config)# interface f0/1
Fz3r0_Switch(config-if)# switchport port-security              
Command rejected: FastEthernet0/1 is a dynamic port.   <<<----| Rejected (because TRUNK DYNAMIC)

Fz3r0_Switch(config-if)# switchport mode access        <<<----| It must be << ACCESS >>
Fz3r0_Switch(config-if)# switchport port-security             |         or
Fz3r0_Switch(config-if)# end                                  |  Manual Trunk (not dynamic default)  
Fz3r0_Switch#
```

- Use the `show port-security` interface command to display the current port security settings for `FastEthernet 0/1`, as shown in the example. 
- Notice how `port security` is enabled, port status is Secure-down which means there are no devices attached and no violation has occurred, the violation mode is Shutdown, and how the maximum number of MAC addresses is 1. 
- If a device is connected to the port, the switch port status would display Secure-up and the switch will automatically add the device’s MAC address as a secure MAC. In this example, no device is connected to the port.

```
Fz3r0_Switch# show port-security interface f0/1
Port Security              : Enabled
Port Status                : Secure-down
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 1
Total MAC Addresses        : 0
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 0
Last Source Address:Vlan   : 0000.0000.0000:0
Security Violation Count   : 0
Fz3r0_Switch#
```

- **Note: If an active port is configured with the switchport port-security command and more than one device is connected to that port, the port will transition to the error-disabled state.** _This condition is discussed later in this topic._

- After port security is enabled, other port security specifics can be configured, as shown in the example:

```
Fz3r0_Switch(config-if)# switchport port-security ?
  aging        Port-security aging commands
  mac-address  Secure mac address
  maximum      Max secure addresses
  violation    Security violation mode  
Fz3r0_Switch(config-if)# switchport port-security
```

- **Limit and Learn MAC Addresses**

- To set the maximum number of MAC addresses allowed on a port, use the following command:

```
Fz3r0_Switch(config-if)# switchport port-security maximum value 
```

- The default port security value is `1`. The maximum number of secure MAC addresses that can be configured depends the switch and the IOS. In this example, the maximum is `8192`.

```
Fz3r0_Switch(config)# interface f0/1
Fz3r0_Switch(config-if)# switchport port-security maximum ? 
  <1-8192>  Maximum addresses
Fz3r0_Switch(config-if)# switchport port-security maximum 10
```

- The switch can be configured to learn about MAC addresses on a secure port in one of three ways:
    
1. Manually Configured:
    -  The administrator manually configures a static MAC address(es) by using the following command for each secure MAC address on the port: 
```
Fz3r0_Switch(config-if)# switchport port-security mac-address mac-address
```

2. Dynamically Learned:
    - When the switchport port-security command is entered, the current source MAC for the device connected to the port is automatically secured but is not added to the startup configuration. 
    - If the switch is rebooted, the port will have to re-learn the device’s MAC address. 

3. Dynamically Learned – Sticky
    - The administrator can enable the switch to dynamically learn the MAC address and "stick" them to the running configuration by using the following command:

```
Fz3r0_Switch(config-if)# switchport port-security mac-address sticky 
```

- Saving the running configuration will commit the dynamically learned MAC address to NVRAM.

    - Full example:
    
        - The following example demonstrates a complete `port security` configuration for `FastEthernet 0/1` with a **host connected to port `Fa0/1`**. 
        - The administrator specifies a **maximum of 2 MAC addresses**, manually configures one secure MAC address, and then configures the port to dynamically learn additional secure MAC addresses up to the 2 secure MAC address maximum. 
        - Use the show port-security interface and the show port-security address command to verify the configuration.  

```
Fz3r0_Switch#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.

Fz3r0_Switch(config)#
Fz3r0_Switch(config)# interface fa0/1
Fz3r0_Switch(config-if)# switchport mode access                                   <<<----| Access (or Manual trunk)
Fz3r0_Switch(config-if)# switchport port-security                                 <<<----| Enable it!
Fz3r0_Switch(config-if)# switchport port-security maximum 2                       <<<----| Max 2 MAC Address
Fz3r0_Switch(config-if)# switchport port-security mac-address aaaa.bbbb.1234      <<<----| Manual
Fz3r0_Switch(config-if)# switchport port-security mac-address sticky              <<<----| Sticky

Fz3r0_Switch# show port-security interface fa0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7272.676a:1
Security Violation Count   : 0
S1# show port-security address
               Secure Mac Address Table
-----------------------------------------------------------------------------
Vlan    Mac Address       Type                          Ports   Remaining Age
                                                                   (mins)    
----    -----------       ----                          -----   -------------
1    a41f.7272.676a    SecureSticky                  Fa0/1        -
1    aaaa.bbbb.1234    SecureConfigured              Fa0/1        -
-----------------------------------------------------------------------------
Total Addresses in System (excluding one mac per port)     : 1
Max  Addresses limit in System (excluding one mac per port) : 8192

Fz3r0_Switch#
```

- The output of the show port-security interface command verifies that port security is enabled, there is a host connected to the port (i.e., Secure-up), a total of 2 MAC addresses will be allowed, and S1 has learned one MAC address statically and one MAC address dynamically (i.e., sticky).

- The output of the show port-security address command lists the two learned MAC addresses.
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



