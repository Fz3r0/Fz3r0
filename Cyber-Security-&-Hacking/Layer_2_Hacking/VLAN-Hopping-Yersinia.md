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

### Example of Double Tagging

- As an example of a double tagging attack, consider a secure web server on a VLAN called VLAN2: 

    - Hosts **on VLAN2** are **allowed** access to the web server; hosts from **outside VLAN2** are **blocked** by layer 3 filters. 
    - An **attacking host on a separate VLAN**, called **VLAN1(Native)**, creates a specially formed packet to attack the web server. 
    - It places a **header tagging the packet as belonging to VLAN2**, **under the header tagging the packet as belonging to VLAN1**. 
    - When the packet is sent, the **switch sees the default VLAN1 header** and removes it and forwards the packet. 
    - The **next switch sees the VLAN2 header** and puts the packet in VLAN2. 
    
        - The packet thus arrives at the target server as though it were sent from another host on VLAN2, ignoring any layer 3 filtering that might be in place.

### Mitigation of Double Tagging

- Double Tagging can only be exploited on switch ports configured to use native VLANs.
- Trunk ports configured with a native VLAN don't apply a VLAN tag when sending these frames. 
- This allows an attacker's fake VLAN tag to be read by the next switch.
- Double Tagging can be mitigated by any of the following actions (Incl. IOS example):

1. Simply do not put any hosts on VLAN 1 (The default VLAN). i.e., assign an access VLAN other than VLAN 1 to every access port

```
Switch (config-if)# switchport access vlan 2
```

2. Change the native VLAN on all trunk ports to an unused VLAN ID.

```
Switch (config-if)# switchport trunk native vlan 999
```

3. Explicit tagging of the native VLAN on all trunk ports. Must be configured on all switches in network autonomy.

```
Switch(config)# vlan dot1q tag native
```
- Fz3r0 PRO Tip: Watch the compatibility between switches for that command! https://blog.pierky.com/remember-the-vlan-dot1q-tag-native-command-untagged-ingress-frames-are-dropped/

- Also check thisone, this guy made it work ;) https://community.cisco.com/t5/switching/native-vlan-tagging/td-p/2267039

```
...I just came back from a lab. I can confirm that if vlan dot1q tag native is configured, a trunk always performs tagging on the outgoing frames (i.e. the native VLAN setting is ignored and all frames are tagged with the corresponding tag value). Untagged frames arriving at a trunk port will be dropped without being forwarded further.

I've tested this on Catalyst 3560 (12.2(55)SE6) and 3560V2 (15.0(1)SE).

Keep in mind that the vlan dot1q tag native command applies only to tagging frames on trunk ports. It has no effect on access ports - these ports will continue operating in untagged mode as usual and will not drop anything :D
```

## Resources

- https://en.wikipedia.org/wiki/VLAN_hopping
- https://www.youtube.com/watch?v=5JQt9m_pDNM
