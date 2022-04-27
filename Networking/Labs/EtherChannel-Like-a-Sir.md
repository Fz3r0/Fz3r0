
---

### Fz3r0 Operations  [Networking]

### Fz3r0 Secure Networking Labs - EtherChannel Like a Sir

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `EtherChannel` `PortChannel`

---

#### Packet Tracer Lab Files & Topology

[**<< DOWNLOAD FILES >>**]

![image](https://user-images.githubusercontent.com/94720207/165641799-809a40c4-1ad2-4f3f-8487-64767a2913e6.png)


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
!
reload
!
exit
!
!
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
!
reload
!
exit
!
!
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
!
reload
!
exit
!
!
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
!
reload
!
exit
!
!
!


```

### Security Best Practices & Standards

- Secure and Harden the Network like a sir ;) 


```



```

---

### References


---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 








