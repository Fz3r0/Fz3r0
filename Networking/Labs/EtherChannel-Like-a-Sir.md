
---

### Fz3r0 Operations  [Networking]

### Fz3r0 Secure Networking Labs - EtherChannel Like a Sir

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `STP`

---

#### Packet Tracer Lab Files & Topology

[**<< DOWNLOAD FILES >>**](https://github.com/Fz3r0/Fz3r0/files/8567524/5___fz3r0_OPs_Routing_._Switching_STP_Bible_3_leaf_datacenter.zip)

![image](https://user-images.githubusercontent.com/94720207/165462904-db720ff7-d0d2-4821-9e05-892510d7443d.png)

---





### SW1 (ROOT-BRIDGE FOR STP)

- SW1 Gi 0/1-2 to > SW2 Gi 0/1-2 **`STATIC`** _(ON)_

- SW1 Fa 0/10-15 to > SW3 Fa 0/10-15 **`LACP`** _(ACTIVE)_

```

enable
configure terminal
hostname SW1-[BID-ROOT-0{0}]
!
no ip domain-lookup
ip domain-name fz3r0.EtherChannel
!
!
!banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         EtherChannel Labs // For more cool stuff:      
           
         Twitter: @fz3r0_Ops
         Github : Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
interface range GigabitEthernet 0/1 - 2
shutdown
description << Gi 0/1-2 FUSSION FOR [PORT-CHANNEL-1] >>
channel-group 1 mode ON
no shutdown
exit
!
!
interface port-channel 1
description << PORT-CHANNEL 1 | Gi 0/1-2(both-sides) >>
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,10,20,40,99,666
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
!
interface range FastEthernet 0/10 - 15
shutdown
description << Fa 0/10-15 FUSSION FOR [PORT-CHANNEL-4] >>
channel-group 4 mode ACTIVE
no shutdown
exit
!
interface port-channel 4
description << PORT-CHANNEL 4 | Fa 0/10-15(both-sides) >>
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,10,20,40,99,666
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
interface FastEthernet 0/24
description << ACCES INTERFACE TO PCS OR SERVERS >>
switchport mode access
switchport access vlan 1
spanning-tree bpduguard enable
spanning-tree portfast
!
spanning-tree bpduguard ENABLE
spanning-tree PORTFAST
no shutdown
exit
!
!
!
spanning-tree mode rapid-pvst
spanning-tree vlan 1 root primary
spanning-tree vlan 1 priority 0
!
!
end
wr
exit
!

```

### SW2

- SW2 Gi 0/1-2 to > SW1 Gi 0/1-2 **`STATIC`** _(ON)_

- SW2 Fa 0/10-13 to > SW4 Fa 0/10-13 **`PAgP`** _(DESIRABLE)_ 

```

enable
configure terminal
hostname SW2-[BID-BCKUP-2{4096}]
!
no ip domain-lookup
ip domain-name fz3r0.EtherChannel
!
!
!banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         EtherChannel Labs // For more cool stuff:      
           
         Twitter: @fz3r0_Ops
         Github : Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
interface range GigabitEthernet 0/1 - 2
shutdown
channel-group 1 mode ON
no shutdown
exit
!
!
interface port-channel 1
description << PORT-CHANNEL 1 | Gi 0/1-2(both-sides) >>
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,10,20,40,99,666
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
!
interface range FastEthernet 0/10 - 13
shutdown
description << Fa 0/10-13 FUSSION FOR [PORT-CHANNEL-2] >>
channel-group 2 mode DESIRABLE
no shutdown
exit
!
interface port-channel 2
description << PORT-CHANNEL 2 | Fa 0/10-13(both-sides) >>
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,10,20,40,99,666
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
interface FastEthernet 0/24
description << ACCES INTERFACE TO PCS OR SERVERS >>
switchport mode access
switchport access vlan 1
spanning-tree bpduguard enable
spanning-tree portfast
!
spanning-tree bpduguard ENABLE
spanning-tree PORTFAST
no shutdown
exit
!
!
!
spanning-tree mode rapid-pvst
spanning-tree vlan 1 priority 4096
!
!
end
wr
exit
!

```

### SW3

- SW3 Fa 0/10-15 to > SW1 Fa 0/10-15 **`LACP`** _(ACTIVE)_

- SW3 Fa 0/1-3 to > SW4 Fa 0/1-3 **`LACP Active/Passive`** _(**active**/passive)_

```

enable
configure terminal
hostname SW3-[BID-3{57344}]
!
no ip domain-lookup
ip domain-name fz3r0.EtherChannel
!
!
!banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         EtherChannel Labs // For more cool stuff:      
           
         Twitter: @fz3r0_Ops
         Github : Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
interface range FastEthernet 0/10 - 15
shutdown
description << Fa 0/10-15 FUSSION FOR [PORT-CHANNEL-4] >>
channel-group 4 mode ACTIVE
no shutdown
exit
!
!
interface port-channel 4
description << PORT-CHANNEL 1 | Fa 0/10-15(both-sides) >>
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,10,20,40,99,666
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
!
interface range FastEthernet 0/1 - 3
shutdown
description << Fa 0/1-3 FUSSION FOR [PORT-CHANNEL-3] >>
channel-group 3 mode ACTIVE
no shutdown
exit
!
!
interface port-channel 3
description << PORT-CHANNEL 4 | Fa 0/1-3(both-sides) >>
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,2,10,20,99
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
interface FastEthernet 0/24
description << ACCES INTERFACE TO PCS OR SERVERS >>
switchport mode access
switchport access vlan 1
spanning-tree bpduguard enable
spanning-tree portfast
!
spanning-tree bpduguard ENABLE
spanning-tree PORTFAST
no shutdown
exit
!
!
!
spanning-tree mode rapid-pvst
spanning-tree vlan 1 priority 57344
!
!
end
wr
exit
!

```

### SW4

- SW4 Fa 0/10-13 to > SW2 Fa 0/10-13 **`PAgP`** _(desirable)_

- SW4 Fa 0/1-3 to > SW3 Fa 0/1-3 **`LACP Active/Passive`** _(active/**passive**)_

```

enable
configure terminal
hostname SW3-[BID-4{61440}]
!
no ip domain-lookup
ip domain-name fz3r0.EtherChannel
!
!
!banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         EtherChannel Labs // For more cool stuff:      
           
         Twitter: @fz3r0_Ops
         Github : Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
interface range FastEthernet 0/10 - 13
description << Fa 0/10-13 FUSSION FOR [PORT-CHANNEL-2] >>
shutdown
channel-group 2 mode DESIRABLE
no shutdown
exit
!
interface port-channel 2
description << PORT-CHANNEL 2 | Fa 0/10-13(both-sides) >>
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,10,20,40,99,666
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
interface range FastEthernet 0/1 - 3
description << Fa 0/1-3 FUSSION FOR [PORT-CHANNEL-3] >>
shutdown
channel-group 3 mode PASSIVE
no shutdown
exit
!
!
interface port-channel 3
shutdown
switchport mode trunk
switchport trunk allowed vlan 1,2,10,20,99
!
spanning-tree bpduguard disable
spanning-tree portfast disable
no shutdown
exit
!
!
interface FastEthernet 0/24
description << ACCES INTERFACE TO PCS OR SERVERS >>
switchport mode access
switchport access vlan 1
spanning-tree bpduguard enable
spanning-tree portfast
!
spanning-tree bpduguard ENABLE
spanning-tree PORTFAST
no shutdown
exit
!
!
!
spanning-tree mode rapid-pvst
spanning-tree vlan 1 priority 61440
!
!
end
wr
exit
!

```

### Security Best Practices & Standards

- Secure and Harden the Network like a sir ;) 


```



```





