

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

### SW5 (STP Bridge) | BID Priority 5:`16384`)

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

### SW6 (STP Bridge) | BID Priority 6:`20480`)

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

### SW7 (STP Bridge) | BID Priority 7:`24576`)

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

### SW8 (STP Bridge) | BID Priority 8:`28672`)

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

### SW9 (STP Bridge) | BID Priority 9:`32768`)

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

### SW10 (STP Bridge) | BID Priority 10:`36864`)

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

### Switches: SW4,SW5,SW6,SW7,SW8,SW9 (Config ALL switches one by one)

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
