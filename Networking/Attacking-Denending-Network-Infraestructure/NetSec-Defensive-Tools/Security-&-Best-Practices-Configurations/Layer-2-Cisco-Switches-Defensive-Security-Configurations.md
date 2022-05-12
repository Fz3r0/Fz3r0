
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

| **Solution**                     | **Description**                |
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

---

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

---

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

- The output of the `show port-security` address command lists the two learned MAC addresses.

- **Port Security Aging**

    - Port security aging can be used to set the aging time for static and dynamic secure addresses on a port. 
    - Two types of aging are supported per port:

        - Absolute: The secure addresses on the port are deleted after the specified aging time.
        
        - Inactivity: The secure addresses on the port are deleted only if they are inactive for the specified aging time.
    
    - Use aging to remove secure MAC addresses on a secure port without manually deleting the existing secure MAC addresses. 
    - Aging time limits can also be increased to ensure past secure MAC addresses remain, even while new MAC addresses are added. 
    - Aging of statically configured secure addresses can be enabled or disabled on a per-port basis.

 Use the switchport port-security aging command to enable or disable static aging for the secure port, or to set the aging time or type.  

```
Fz3r0_Switch(config-if)# switchport port-security aging { static | time time | type {absolute | inactivity}}
```

- The parameters for the command are described in the table.

| **Parameter**        | **Description**                  |
|----------------------|----------------------------------|
| **static**          | Enable aging for statically configured secure addresses on this port.         |
| **time time**      | Specify the aging time for this port. The range is 0 to 1440 minutes. If the time is 0, aging is disabled for this port.                                               |
| **type absolute**   | Set the absolute aging time. All the secure addresses on this port age out exactly after the time (in minutes) specified and are removed from the secure address list. |
| **type inactivity** | Set the inactivity aging type. The secure addresses on this port age out only if there is no data traffic from the secure source address for the specified time period |

- Note: MAC addresses are shown as 24 bits for simplicity.

- The example shows an administrator configuring the aging type to 10 minutes of inactivity and by using the show port-security interface command to verify the configuration.

```
Fz3r0_Switch(config)# interface fa0/1
Fz3r0_Switch(config-if)# switchport port-security aging time 10 
Fz3r0_Switch(config-if)# switchport port-security aging type inactivity 
Fz3r0_Switch(config-if)# end
Fz3r0_Switch# show port-security interface fa0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Shutdown
Aging Time                 : 10 mins
Aging Type                 : Inactivity
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7272.676a:1
Security Violation Count   : 0
Fz3r0_Switch#
```

- **Port Security Violation Modes**

- If the MAC address of a device attached to the port differs from the list of secure addresses, then a port violation occurs. By default, the port enters the error-disabled state.

    - To set the port security violation mode, use the following command:

```
Fz3r0_Switch(config-if)# switchport port-security violation { protect | restrict | shutdown}
```

- Violation Modes Comparations:

| **Violation Mode** | **Discards Offending Traffic** | **Sends Syslog Message** | **Increase Violation Counter** | **Shuts Down Port** |
|--------------------|--------------------------------|--------------------------|--------------------------------|----------------------|
| **Protect**        | Yes                            | No                       | No                             | No                   |
| **Restrict**       | Yes                            | Yes                      | Yes                            | No                   |
| **Shutdown**       | Yes                            | Yes                      | Yes                            | Yes                  |

- The following example shows an administrator changing the security violation to “restrict”. The output of the show port-security interface command confirms that the change has been made.

```
Fz3r0_Switch(config)# interface f0/1
Fz3r0_Switch(config-if)# switchport port-security violation restrict
Fz3r0_Switch(config-if)# end
Fz3r0_Switch#
Fz3r0_Switch# show port-security interface f0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Restrict
Aging Time                 : 10 mins
Aging Type                 : Inactivity
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7272.676a:1
Security Violation Count   : 0
Fz3r0_Switch#
```

- **Ports in error-disabled State**

