
---

### Fz3r0 Operations  [Networking]

### Fz3r0 Secure Networking Labs - RSTP+ (STP) Spanning Tree in 3-Leaf-Spine (Using only 1 VLAN)

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `STP`

---

#### Packet Tracer Lab Files & Topology

[<< DOWNLOAD FILES >>](https://user-images.githubusercontent.com/94720207/165407633-9cd41970-bc95-4460-be54-8abeee24d083.png)

![1d____VLAN_(3-vlans_1-switch_1-router)_R_OnAStick_TOPOLOGY](https://user-images.githubusercontent.com/94720207/163690161-d79fc452-ffe2-4876-8990-1ef934e81db8.png)

---

### SW1 (ROOT-Bridge | BID Priority 1:`0`) _Distribution Layer_

```
!
enable
configure terminal
spanning-tree mode rapid-pvst
spanning-tree vlan 1 root primary
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 0
exit
wr
!

``` 

### SW2 (Root Backup) | BID Priority 2:`4096`) _Distribution Layer_

```
!
enable
configure terminal
spanning-tree mode rapid-pvst
spanning-tree vlan 1 root secondary
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 4096
exit
wr
!

``` 

### SW3 (STP Bridge) | BID Priority 3:`8192`) _Core Layer_

```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 8192
exit
wr
!

``` 

### SW4 (STP Bridge) | BID Priority 4:`12288`) _Core Layer_

```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 12288
exit
wr
!

``` 

### SW5 (STP Bridge) | BID Priority 5:`16384`) _Access Layer_


```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 16384
exit
wr
!

``` 

### SW6 (STP Bridge) | BID Priority 6:`20480`) _Access Layer_

```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 20480
exit
wr
!

``` 

### SW7 (STP Bridge) | BID Priority 7:`24576`) _Access Layer_

```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 24576
exit
wr
!

``` 

### SW8 (STP Bridge) | BID Priority 8:`28672`) _Access Layer_

```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 28672
exit
wr
!

``` 

### SW9 (STP Bridge) | BID Priority 9:`32768`) _Access Layer_

```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 32768
exit
wr
!

``` 

### SW10 (STP Bridge) | BID Priority 10:`36864`) _Access Layer_

```

!
enable
configure terminal
spanning-tree mode rapid-pvst
!
interface range Fa 0/1 - 24
spanning-tree bpduguard disable
spanning-tree portfast disable
spanning-tree vlan 1 priority 36864
exit
wr
!

```

### Switches: SW4,SW5,SW6,SW7,SW8,SW9 {ALL ACCESS SWITCHES} (Config ALL switches one by one)

```

!
enable
config t
interface range Fa 0/1 - 22
spanning-tree bpduguard enable
spanning-tree portfast
do wr
end
!

```
