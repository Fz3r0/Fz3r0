
# Configure WLAN on WLC like a sir!

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## Fz3r0 Operations: `Networking`

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `Wireless` `WLAN` `WLC` `CCNA` `CCNP` 
  
## Index

- < **Before anything else!!!** >

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

- < **Troubleshooting** & **show commands** for this configuration >** 

### Background Knowledge about this config:

- < **Nerd Pocket-Bible about this configuration** >

## Configure a Basic WLAN on the WLC

### WLC Topology

- WLC Topology Example:

    - ![image](https://user-images.githubusercontent.com/94720207/172289758-97f2192c-7afb-4188-8044-cca299cdd233.png)
    
- Packet Tracer Version:

    - ![image](https://user-images.githubusercontent.com/94720207/172294423-4197db96-f8e6-4726-8af5-84929aa06005.png)
 
- The access point `AP` is a `controller-based AP` as opposed to an `autonomous AP`. 

    - Recall that controller-based APs require no initial configuration and are often called lightweight APs (LAPs). 
    
    - `LAPs` use the `Lightweight Access Point Protocol` `LWAPP` to communicate with a `WLAN controller` `WLC`. 
    
    - Controller-based APs are useful in situations where many APs are required in the network. 
    
    - As more APs are added, each AP is automatically configured and managed by the WLC.

- The previous figure shows a wireless LAN controller (WLC) topology. 

    - `PC-A` is a `RADIUS/SNMP Server` connected to `R1` on `Gi 0/0` interface. 

    - `PC-B` is connected to `S1` on S1s `F0/6` port. 
    
    - `R1` and `S1` are connected together on `R1s Gi 0/1` interface and on `S1s F0/5` interface. 
    
    - `S1` is connected to a `WLC` on its `F0/18` port. 
    
    - On `S1s F0/1` port its connected to an access point, `AP1`. 
    
    - A `laptop` is wirelessly connected to `AP1`.

- Addressing Table: 

| **Device**      | **Interface** | **IP Address**  | **Subnet Mask**  |
|-----------------|---------------|-----------------|------------------|
| R1              | Gi0/0         | 172.16.1.1      | 255.255.255.0    |
| R1              | Gi0/1.1       | 192.168.200.1   | 255.255.255.0    |
| S1              | VLAN 1        | DHCP            |                  |
| WLC             | Management    | 192.168.200.254 | 255.255.255.0    |
| AP1             | Wired 0       | 192.168.200.3   | 255.255.255.0    |
| PC-A            | NIC           | 172.16.1.254    | 255.255.255.0    |
| PC-B            | NIC           | DHCP            |                  |
| Wireless Laptop | NIC           | DHCP            |                  |

### `R1` 

```
enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.domain.WLAN+WLC

hostname R1

enable secret cisco12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60

username root privilege 15 secret cisco12345
username user privilege 10 secret cisco12345

line console 0
password cisco12345
login
exit

line vty 0 8
access-class 8 in
exec-timeout 5 30
transport input ssh
login local
exit

crypto key generate rsa
1024
ip ssh version 2

banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Fz3r0 - WLAN + WLC Lab

             << R1 :  Only authorized access! >>     
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

interface range g0/0 - 2
description << Unused Router Ports >>
shutdown
exit

interface gigabitEthernet 0/0
description << Connect RADIUS/SNMP Server >>
ip address 172.16.1.1 255.255.255.255
duplex full
speed 1000
no shutdown
exit

interface gigabitEthernet 0/1
description << Connect SUB-Interfaces 0.1 >>
duplex full
speed 1000
no shutdown
exit

interface gigabitEthernet 0/1.1
description << Connect to Subnet 10 >>
encapsulation dot1Q 10
ip address 192.168.200.1 255.255.255.0
no shutdown 
exit

interface loopback 0
description << loopback 10.10.10.10 >>
ip address 10.10.10.10 255.255.255.255
exit

end
copy running-config startup-config

exit
```

### `S1`

```

enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.domain.WLAN+WLC

hostname S1

enable secret cisco12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60

username root privilege 15 secret cisco12345
username user privilege 10 secret cisco12345

line console 0
password cisco12345
login
exit

line vty 0 8
access-class 8 in
exec-timeout 5 30
transport input ssh
login local
exit

crypto key generate rsa
1024
ip ssh version 2

banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Fz3r0 - WLAN + WLC Lab

             << S1 :  Only authorized access! >>     
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

vlan 1
name VLAN1-Only_Test_VLAN

vlan 100
name VLAN100-Admin/SSH

vlan 99
name VLAN99-TRUNK
exit

interface vlan 100
description << Switch 1 Admin/SSH >>
ip address 192.168.200.100 255.255.255.0
no shutdown 
exit

ip default-gateway 192.168.200.1

interface range f0/1 - 24, g0/1 - 2
description << Unused Switch Ports (Access) >>
switchport mode access
switchport access vlan 666
disable DTP
spanning-tree bpduguard enable
spanning-tree portfast
no CDP enable
no lldp transmit
no lldp receive
switchport no negotiate
shutdown
exit

interface range fastEthernet 0/1
description << Trunk VLAN 99 - Connect to AP1 - USING POE >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
no shutdown
exit

interface range fastEthernet 0/5
description << Trunk VLAN 99 - Connect to R1 USING POE >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
no shutdown
exit

end
copy running-config startup-config

exit

```


---

### Log in to the WLC

- Configuring a wireless LAN controller (WLC) is not that much different from configuring a wireless router. 

- The big difference is that a WLC controls APs and provides more services and management capabilities, many of which are beyond the scope of this module.

    - **Note: The figures in this topic that show the graphical user interface (GUI) and menus are from a `Cisco 3504 Wireless Controller`.** 

    - However, other WLC models will have similar menus and features.

- The figure shows the user logging into the WLC with credentials that were configured during initial setup.

    - ![image](https://user-images.githubusercontent.com/94720207/172291053-b8b24e5c-768e-4f23-be10-fd961225a03d.png)

- The Network Summary page is a dashboard that provides a quick overview of the number of configured wireless networks, associated access points (APs), and active clients. 

- You can also see the number of rogue access points and clients, as shown in the figure.

    - ![image](https://user-images.githubusercontent.com/94720207/172291328-54e4e5ce-2796-4a4b-b9a6-db3dfe7f648f.png)

--- 

### View AP Information



---

### References

- https://ccna-200-301.online/remote-site-wlan-configuration/
- https://contenthub.netacad.com/srwe-dl/1.3.6

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