- What happens when the port security violation is shutdown and a port violation occurs? 
- The port is physically shutdown and placed in the error-disabled state, and no traffic is sent or received on that port.
- In the example, the show interface command identifies the port status as err-disabled. 
- The output of the show port-security interface command now shows the port status as Secure-shutdown instead of Secure-up. 
- The Security Violation counter increments by 1.

```
Fz3r0_Switch# show interface fa0/1 | include down
FastEthernet0/18 is down, line protocol is down (err-disabled)
(output omitted)
Fz3r0_Switch# show port-security interface fa0/1
Port Security              : Enabled
Port Status                : Secure-shutdown
Violation Mode             : Shutdown
Aging Time                 : 10 mins
Aging Type                 : Inactivity
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 2
Total MAC Addresses        : 2
Configured MAC Addresses   : 1
Sticky MAC Addresses       : 1
Last Source Address:Vlan   : a41f.7273.018c:1
Security Violation Count   : 1
Fz3r0_Switch#
```

- The administrator should determine what caused the security violation If an unauthorized device is connected to a secure port, the security threat is eliminated before re-enabling the port.

- In the next example, the first host is reconnected to Fa0/1. To re-enable the port, first use the shutdown command, then, use the no shutdown command to make the port operational, as shown in the example.

```
Fz3r0_Switch(config)# interface fa0/1
Fz3r0_Switch(config-if)# shutdown
Fz3r0_Switch(config-if)#
*Mar  1 00:39:54.981: %LINK-5-CHANGED: Interface FastEthernet0/1, changed state to administratively down
Fz3r0_Switch(config-if)# no shutdown
Fz3r0_Switch(config-if)#
*Mar  1 00:40:04.275: %LINK-3-UPDOWN: Interface FastEthernet0/1, changed state to up
*Mar  1 00:40:05.282: %LINEPROTO-5-UPDOWN: Line protocol on Interface FastEthernet0/1, changed state to up
Fz3r0_Switch(config-if)#
```

- **Verify Port Security**

```
show port-security interface f0/1
show port-security
show run interface fa0/1
show port-security address
```

---

### 3. Mitigate VLAN Attacks - DTP `nonegotiate` & manual vlans

- As a quick review, a VLAN hopping attack can be launched in one of three ways:

    1. Spoofing DTP messages from the attacking host to cause the switch to enter trunking mode. 
        - From here, the attacker can send traffic tagged with the target VLAN, and the switch then delivers the packets to the destination.
    2.Introducing a rogue switch and enabling trunking. 
        - The attacker can then access all the VLANs on the victim switch from the rogue switch.
    3.Another type of VLAN hopping attack is a double-tagging (or double-encapsulated) attack. 
        - This attack takes advantage of the way hardware on most switches operate.

- **Steps to Mitigate VLAN Hopping Attacks:**

    - Step 1: **Disable DTP (auto trunking) negotiations on non-trunking ports** by using the `switchport mode access` interface configuration command.

    - Step 2: **Disable unused ports and put them in an unused VLAN.**

    - Step 3: **Manually enable the trunk link on a trunking port** by using the `switchport mode trunk` command.

    - Step 4: **Disable DTP (auto trunking) negotiations on trunking ports** by using the `switchport nonegotiate` command.

    - Step 5: **Set the native VLAN to a VLAN other than VLAN 1** by using the `switchport trunk native vlan vlan_number` command.

- For example, assume the following:

    - FastEthernet ports 0/1 through fa0/16 are active access ports
    - FastEthernet ports 0/17 through 0/20 are not currently in use
    - FastEthernet ports 0/21 through 0/24 are trunk ports.

        - **VLAN hopping can be mitigated by implementing the following configuration.**

```
Fz3r0_Switch(config)# interface range fa0/1 - 16
Fz3r0_Switch(config-if-range)# switchport mode access
Fz3r0_Switch(config-if-range)# exit
Fz3r0_Switch(config)# 

Fz3r0_Switch(config)# interface range fa0/17 - 20
Fz3r0_Switch(config-if-range)# switchport mode access
Fz3r0_Switch(config-if-range)# switchport access vlan 1000
Fz3r0_Switch(config-if-range)# shutdown
Fz3r0_Switch(config-if-range)# exit
Fz3r0_Switch(config)# 

Fz3r0_Switch(config)# interface range fa0/21 - 24
Fz3r0_Switch(config-if-range)# switchport mode trunk
Fz3r0_Switch(config-if-range)# switchport nonegotiate
Fz3r0_Switch(config-if-range)# switchport trunk native vlan 999
Fz3r0_Switch(config-if-range)# end
Fz3r0_Switch#
```

