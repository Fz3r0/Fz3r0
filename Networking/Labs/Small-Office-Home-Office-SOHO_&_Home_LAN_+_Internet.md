## Fz3r0 Operations

### [Networking]

### Small Office Home Network SOHO

#### Cisco Packet Tracer
---

##### Twitter : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Cisco` `Routing` `Switching` `CLI` `IOS` `CCNA` `CCNP` `Secure Network` `SOHO` `Networking` `Wireless` `WiFi`

---

#### Packet Tracer Lab Files & Topology

- insertar archivo!!

- insertar imagen!!

___

### < ISP >

```

enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.ISP

hostname ISP

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

         fz3r0 - ISP :  Only authorized access!      
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

interface range g0/0 - 2
description << Unused Router Ports >>
shutdown
exit

interface gigabitEthernet 0/0
description << Connect to Home Gateway - Direct (No Sub-Interfaces) >>
ip address 209.165.201.10 /29
duplex full
speed 1000
no shutdown
exit

interface gigabitEthernet 0/2
description << Connect to Internet - SW666 Internet Gi 0/1 >>
ip address 1.1.1.254 /24
duplex auto
speed auto
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

### < Switch 1 - Home Network Switch>

```

enable
configure terminal 

no ip domain-lookup
ip domain-name fz3r0.SOHO-LAN

hostname SW1-SOHO-LAN

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

         fz3r0 - SOHO-LAN :  Only authorized access!      
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#

vlan 10
name VLAN10-SOHO-LAN
vlan 666
name VLAN666-HoneyPot.DeadEnd
exit

interface vlan 100
description << Switch 1 Admin/SSH >>
ip address 192.168.1.253 255.255.255.0
no shutdown 
exit

ip default-gateway 192.168.1.254

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
description << Connect to Home Gateway  - Home-GW:Internet >>
switchport mode access
switchport access vlan 10
duplex auto
speed auto
spanning-tree bpduguard disable
spanning-tree portfast disable
CDP enable
lldp transmit
lldp receive
switchport port-security
switchport port-security maximum 12
switchport port-security mac-address sticky
switchport port-security mac-address sticky F0F0.F0F0.F666
no shutdown
exit

interface range fastEthernet 0/1 - 3
description << VLAN10-SOHO-LAN - SW1 >>
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

end
copy running-config startup-config

exit

```

### < SOHO-LAN: Hosts & End Devices >

- VLAN10-SOHO Hosts Configuration:

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

Printer_1 Network Configuration

IPv4 Address          192.168.10.2
Subnet Mask         255.255.255.0
IPv4 Default Gateway  192.168.10.254
DNS

Laptop_1 Network Configuration

< DHCP - Wireless>

Smartphone_1 Network Configuration

< DHCP - Wireless>

```

### < Public Internet Devices >

```

Public Internet Cloud

< Untouched Switch Simulating WWW Inter-Connection >

DNS Server Cloudflare

IPv4 Address          1.1.1.1/8
Subnet Mask         255.255.255.0
IPv4 Default Gateway  1.1.1.254/8
DNS

github.com Server

IPv4 Address          1.1.1.10/8
Subnet Mask         255.255.255.0
IPv4 Default Gateway  1.1.1.254/8
DNS

google.com Server

IPv4 Address          1.1.1.30/8
Subnet Mask         255.255.255.0
IPv4 Default Gateway  1.1.1.254/8
DNS

```
___

### Notes:

- WATCH ALWAYS GATEWAYS CONFIG ON PC DUE TO PACKET TRACER BUG THAT DELETE THE GATEWAY RANDOMLY!!!!!

- "Public Internet" is just a Switch simulating the Internet-Interconnection

- DNS Server 1.1.1.1 "Cloudflare" is resolving the Domain Names of google.com and github.com

- There's only 1 VLAN configured in the SOHO-LAN... this is because the Home Router of Packet Tracer does not have the option to add Sub-Interfaces for InterVLAN Routing. That's why I configured the Admin/SSH SVI in the same VLAN (VLAN10) as the other devices _(Best Practice is using an unique VLAN for Admin/SSH)._ 

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
