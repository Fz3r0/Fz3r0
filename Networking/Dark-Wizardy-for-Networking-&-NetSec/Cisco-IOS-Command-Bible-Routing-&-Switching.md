---
	

# CCNA Switch command cheat-sheet
#### Useful command collection for Cisco Switches. Based on Cisco Networking Academy CCNA version 6 and version 7 course material, and recommended for CCNA exam preparation.

![calaverita](https://user-images.githubusercontent.com/94720207/171378091-12dd2619-1201-435a-8354-461922d876e8.gif)


---
## Table of contents

- [Important ``show`` commands](#important-show-commands)
- [Interface ranges](#managing-more-than-one-interface-at-the-same-time)
- [**VLANs**](#VLANS)
    - [Configuring VLANs](#configuring-vlans)
    - [Deleting VLANS](#deleting-a-vlan)
    - [Removing interface(s) from a VLAN](removing-interfaces-from-a-vlan)
    - [Configuring Trunks](#configuring-ieee-802.1q-trunk-links)
    - [Dynamic Trunking Protocol](#dynamic-trunking-protocol-DTP)
    - [VLAN troubleshooting](#troubleshooting-vlans)
    - [Trunk link troubleshooting](#troubleshooting-trunks)
    - [Voice VLANs](#voice-vlans)
- [Configuring SSH](#configuring-ssh)
- [Modifying SSH configuration](#modifying-ssh-configuration)
- [Port Security](#port-security)
    - [Configuring Dynamic Port Security](#closed_lock_with_key-configuring-dynamic-port-security)
    - [Configuring Sticky Port Security](#closed_lock_with_key-configuring-sticky-port-security)
    - [Verifying Port Security & secure MAC addresses](#closed_lock_with_key-white_check_mark-verifying-port-security-&-secure-mac-addresses)
        - [``Err-disabled`` interfaces](#bringing-an-err-disabled-interface-back-up)
- [VLAN management with VTP](#VLAN-trunking-protocol-VTP)
    - [VTP verification](#VTP-verification)
- [STP](#Spanning-Tree-Protocol)
- [EtherChannel](#etherchannel)














---

# CCNA Cheat Sheet

## Table of Contents

<!-- MarkdownTOC lowercase_only_ascii="true" depth=3 autolink="true" bracket="round" -->

- [Configure basic Networking](#configure-basic-networking)
	- [Troubleshoot basic Networking](#troubleshoot-basic-networking)
	- [Troubleshoot networks with SPAN](#troubleshoot-networks-with-span)
- [Port Security](#port-security)
	- [Troubleshooting Port Security](#troubleshooting-port-security)
- [Configure vlans](#configure-vlans)
	- [Layer2 Switch Vlan Config](#layer2-switch-vlan-config)
	- [Layer3 Switch Vlan Config](#layer3-switch-vlan-config)
	- [Router \(on a Stick\) Vlan Config](#router-on-a-stick-vlan-config)
	- [Troubleshoot Vlans on a switch](#troubleshoot-vlans-on-a-switch)
	- [VTP](#vtp)
	- [Troubleshoot VTP](#troubleshoot-vtp)
- [STP](#stp)
	- [Troubleshoot STP](#troubleshoot-stp)
	- [RSTP](#rstp)
- [Etherchannel \(Link Aggregation\)](#etherchannel-link-aggregation)
	- [Troubleshoot Etherchannel \(Link Aggregation\)](#troubleshoot-etherchannel-link-aggregation)
- [Configure a Serial](#configure-a-serial)
- [ACLs](#acls)
	- [Interface ACLs](#interface-acls)
	- [Troubleshooting ACLs](#troubleshooting-acls)
- [NAT](#nat)
	- [SNAT](#snat)
	- [DNAT](#dnat)
	- [PAT](#pat)
	- [Troubleshooting NAT](#troubleshooting-nat)
- [DHCP Server](#dhcp-server)
	- [Troubleshooting DHCP](#troubleshooting-dhcp)
- [HSRP](#hsrp)
	- [Troubleshooting HSRP](#troubleshooting-hsrp)
- [SLAs](#slas)
	- [Troubleshooting SLAs](#troubleshooting-slas)
- [Device Management](#device-management)
	- [Firmware Management](#firmware-management)
	- [License Management](#license-management)
	- [Reset Password](#reset-password)
	- [Telnet / Console](#telnet--console)
	- [SSH](#ssh)
	- [Clock](#clock)
	- [Disable unused services](#disable-unused-services)
	- [Radius](#radius)
	- [TACACS+](#tacacs)
	- [Syslog](#syslog)
	- [SNMP](#snmp)
	- [CDP - Cisco Discovery Protocol](#cdp---cisco-discovery-protocol)
	- [LLDP - Link Layer Discovery Protocol](#lldp---link-layer-discovery-protocol)
- [PPP](#ppp)
	- [Troubleshooting PPP](#troubleshooting-ppp)
	- [MLP](#mlp)
		- [Troubleshooting MLP](#troubleshooting-mlp)
	- [PPPoE](#pppoe)
		- [Troubleshooting PPPoE](#troubleshooting-pppoe)
- [GRE](#gre)
	- [Troubleshooting GRE](#troubleshooting-gre)
- [RIPv2](#ripv2)
	- [Troubleshooting RIPv2](#troubleshooting-ripv2)
- [EIGRP](#eigrp)
	- [EIGRP with ipv6](#eigrp-with-ipv6)
- [OSPF](#ospf)
	- [Router Types](#router-types)
	- [OSPF with ipv6 \(OSPFv3\)](#ospf-with-ipv6-ospfv3)
	- [Troubleshooting OSPF](#troubleshooting-ospf)
- [BGP](#bgp)
- [CLI](#cli)
	- [Default Behavior](#default-behavior)
	- [Modes](#modes)
	- [Filters](#filters)
	- [Navigation](#navigation)
- [Packet Types](#packet-types)
	- [Ethernet Frame](#ethernet-frame)
	- [IPv4 Header](#ipv4-header)
	- [TCP Segment](#tcp-segment)
	- [UDP Segment](#udp-segment)
- [To Sort and Misc](#to-sort-and-misc)

<!-- /MarkdownTOC -->

---
## Before we start: Configuration modes
Three basic configuration modes we MUST be familiar with already (you will see them below, a lot).  

Mode (prompt)|Device configuration mode|"Mode change" command (current -> next)
---|---|---
``S1>``|EXEC mode|type ``enable`` to pass to next mode
``S1#``|Privileged EXEC mode|type ``configure terminal`` to pass to next mode
``S1(config)#``|Global congiguration mode|N/A

Common abbreviations to the commands above (separated by commas):
```
en, ena
conf t, config term
```

## Tips & Tricks!

### Managing more than one interface at the same time
When we want to execute a sequence on commands on more than one port, selecting an interface range makes the job a lot easier.  
Use: ``S1(config)#interface range [typeModule/firstNumber]-[lastNumber]``

*typeModule*s|some possible abbreviations
---|---
``FastEthernet``|``f, fa, ...``
``GigabitEthernet``|``g, gi, gig, ...``

Here's an example:
``S1(config)#interface range f0/1-12``  

Note that you can select multiple ranges on a single command.  
Here's an example:
``S1(config)#interface range f0/1-12, 15-24, g0/1-2``

You might need to use it frequently on scenarios where the following blocks of commands are used.

### Filtering information from ``show`` commands:
Some commands, such as ``show running-config``, generate multiple lines of output.  

To filter output, you can use the *pipe* (``|``) character along with a **filtering parameter** and a **filtering expression**.
Filtering parameters|Effect
---|---
``section [filtering-expression]``|shows the section of the _filtering expression_
``include [filtering-expression]``|includes all lines of output that match the _filtering expression_ **ONLY**
``exclude [filtering-expression]``|excludes all lines of output that match the _filtering expression_
``begin [filtering-expression]``|shows all the lines of output **beginning from** the line that matches the _filtering expression_

### Usage:
Here's an example of the usage of filtering with a ``show`` command:  
``R1#show running-config | include line con``

:bulb: ProTip: By default, the screen of output consists of 24 lines. Should you want to change the number of output lines displayed on the terminal screen, you can use the command: ``R1# terminal length [number-of-lines]``  
:warning: Unfortunately, this command is NOT supported in Cisco Packet Tracer (tested on version 7.2.2).


### Important Switching ``show`` commands
Note that these commands are executed on privileged EXEC mode (``S1#`` prompt).  
You can execute them from global configuration mode (``S1(config)#`` prompt) by adding the ``do`` keyword before the command.  
example:  
``S1(config)#do show ip interface brief``  

Command|Description
---|---
``S1#show running-config``|N/A
``S1#show history``|
``S1#show interface [int-id]``|useful to detect errors or verify packets are being sent and received
``S1#show mac address-table``|
``S1#show port-security``|displays Port Security configuration for all interfaces
``S1#show port-security interface [int-id]``|display Port Security configuration of an interface
``S1#show vlan``|
``S1#show vlan brief``|**only** displays VLANs, statuses, names, and assigned ports
``S1#show interface vlan [id]``|
``S1#show interfaces trunk``|




## Configure basic Networking

| Command                                                         | Description                                              |
|:----------------------------------------------------------------|:---------------------------------------------------------|
| (config)# interface g1/0                                        | Enter their interface config mode                        |
| (config-if)# description Link to Somehost                       | Human readable link description                          |
| (config-if)# ip address 10.23.42.5 255.255.0.0                  | Add IPv4 address to interface.                           |
| (config-if)# mac address 1234.5678.90AB                         | Overwrite MAC address.                                   |
| (config-if)# no mac address                                     | Remove MAC overwrite.                                    |
| (config-if)# ipv6 address 2001:41d0:8:e115::ccc/64              | Add IPv6 address to interface.                           |
| (config-if)# ipv6 address 2001:41d0:8:e115::/64 eui-64          | Add IPv6 address based on MAC to interface.              |
| (config-if)# ip address dhcp                                    | Get IPv4 address via dhcp.                               |
| (config-if)# ipv6 address autoconfig [default]                  | Get IPv6 address [and default route] via autoconfig      |
| (config-if)# ip dhcp client client-id asccii SW2                | Set hostname transmitted as dhcp client to SW2           |
| (config)# interface g1/0 - 2                                    | Configure both interfaces at once.                       |
| (config-if)# [no] shutdown                                      | En- or Disable interface. Often shutdown is the default. |
| (config)# ip default-gateway 10.23.42.1                         | Set 10.23.42.1 as the default gateway                    |
| (config)# ip route 10.20.30.0 255.255.255.0 {1.2.3.4,e0/0} [ad] | Add static route via next hop or interface               |
| (config)# ipv6 route 2001:41d0:8:e115::/64 [g1/1] [next hop]    | Next hop is required for Ethernet interface in IPv6      |
| (config)# ip host the-space.agency 178.32.222.21                | Create a static host entry on this device.               |
| (config)# ipv6 unicast-routing                                  | Globally enable ipv6 routing.                            |

### Troubleshoot basic Networking

| Command                                 | Description                                              |
|:----------------------------------------|:---------------------------------------------------------|
| # show interfaces [if-name]             | Show interfaces mac, bandwidth, mtu, packet stats...     |
| # show ip[v6] route [static]            | Show routes and how they were learned.                   |
| # show ip[v6] interface [if-name]       | Show interfaces ip/arp/icmp/nd... configuration          |
| # show ip[v6] interface brief [if-name] | Only show ip, status and operational status              |
| # show protocols [if-name]              | Much like show ip int brief, w/ cidr, w/o ok/method      |
| # show mac address-table                | Show the mac address table of a switch.                  |
| # clear mac address-table [dynamic]     | Clear the dynamically learned mac address table entries. |
| # show arp                              | Show {ip,ipx,appletalk}-mac bindings                     |
| # show ip arp [{ip, mac, if-name}]      | Show ip-mac bindings                                     |
| # clear [ip] arp 192.168.1.1            | Remove arp entry for ip                                  |
| # debug arp                             | Show debug messages when receiving/sending arp packets   |
| # undebug all                           | Disable all previously enabled debugs                    |
| # show ipv6 neighbors                   | Show neighbor discovery table cache                      |
| # ping 1.2.3.4 [source g1/1]            |                                                          |
| # traceroute 1.2.3.4 [source g1/1]      |                                                          |
| # show control-plane host open-ports    | netstat -tulpn on this cisco device, basically           |


### Troubleshoot networks with SPAN

| Command                                                         | Description                    |
|:----------------------------------------------------------------|:-------------------------------|
| (config)# monitor session 23 source interface g1/1 {rx,tx,both} | Define SPAN #23 input as g1/1  |
| (config)# monitor session 23 destination interface g1/2         | Define SPAN #23 output as g1/2 |
| # show monitor                                                  | Show all configured SPANs      |

## Port Security

### :closed_lock_with_key: Configuring Dynamic Port Security
Command|Description
---|---
``S1(config)#interface [int-id]``|
``S1(config-if)#switchport mode access``|Set interface mode to *access*.
``S1(config-if)#switchport port-security``|Enable port security on the interface
``S1(config-if)#switchport port-security violation [violation-mode]``|set violation mode (``protect``, ``restrict``, ``shutdown``)

>:trophy: **Best practice:** It is a best security and general practice to "hard-type" the ``switchport mode access`` command. This also applies to Trunk ports (``switchport mode trunk``).

### :closed_lock_with_key: Configuring Sticky Port Security
Command|Description
---|---
``S1(config)#interface [int-id]``|
``S1(config-if)#switchport mode access``|Set interface mode to *access*.
``S1(config-if)#switchport port-security``|Enable port security on the interface
``S1(config-if)#switchport port-security maximum [max-addresses]``|Set maximum number of secure MAC addresses allowed on port
``S1(config-if)#switchport port-security mac-address sticky``|Enable sticky learning
``S1(config-if)#switchport port-security violation [violation-mode]``|set violation mode (``protect``, ``restrict``, ``shutdown``)

### :closed_lock_with_key: :white_check_mark: Verifying Port Security & secure MAC addresses
Now that we have configured Port Security, the following commands will be handy to verify and troubleshoot.

Command|Description
---|---
``S1#show port-security interface [int-id]``|displays interface's Port Security configuration. If violations occured, they can be checked here.
``S1#show port-security address``|displays secure MAC addresses configured on **all switch interfaces**
``S1#show interface [int-id] status``|displays port status. Useful to verify if an interface is in ``err-disabled`` status.

### Bringing an ``err-disabled`` interface back up

:bulb: Recall: After a violation, a port in **Shutdown violation mode** changes its status to *error disabled*, and is effectively **shut down**. To resume operation (sending and receiving traffic), we must bring it back up. Here's how:

* Access the interface configuration mode with ``S1(config)#interface [int-id]``.
* Shut the interface down using ``S1(config-if)#shutdown``.
* Bring the interface back up using ``S1(config-if)#no shutdown``.

| Command                                                          | Description                                         |
|:-----------------------------------------------------------------|:----------------------------------------------------|
| (config-if)# switchport mode {access, trunk}                     |                                                     |
| (config-if)# [no] switchport port-security                       | En/Disable port-security                            |
| (config-if)# switchport port-security maximum 1                  | Number of allowed MACs.                             |
| (config-if)# switchport port-security mac-address 1234.5678.9abc | Manually allow a MAC on this port.                  |
| (config-if)# switchport port-security mac-address sticky         | Allow learning of connected macs until mac reached. |
| (config-if)# switchport port-security violation shutdown         | Shutdown port when other device gets connected.     |
| (config-if)# shutdown  (config-if)# no shutdown                  | Reenable if after port-security violation.          |
| (config)# errdisable recovery cause psecure-violation            | Reenable if automatically after problem is fixed.   |
| (config)# errdisable recovery interval 42                        | Recheck every 42 seconds. (min 30, default 300)     |

Port-security violation terms

| Term       | Definition                                           |
|:-----------|:-----------------------------------------------------|
| protect    | Drops packets, no alert                              |
| restrict   | Drops packets, increments security-violation count   | 
| shutdown   | Shuts down the port (default)                        |

### Troubleshooting Port Security

| Command                               | Description                                            |
|:--------------------------------------|:-------------------------------------------------------|
| # show port-security [interface g1/1] | port status, violation mode, max/total MACs,...        |
| # show port-security address          | Secure MACs on ports.                                  |
| # show errdisable recovery            | Check if autorecovery is enabled. Disabled by default. |


## Virtual Local Area Network (VLAN)

Note: Even when a switch port is changed from access to trunk, its access vlan is maintained in the config.
When automatic trunk negotiation fails (e.g. because I unplug a link between to switches and put it into
my laptop) the configured access vlan becomes active once again and I might be able to reach network parts
I'm not supposed to. Always disable DTP / trunk auto negotiation.

### Configuring VLANs
Command|Description
---|---
``S1(config)#vlan [vlan-ID]``|create VLAN and assign its VLAN number
``S1(config-vlan)#name [someName]``| assign a name to the VLAN

Now it is time to assign ports to the newly created VLAN  

Command|Description
---|---
``S1(config)#interface [int-id]``|remember, ``interface range`` might be useful
``S1(config-if)#switchport mode access``|
``S1(config-if)#switchport access vlan [vlan-id]``|assign/change port VLAN

### Deleting a VLAN
Command|Description
---|---
``S1(config)#no vlan [vlan-id]``|:warning: deletes specified VLAN
``S1(config)#delete flash:vlan.dat``|:warning: erases **the whole VLAN database**

### Removing interface(s) from a VLAN
Command|Description
---|---
``S1(config)#interface [int-id]``|
``S1(config-if)#no switchport access vlan [vlan-id]``|remove the VLAN from the port

#### Know the difference!

>:bulb: When a VLAN is deleted. Any switchport assigned to that VLAN **becomes inactive**  
:bulb: On the other hand, when the ``no switchport access vlan [vlan-id]`` is executed on a switchport, the port will be returned to VLAN 1

### Configuring IEEE 802.1q trunk links
Command|Description
---|---
``S1(config)#interface [int-id]``|
``S1(config-if)#switchport mode trunk``|
``S1(config-if)#switchport trunk native vlan [vlan-id]``|
``S1(config-if)#switchport trunk allowed vlan [vlan-list]``|**All** allowed VLAN IDs.
``S1(config-if)#switchport trunk allowed vlan remove [vlan-id]``|:no_pedestrians: **PROHIBITS ONLY** the VLAN with the specified ID on the trunk interface

:bulb: Tip: You might also want to check out the router commands necessary for inter-VLAN-routing via [Router-On-A-Stick](https://github.com/r7perezyera/Cisco-IOS-Command-CheatSheets/blob/master/router_commands.md#configuring-Router-on-a-stick-inter-VLAN-routing)

### Dynamic Trunking Protocol (DTP)

This Cisco proprietary protocol contributes in the configuration of trunking interfaces between Cisco switches.

:bulb: Remember: The **default** configuration for interfaces on Cisco Catalyst 2960 and 3650 switches is _dynamic auto_.

Command|Description
---|---
``S1(config-if)#switchport mode trunk``|configures an interface to specifically be in **trunk mode**. Also negotiates to convert the neighboring link into a trunk.
``S1(config-if)#switchport mode access``|configures an interface to specifically be in **access mode**, a NON-trunk interface, even if its neighboring interface is in mode ``trunk``
``S1(config-if)#switchport mode dynamic auto``|interface will convert into a **trunk interface** if its neighboring interface is in **mode ``trunk`` or ``desirable`` ONLY**
``S1(config-if)#switchport mode dynamic desirable``|interface will convert into a **trunk interface** if its neighboring interface is in **mode ``trunk``, ``dynamic auto``, or ``dynamic desirable`` ONLY**
``S1(config-if)#switchport nonegotiate``|:no_entry: stops DTP negotiation, in which interfaces may engage, as you saw above, i.e.,  an interface will NOT change its mode even if the neighboring interface could change it through negotiation

### Troubleshooting VLANs
Command|Description
---|---
``S1#show vlan``|check whether a port belongs to the expected VLAN
``S1#show mac address-table``|check which addresses were learned on a particular port of the switch, and to which VLAN that port is assigned
``S1#show interfaces [int-id] switchport``|helpful in verifying an inactive VLAN is assigned to a port

### Troubleshooting Trunks
Command|Description
---|---
``S1#show interfaces trunk``|- check native VLAN id matches on both ends of link  - check whether a trunk link has been established between switches

### Voice VLANs

VLANs supporting voice traffic usually have quality of service (QoS). Voice traffic must have a *trusted* label.

>Note that the implementation of QoS is beyond the scope of the CCNA2 (version 6) course.

Command|Description
---|---
``S1(config)#interface [int-id]``|access interface on which the voice VLAN will be assigned
``S1(config-if)#switchport mode access``|
``S1(config-if)#switchport access vlan [vlan-id]``|
``S1(config-if)#mls qos trust cos``|set trusted state of an interface and indicate which packet fields are used to classify traffic
``S1(config-if)#switchport voice vlan [vlan-id]``|assign a voice VLAN to that port


### Layer2 Switch Vlan Config

| Command                                           | Description                                             |
|:--------------------------------------------------|:--------------------------------------------------------|
| (config)# [no] vlan 23                            | [delete vlan or] create vlan and enter config-vlan mode |
| (config-vlan)# name TelephoneSanitizer            | Name this vlan TelephoneSanitizer                       |
| (config)# int g1/1                                |                                                         |
| (config-if)# switchport mode access               | Make frames out this port untagged                      |
| (config-if)# switchport access vlan 23            |                                                         |
| (config)# int g1/2                                |                                                         |
| (config-if)# switchport mode trunk                | Make frames out this port tagged by default             |
| (config-if)# switchport trunk encapsulation dot1q | Sometimes the default is ciscos old isl.                |
| (config-if)# switchport trunk native vlan 256     | Except for vlan 256, which is still untagged.           |
| (config-if)# switchport nonegotiate               | Disable DTP                                             |

### Layer3 Switch Vlan Config

| Command                                       | Description                                |
|:----------------------------------------------|:-------------------------------------------|
| (config)# interface vlan 23                   | enter interface config mode                |
| (config-if)# ip address 1.2.3.4 255.255.255.0 | set device ip in vlan 23                   |
| (config-if)# no shutdown                      | virtual interfaces are disabled by default |
| (config-if)# int g                            |                                            |
| (config)# no vlan 23                          | delete vlan 23                             |

### Router (on a Stick) Vlan Config

| Command                                            | Description                                                      |
|:---------------------------------------------------|:-----------------------------------------------------------------|
| (config)# interface g1/1.10                        | Create subinterface g1/1.10 on g1/1                              |
| (config-subif)# encapsulation dot1q 10             | enable ieee 802.1Q vlan tagging with vlan 10 on the subinterface |
| (config-subif)# ip address 10.0.10.1 255.255.255.0 |                                                                  |
| # show vlans                                       | Show vlans and their trunk interfaces                            |


### Troubleshoot Vlans on a switch

| Command                                                | Description                             |
|:-------------------------------------------------------|:----------------------------------------|
| # show vlan [{id 23, name TelephoneSanitizer}] [brief] | Show vlan settings for all switch ports |
| # show interfaces g1/1 switchport                      | Verify mode and vlan of g1/1            |
| # show interfaces g1/1 trunk                           | Show trunk settings and state           |
| # show run interface vlan 1                            | Quick way to search the running config. |
| # show interface status                                | Show trunk mode / access vlan           |
| # show dtp interface g1/1                              | Show current DTP mode for g1/1          |


## VLAN trunking protocol (VTP)

Command|Description
---|---
``S1(config)#vtp mode [mode]``|mode can be ``server`` or ``client``
``S1(config)#vtp password [password]``|optional - :warning: password is case-sensitive
``S1(config)#vtp domain [name]``|optional - :warning: domain name is case sensitive as well
``S1(config)#vtp pruning``|optional - configure VTP pruning on server
``S1(config)#vtp version 2``|optional - enables VTP version 2

:heavy_exclamation_mark: After this, remember to enable trunk links between the *VTP domain* switches so *VTP advertisements* can be shared among the switches.
This command sequence is all that's needed to get VTP running on our *VTP domain* :white_check_mark:

:bulb: Tip: There are 3 VTP versions. Versions 1 and 2 (which are within the scope of the CCNA exam) **DO NOT** support *extended-range VLANS* (ID from 1006 to 4095). VTP version 3 (NOT covered on the CCNA exam) does support such VLANS.

### VTP verification

Command|Description
---|---
``S1#show vtp status``|verify your configuration and the status of VTP on the device
``S1#show vtp password``|verify the configured VTP password
``S1#show vlan brief``|this VLAN verification command might be useful as well when verifying VTP configuration

| Command                                          | Description |
|:-------------------------------------------------|:------------|
| (config)# vtp mode [server, client, transparent] |             |
| (config)# vtp domain <domain-name>               |             |
| (config)# vtp password <password>                |             |
| (config)# vtp pruning                            |             |


### Troubleshoot VTP

| Command           | Description                             |
|:------------------|:----------------------------------------|
| show vtp status   | show vtp domain, pruning, mode and more |
| show vtp password |                                         |


## Spanning Tree Protocol (STP)

- Spaning Tree Protocol (802.1D) blocks ports with redundant links to prevent layer 2 loops and broadcast storms.
	
### Bridge ID configuration
Command|Description
---|---
``S1(config)#spanning-tree vlan [vlan-id] root primary``|ensures this switch has the lowest priority value
``S1(config)#spanning-tree vlan [vlan-id] root secondary``|Use if the configuration of an alternative bridge is desired. Sets the switch priority value to ensure it becomes the root bridge if the primary root bridge fails.
``S1(config)#spanning-tree vlan [vlan-id] priority [priority]``|manually configure the bridge's priority value

:bulb: Recall: priority values are between 0 and 61,440.  
:warning: The priority value can only be a multiple of 4096

### Bridge ID Verification
Command|Description
---|---
``S1#show spanning-tree``|verify current spanning-tree instances and root bridges
### PortFast and BPDU guard
Must only be configured on interfaces connected point-to-point to an end device

Command|Description
---|---
``S1(config)#interface [int-id]``|access the interface
``S1(config)#interface range [int-type][lowest-id]-[highest-id]``|access a range of contiguous interfaces if necessary
``S1(config-if)#switchport mode access``|as a good practice, hard-type this command so the switchport is in access mode
``S1(config-if)#spanning-tree portfast``|enables PortFast on the access port(s)
``S1(config-if)#spanning-tree bpduguard enable``|enables BPDU Guard on the access port(s)
``S1(config)#spanning-tree portfast default``|:warning: configures PortFast to be the default for all switch interfaces
``S1(config)#spanning-tree bpduguard default``|:warning: configures BPDU Guard to be the default for all switch interfaces

### PortFast and BPDU guard verification

Command|Description
---|---
``S1#show running-config | begin spanning-tree``|display spanning tree features configured on the switch
``S1#show running-config interface [int-id]``|display the current configuration portion corresponding to the interface


### Configuring Rapid PVST+

PVST+ is the STP flavor operating by default on Cisco switches.
To configure Rapid PVST+, we just need to type a global command.  

Command|Description
---|---
``S1(config)#spanning-tree mode rapid-pvst``|configure Rapid PVST+ as the STP mode on the switch
``S1(config-if)#spanning-tree link-type point-to-point``|specify that a link is point-to-point
``S1#clear spanning-tree detected-protocols (interface [int-id])``|forces renegotiation with neighboring switches on all interfaces or the specified interface

### General STP verification commands

Command|Description
---|---
``S1#show spanning-tree``|display STP information - useful to find information about the bridge you are in, and the root bridge at a glance
``S1#show spanning-tree active``|display STP information for active interfaces only
``S1#show spanning-tree brief``|at-a-glance information for all STP instances running on the switch
``S1#show spanning-tree detail``|detailed information for all STP instances running on the switch
``S1#show spanning-tree interface [int-id]``|STP information for the specified interface
``S1#show spanning-tree vlan [vlan-id]``|STP information for the specified VLAN
``S1#show spanning-tree summary``|summary of STP port states	

| Command                                                  | Description                                          |
|:---------------------------------------------------------|:-----------------------------------------------------|
| (config)# spanning-tree vlan 1 root {primary, secondary} | Make this device the primary/secondary root bridge.  |
| (config)# spanning-tree portfast bpduguard default       | Enable bpdu guard for all portfast enable interfaces |
| (config)# spanning-tree portfast default                 | Enable portfast for all non-trunk interfaces         |
| (config-if)# spanning-tree bpduguard enable              | Enable gpduguard on this interface                   |
| (config-if)# spanning-tree portfast                      | Enable portfast on this interface                    |
| (config-if)# spanning-tree guard root                    | Enable root guard on this interface                  |

### Troubleshoot STP

| Command                                      | Description                                         |
|:---------------------------------------------|:----------------------------------------------------|
| # show spanning-tree [vlan 1]                | Who's the root and how do I get there?              |
| # show spanning-tree summary                 | Is global portfast/bpduguard configured?            |
| # show running-config interface g1/1         | Is portfast/bpduguard configured on this interface? |
| # show spanning-tree interface g1/1 portfast | Is portfast active on this interface?               |

### RSTP
Rapid Spanning Tree Protocol (802.1w) reduces convergence time after a topology change compares to STP.

| Command                                       | Description                          |
|:----------------------------------------------|:-------------------------------------|
| (config)# spanning-tree mode rapid-pvst       | Change spanning-tree mode to RSTP    |




🚧🚧🚧
	
## EtherChannel (Link Aggregation) 🔛 ➕ 

Command|Description
---|---
``S1(config)#interface range [start-int]-[end-int]``|start by selecting the interfaces to be bundled into a **single logical link**, i.e., the EtherChannel.
``S1(config-if-range)#channel-group [number] mode [mode]``|specify the group ID (``1`` to ``6``, inclusive) and [operation mode](#available-etherchannel-modes) of the EtherChannel
``S1(config)#interface port-channel [number]``|enter the **port channel interface configuration mode** to change settings

### PortChannel interface additional configuration
Command|Description
---|---
``S1(config-if)#switchport mode trunk``|set the interface in trunking mode, so it can carry traffic of multiple VLANs
``S1(config-if)#switchport trunk native vlan [native-vlan-id]``|specify the link's native VLAN
``S1(config-if)#switchport trunk allowed vlan [vlan-id-1 (,vlan-id-2,...)]``|specify allowed VLANs (VLAN IDs) on trunk link
``S1(config-if)#switchport trunk allowed vlan add [vlan-id-1 (,vlan-id-2,...)]``|**add** VLANs to the list of **already allowed** VLANs on the trunk link

:warning: The **EtherChannel negotiation protocols** you use for your interface bundles **MUST MATCH ON BOTH ENDS**, whether it is LACP, PAgP (Cisco Proprietary), or no protocol (``on`` mode).

#### Available EtherChannel modes
EC mode|Description
---|---
``active``|Enable LACP unconditionally
``auto``|Enable PAgP only if another PAgP device is detected.
``desirable``|Enable PAgP unconditionally
``on``|Enable EtherChannel only
``passive``|Enable LACP only if another LACP device is detected

	
How to set LACP? TODO:
Look at modes again


| Command                                                       | Description                                    |
|:--------------------------------------------------------------|:-----------------------------------------------|
| (config)# interface range g1/1 - 2                            | configure g1/1 and g1/2 at the same time       |
| (config-if-range)# channel-group 1 mode {auto, desirable}     | Add both interfaces to etherchannel 1 (PAgP)   |
| (config-if-range)# channel-group 1 mode {active, passive}     | Add both interfaces to etherchannel 1 (LACP)   |
| (config-if-range)# channel-group 1 mode on                    | Add both interfaces to etherchannel 1 (Static) |
| (config)# interface port-channel 1                            | Configure virtual interface for etherchannel 1 |
| (config-if)# switchport mode trunk                            | Put etherchannel 1 in trunk mode               |
| (config-if)# switchport trunk allowed vlan 10,20,30           | Add tagged vlans 10,20,30 on ethercahnnel 1    |



### Troubleshoot Etherchannel (Link Aggregation)

| Command                            | Description                                           |
|:-----------------------------------|:------------------------------------------------------|
| # show interface port-channel 1    | Has the combined bandwidth and members as extra info. |
| # show etherchannel summary        | Show etherchannel protocols and members as a list     |
| # show etherchannel port-channel 1 | Show per member state and stats                       |

[Back to beginning of section](#etherchannel)

	
## Configure a Serial
Layer 1 link speed is dictated by a CSU/DSU, in a lab without an external CSU/DSU a DTE (Data Terminal Equipment) cable and DCE (Data Communications Equipment) cable are used.

| Command                                 | Description                                     |
|:----------------------------------------|:------------------------------------------------|
| (config)# interface serial 1/0          | Configure interface serial 1/0                  |
| (config-if)# clock rate 128000          | Set clock rate on DCE router side to 128 kbps   |
| (config)# show controllers serial 1/0   | Verify clock rate for serial interface 1/0      |


## ACLs

\#1-#99, #1300-#1999: Standard IPv4 ACL

\#100-#199, #2000-#2699: Extended IPv4 ACL

Default mask for standard ACLs: 0.0.0.0

| Command                                                    | Description                                               |
|:-----------------------------------------------------------|:----------------------------------------------------------|
| (config)# access-list 23 permit 1.2.3.4 [0.0.255.255]      | Create ACL #23 or append a rule to ACL #23, allow 1.2.x.x |
| (config)# no access-list 23                                | Delete entire ACL #23                                     |
| (config)# ip[v6] access-list resequence local_only 5 10    | Renumber ACL Rules, put first on #5, increment by 10.     |
| (config)# ip access-list {standard, extended} 23           | Create ACL and/or enter config mode for ACL #23           |
| (config)# ip access-list {standard, extended} local_only   | Create ACL and/or enter config mode for ACL 'local_only'  |
| (config-std-nac1)# permit 10.20.30.0 0.0.0.255             | Append rule to standard ACL 'local_only'                  |
| (config-std-nac1)# 5 permit 10.20.30.0 0.0.0.255           | Append rule to ACL at sequence number 5.                  |
| (config-std-nac1)# no <sequence#>                          | Remove rule with sequence# from ACL                       |
| (config-ext-nac1)# deny tcp any any                        |                                                           |
| (config-ext-nac1)# permit udp host 10.20.30.40 any lt 1024 |                                                           |
| (config-ext-nac1)# permit udp host 10.20.30.40 any eq dns  |                                                           |
| (config-ext-nac1)# deny udp host 10.20.30.40 any           |                                                           |
| (config-ext-nac1)# permit ip any any                       |                                                           |

### Interface ACLs

| Command                                          | Description                                                               |
|:-------------------------------------------------|:--------------------------------------------------------------------------|
| (config)# inter g1/1                             | Enter if-config mode for g1/1                                             |
| (config-if)# ip access-group 23 out              | Apply ACL #23 to outgoing packets, not send by the router                 |
| (config-if)# ip access-group 42 in               | Apply ACL #42 to incoming packets                                         |
| (config-if)# ip access-group local_only in       | Overwrite the used ACL, only one ACL per if + proto + direction!          |
| (config-if)# ipv6 traffic-filter 23 out          | The v6 syntax of course differs...                                        |
| # show ip interface g1/1 &#124; incl access list | Show ACLs on g1/1 (When none set shows not set for v4 and nothing for v6) |

### Troubleshooting ACLs

| Command                      | Description                                              |
|:-----------------------------|:---------------------------------------------------------|
| # show [ip[v6]] access-lists | Show all configured ACLs                                 |
| # show access-list 10        | Display all rules in ACL #10 and how often they matched. |


## NAT

Local addresses are any address as it appears inside the network. Global addresses are any address as it appears outside the network.

| Term           | Definition                                                                   |
|:---------------|:-----------------------------------------------------------------------------|
| inside local   | IP address assigned to a host inside the network, non-routable               |
| inside global  | IP address assigned by Network Information Center or ISP, routable           |
| outside local  | IP address of a remote host as it appears inside the network, non-routable   |
| outside global | IP address of a  remote host assigned by the host owner, routable            |

| Command                                          | Description                                                          |
|:-------------------------------------------------|:---------------------------------------------------------------------|
| (config)# int g1/1                               | Enter if-config mode for g1/1                                        |
| (config-if)# ip address 1.2.3.4 255.255.255.240  | configure 1.2.3.4/28 on g1/1                                         |
| (config-if)# ip nat outside                      | Packets going out, need to change their src, incoming their dest ip. |
| (config)# int g1/2                               | Enter if-config mode for g1/2                                        |
| (config-if)# ip address 10.10.23.1 255.255.255.0 | configure 10.10.23.1/24 on g1/2                                      |
| (config-if)# ip nat inside                       | Packets going out, need to change their dest, incoming their src ip. |


### SNAT

| Command                                                  | Description                                                 |
|:---------------------------------------------------------|:------------------------------------------------------------|
| (config)# ip nat inside source static 10.10.23.2 1.2.3.5 | SNAT - statically map an internal ip 1:1 to an external ip. |

### DNAT

| Command                                                             | Description                                                  |
|:--------------------------------------------------------------------|:-------------------------------------------------------------|
| (config)# access-list 42 permit 10.10.23.0 0.0.0.255                | Create an ACL identifying 10.10.23/24                        |
| (config)# ip nat pool POOL 1.2.3.5 1.2.3.10 netmask 255.255.255.240 | Create an IP Address Pool for NATing                         |
| (config)# ip nat inside source list 42 pool POOL                    | DNAT IPs matching ACL #42 1:1 with IPs from nat pool 'POOL'. |

Note the missing overload.

### PAT

The overload keyword means, that one or a couple of external IPs are to be used for multiple
internal IPs. Higher level information like connection port numbers are used to identify the
correct internal destination for incoming packets. Cisco calls this PAT, while this is what your
average joes home router would call NAT.

| Command                                                        | Description                                          |
|:---------------------------------------------------------------|:-----------------------------------------------------|
| (config)# access-list 10 permit 10.10.0.0 0.0.255.255          | Create an ACL identifying 10.10/16                   |
| (config)# ip nat inside source list 10 interface g1/1 overload | PAT IPs matching ACL #10 many:1 with g1/1s public IP |


### Troubleshooting NAT

| Command                            | Description                                                                     |
|:-----------------------------------|:--------------------------------------------------------------------------------|
| # show ip nat translations         | Show nat table entries if any                                                   |
| # show ip nat statistics           | Show translations are actually used and interfaces are marked in/out correctly. |
| # clear ip nat translation {ip, *} | Clear dynamic translations. Doesn't mess with SNAT!                             |
| # debug ip nat [detailed]          |                                                                                 |

Is the ACL correct? Is there a route to the address?
Note: NAT Table entries are kept for 24h after the last use by default.

## DHCP Server

| Command                                                  | Description                                            |
|:---------------------------------------------------------|:-------------------------------------------------------|
| (config)# ip dhcp excluded-address 10.30.4.1 10.30.4.100 | Don't distribute these IPs in leases                   |
| (config)# ip dhcp pool PCs                               | Creat and/or enter dhcp config for pool 'PCs'          |
| (dhcp-config)# network 10.30.4.0 /24                     | define pool addresses                                  |
| (dhcp-config)# default-router 10.2.1.1                   | define default-gateway to be distributed in the leases |
| (dhcp-config)# dns-server 10.30.4.1                      |                                                        |
| (dhcp-config)# domain-name acme.com                      |                                                        |
| (dhcp-config)# lease <days> <hours> <mins>               | lease validity time                                    |
| (config)# int g1/1                                       | Enter interface config mode on client facing interface |
| (config-if)# ip helper-address 192.168.1.1               | Relay DHCP Requests to this host                       |


### Troubleshooting DHCP

| Command                       | Description                                           |
|:------------------------------|:------------------------------------------------------|
| # debug ip dhcp server packet |                                                       |
| # show dhcp lease             | Show dhcp lease information                           |
| # show ip dhcp pool           | Show pool size and addresses in use                   |
| # show ip dhcp binding        | Show which mac got which ip                           |
| # sh run &#124; section dhcp  | See if ip dhcp exclude-address / pool stuff is wrong. |
| # sh run int g1/1             | See if ip helper-address is wrong.                    |


## HSRP

| Command                                             | Description                                                      |
|:----------------------------------------------------|:-----------------------------------------------------------------|
| (config-if)# standby [group-number] ip <ip>         | Join HSRP Group                                                  |
| (config-if)# standby [group-number] priority <prio> | (optional) Set prio of this router.                              |
| (config-if)# standby [group-number] preempt         | (optional) Preempt other routers when this router becomes active |
| (config-if)# standby {1,2}                          | (optional) Set HSRP Version                                      |

### Troubleshooting HSRP

| Command        | Description                                                                |
|:---------------|:---------------------------------------------------------------------------|
| # show standby | HSRP Groups, their VIPs, state, active router, standby router, preemption. |


## SLAs

| Command                                                             | Description                                       |
|:--------------------------------------------------------------------|:--------------------------------------------------|
| (config)# ip sla 23                                                 | Create ip sla test #23 and enter its config mode. |
| (config-ip-sla)# icmp-echo 1.2.3.4                                  | Define icmp-echo test.                            |
| (config-ip-sla)# frequency 42                                       | frequency in seconds.                             |
| (config)# ip sla schedule 23 life {forever, seconds} start-time now | Start test #23 now and until manually stopped.    |

### Troubleshooting SLAs

| Command                     | Description                        |
|:----------------------------|:-----------------------------------|
| # show ip sla configuration | Show all configured ip sla configs |
| # show ip sla statistics    | Show sla results                   |


## Device Management

| Command                               | Description                                                                  |
|:--------------------------------------|:-----------------------------------------------------------------------------|
| (config)# hostname R1                 | Set hostname to R1                                                           |
| (config)# enable password <password>  | Set enable passwort.                                                         |
| (config)# enable secret <password>    | Same, but with hashing.                                                      |
| (config)# service password-encryption | Very weak encryption of passwords passwords.                                 |
| # copy flash0: tftp:                  | Copy something from flash to tftp. Wizard asks for details. Works both ways. |
| # write                               | # copy running-config startup-config                                         |
| # write erase                         | # erase startup-config                                                       |
| # reload                              | restart the device and load the startup-config                               |
| # copy running-config tftp:           | copy running-config to an tftp server. (interactive)                         |
| # copy <any> running-config           | Merge source config into the running config.                                 |
| # setup                               | initial configuration dialog                                                 |
| # show version                        | ios, bootloader and hardware infos, uptime, configuration register           |
| # show {running,startup}-config       |                                                                              |

### Firmware Management

Note: flash: is the main flash memory on all iOS devices

| Command                                               | Description                                                   |
|:------------------------------------------------------|:--------------------------------------------------------------|
| (config)# boot system flash:filename.bin              | Boot filename.bin from flash memory.                          |
| (config)# boot system tftp://10.20.30.40/filename.bin | Boot filename.bin from tftp.                                  |
| (config)# boot system rom                             | Boot ROM monitor as a backup.                                 |
| (config)# config-register 0x2342                      | Set the 16bit Configuration Register value used after reboot. |
|                                                       |                                                               |
| # show file systems                                   | Lists available file systems                                  |
| # show flash0:                                        | List fs content and free space.                               |

### License Management

| Command                                                                       | Description                                              |
|:------------------------------------------------------------------------------|:---------------------------------------------------------|
| # license save flash:licenses.lic                                             | Save a copy of all licenses.                             |
| # license install flash0:license.xml                                          | Install a license.                                       |
| (config)# license boot module <name> technology-package <pkg-name>            | active a evaluation right-to-use license.                |
| # reload                                                                      | Reboot to activate the package and right to use license. |
|                                                                               |                                                          |
| (config)# license boot module <name> technology-package <pkg-name> disable    | deactive a technology-package.                           |
| # reload                                                                      | Reboot without that technology-package.                  |
| # license clear <pkg-name>                                                    | Remove license from the license storage.                 |
| (config)# no license boot module <name> technology-package <pkg-name> disable | Remove the no longer needed line from the config.        |
| # reload                                                                      | I don't even know why this is needed. Fu cisco.          |
|                                                                               |                                                          |
| # show license                                                                | active licenses                                          |
| # show license feature                                                        | technology packe and feature licenses supported.         |
| # show license udi                                                            | product id and serial number needed to order licenses    |


### Reset Password

| Command                          | Description                                                            |
|:---------------------------------|:-----------------------------------------------------------------------|
| > confreq                        | Show the configuration register in rom monitor                         |
| > confreq 0x2142                 | Set the configuration register in rom monitor to not load startup-conf |
| > reset                          | Reboot in rom monitor                                                  |
| # copy startup running           |                                                                        |
| (config)# enable secret foobar   | Overwrite forgotten password                                           |
| (config)# config-register 0x2102 | Do load startup-config after boot again.                               |
| # save                           |                                                                        |


### Telnet / Console

| Command                                        | Description                                                 |
|:-----------------------------------------------|:------------------------------------------------------------|
| (config)# banner login "Insert snarky banner." | Make sure to include legal terms to sound smart.            |
| (config)# banner motd "Insert snarky banner."  | Set Login Banner.                                           |
| (config)# line vty 0 4                         | Enter config mode for vty 0 to 4 (up to 15 allowed).        |
| (config)# line console 0                       | Enter config mode for the console port                      |
| (config-line)# login                           | Require login on telnet/console connection.                 |
| (config-line)# password <password>             | Enable Telnet and set vty login password.                   |
| (config-line)# access-class 10 in              | Set ACL to limit inbound IPs allowed to access vty          |
| (config-line)# access-class 42 in              | Overwrite the used ACL, only one ACL per vty + direction!   |
| (config-line)# exec-timeout 10                 | Autologout after 10 Minutes                                 |
| (config-line)# login local                     | Require login on telnet/console connection via local users. |
| (config)# username h.acker secret C1sco123     | Create local user with encrypted password.                  |


## Secure Shell (SSH)
Command|Description
---|---
``S1#show ip ssh``|Use it to verify that the switch supports SSH
``S1(config)#ip domain-name [domain-name]``|
``S1(config)#crypto key generate rsa``|
``S1(config)#username [admin] secret [ccna]``|
``S1(config)#line vty 0 15``|
``S1(config-line)#transport input ssh``|
``S1(config-line)#login local ``|
``S1(config-line)#exit``|
``S1(config)#ip ssh version 2``|enable SSH version 2
``S1(config)#crypto key zeroise rsa``|:warning: use to **delete** RSA key pair

### Modifying SSH configuration
Command|Description
---|---
``S1(config)#ip ssh time-out [time]``|Change timeout setting (time in seconds)
``S1(config)#ip ssh authentication-retries [retries]``|Change number of allowed authentication attempts

- Verify your newly configured settings with ``S1#show ip ssh``	
	
	
| Command                                        | Description                                              |
|:-----------------------------------------------|:---------------------------------------------------------|
| (config)# hostname Foobar                      | Required to generate SSH keys.                           |
| (config)# ip domain-name example.com           | Required to generate SSH keys.                           |
| (config)# crypto key generate rsa modulus 2048 | Generate keys like it's 1995! Potentially takes forever. |
| (config)# ip ssh version 2                     | Force SSHv2                                              |
| (config-line)# transport input ssh             | Force ssh, disable telnet.                               |
| # show ip ssh                                  | SSH version, timeout time, auth retries..                |
| # show ssh                                     | List of active connections                               |

### Clock

| Command                                  | Description                    |
|:-----------------------------------------|:-------------------------------|
| # show clock                             | Show time and date             |
| (config)# clock set 23:50:42 10 Jan 2017 | Update clock                   |
| (config)# clock timezone EST 0           | Update timezone to EST         |
| (config)# ntp server 10.20.30.40         | Configure upstream ntp server. |
| (config)# ntp master [stratum]           | Enable ntp server.             |
| # show ntp associations                  | ntp connections.               |
| # show ntp status                        | synchronized?, statum, ...     |

### Disable unused services

| Command                              | Description                           |
|:-------------------------------------|:--------------------------------------|
| # show control-plane host open-ports | Show open ports                       |
| (config)# no ip http server          | Stop the http server (but not https). |
| (config)# no cdp enable              | Stop CDP                              |
| # auto secure                        |                                       |

### Radius

| Command                                                         | Description                          |
|:----------------------------------------------------------------|:-------------------------------------|
| (config)# username <user> password <pass>                       | Local backup user.                   |
| (config)# aaa new-model                                         | Enable aaa services.                 |
| (config)# radius server <radius-conf-name>                      | Add and define Radius conf.          |
| (config-radius-server)# address ipv4 <host> [auth-port <port> ] | Use this hostname/ip of server.      |
| (config-radius-server)# key <key>                               | Radius PSK                           |
| (config)# aaa group server radius <group-name>                  | Create authentication group.         |
| (config-sg-radius)# server name <radius-conf-name>              | Using the radius config.             |
| (config)# aaa authentication login group <group-name> local     | Allow that group and local users in. |


### TACACS+

| Command                                                     | Description                          |
|:------------------------------------------------------------|:-------------------------------------|
| (config)# username <user> password <pass>                   | Local backup user.                   |
| (config)# aaa new-model                                     | Enable aaa services.                 |
| (config)# tacacs server <tacacs-conf-name>                  | Add and define TACACS conf.          |
| (config-server-tacacs)# address ipv4 <host>                 |                                      |
| (config-server-tacacs)# [port <port>]                       |                                      |
| (config-server-tacacs)# key <key>                           |                                      |
| (config)# aaa group server tacacs+ <group-name>             | Multiple possible.                   |
| (config-sg-tacacs+)# server name <tacacs-conf-name>         |                                      |
| (config)# aaa authentication login group <group-name> local | Allow that group and local users in. |


### Syslog

| Command                      | Description                                    |
|:-----------------------------|:-----------------------------------------------|
| # logging 10.20.30.40        | Log to this syslog server (name or ip)         |
| # logging trap informational | Only log messages with min. informational sev. |

service sequence-number | Needed for seqence number in syslog messages
service time stamps log [datetime, log] | Needed for date and time in syslog messages

| Command        | Description                         |
|:---------------|:------------------------------------|
| # show logging | syslog status, local logging buffer |


### SNMP

| Command                                           | Description                  |
|:--------------------------------------------------|:-----------------------------|
| (config)# snmp-server contact admin@example.com   | Contact email                |
| (config)# snmp-server location RZ-Hamburg         | Where is the device          |
| (config)# snmp-server community <string> [ro, rw] | Add community                |
| (config)# snmp-server host 10.20.30.40 <string>   | SNMP notifications recipient |

| Command               | Description |
|:----------------------|:------------|
| # show snmp community |             |
| # show snmp location  |             |
| # show snmp contact   |             |
| # show snmp host      |             |


### CDP - Cisco Discovery Protocol

| Command                        | Description                                                     |
|:-------------------------------|:----------------------------------------------------------------|
| # [no] cdp run                 | Enables cdp globaly and on all interfaces (default)             |
| # (config-if)# [no] cdp enable | Enable cdp on an interface                                      |
| # show cdp neighbors [detail]  | List connected cisco devices (name, local/remote port, [ip] ..) |
| # show cdp entry *             |                                                                 |

### LLDP - Link Layer Discovery Protocol

| Command                         | Description                                  |
|:--------------------------------|:---------------------------------------------|
| # [no] lldp run                 | Enables lldp globaly and on all interfaces   |
| (config-if)# [no] lldp transmit | Enable lldp packet transmission on interface |
| (config-if)# [no] lddp receive  | Enable lldp packet reception on interace     |


## PPP

| Command                                                   | Description                                       |
|:----------------------------------------------------------|:--------------------------------------------------|
| (config)# username fnord password pass                    | Create users for pap auth.                        |
| (config)# inteface S0/0/0                                 |                                                   |
| (config-if)# clock rate 125000                            | Baud rate. Only on DCE cable!                     |
| (config-if)# bandwidth 125                                | Logical speed used for routing cost calc, RSVP... |
| (config-if)# encapsulation ppp                            | Default is HDLC                                   |
| (config-if)# ppp authentication pap                       | Require remote to authenticate via pap            |
| (config-if)# ppp pap sent-username fnord password pass    | Authenticate to remote pap                        |
|                                                           |                                                   |
| (config)# hostname routy1                                 | Required for CHAP, used as chap client username   |
| (config)# username routy2 password foobar                 | Create users for chap auth for routy2             |
| (config)# inteface S0/0/0                                 |                                                   |
| (config-if)# no ppp authentication pap                    | Remove in favor of chap                           |
| (config-if)# no ppp pap sent-username fnord password pass | Remove in favor of chap                           |
| (config-if)# ppp authentication chap                      | Require remote to authenticate via chap           |

Note: When routy1 connects to routy2 it looks in it's local user database for a user named routy2 and uses that users password. This means the passwords have to be the same on both sides and the usernames must be the other sides hostname.


### Troubleshooting PPP

| Command                    | Description                                    |
|:---------------------------|:-----------------------------------------------|
| # show controllers S0/0/0  | interface, connected type of cable, clock rate |
| # show interfaces          | encapsulation, logical bandwidth               |
| # show ppp all             | session state, auth type, peer ip and name     |
| # debug ppp authentication |                                                |

### MLP

| Command                                           | Description                      |
|:--------------------------------------------------|:---------------------------------|
| (config)# interface Multilink23                   | Create and configure virtual if  |
| (config-if)# ip address 10.20.30.40 255.255.255.0 |                                  |
| (config-if)# ppp multilink                        | Enable mlp                       |
| (conifg-if)# ppp multilink group 23               | Make phys ifs with mlp #23 join. |
| (config)# interface s0/0/0                        | Configure phys ifs               |
| (config-if)# no ip address                        | Remove ip addrs.                 |
| (config-if)# encapsulation ppp                    |                                  |
| (config-if)# ppp multilink                        |                                  |
| (config-if)# ppp multilink group 23               | Join mlp group #23.              |

#### Troubleshooting MLP

| Command            | Description   |
|:-------------------|:--------------|
| show ppp multilink | Physical IFs, |

### PPPoE

| Command                                       | Description                                                 |
|:----------------------------------------------|:------------------------------------------------------------|
| (config)# interface Dialer23                  | Create and configure virtual dialer interface.              |
| (config-if)# ip address negotiated            | Get IP via PPP/IPCP                                         |
| (config-if)# encapsulation ppp                |                                                             |
| (config-if)# dialer pool 23                   | The dialer interface is a member of one dialer pool...      |
| (config)# interface s0/0/0                    |                                                             |
| (config-if)# no ip address                    |                                                             |
| (config-if)# pppoe-client dial-pool-number 23 | ... the pool is a group of one or more physical interfaces. |

#### Troubleshooting PPPoE

| Command                   | Description                                               |
|:--------------------------|:----------------------------------------------------------|
| # show ip interface brief | is the dialer if up? Does the dialer have an IP via IPCP? |
| # show pppoe session      | Are PPPoE sessions established? Which ports.              |


## GRE

Note: We can run OSPF and other routing protocols through this gre tunnel, as gre supports multicast.

| Command                                           | Description              |
|:--------------------------------------------------|:-------------------------|
| (config)# interface tunnel23                      |                          |
| (config-if)# ip address 192.168.1.1 255.255.255.0 | transit net              |
| (config-if)# tunnel source 10.20.30.40            | local, can be linklocal  |
| (config-if)# tunnel destination 6.5.4.3           | remote, can be linklocal |

tunnel mode gre ip
ip mtu

### Troubleshooting GRE

| Command                            | Description                                           |
|:-----------------------------------|:------------------------------------------------------|
| # show ip interface brief tunnel23 | Line hould be up, given a route to the destination.   |
| # show inteface tunnel23           | Tunnel source, dest, protocol                         |
| # show ip route                    | Should include the transit net as directly connected. |


## RIPv2

| Command                                                             | Description                                             |
|:--------------------------------------------------------------------|:--------------------------------------------------------|
| (config)# router rip                                                | Enable RIP and enter it's config mode                   |
| (config-router)# version 2                                          | Set RIPv2, which is Classless                           |
| (config-router)# network 192.168.0.0                                | Advertise connected networks which are within <net>.    |
| (config-router)# network 0.0.0.0                                    | Advertise all connected networks.                       |
| (config-router)# timers basic <update> <invalid> <holddown> <flush> |                                                         |
| (config-router)# no auto-summary                                    | Don't summarize a smaller subnet route in a bigger one. |
| (config-router)# passive-interface g1/1                             | Don't send RIP updates out this interface               |
| (config-router)# passive-interface default                          | Don't send RIP updates on any if by default             |
| (config-router)# no passive-interface g1/2                          | Overwrite passive-interface default                     |
| (config-router)# default information originate                      | Advertise the default route.                            |
| (config-if)# no ip rip advertise 123                                |                                                         |

### Troubleshooting RIPv2

| Command                 | Description                                              |
|:------------------------|:---------------------------------------------------------|
| # show ip[v6] protocols | Show rip timers, interfaces, networks,                   |
| # show ip rip database  | Routes learned by rip, used to combile the routing table |
| # show ip route         | Show learned routes                                      |
| # clear ip route *      | Get rid of all routes                                    |


## Dynamic routing: Enhanced Interior Gateway Routing Protocol (EIGRP) 

### EIGRP Configuration
Command|Description
---|---
``R1(config)#router eigrp [AS-number]``|[AS-number] value range: 1-65535.
``R1(config-router)#eigrp router-id [a.b.c.d]``|(optional) manually configure a **router ID**, in an IPv4 address format
``R1(config-router)#network [network-address]``|add the classful network address for each directly connected network
``R1(config-router)#network [network-address] ([wildcard-mask])``|add the network address with the wildcard mask, recommended when using classless addresing


- 💡 If no EIGRP router ID is configured, the router will use the highest IPv4 address of any active loopback interface. 
    - If the router has NO active loopback interfaces, the router ID will be the highest IPv4 address of any active physical interface.

- 👑 **Pro Tip:**

    - How can I easily visualize all the directly connected networks a router has? Using:
	
        - **``R1(config)# do show ip route con``** 

    - It will display the routing table ONLY with the directly connected networks (routes).

- 💡 Recall: by default, EIGRP does NOT automatically summarize networks.

### EIGRP Verification
Command|Description
---|---
``R1#show ip protocols``|verifies the current configured values for EIGRP (and any additional enabled routing protocol on the device)
``R1#show ip eigrp neighbors``|displays the nighbor table. Use it to verify the router recognizes its neighbors.
``R1#show ip route eigrp``|display **only EIGRP** entries in the routing table
``R1#show ip eigrp interface``|verifies which interface are enabled for EIGRP, number of peers, and transmit queues

:bulb: Recall: (internal) EIGRP's default AD is ``90``  
You can find common AD values [here](#appendix-common-administrative-distance-ad-values).
- _The AD for an **EIGRP summary route** is 5._
- _The AD for an **EIGRP external route** is 170._

### EIGRP Fine tuning
Command|Description
---|---
``R1(config-router)#variance [variance]``|change variance to perform **unequal cost load balancing**. [variance] value range: 1-128.
``R1(config-router)#auto-summary``|enable **automatic summarization**
``R1(config-router)#redistribute static``|propagate a **default static route**. Works on both IPv4 and IPv6. :bulb: remember to check routing tables to ensure correct/desired configuration
``R1(config-if)#bandwidth [BW in kilobits]``|modify the EIGRP metric. :warning: this is done in **interface configuration mode**
``R1(config-if)#ip hello-interval eigrp [AS-number] [time in seconds]``|modify hello interval on IPv4. :warning: this is done in **interface configuration mode**
``R1(config-if)#ipv6 hello-interval eigrp [AS-number] [time in seconds]``|modify hello interval on IPv6. :warning: this is done in **interface configuration mode**
``R1(config-if)#ip hold-time eigrp [AS-number] [time in seconds]``|modify hold timer length on IPv4 :warning: this is done in **interface configuration mode**
``R1(config-if)#ipv6 hold-time eigrp [AS-number] [time in seconds]``|modify hold timer length on IPv6 :warning: this is done in **interface configuration mode**

:bulb: Recall: **automatic summarization** is **disabled** by default

:warning: When modifying EIGRP hello intervals and hold timers, ALWAYS MAKE SURE your Hello intervals are LESS THAN your hold timers. Otherwise, you could have a _flapping link_ (due to timer misconfiguration, constantly goes up, down, up, ...)


## Dynamic routing: EIGRP for IPv6

### Configuration
Command|Description
---|---
``R1(config)#ipv6 unicast-routing``|this **global configuration command** enables the router to forward IPv6 packets
``R1(config)#ipv6 router eigrp [AS-number]``|enter router configuration mode for EIGRP for IPv6, specifying the AS number
``R1(config-rtr)#eigrp router-id [a.b.c.d]``|:bulb: The EIGRP for IPv6 process will start running **after** you enter the router ID
``R1(config-rtr)#no shutdown``|:bulb: This is a best practice, since EIGRP for IPv6 has a **shutdown feature**
``R1(config-rtr)#interface [int-id]``|now, go to **each interface** where you want to enable EIGRP for IPv6
``R1(config-if)#ipv6 eigrp [AS-number]``|use this command with the AS-number you used when configuring EIGRP for IPv6 on **each desired interface**

:bulb: Note that the configuration mode prompt when configuring EIGRP for IPv6 is different. While EIGRP for IPv4 is configured under the configuration mode with prompt ``R1(config-router)#``, EIGRP for IPv6 is configured under the mode/prompt ``R1(config-rtr)#``

### Verification
The same process for verification or troubleshooting for IPv4 can be used on IPv6 implementations. Replace ``ip`` for ``ipv6`` in your commands

Command|Description
---|---
``R1#show ipv6 protocols``|verifies the current configured values for EIGRP (and any additional enabled routing protocol on the device)
``R1#show ipv6 eigrp neighbors``|displays the nighbor table. Use it to verify the router recognizes its neighbors.
``R1#show ipv6 route eigrp``|display **only EIGRP** entries in the routing table
``R1#show ipv6 eigrp interface``|verifies which interface are enabled for EIGRP, number of peers, and transmit queues

Note: The network command enables any interface with an ip in that net to send and receive EIGRP updates. Also it enables routes to this nets to start beeing advertised.

| Command                                         | Description                                          |
|:------------------------------------------------|:-----------------------------------------------------|
| # show run &#124 section eigrp                  | Show EIGRP settings.                                 |
| # show interfaces g1/1                          | Show configured/default bandwith and delay.          |
| (config-if)# bandwidth <kbps>                   | Overwrite bandwidth used for eigrp metric.           |
| (config-if)# delay <micros>                     | Overwrite deplay used for eigrp metric.              |
| (config)# router eigrp 23                       | Add and conf EIGRP AS#23                             |
| (config-router)# network 10.20.30.0 0.0.0.255   | Announce routes to 10.20.30.0/24                     |
| (config-router)# no shutdown                    | On some iOS versions it's off by default.            |
| (config-router)# [no] eigrp router-id <id-ip>   | Defaults to highest loopback ip                      |
| (config-router)# [no] passive-interface g1/2    | Disable EIGRP here. Ignore incoming pkgs.            |
| (config-router)# [no] passive-interface default | Disable EIGRP on all ifs by default.                 |
| (config-router)# maximum-paths <nr>             | Default 4, must match, number of loadbalanced paths. |
| (config-router)# variance 4                     | Default 1, Max 4:1 variance for unequal lb.          |
| (config-router)# no auto-summary                | Don't summarize a smaller subnet route in a big one. |
| # show ip[v6] eigrp neighbors                   | Neighbor addr, if, hold time, uptime, queued pkgs    |
| # show ip[v6] eigrp interfaces [if-name]        | If, Number of peers, pending routes, queued pkgs     |
| # show ip[v6] route [eigrp]                     | Routes starting with D were learned via EIGRP        |
| # show ip[v6] eigrp topology [all-links]        | Topology table, as#, router-id                       |

### EIGRP with ipv6

| Command                         | Description                                   |
|:--------------------------------|:----------------------------------------------|
| (config)# ipv6 unicast-routing  | Enable v6 routing on the router               |
| (config)# ipv6 router eigrp 23  | Configure eigrp as #23                        |
| (config-rtr)# no shutdown       | Enable this eigrp routing process.            |
| (config-if)# [no] ipv6 eigrp 23 | Enable eigrp with ipv6 for as #23 on this if. |

## OSPF

cost = reference bandwidth / interface bandwidth

The default reference bandwith is 100Mbps. Everything faster has a cost of 1.

| Command                                                        | Description                                     |
|:---------------------------------------------------------------|:------------------------------------------------|
| (config)# router ospf 1                                        | 1 is the pid, not the area.                     |
| (config-router)# router-id 1.2.3.4                             | Defaults to highest IPv4 on lo, then other ifs. |
| (config-router)# network 10.20.30.0 0.0.0.255 area 0           | enable interfaces for ospf with matching IPs    |
| (config-router)# (no) passive-interface g1/1                   | Stop in- and egress ospf hello packets.         |
| (config-router)# passive-interface default                     | Mark all ifs passive by default.                |
| (config-router)# default-information originate (always)        | Advertise default routes into a normal area     |
| (config-router)# auto-cost reference-bandwidth <refbw in Mb/s> | Change reference bandwidth speed                |
| (config-if)# ip ospf cost 23                                   | Overwrite interface cost to 23                  |
| (config-if)# bandwidth <bw in kb/s>                            | Change interface bandwidth                      |

### Router Types
| Term                                     | Definition                                                                       |
|:-----------------------------------------|:---------------------------------------------------------------------------------|
| Internal Router                          | All OSPF interfaces in one area                                                  |
| Backbone Router                          | Has one or more OSPF interfaces in the backbone                                  | 
| Area Boundary Router (ABR)               | Has at least one interface in the backbone area and at least one in another area |
| Autonomous System Boundary Router (ASBR) | Injects routes into OSPF via redistribution from other routing protocols         |

### OSPF with ipv6 (OSPFv3)

| Command                                     | Description                                        |
|:--------------------------------------------|:---------------------------------------------------|
| (config)# ipv6 unicast-routing              |                                                    |
| (config)# ipv6 router ospf <pid>            |                                                    |
| (config-router)# router-id <ipv4>           | Required if we don't have any v4 addrs configured. |
| (config-if)# ipv6 ospf <pid> area <area id> | Required for OSPFv3.                               |

The networks command does not exist, non mentioned commands are the same.


### Troubleshooting OSPF

| Command                            | Description                                                  |
|:-----------------------------------|:-------------------------------------------------------------|
| # show run &#124; sect ospf        |                                                              |
| # show ip(v6) protocols            | Other protocols with lower AD?                               |
| # show ipv6 ospf                   | reference bandwidth, router id, networks, interface per area |
| # show ip(v6) ospf neighbor        | neighbor IDs, IPs and via interface.                         |
| # show ip(v6) ospf neighbor detail | dr, bdr, timers, ...                                         |
| # show interface brief             | admin down? link?                                            |
| # show ip(v6) ospf interface brief | ospf enabled interfaces                                      |
| # show ip(v6) ospf interface g1/1  | ospf related infos for g1/1, passive?                        |
| # show ip(v6) route (ospf)         | ospf routes are marked O, show route ad and cost             |


## BGP

Note: In other routing protocols the network statement is used to determin the interfaces over which the protocol should talk to its neighbors. In BGP it indicates only which routes should be advertised to the BGP neighbors. The network needs to match an exact route in the routing table or it will still not be announced.

| Command                                          | Description                           |
|:-------------------------------------------------|:--------------------------------------|
| (config)# router bgp <local-as>                  | Create routing process.               |
| (config)# neighbor <peer-ip> remote-as <peer-as> | BGP does not auto discover neighbors. |
| (config)# network <net> [mask <mask>]            | Advertise this network.               |

| Command                           | Description                                        |
|:----------------------------------|:---------------------------------------------------|
| # show run &#124; sect bgp        |                                                    |
| # show ip bgp summary             | neighbors IPs, ASs and session states, bgp version |
| # show ip bgp neighbors [peer-ip] | tcp sessions and timers, bgp parameters            |
| # show ip bgp                     | routing infos received from all peers              |

## CLI

### Default Behavior

Here I'll collect crazy default behaviors and how to fix them, I guess..

| Command                       | Description                                      |
|:------------------------------|:-------------------------------------------------|
| (config)# no ip domain-lookup | Don't try to telnet unknown single word commands |

### Modes

| Mode      | Prompt         | enter                         |
|:----------|:---------------|:------------------------------|
| User      | >              | N/A                           |
| Exec      | #              | > enable                      |
| Config    | (config)#      | # configure terminal          |
| Interface | (config-if)#   | (config)# interface g1/0      |
| Line      | (config-line)# | (config)# line vty 0 4        |
| DHCP      | (dhcp-config)# | (config)# ip dhcp pool Foobar |

### Filters

| Name              | Function                                                                  |
|:------------------|:--------------------------------------------------------------------------|
| include hostname  | find a line including 'hostname'                                          |
| section interface | find a section including 'interface'                                      |
| begin interface   | Show remaining config starting with the first line containing 'interface' |
| exclude !         | exclude all line containing ! (comments)                                  |

### Navigation

| Sequence       | Function                                       |
|:---------------|:-----------------------------------------------|
| Ctrl-Shfit-6   | Kill many commands                             |
| Ctrl-Shift-6 x | Move telnet session to background              |
| Esc-B          | Ctrl-Left arrow                                |
| Esc-F          | Ctrl-Right arrow                               |
| Ctrl-R         | Redraw the current line                        |
| Ctrl-U         | Erase line                                     |
| Ctrl-W         | Delete the word left of the cursor             |
| Ctrl-C         | Drop back to Exec, does _not_ kill processes.. |
| Ctrl-A         | Move Cursor to the beginning of the line       |
| Ctrl-E         | Move Cursor to the end of the line             |
| Tab            | Autocompletion                                 |
| ?              | Help, can be entered mostly everywhere         |



## Packet Types

### Ethernet Frame

| Field                      | Field Length    | Description                                                                 |
|:---------------------------|:----------------|:----------------------------------------------------------------------------|
| Preamble                   | 8 bytes         | Alternating 1s and 0s used to synchronize                                   |
| Destination MAC (DA)       | 6 bytes         | MAC of recipient                                                            |
| Source MAC (SA)            | 6 bytes         | MAC of sender                                                               |
| 802.1Q tag (optional)      | 4 bytes         | Optional vlan tag. Starts with 0x8100 to mark 802.1Q mode in type location. |
| Type or Length             | 2 bytes         | Layer three type OR length if smaler then 1536 bytes.                       |
| Data                       | 46 - 1500 bytes | Payload                                                                     |
| Frame check sequence (FCS) | 4 bytes         | 32 bit CRC Checksum                                                         |

### IPv4 Header

| Field                        | Field Length | Description                            |
|:-----------------------------|:-------------|:---------------------------------------|
| Version                      | 4 bits       | IP Version, always four                |
| Internet Header Length (IHL) | 4 bits       | Length of the header                   |
| Service Type                 | 8 bits       | Desired QOS information (DSCP and ECN) |
| Total Length                 | 2 bytes      | Packet length, including this header   |
| Identification               | 2 bytes      | A unique ID                            |
| Flag                         | 3 bits       | fragmentation behaviour                |
| Fragment Offset              | 13 bits      |                                        |
| TTL                          | 1 byte       | TTL, decreased by every router by one. |
| Protocol                     | 1 byte       | Layer four type                        |
| Header Checksum              | 2 bytes      |                                        |
| Options (optional)           | 16 bytes     |                                        |
| Padding                      | max. 31 bits | Pad to the nearest 32 bit boundary     |

### TCP Segment

| Field                  | Field Length | Description                                                                 |
|:-----------------------|:-------------|:----------------------------------------------------------------------------|
| Source Port            | 2 bytes      |                                                                             |
| Destination Port       | 2 bytes      |                                                                             |
| Squence Number         | 4 bytes      | Unique Number for this Segment                                              |
| Acknowledgement Number | 4 bytes      | Next expected sequence number, acknowledge all prior Segments.              |
| Header Lenght          | 4 bits       | Header size in multiples of 4 bytes, sometimes also called Data Offset.     |
| Reserved               | 3 bits       | N/A                                                                         |
| Flags                  | 9 bits       | Control Flags like SYN, ACK, FIN, RST and Flags for congestion control.     |
| Window size            | 2 bytes      | bytes sender is currently willing to receive                                |
| Checksum               | 2 bytes      | Header Checksum                                                             |
| Urgent Pointer         | 2 bytes      | Points to the last 'urgent' byte in the Segment, used when URG flag is set. |
| Options                | 0 - 320 bits | The Size is determined by Header length. TODO:                              |
| Data                   | variable     |                                                                             |

### UDP Segment

| Field               | Field Length | Description                   |
|:--------------------|:-------------|:------------------------------|
| Source Port         | 2 bytes      |                               |
| Destination Port    | 2 bytes      |                               |
| Length              | 2 bytes      | Length of the whole Segment   |
| Checksum (optional) | 2 bytes      | Checksum of the whole Segment |
| Data                | variable     |                               |



## To Sort and Misc

| Command                          | Description                                   |
|:---------------------------------|:----------------------------------------------|
| # telnet 1.2.3.4 23              | Telnet to `1.2.3.4` using port `23`           |
| # disconnect                     | Disconnect background telnet session          |
| # ssh -l h.acker 1.2.3.4         | SSH to `1.2.3.4` using `h.acker` user         |
| (config-if)# duplex {full, auto} | Set duplex mode or set it to autonegotiation. |
| (config-if)# speed {100, auto}   | Set speed or set it to autonegotiation.       |
	
	
	
	
	
	
---
	
	

# CCNA Router command cheat-sheet
#### Useful router commands for CCNA2 v6 (Routing and Switching Essentials) Cisco Networking Academy course.

---
## Table of contents

- [Important ``show`` commands](#important-show-commands)
- [Output filtering](#filtering-information-from-show)
- [**Static routing**](#static-routing)
- [**Dynamic routing: OSPF**](#dynamic-routing-ospf)
- [Routing between VLANS: ROAS](#configuring-Router-on-a-stick-inter-VLAN-routing)
- [Access Control Lists (ACL)](#no_pedestrians-access-control-lists-acl)
- [DHCPv4](#DHCPv4)
- [DHCPv6](#DHCPv6)
- [NAT](#NAT)  
- [HSRP](#HSRP)
- Appendices:
    - [Common administrative distance values](#appendix-common-administrative-distance-ad-values)
    - [IPv4 address classes](#appendix-ipv4-address-classes)
    - [Private IPv4 address ranges](#appendix-private-ipv4-address-ranges)
- [Previous exam version content](#legacy-section-CCNA-version-6-200-125-exam)
    - [RIP](#dynamic-routing-rip)
        - [RIPv1](#ripv1-configuration)
        - [RIPv2](#ripv2-configuration)
    - [EIGRP](#dynamic-routing-eigrp)
        - [Configuration](#configuration)
        - [Verification](#verification)
        - [Fine tuning](#fine-tuning)
    - [EIGRP for IPv6](#dynamic-routing-eigrp-for-ipv6)

---
## Before we start: Configuration modes
Three basic configuration modes we MUST be familiar with already (you will see them below, a lot).  

Mode (prompt)|Mode|Mode change (current -> next)
---|---|---
``R1>``|user EXEC mode  AKA _view-only mode_|type ``enable`` to pass to next mode
``R1#``|Privileged EXEC mode|type ``configure terminal`` to pass to next mode
``R1(config)#``|Global configuration mode|N/A

Common abbreviations to the commands above (separated by commas):
```
en, ena
conf t, config term
```

On a Cisco router, from **global configuration mode**, you can also access the two following configuration modes:

Mode (prompt)|Mode|Description
---|---|---
``R1(config-if)#``|Interface configuration mode|used to configure an individual interface
``R1(config-router)#``|Router configuration mode|used when configuring an IPv4 routing protocol

> :bulb: When configuring an IPv6 routing protocol, such as OSPFv3, the router configuration mode prompt will be: ``R1(config-rtr)#``

---
## Important ``show`` commands:
Note that these commands are executed on privileged EXEC mode (``R1#`` prompt).  
You can execute them from global configuration mode (``R1(config)#`` prompt) by adding the ``do`` keyword before the command.  
example:  
``R1(config)#do show ip interface brief``  

Command|Description
---|---
``R1#show running-config``|display config saved in RAM (and the currently running configuration in the device)
``R1#show startup-config``|display config saved in NVRAM
``R1#show history``|

## Filtering information from ``show`` commands:
Some commands, such as ``show running-config``, generate multiple lines of output.  

To filter output, you can use the *pipe* (``|``) character along with a **filtering parameter** and a **filtering expression**.
Filtering parameters|Effect
---|---
``section [filtering-expression]``|shows the section of the _filtering expression_
``include [filtering-expression]``|includes all lines of output that match the _filtering expression_ **ONLY**
``exclude [filtering-expression]``|excludes all lines of output that match the _filtering expression_
``begin [filtering-expression]``|shows all the lines of output **beginning from** the line that matches the _filtering expression_

### Usage:
Here's an example of the usage of filtering with a ``show`` command:  
``R1#show running-config | include line con``

:bulb: ProTip: By default, the screen of output consists of 24 lines. Should you want to change the number of output lines displayed on the terminal screen, you can use the command: ``R1# terminal length [number-of-lines]``  
:warning: Unfortunately, this command is NOT supported in Cisco Packet Tracer (tested on version 7.2.2).

---
## Static routing

With an administrative distance (AD) of ``1``. These are, just after the **directly connected routes**, the most trustworthy routes a router can have on its routing table.

Static routes are all configured in **global configuration mode**, with the ``ip route`` command, i.e.,
>``R1(config)#ip route [network-address] [subnet-mask] ....``


### There are essentially four types of static routes, with particular purposes.

### Standard Static Route
>``R1(config)#ip route [network-address] [subnet-mask] ([next-hop-ip] [exit-int])``

### Default Static Route
>``R1(config)#ip route 0.0.0.0 0.0.0.0 ([next-hop-ip] [exit-int])``

### Floating Static Route
>``R1(config)#ip route [network-address] [subnet-mask] ([next-hop-ip] [exit-int]) [AD]``

### Summary Static Route
>``R1(config)#ip route [network-address] [subnet-mask*] ([next-hop-ip] [exit-int])``  
``*`` Using the appropriate subnet mask that summarizes the otherwise separate routes into a **single**, static route.


---
## Dynamic routing: OSPF

### OSPF configuration
Command|Description
---|---
``R1(config)#router ospf [PID]``|create OSPF process with Process ID [PID] (1 - 65535)
``R1(config-router)#router-id [a.b.c.d]``|manually assign the router an ID, in an IPv4 address format.
``R1(config-router)#network [network-address] [wildcard-mask] area [area id]``|for all directly connected networks, announce each network following this nomenclature. Area ID can go from 0 to 4294967295

:bulb: The ``area id`` can also be expressed in IP address format, hence the range of available ``area id``s.

:bulb: ProTip: How can I easily visualize all the directly connected networks a router has?  
Issue the ``R1(config)#do show ip route con`` command.  
It will display the routing table ONLY with the directly connected networks (routes).

>:trophy: **Best practice:** OSPF routers **within an area** use **and need unique IDs** to identify themselves. It is highly convenient to manually set a desired router ID with the ``router-id`` command.


### OSPF verification

The following are useful commands to verify and troubleshoot your OSPF configurations.

Command|Description
---|---
``R1#show ip protocols``|your go-to command to quickly verify key OSPF configuration information on a router, including PID, router ID, advertised networks, neighbors and administrative distance.
``R1#show ip route``|adfa. Additionally, issue ``shw ip route ospf`` to see only the OSPF-learned networks (entries) on the routing table.
``R1#show ip ospf neighbor``|list of this router's OSPF _neighbor_ routers
``R1#show ip ospf``|useful to identify the PID, router ID, area information, and when the SPF algorithm was run for the last time
``R1#show ip ospf interface brief``|summary of router's OSPF-enabled interfaces. :warning: This command does NOT seem to work on Packet Tracer 7.3
``R1#show ip ospf interface``|in-detail list of every OSPF-enabled interface
``R1#show ip ospf interface [int-id]``|in-detail information for a particular OSPF-enabled interface


:bulb: Recall: OSPF's default AD is ``110``  
You can find common AD values [here](#appendix-common-administrative-distance-ad-values).

---
## Configuring Router-on-a-stick inter-VLAN routing

To enable router-on-a-stick inter-VLAN routing, we must configure multiple **subinterfaces** (as many as the number of VLANs over which we want to route traffic).  
Through this process, only one physical interface, and thus, one trunk link, are required.  

In global configuration mode, i.e., ``R1(config)#`` prompt:

Command|Description
---|---
``R1(config)#interface g0/0.[vlan-id]``|create the ``.[vlan-id]`` **subinterface** on interface Gigabit Ethernet 0/0
``R1(config-subif)#encapsulation dot1q [vlan-id]``|configure subinterface to operate on a specified VLAN
``R1(config-subif)#encapsulation dot1q [vlan-id] native``|must be configured on the subinterfaace belonging to the **native** VLAN
``R1(config-subif)#ip address [ip-address] [subnet-mask]``|:exclamation: don't forget to assign the subinterface an IP address!
``R1(config-subif)#interface g0/0``|access the Gigabit0/0 interface (i.e., the actual physical interface) to enable it
``R1(config-if)#no shutdown``|enable the physical interface. This enables **all** configured subinterfaces **on that interface**

---
## :no_pedestrians: Access Control Lists (ACL)

:bulb: ProTip: **_Standard or extended?_** - Standard ACLs are generally -if not always- placed closest to the destination. Extended ACLs are placed closest to the source. Think you might have trouble remembering that? Try this:
> _"Standard closest to Destination"_, i.e., **S - D**  
_"Extended closest to Source"_, i.e., **E - S**  
Notice (and remember) there is **_only one S_** on each the previous letter pairs.

:bulb: Recall: **_How many ACLs can I have on the router?_** - One per interface, per protocol (IPv4, IPv6), per direction (inbound, outbound)

### Procedure for configuring Standard Numbered ACLs

Command|Description
---|---
``R1(config)#access-list [number] [permit/deny] [address] [wildcard mask]``|create entry in standard IPv4 ACL with specified number
``R1(config)#interface [int-id]``|select the interface to which the ACL will be applied
``R1(config-if)#ip access-group [number] [in/out]``|activate the ACL on the selected interface
``R1(config)#no access-list [number]``|:warning: This **ERASES** the ACL, i.e., **EVERY ACE** (Access Control entry) **that makes it up**

>:trophy: :warning: **Best practice / IMPORTANT:** It is HIGHLY recommended to always have EACH of your ACLs **backed-up.**


### Procedure for configuring Standard Named ACLs

Command|Description
---|---
``R1(config)#ip access-list [standard] [name]``|creates a standard named ACL. Will take you to standard (``std``) named ACL (``nacl``) configuration mode after entering it
``R1(config-std-nacl)#``|


---
## DHCPv4

### Configure a Cisco router as a DHCPv4 server

Command|Description
---|---
``R1(config)#ip dhcp excludded-address [start-address (end-address)]``|exclude a single or a range of IPv4 addresses, i.e., these addresses will not be available for DHCP assignment to hosts
``R1(config)#ip dhcp pool [pool name]``|create and name the pool of available addresses to assign. Takes you to **DHCP config mode**.
``R1(dhcp-config)#network [network-id] [mask]``|specify the network address with either the subnet mask OR the prefix length
``R1(dhcp-config)#default-router [address]``|specify the IPv4 address of the default gateway (router) the hosts will use

That's all a simple DHCP server configuration is comprised of.
Some additional configuration can be made with help of the follwing commands:

Command|Description
---|---
``R1(dhcp-config)#lease [days] ([hours] [minutes])``|specify the time of the lease of every address
``R1(dhcp-config)#dns-server [dns-address-1] ([dns-address-2 ... dns-address-8])``|specify up to 8 DNS server addresses
``R1(dhcp-config)#domain-name [name]``|specify the domain name

### The ip helper address:

If your DHCP server is on a **separate network segment**, you will have to (and can) relay external DHCPv4 requests.  
You will have to enter the following command on every interface of the router that needs to reach the DHCP server's segment.

Command|Description
---|---
``R1(config-if)#ip helper address [DHCP-server-address]``|indicates the router to relay (instead of discarding) DHCP messages to the DHCP server's address.


---
## DHCPv6

### Stateless DHCPv6

---
## NAT

### Configuring Static NAT
Command|Description
---|---
``R1(config)#ip nat inside source static [local-add] [global-add]``|configure static nat, specifying the local address that will be mapped to a global address

### Inside and outside interfaces
:bulb: Recall: After this, **always remember** to specify the **inside** and **outside** interfaces.  
>Though it might be easy for us to identify them with our topology diagram, it's not that easy for the router.

Command|Description
---|---
``R1(config)#interface [int-id]``|enter configuration mode for the _inside_ interface
``R1(config-if)#ip nat inside``|
``R1(config)#interface [int-id]``|enter configuration mode for the _outside_ interface
``R1(config-if)#ip nat outside``|


### Configuring Dynamic NAT
Command|Description
---|---
``R1(config)#ip nat pool [pool-name] [start-address] [end-address] {netmask [mask] \| prefix-length [prefix-length]}``|create the pool of routable addresses that hosts will use to exit the private network
``access-list [number] {permit \| deny} [source] [wildcard mask]``|create an access list to blah blah
``ip nat inside source list [acl-number] pool [pool name]``|we now bind the pool to the ACL

:bulb: Lastly, **DO NOT forget to [specify the inside and outside interfaces](#inside-and-outside-interfaces)**



---
## HSRP
Command|Description
---|---
``R1(config-if)#standby version 2``|(optional) specify HSRP version 2 will be used. Otherwise, your HSRP instance will be running in version 1 by default.
``R1(config-if)#standby [group] ip [virtual-ip]``|specify the router group and the virtual gateway's IP address
``R1(config-if)#standby [group] priority [0-255]``|(optional) specify each router a priority for **active router** election
``R1(config-if)#standby [group] preempt``|(optional) enables **preemption**, i.e., a router with higher priority will take the active role if current active router's priority is lower
``R1(config-if)#standby [group] timers [hello-timer] [hold-timer]``|specify hello and hold (dead) timers. HSRP automatically ensures that the hold timer value is greater than the hello timer value to avoid incorrect behavior.

:warning: **ALWAYS use the SAME HSRP version on your groups/topologies**  
For Cisco routers, having instances of the 2 different HSRP versions running is like having two different HSRP groups. Hence, you will come across a duplicate address error (assuming you configured HSRPv1 and HSRPv2 using the same virtual router address).

### :bulb: HSRPv1 vs HSRPv2: What's different?
- v2 supports IPv6, v1 does NOT.
- v2 supports 4095 groups, v1 supports 255.
- v2 sends multicast HSRP traffic to ``224.0.0.102``, v1 multicasts to``224.0.0.2``
- the **virtual MAC addresses are also different**
    - v1: ``0000.0C07.ACxx``
    - v2: ``0000.0C9F.Fxxx``
    - :bulb: the ``x`` characters at the end are replaced by the **group number** in HEX.



---
# Appendix: Common administrative distance (AD) values:

Default values:

code|type|AD value
---|---|---
``C``|Directly connected network|``0``
``S``|Static route|``1``
``D``|Internal EIGRP|``90``
``O``|OSPF|``110``
``R``|RIP|``120``

[Back to table of contents](#table-of-contents)  
[Back to OSPF verification](#ospf-verification)  
[Back to EIGRP verification](#eigrp-verification)
[Back to RIP](#dynamic-routing-rip)


# Appendix: IPv4 address classes
There are five class groups in which IPv4 addresses are segmented: A, B, C, D, and E.  
:bulb: Classes D and E are reserved groups.  
- Class D addresses are **multicast groups**
- Class E addresses are reserved for research purposes

Class|Range (**first octet**)
---|---
A|``1 - 127``
B|``128 - 191``
C|``192 - 223``
D|``224 - 239``
E|``240 - 255``

[Back to table of contents](#table-of-contents)


# Appendix: Private IPv4 address ranges

The following private IPv4 address spaces are defined in RFC 1918 ("Address Allocation for Private Internets").  
These addresses are used within private networks and are thus NOT routable to the **public Internet**.  
To forward traffic from a private to a public network, you'd use Network Address Translation (NAT), defined in RFC 3022.
NAT configuration on Cisco routers is covered [here](#nat).

Class|Range (CIDR notation)|Range (start - end)
---|---|---
A|``10.0.0.0/8``|``10.0.0.0 - 10.0.0.255``
B|``172.16.0.0/12``|``172.16.0.0 - 172.31.255.255``
C|``192.168.0.0/16``|``192.168.0.0 - 192.168.255.255``

[Back to table of contents](#table-of-contents)


---
# Legacy section (CCNA version 6, 200-125 exam)
:warning: **Attention:** the following topics are no longer on the **current** version (7) of the 200-301 CCNA exam.

## Dynamic routing: RIP
### RIPv1 configuration

Command|Description
---|---
``R1(config)#router rip``|enter router configuration mode, with RIP as the routing protocol
``R1(config-router)#network [network-id]``|specify the network segment address. Note that this is done without the **subnet mask**.
``R1(config-router)#passive-interface [int-id]``|(optional) - prevent an interface from sending RIP updates

:bulb: For safety reasons, interfaces that do NOT need to send RIP updates (e.g., interfaces facing network segments with hosts instead of other routers) should be configured as passive. It's also a good practice as RIP updates on these segments would be nothing but wasted bandwidth.

:bulb: As you see, NO subnet mask information is configured. When forwarding updates, the router uses either the mask configured on the local interface or the default mask based on the address class (A, B, or C).
:bulb: You can find out more about address classes [here](#appendix-ipv4-address-classes)  
:warning: Because of this, your networks on a RIPv1 scheme **MUST BE CONTIGUOUS**, meaning that VLSM or supernetting is not supported by version 1 of RIP

:bulb: Recall: RIP's default AD is ``120``  
You can find common AD values [here](#appendix-common-administrative-distance-ad-values).

### Additional RIPv1 configuration

Command|Description
---|---
``R1(config-router)#default-information originate``|**if a [default static route](#default-static-route) is configured on the router** propagate the default route to other routers receiving RIP updates


### RIPv2 configuration

Command|Description
---|---
``R1(config)#router rip``|enter router configuration mode, with RIP as the routing protocol
``R1(config-router)#version 2``|change RIP process version from 1 to 2
``R1(config-router)#no auto-summary``|disable network auto summarization

:bulb: Recall: by default (without previously configuring version 2), RIP can **receive both** RIPv1 and RIPv2 routing updates.  
:bulb: You can see this with the ``R1#show ip protocols`` command.


	

	














	
	