- FastEthernet ports 0/1 to 0/16: 
    - Are access ports and therefore trunking is disabled by explicitly making them access ports.

- FastEthernet ports 0/17 to 0/20:  
    - Are unused ports and are disabled and assigned to an unused VLAN.

- FastEthernet ports 0/21 to 0/24:
    - Are trunk links and are manually enabled as trunks with DTP disabled. 
    - The native VLAN is also changed from the default VLAN 1 to an unused VLAN 999.

---

### 4. Mitigate DHCP Attacks -  `DHCP snooping`

- **DHCP Attack Review**

    -  The goal of a DHCP starvation attack is to create a Denial of Service (DoS) for connecting clients. 
    -  DHCP starvation attacks require an attack tool such as Gobbler. 
    -  Recall that DHCP starvation attacks can be effectively mitigated by using port security because Gobbler uses a unique source MAC address for each DHCP request sent.
        
        - However, mitigating DHCP spoofing attacks requires more protection. 
        - Gobbler could be configured to use the actual interface MAC address as the source Ethernet address, but specify a different Ethernet address in the DHCP payload. 
        
            - **This would render port security ineffective because the source MAC address would be legitimate.**

    - **DHCP spoofing attacks can be mitigated by using `DHCP snooping` on `trusted ports`.**

- **DHCP Snooping**

    - **DHCP snooping does not rely on source MAC addresses.** 
        - Instead, DHCP snooping determines whether DHCP messages are from an administratively configured trusted or untrusted source. 
        - It then filters DHCP messages and rate-limits DHCP traffic from untrusted sources.

    - Devices under your administrative control, such as switches, routers, and servers, are trusted sources. 
        - **Any device beyond the firewall or outside your network is an untrusted source.** 
        - **In addition, **all access ports are generally treated as untrusted sources.** 
    
    - The figure shows an example of trusted and untrusted ports:

