# VLAN hopping

## What is VLAN Hopping Attack?

- VLAN hopping is a computer security exploit, a method of attacking networked resources on a virtual LAN (VLAN). 
- The basic concept behind all VLAN hopping attacks is for an attacking host on a VLAN to gain access to traffic on other VLANs that would normally not be accessible. 
- There are two primary methods of VLAN hopping: 
 
    1. Switch spoofing
    2. Double tagging. 
   
- Both attack vectors can be mitigated with proper switch port configuration.

## Switch spoofing

- In a switch spoofing attack, an attacking host imitates a trunking switch by speaking the tagging and trunking protocols (e.g. Multiple VLAN Registration Protocol, IEEE 802.1Q, Dynamic Trunking Protocol) used in maintaining a VLAN. 
- Traffic for multiple VLANs is then accessible to the attacking host.

### Switch Spoofing Mitigation

- Switch spoofing can only be exploited when interfaces are set to **negotiate a trunk**. 
- To prevent this attack on **Cisco IOS**, use one of the following methods:

1. Ensure that ports are not set to negotiate trunks automatically by disabling DTP:

```
Switch (config-if)# switchport nonegotiate
```

2. Ensure that ports that are not meant to be trunks are explicitly configured as access ports

```
Switch (config-if)# switchport mode access
```

## Double Tagging

- In a double tagging attack, an attacker connected to an 802.1Q-enabled port prepends two VLAN tags to a frame that it transmits. 
- The frame (externally tagged with VLAN ID that the attacker's port is really a member of) is forwarded without the first tag because it is the native VLAN of a trunk interface. 
- The second tag is then visible to the second switch that the frame encounters. 
- This second VLAN tag indicates that the frame is destined for a target host on a second switch. 
- The frame is then sent to the target host as though it originated on the target VLAN, effectively bypassing the network mechanisms that logically isolate VLANs from one another.
- However, possible replies are not forwarded to the attacking host (unidirectional flow). 

## Resources

- https://en.wikipedia.org/wiki/VLAN_hopping
- https://www.youtube.com/watch?v=5JQt9m_pDNM
