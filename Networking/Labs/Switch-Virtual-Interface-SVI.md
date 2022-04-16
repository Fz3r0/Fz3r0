## Fz3r0 Operations

### [Networking]

### Switch Virtual Interface (SVI)

#### Cisco Packet Tracer
---

##### Twitter : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Cisco` `Routing` `Switching` `CLI` `IOS` `CCNA` `CCNP` `Secure Network` `SVI`

---

#### Packet Tracer Lab Files & Topology

[<< Download Files >>](https://github.com/Fz3r0/Fz3r0/files/8500676/2____fz3r0_OPs_Routing_._Switching_.3-vlans_1-switch_1-router._R_SwitchVirtualInterface_SVI.zip)

![image](https://user-images.githubusercontent.com/94720207/163691708-354160a3-3648-4bcd-910b-f510c29f1443.png)

___

### < Switch 2 - SVI >

```

enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.domain

hostname SW2-SVI

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

          fz3r0 - SW2-SVI - ZoneA :  Only authorized access!      
                  (banner seen after a SSH login)

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

vlan 10
name VLAN10-BLUE
vlan 20
name VLAN10-RED
vlan 30
name VLAN10-GREEN

vlan 100
name VLAN100-Admin/SSH

vlan 99
name VLAN99-TRUNK
exit

vlan 666
name VLAN666-Unused_Honeypot
exit

interface range Gi1/0/1 - 24, Gi1/1/1 - 4
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
spanning-tree mode rapid

interface gigabitEthernet 1/0/1
description << Trunk | Connect to SW1  - SW1:Gi0/1 >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
duplex auto
speed 1000
spanning-tree bpduguard disable
spanning-tree portfast disable
CDP enable

lldp transmit
lldp receive

no shutdown
exit

interface vlan 10
description << SVI - VLAN10-BLUE >>
ip address 192.168.10.254 255.255.255.0
no shutdown 
exit

interface vlan 20
description << SVI - VLAN20-RED >>
ip address 192.168.20.254 255.255.255.0
no shutdown 
exit

interface vlan 30
description << SVI - VLAN30-GREEN >>
ip address 192.168.30.254 255.255.255.0
no shutdown 
exit

interface loopback 0
description << SVI - loopback 0 >>
ip address 10.10.10.10 255.255.255.255
no shutdown 
exit

ip routing

end
copy running-config startup-config

exit

```
___

### < Switch 1 >

```

enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.domain

hostname SW1

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

           fz3r0 - R1 - ZoneA :  Only authorized access!      
                  (banner seen after a SSH login)

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

vlan 10
name VLAN10-BLUE
vlan 20
name VLAN10-RED
vlan 30
name VLAN10-GREEN

vlan 100
name VLAN100-Admin/SSH

vlan 99
name VLAN99-TRUNK
exit

vlan 666
name VLAN666-Unused_Honeypot
exit

interface vlan 100
description << Switch 1 Admin/SSH >>
ip address 192.168.100.1 255.255.255.0
no shutdown 
exit

ip default-gateway 192.168.100.254

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

interface gigabitEthernet 0/1
description << Trunk | Connect to SVI  - SW2-SVI:Gi1/0/1 >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
duplex auto
speed 1000

spanning-tree bpduguard disable
spanning-tree portfast disable
CDP enable
lldp transmit
lldp receive

switchport port-security
switchport port-security maximum 15
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666

no shutdown
exit

interface range fastEthernet 0/1 - 2
description << VLAN10-BLUE - SW1 >>
switchport mode access
switchport access vlan 10
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
no shutdown
exit

interface range fastEthernet 0/3 - 4
description << VLAN20-RED - SW1 >>
switchport mode access
switchport access vlan 20
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
no shutdown
exit

interface range fastEthernet 0/5 - 6
description << VLAN30-GREEN - SW1 >>
switchport mode access
switchport access vlan 30
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
no shutdown
exit

end
copy running-config startup-config

exit

```

### < Hosts & End Devices >

- VLAN10-BLUE PCs Configuration:

```
PC_1 Network Configuration

IPv4 Address	        192.168.10.1
Subnet Mask	        255.255.255.0
IPv4 Default Gateway	192.168.10.254
DNS                     1.1.1.1

PC_2 Network Configuration

IPv4 Address	        192.168.10.2
Subnet Mask	        255.255.255.0
IPv4 Default Gateway	192.168.10.254
DNS                     1.1.1.1
```

- VLAN20-RED PCs Configuration:

```

PC_3 Network Configuration

IPv4 Address	        192.168.20.1
Subnet Mask	        255.255.255.0
IPv4 Default Gateway	192.168.20.254
DNS                     1.1.1.1

PC_4 Network Configuration

IPv4 Address	        192.168.20.2
Subnet Mask	        255.255.255.0
IPv4 Default Gateway	192.168.20.254
DNS   
                  1.1.1.1
```

- VLAN30-GREEN PCs Configuration:

```

PC_5 Network Configuration

IPv4 Address	        192.168.30.1
Subnet Mask	        255.255.255.0
IPv4 Default Gateway	192.168.30.254
DNS                     1.1.1.1

PC_6 Network Configuration

IPv4 Address	        192.168.30.2
Subnet Mask	        255.255.255.0
IPv4 Default Gateway	192.168.30.254
DNS 
                    1.1.1.1
```
___

### NOTES:

- WATCH ALWAYS GATEWAYS CONFIG ON PC DUE TO PACKET TRACER BUG THAT DELETE THE GATEWAY RANDOMLY!!!!!

- I WAS UNABLE TO MANUALLY CONFIG FULL DUPLEX BETWEEN SW1 AND SW2 BECAUSE LAYER 3 SWITCHES DO NOT HAVE THE OPTION LIKE THE ROUTER...SO! SPEED IS CONFIGURED 1000MBPS AND DUPLEX AUTO ON BOTH SWITCHES. GOOD PRACTICE WOULD BE MANUALLY SET TO FULL DUPLEX AND 1000MBPS FOR FAST ETHERNET. 

- NOTE 1 - Port Security on Trunk:

    - WHEN I TESTED ALL HOSTS PINGING ALL IP'S, THE RESULTS FOR PORT SECURITY WERE:

    - (and remember, the VLAN100 fro Manage/SSH don't use MAC Addres, that's why is not shown on table ;) ) 

```

SW1#
SW1#show port-security address
               Secure Mac Address Table
-----------------------------------------------------------------------------
Vlan    Mac Address       Type                          Ports   Remaining Age
                                                                   (mins)
----    -----------       ----                          -----   -------------
  10    000C.8535.231E    SecureSticky                  Fa0/1        -   PC VLAN10-BLUE
  10    F0F0.F0F0.F666    SecureSticky                  Fa0/1        -   (MAC ADMIN fz3r0 agregada manual por mi)
  10    0060.2FB5.4AB6    SecureSticky                  Fa0/2        -   PC VLAN10-BLUE
  20    0006.2A77.8B5D    SecureSticky                  Fa0/3        -   PC VLAN20-RED
  20    F0F0.F0F0.F666    SecureSticky                  Fa0/3        -   (MAC ADMIN fz3r0 agregada manual por mi)
  20    0090.0CD5.8875    SecureSticky                  Fa0/4        -   PC VLAN20-RED
  30    0060.479C.B446    SecureSticky                  Fa0/5        -
  30    F0F0.F0F0.F666    SecureSticky                  Fa0/5        -   (MAC ADMIN fz3r0 agregada manual por mi)
  30    0001.4270.AD13    SecureSticky                  Fa0/6        -
  99    0090.21E5.EB01    SecureSticky                  Gig0/1       -   INTERFACE FÍSICA R1 Gi0/1 (LA ÚNICA MAC GUARDADA EN LA TRUNK)
  99    F0F0.F0F0.F666    SecureSticky                  Gig0/1       -   (MAC ADMIN fz3r0 agregada manual por mi)
-----------------------------------------------------------------------------
Total Addresses in System (excluding one mac per port)     : 4
Max Addresses limit in System (excluding one mac per port) : 1024
SW1#show port-security interface gi0/1
Port Security              : Enabled
Port Status                : Secure-up
Violation Mode             : Shutdown
Aging Time                 : 0 mins
Aging Type                 : Absolute
SecureStatic Address Aging : Disabled
Maximum MAC Addresses      : 18
Total MAC Addresses        : 6
Configured MAC Addresses   : 0
Sticky MAC Addresses       : 2
Last Source Address:Vlan   : 0090.21E5.EB01:10
Security Violation Count   : 0

SW1#

```

___

### Direct Commands:
___

### < Switch 2 - SVI >

```

enable
configure terminal 
!
no ip domain-lookup
ip domain-name fz3r0.domain
!
hostname SW2-SVI
!
enable secret cisco12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60
!
username root privilege 15 secret cisco12345
username user privilege 10 secret cisco12345
!
line console 0
password cisco12345
login
!
line vty 0 8
access-class 8 in
exec-timeout 5 30
transport input ssh
login local
!
crypto key generate rsa
1024
ip ssh version 2
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

          fz3r0 - SW2-SVI - ZoneA :  Only authorized access!      
                  (banner seen after a SSH login)

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
vlan 10
name VLAN10-BLUE
vlan 20
name VLAN10-RED
vlan 30
name VLAN10-GREEN
vlan 100
name VLAN100-Admin/SSH
vlan 99
name VLAN99-TRUNK
vlan 666
name VLAN666-Unused_Honeypot
!
interface range Gi1/0/1 - 24, Gi1/1/1 - 4
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
spanning-tree mode rapid
!
interface gigabitEthernet 1/0/1
description << Trunk | Connect to SW1  - SW1:Gi0/1 >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
duplex auto
speed 1000
spanning-tree bpduguard disable
spanning-tree portfast disable
CDP enable
lldp transmit
lldp receive
no shutdown
!
interface vlan 10
description << SVI - VLAN10-BLUE >>
ip address 192.168.10.254 255.255.255.0
no shutdown 
!
interface vlan 20
description << SVI - VLAN20-RED >>
ip address 192.168.20.254 255.255.255.0
no shutdown 
!
interface vlan 30
description << SVI - VLAN30-GREEN >>
ip address 192.168.30.254 255.255.255.0
no shutdown 
!
interface loopback 0
description << SVI - loopback 0 >>
ip address 10.10.10.10 255.255.255.255
no shutdown 
!
ip routing
!
end
copy running-config startup-config

exit

```

___

### < Switch 1 >

```

enable
configure terminal 
!
no ip domain-lookup
ip domain-name fz3r0.domain
!
hostname SW1
!
enable secret cisco12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60
!
username root privilege 15 secret cisco12345
username user privilege 10 secret cisco12345
!
line console 0
password cisco12345
login
!
line vty 0 8
access-class 8 in
exec-timeout 5 30
transport input ssh
login local
!
crypto key generate rsa
1024
ip ssh version 2
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

           fz3r0 - R1 - ZoneA :  Only authorized access!      
                  (banner seen after a SSH login)

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
vlan 10
name VLAN10-BLUE
vlan 20
name VLAN10-RED
vlan 30
name VLAN10-GREEN
vlan 100
name VLAN100-Admin/SSH
vlan 99
name VLAN99-TRUNK
vlan 666
name VLAN666-Unused_Honeypot
!
interface vlan 100
description << Switch 1 Admin/SSH >>
ip address 192.168.100.1 255.255.255.0
no shutdown 
!
ip default-gateway 192.168.100.254
!
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
!
interface gigabitEthernet 0/1
description << Trunk | Connect to SVI  - SW2-SVI:Gi1/0/1 >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
duplex auto
speed 1000
spanning-tree bpduguard disable
spanning-tree portfast disable
CDP enable
lldp transmit
lldp receive
switchport port-security
switchport port-security maximum 15
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
no shutdown
!
interface range fastEthernet 0/1 - 2
description << VLAN10-BLUE - SW1 >>
switchport mode access
switchport access vlan 10
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
no shutdown
!
interface range fastEthernet 0/3 - 4
description << VLAN20-RED - SW1 >>
switchport mode access
switchport access vlan 20
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
no shutdown
!
interface range fastEthernet 0/5 - 6
description << VLAN30-GREEN - SW1 >>
switchport mode access
switchport access vlan 30
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
no shutdown
!
end
copy running-config startup-config

exit

```


### Troubleshooting
___

* Port Security

```

show port-security interface fa0/1
show port-security

```
* Trunk

```

show interface trunk

```

### // References

https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4000/8-2glx/configuration/guide/stp_enha.html#wp1019922
https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/release/12-2_37_ey/configuration/guide/scg/swlldp.pdf
https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9500/software/release/16-10/configuration_guide/sec/b_1610_sec_9500_cg/b_1610_sec_9500_cg_chapter_0101010.html
https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25sg/configuration/guide/conf/port_sec.pdf

---

> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_
>
> _"In the mist of the night you could see me come, where the shadows move and Demons lie..."_
