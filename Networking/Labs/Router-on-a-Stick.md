## Fz3r0 Operations

### [Networking]

### Router on a Stick

#### Cisco Packet Tracer
---

##### Twitter : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Cisco` `Routing` `Switching` `CLI` `IOS` `CCNA` `CCNP` `Secure Network`

---

#### Packet Tracer Lab Files & Topology

[<< DOWNLOAD FILES >>](https://github.com/Fz3r0/Fz3r0/files/8500585/1____fz3r0_OPs_Routing_._Switching_.3-vlans_1-switch_1-router._RouterOnAStick.zip)

![1d____VLAN_(3-vlans_1-switch_1-router)_R_OnAStick_TOPOLOGY](https://user-images.githubusercontent.com/94720207/163690161-d79fc452-ffe2-4876-8990-1ef934e81db8.png)

___

### < Router 1 >

```

enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.domain

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

banner login #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Unauthorized access to this device is prohibited!

         Twitter @fz3r0_Ops
         Github  Fz3r0    
             
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         fz3r0 - R1 - ZoneA :  Only authorized access!      
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

interface range g0/0 - 2
description << Unused Router Ports >>
shutdown
exit

interface gigabitEthernet 0/0
description << Connect SUB-Interfaces 10,20,30,99,100 >>
duplex full
speed 1000
no shutdown
exit

interface gigabitEthernet 0/0.10
description << Connect to Subnet 10 >>
encapsulation dot1Q 10
ip address 192.168.10.254 255.255.255.0
no shutdown 
exit

interface gigabitEthernet 0/0.20
description << Connect to Subnet 20 >>
encapsulation dot1Q 20
ip address 192.168.20.254 255.255.255.0
no shutdown 
exit

interface gigabitEthernet 0/0.30
description << Connect to Subnet 30 >>
encapsulation dot1Q 30
ip address 192.168.30.254 255.255.255.0
no shutdown 
exit

interface gigabitEthernet 0/0.99
description << Connect to Subnet 99 >>
encapsulation dot1Q 99
ip address 192.168.99.254 255.255.255.0
no shutdown 
exit

interface gigabitEthernet 0/0.100
description << Connect to Subnet 100 >>
encapsulation dot1Q 100
ip address 192.168.100.254 255.255.255.0
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
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

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
description << Trunk | Connect to Gateway  - R1:Gi0/0 >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
duplex full
speed 1000
spanning-tree bpduguard disable
spanning-tree portfast disable
CDP enable
lldp transmit
lldp receive

switchport port-security
switchport port-security maximum 6
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
DNS                     1.1.1.1
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
DNS                     1.1.1.1
```
___

### NOTES:

- WATCH ALWAYS GATEWAYS CONFIG ON PC DUE TO PACKET TRACER BUG THAR DELETE THE GATEWAY RANDOMLY!!!!!

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

### < Router 1 >

```

enable
configure terminal 
!
no ip domain-lookup
ip domain-name fz3r0.domain
!
hostname R1
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
banner login #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Unauthorized access to this device is prohibited!

         Twitter @fz3r0_Ops
         Github  Fz3r0    
             
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         fz3r0 - R1 - ZoneA :  Only authorized access!      
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
interface range g0/0 - 2
description << Unused Router Ports >>
shutdown
!
interface gigabitEthernet 0/0
description << Connect SUB-Interfaces 10,20,30,99,100 >>
duplex full
speed 1000
no shutdown
!
interface gigabitEthernet 0/0.10
description << Connect to Subnet 10 >>
encapsulation dot1Q 10
ip address 192.168.10.254 255.255.255.0
no shutdown 
!
interface gigabitEthernet 0/0.20
description << Connect to Subnet 20 >>
encapsulation dot1Q 20
ip address 192.168.20.254 255.255.255.0
no shutdown 
!
interface gigabitEthernet 0/0.30
description << Connect to Subnet 30 >>
encapsulation dot1Q 30
ip address 192.168.30.254 255.255.255.0
no shutdown 
!
interface gigabitEthernet 0/0.99
description << Connect to Subnet 99 >>
encapsulation dot1Q 99
ip address 192.168.99.254 255.255.255.0
no shutdown 
!
interface gigabitEthernet 0/0.100
description << Connect to Subnet 100 >>
encapsulation dot1Q 100
ip address 192.168.100.254 255.255.255.0
no shutdown 
!
interface loopback 0
description << loopback 10.10.10.10 >>
ip address 10.10.10.10 255.255.255.255
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
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

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
description << Trunk | Connect to Gateway  - R1:Gi0/0 >>
switchport encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
duplex full
speed 1000
spanning-tree bpduguard disable
spanning-tree portfast disable
CDP enable
lldp transmit
lldp receive
switchport port-security
switchport port-security maximum 6
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

Router Jalando:

````
service password-encryption
security passwords min-length 10
!
hostname R1
!
login block-for 120 attempts 3 within 60
!
!
enable secret 5 $1$mERr$WvpW0n5HghRrqnrwXCUUl.
!
!
!
!
!
!
ip cef
no ipv6 cef
!
!
!
username root privilege 15 secret 5 $1$mERr$WvpW0n5HghRrqnrwXCUUl.
username user privilege 10 secret 5 $1$mERr$WvpW0n5HghRrqnrwXCUUl.
!
!
license udi pid CISCO2911/K9 sn FTX1524L821-
!
!
!
!
!
!
!
!
!
ip ssh version 2
no ip domain-lookup
ip domain-name fz3r0.domain
!
!
spanning-tree mode pvst
!
!
!
!
!
!
interface Loopback0
 description << loopback 10.10.10.10 >>
 ip address 10.10.10.10 255.255.255.255
!
interface GigabitEthernet0/0
 description << Connect SUB-Interfaces 10,20,30,99,100 >>
 no ip address
 duplex full
 speed 1000
!
interface GigabitEthernet0/0.10
 description << Connect to Subnet 10 >>
 encapsulation dot1Q 10
 ip address 192.168.10.254 255.255.255.0
!
interface GigabitEthernet0/0.20
 description << Connect to Subnet 20 >>
 encapsulation dot1Q 20
 ip address 192.168.20.254 255.255.255.0
!
interface GigabitEthernet0/0.30
 description << Connect to Subnet 30 >>
 encapsulation dot1Q 30
 ip address 192.168.30.254 255.255.255.0
!
interface GigabitEthernet0/0.99
 description << Connect to Subnet 99 >>
 encapsulation dot1Q 99 native
 ip address 192.168.99.254 255.255.255.0
!
interface GigabitEthernet0/0.100
 description << Connect to Subnet 100 >>
 encapsulation dot1Q 100
 ip address 192.168.100.254 255.255.255.0
!
interface GigabitEthernet0/1
 description << Unused Router Ports >>
 no ip address
 duplex auto
 speed auto
 shutdown
!
interface GigabitEthernet0/2
 description << Unused Router Ports >>
 no ip address
 duplex auto
 speed auto
 shutdown
!
interface Vlan1
 no ip address
 shutdown
!
ip classless
!
ip flow-export version 9
!
!
ip access-list extended sl_def_acl
 deny tcp any any eq telnet
 deny tcp any any eq www
 deny tcp any any eq 22
 permit tcp any any eq 22
!
banner login ^C

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Unauthorized access to this device is prohibited!

         Twitter @fz3r0_Ops
         Github  Fz3r0    
             
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

^C
banner motd ^C

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         fz3r0 - R1 - ZoneA :  Only authorized access!      
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

^C
!
!
!
!
line con 0
 password 7 0822455D0A165445415F59
 login
!
line aux 0
!
line vty 0 4
 access-class 8 in
 exec-timeout 5 30
 login local
 transport input ssh
line vty 5 8
 access-class 8 in
 exec-timeout 5 30
 login local
 transport input ssh
!
!
!
end
````

### Jurassic:

````
enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.site_a

hostname R1_GW0_SITE-A

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

banner login #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Fz3r0 - R1 - Site A :  Only authorized access! 

         Twitter @fz3r0_OPs
         Github  Fz3r0    
             
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Fz3r0 - R1 - Site A :  Only authorized access!      
           
         Twitter @fz3r0_OPs
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

interface range g0/0 - 2
description << Unused Router Ports >>
shutdown
exit
!
interface gigabitEthernet 0/0
description << Connect SUB-Interfaces 10,50,60,70,80,90,66 >>
duplex full
speed 1000
no shutdown
exit
!
interface gigabitEthernet 0/0.10
description << VLAN_10 : MANAGEMENT >>
encapsulation dot1Q 10
ip address 10.10.0.1 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.50
description << VLAN_50 : ALFA_OPEN >>
encapsulation dot1Q 50
ip address 10.50.0.1 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.60
description << VLAN_60 : BRAVO_WPA2-PSK >>
encapsulation dot1Q 60
ip address 10.60.0.1 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.70
description << VLAN_70 : CHARLIE_802.1X-EAP >>
encapsulation dot1Q 70
ip address 10.70.0.1 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.80
description << VLAN_80 : DELTA_HOTSPOT-WISPr >>
encapsulation dot1Q 80
ip address 10.80.0.1 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.90
description << VLAN_90 : ECHO_HOTSPOT2.0-PASSPOINT >>
encapsulation dot1Q 90
ip address 10.90.0.1 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.66
description << VLAN_66 : HONEYPOT >>
encapsulation dot1Q 66
ip address 10.66.0.1 255.255.255.0
no shutdown 
exit
!
interface loopback 0
description << loopback 111.111.111.111 >>
ip address 111.111.111.111 255.255.255.255
exit
!
end
copy running-config startup-config
!
exit
!
!


````

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

### References

https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4000/8-2glx/configuration/guide/stp_enha.html#wp1019922
https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst2960/software/release/12-2_37_ey/configuration/guide/scg/swlldp.pdf
https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst9500/software/release/16-10/configuration_guide/sec/b_1610_sec_9500_cg/b_1610_sec_9500_cg_chapter_0101010.html
https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25sg/configuration/guide/conf/port_sec.pdf

---

> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_