![image](https://user-images.githubusercontent.com/94720207/167978298-6a0bf48a-4871-4f34-931e-d4512acfd9be.png)

- Notice that the rogue DHCP server would be on an untrusted port after enabling DHCP snooping. 
- All interfaces are treated as untrusted by default. 
- Trusted interfaces are typically trunk links and ports directly connected to a legitimate DHCP server. 
- These interfaces must be explicitly configured as trusted.
- A DHCP table is built that includes the source MAC address of a device on an untrusted port and the IP address assigned by the DHCP server to that device. 
- The MAC address and IP address are bound together. 

    - Therefore, this table is called the DHCP snooping binding table.

- **Steps to Implement DHCP Snooping:**

    - Step 1. Enable DHCP snooping by using the `ip dhcp snooping` **global configuration command**.

    - Step 2. On trusted ports, use the `ip dhcp snooping trust` interface configuration command.

    - Step 3. Limit the number of DHCP discovery messages that can be received per second on untrusted ports by using the `ip dhcp snooping limit rate` interface configuration command.

    - Step 4. **Enable DHCP snooping by VLAN, or by a range of VLANs**, by using the ip `dhcp snooping vlan` global configuration command.

- **DHCP Snooping Configuration Example:**

    - The reference topology for this DHCP snooping example is shown in the figure. 

        - Notice that F0/5 is an untrusted port because it connects to a PC. 
        - F0/1 is a trusted port because it connects to the DHCP server.

![image](https://user-images.githubusercontent.com/94720207/167979425-f4f48089-25a9-475a-aa66-1fff88de4f05.png)

- The following is an example of how to configure DHCP snooping on S1. 
    - Notice how DHCP snooping is first enabled. 
    - Then the upstream interface to the DHCP server is explicitly trusted.(F0/1) 
    - Next, the range of FastEthernet ports from F0/5 to F0/24 are untrusted by default, so a rate limit is set to six packets per second. 
    - Finally, DHCP snooping is enabled on VLANS 5, 10, 50, 51, and 52.

```
Fz3r0_Switch(config)# ip dhcp snooping
Fz3r0_Switch(config)# interface f0/1
Fz3r0_Switch(config-if)# ip dhcp snooping trust
Fz3r0_Switch(config-if)# exit

Fz3r0_Switch(config)# interface range f0/5 - 24
Fz3r0_Switch(config-if-range)# ip dhcp snooping limit rate 6
Fz3r0_Switch(config-if-range)# exit
Fz3r0_Switch(config)# ip dhcp snooping vlan 5,10,50-52
Fz3r0_Switch(config)# end
Fz3r0_Switch#
```

- Use the `show ip dhcp snooping`rivileged EXEC command to verify DHCP snooping and `ow ip dhcp snooping binding to view the clients that have received DHCP information, as shown in the example.

Note: DHCP snooping is also required by Dynamic ARP Inspection (DAI), which is the next topic

```
Fz3r0_Switch# show ip dhcp snooping
Switch DHCP snooping is enabled
DHCP snooping is configured on following VLANs:
5,10,50-52
DHCP snooping is operational on following VLANs:
none
DHCP snooping is configured on the following L3 Interfaces:
Insertion of option 82 is enabled
   circuit-id default format: vlan-mod-port
   remote-id: 0cd9.96d2.3f80 (MAC)
Option 82 on untrusted port is not allowed
Verification of hwaddr field is enabled
Verification of giaddr field is enabled
DHCP snooping trust/rate is configured on the following Interfaces:
Interface                  Trusted    Allow option    Rate limit (pps)
-----------------------    -------    ------------    ----------------   
FastEthernet0/1            yes        yes             unlimited
  Custom circuit-ids:
FastEthernet0/5            no         no              6         
  Custom circuit-ids:
FastEthernet0/6            no         no              6         
  Custom circuit-ids:
S1# show ip dhcp snooping binding
MacAddress         IpAddress       Lease(sec) Type          VLAN Interface
------------------ --------------- ---------- ------------- ---- --------------------
00:03:47:B5:9F:AD  192.168.10.11   193185     dhcp-snooping 5    FastEthernet0/5

Fz3r0_Switch#
```

---

### 5. Mitigate ARP Attacks `Dynamic ARP Inspection`

- **Dynamic ARP Inspection**

    - In a typical ARP attack, a threat actor can send unsolicited ARP requests to other hosts on the subnet with the MAC Address of the threat actor and the IP address of the default gateway. 
    - To prevent `ARP spoofing` and the resulting `ARP poisoning`, **a switch must ensure that only valid ARP Requests and Replies are relayed.**
    
        - **`Dynamic ARP inspection (DAI)` requires `DHCP snooping` and helps prevent ARP attacks by:**
        
            - Not relaying invalid or gratuitous ARP Requests out to other ports in the same VLAN.
            - Intercepting all ARP Requests and Replies on untrusted ports.
            - Verifying each intercepted packet for a valid IP-to-MAC binding.
            - Dropping and logging ARP Requests coming from invalid sources to prevent ARP poisoning.
            - Error-disabling the interface if the configured DAI number of ARP packets is exceeded.

- **DAI Implementation Guidelines**

    - **To mitigate the chances of ARP spoofing and ARP poisoning, follow these DAI implementation guidelines:**
    
        - Enable DHCP snooping globally.
        - Enable DHCP snooping on selected VLANs.
        - **Enable DAI on selected VLANs.**
        - **Configure trusted interfaces for DHCP snooping and ARP inspection.**   
 
     - **It is generally advisable to configure `all access switch ports as UNTRUSTED`** 
     
     - **And configure `all uplink ports that are connected to other switches as TRUSTED.`**

The sample topology in the figure identifies trusted and untrusted ports.

![image](https://user-images.githubusercontent.com/94720207/167986541-6f2d5b0f-a4a2-43c3-a51f-de8e422bf238.png)

- **DAI Configuration Example**:

    - 


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



