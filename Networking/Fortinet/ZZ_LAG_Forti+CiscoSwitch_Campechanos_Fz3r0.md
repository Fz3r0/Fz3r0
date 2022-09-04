## Link Aggregation

### Intro

#### Puertos/Interfaces a utilizar:

- **FortiGate**

    - WAN

        - Port1

    - LAG:

        - Port3
        - Port4

- **Cisco Switch**

    - LAG

        - Gi 0/0
        - Gi 0/1

#### VLANs

- VLAN_10_RED
- VLAN_20_BLUE
- VLAN_30_YELLOW
- VLAN_88_Management
- VLAN_99_TrunkNative

## Configuraciones

### Intro

- El Fortigate solo tiene configurada una interfaz via DHCP para entra rpor UI.
- El Cisco Switch no tiene nada, está por defecto. 

### 1 - Crear VLANs en Switch

```
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 30
name VLAN_30_YELLOW  
vlan 40
name VLAN_88_Management  
vlan 99
name VLAN_99_TrunkNative
!
```

### 2 - Asignar Direccionamiento IP a cada Interfaz VLAN (_Excepto la Trunk `99`_)

- NOTA: Hasta el momento todos los puertos se verán down, no malviajarse!!! 

```
!
interface vlan 10
ip address 192.168.10.1 255.255.255.0
no shutdown
exit
interface vlan 20
ip address 192.168.20.1 255.255.255.0
no shutdown
exit
interface vlan 30
ip address 192.168.30.1 255.255.255.0
no shutdown
exit
interface vlan 88
ip address 192.168.88.1 255.255.255.0
no shutdown
exit
```

### 3 - Crear Link Aggregation LAG (EtherChannel)

- Recomendación: `ACTIVO/Static/On ` - `ACTIVO/Static/On` (son sinónimos los 3)
- Esto porque Forti necesita LACP que es open vendors (no PAGP de Cisco)
- En este caso utilizaré `Port-Channel 10`

```
!
interface range gi 0/0 - 1
channel-group 10 mode active
no shutdown 
exit
!
```

### 4 - Configurar LAG (como si fuera cualquier interfaz)

```
!
interface port-channel 10
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,88
no shutdown 
exit
!
```

### 5 - Configurar Interfaz Trunk hacia el SW2-Cisco-DISTRIBUTION

- Nota: Yo usaré la VLAN 99 para no usar la Default Native VLAN 1

```
!
interface gi 3/3
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,88
no shutdown 
exit
!
```

## Switch 1 Full Command Fz3r0 God

```
!
!
enable
configure terminal
!
hostname SW1_Core-F0
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                       "
"              I can read people's minds...             "
"      I have read the pasts, presents and futures      "
"            And each mind that I peered into           "
" was stuffed with the same single object of obssesion  "
"                                                       "
"                -- HECHO EN MEXICO --                  "
"                                                       "
"                 Twitter:  @fz3r0_OPs                  "
"                 GitHub :  Fz3r0                       " 
"                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

$
!
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 30
name VLAN_30_YELLOW  
vlan 88
name VLAN_88_Management  
vlan 99
name VLAN_99_TrunkNative
!
interface vlan 10
ip address 192.168.10.1 255.255.255.0
no shutdown
exit
interface vlan 20
ip address 192.168.20.1 255.255.255.0
no shutdown
exit
interface vlan 30
ip address 192.168.30.1 255.255.255.0
no shutdown
exit
interface vlan 88
ip address 192.168.88.1 255.255.255.0
no shutdown
exit
interface vlan 99
ip address 192.168.99.1 255.255.255.0
no shutdown
exit
!
interface range gi 0/0 - 1
channel-group 10 mode active
no shutdown 
exit
!
interface port-channel 10
description LAG_LAN_FORTI<>SWITCH
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,88
no shutdown 
exit
!
interface gi 3/3
description TRUNK>>>SWITCH2_DISTRIBUTION_GI3/3
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,88
no shutdown 
exit
!
interface gi 1/1
description TEST_CORE_PC
switchport mode access
switchport access vlan 88
no shutdown 
exit
!
end
!
wr
!
!
!
```

### Shows

```
!
show vlan brief
!
show ip interface brief
!
show etherchannel summary
!
```

...

### Full CLI visualization:

```
Switch>
Switch>!
Switch>!
Switch>enable
Switch#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#!
Switch(config)#hostname SW1_Core-F0
SW1_Core-F0(config)#banner motd $
Enter TEXT message.  End with the character '$'.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                       "
"              I can read people's minds...             "
"      I have read the pasts, presents and futures      "
"            And each mind that I peered into           "
" was stuffed with the same single object of obssesion  "
"                                                       "
"                -- HECHO EN MEXICO --                  "
"                                                       "
"                 Twitter:  @fz3r0_OPs                  "
"                 GitHub :  Fz3r0                       " 
"                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

$
SW1_Core-F0(config)#!
SW1_Core-F0(config)#!
SW1_Core-F0(config)#vlan 10
SW1_Core-F0(config-vlan)#name VLAN_10_RED 
SW1_Core-F0(config-vlan)#vlan 20
SW1_Core-F0(config-vlan)#name VLAN_20_BLUE 
SW1_Core-F0(config-vlan)#vlan 30
SW1_Core-F0(config-vlan)#name VLAN_30_YELLOW  
SW1_Core-F0(config-vlan)#vlan 88
SW1_Core-F0(config-vlan)#name VLAN_88_Management  
SW1_Core-F0(config-vlan)#vlan 99
SW1_Core-F0(config-vlan)#name VLAN_99_TrunkNative
SW1_Core-F0(config-vlan)#!
SW1_Core-F0(config-vlan)#interface vlan 10
SW1_Core-F0(config-if)#ip address 192.168.10.1 255.255.255.0
SW1_Core-F0(config-if)#no shutdown
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#interface vlan 20
SW1_Core-F0(config-if)#ip address 192.168.20.1 255.255.255.0
SW1_Core-F0(config-if)#no shutdown
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#interface vlan 30
SW1_Core-F0(config-if)#ip address 192.168.30.1 255.255.255.0
SW1_Core-F0(config-if)#no shutdown
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#interface vlan 88
SW1_Core-F0(config-if)#ip address 192.168.88.1 255.255.255.0
SW1_Core-F0(config-if)#no shutdown
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#interface vlan 99
SW1_Core-F0(config-if)#ip address 192.168.99.1 255.255.255.0
SW1_Core-F0(config-if)#no shutdown
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface range gi 0/0 - 1
SW1_Core-F0(config-if-range)#channel-group 10 mode active
Creating a port-channel interface Port-channel 10

SW1_Core-F0(config-if-range)#no shutdown 
SW1_Core-F0(config-if-range)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface port-channel 10
SW1_Core-F0(config-if)#description LAG_LAN_FORTI<>SWITCH
SW1_Core-F0(config-if)#switchport trunk encapsulation dot1q
SW1_Core-F0(config-if)#switchport mode trunk
SW1_Core-F0(config-if)#switchport trunk native vlan 99
SW1_Core-F0(config-if)#switchport trunk allowed vlan 10,20,30,88
SW1_Core-F0(config-if)#no shutdown 
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface gi 3/3
SW1_Core-F0(config-if)#description TRUNK>>>SWITCH2_DISTRIBUTION_GI3/3
SW1_Core-F0(config-if)#switchport trunk encapsulation dot1q
SW1_Core-F0(config-if)#switchport mode trunk
SW1_Core-F0(config-if)#switchport trunk native vlan 99
SW1_Core-F0(config-if)#switchport trunk allowed vlan 10,20,30,88
SW1_Core-F0(config-if)#no shutdown 
SW1_Core-F0(config-if)#exi
*Sep  4 22:04:23.155: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to down
*Sep  4 22:04:23.486: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to down
*Sep  4 22:04:23.566: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan30, changed state to down
*Sep  4 22:04:23.643: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan88, changed state to down
*Sep  4 22:04:23.724: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan99, changed state to down
*Sep  4 22:04:24.464: %LINK-3-UPDOWN: Interface Vlan10, changed state to down
*Sep  4 22:04:24.542: %LINK-3-UPDOWN: Interface Vlan20, changed state to down
*Sep  4 22:04:24.621: %LINK-3-UPDOWN: Interface Vlan30, changed state to down
*Sep  4 22:04:24.703: %LINK-3-UPDOWN: Interface Vlan88, changed state to down
*Sep  4 22:04:24.783: %LINK-3-UPDOWN: Interface Vlan99, changed state to downt
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface gi 1/1
SW1_Core-F0(config-if)#description TEST_CORE_PC
SW1_Core-F0(config-if)#switchport mode access
SW1_Core-F0(config-if)#switchport access vlan 88
SW1_Core-F0(config-if)#no shutdown 
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#end
SW1_Core-F0#!
SW1_Core-F0#wr
Building configuration...

*Sep  4 22:04:27.332: %SYS-5-CONFIG_I: Configured from console by consoleCompressed configuration from 5366 bytes to 2387 bytes[OK]
SW1_Core-F0#!
SW1_Core-F0#!
SW1_Core-F0#!
*Sep  4 22:04:29.678: %GRUB-5-CONFIG_WRITING: GRUB configuration is being updated on disk. Please wait...
*Sep  4 22:04:30.331: %GRUB-5-CONFIG_WRITTEN: GRUB configuration was written to disk successfully.
SW1_Core-F0#
*Sep  4 22:04:32.530: %LINK-3-UPDOWN: Interface Port-channel10, changed state to up
*Sep  4 22:04:33.530: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel10, changed state to up
SW1_Core-F0#
*Sep  4 22:04:58.263: %LINK-3-UPDOWN: Interface Vlan10, changed state to up
*Sep  4 22:04:58.265: %LINK-3-UPDOWN: Interface Vlan20, changed state to up
*Sep  4 22:04:58.267: %LINK-3-UPDOWN: Interface Vlan30, changed state to up
*Sep  4 22:04:58.268: %LINK-3-UPDOWN: Interface Vlan88, changed state to up
*Sep  4 22:04:59.263: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to up
*Sep  4 22:04:59.266: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to up
*Sep  4 22:04:59.268: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan30, changed state to up
*Sep  4 22:04:59.269: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan88, changed state to up
SW1_Core-F0#

*Sep  4 19:35:50.196: %CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on GigabitEthernet3/3 (99), with Switch GigabitEthernet3/3 (1).

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

<< NOTA: EL MISSMATCH QUE MARCA ES ENTRE SWITCHES Y ES NORMAL YA QUE NO HE CONFIGURADO EL OTRO, NO MALVIAJARSE!!!! >>

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

SW1_Core-F0#

```

- **NOTA: En caso que hasta el momento no se ha conectado físicamente el cableado ni configurado Fortigate se verán las VLANs down y el LACP en espera.**
- **En el momento que se configure y se conecten ambos puertos entre Switch <> Firewall se verá automáticamente la formación del LACP Channel-Port y VLANs UP:**

```
SW1_Core-F0#
SW1_Core-F0#!
SW1_Core-F0#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/2, Gi0/3, Gi1/0, Gi1/2
                                                Gi1/3, Gi2/0, Gi2/1, Gi2/2
                                                Gi2/3, Gi3/0, Gi3/1, Gi3/2
10   VLAN_10_RED                      active    
20   VLAN_20_BLUE                     active    
30   VLAN_30_YELLOW                   active    
88   VLAN_88_Management               active    Gi1/1
99   VLAN_99_TrunkNative              active    
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 
SW1_Core-F0#!
SW1_Core-F0#show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     unassigned      YES unset  up                    up      
GigabitEthernet0/1     unassigned      YES unset  up                    up      
GigabitEthernet0/2     unassigned      YES unset  down                  down    
GigabitEthernet0/3     unassigned      YES unset  down                  down    
GigabitEthernet1/0     unassigned      YES unset  down                  down    
GigabitEthernet1/1     unassigned      YES unset  up                    up      
GigabitEthernet1/2     unassigned      YES unset  down                  down    
GigabitEthernet1/3     unassigned      YES unset  down                  down    
GigabitEthernet2/0     unassigned      YES unset  down                  down    
GigabitEthernet2/1     unassigned      YES unset  down                  down    
GigabitEthernet2/2     unassigned      YES unset  down                  down    
GigabitEthernet2/3     unassigned      YES unset  down                  down    
GigabitEthernet3/0     unassigned      YES unset  down                  down    
GigabitEthernet3/1     unassigned      YES unset  down                  down    
GigabitEthernet3/2     unassigned      YES unset  down                  down    
GigabitEthernet3/3     unassigned      YES unset  up                    up      
Port-channel10         unassigned      YES unset  up                    up      
Vlan10                 192.168.10.1    YES manual up                    up      
Vlan20                 192.168.20.1    YES manual up                    up      
Vlan30                 192.168.30.1    YES manual up                    up      
Vlan88                 192.168.88.1    YES manual up                    up      
          
SW1_Core-F0#
SW1_Core-F0#show etherchannel summary
Flags:  D - down        P - bundled in port-channel
        I - stand-alone s - suspended
        H - Hot-standby (LACP only)
        R - Layer3      S - Layer2
        U - in use      N - not in use, no aggregation
        f - failed to allocate aggregator

        M - not in use, minimum links not met
        m - not in use, port not aggregated due to minimum links not met
        u - unsuitable for bundling
        w - waiting to be aggregated
        d - default port

        A - formed by Auto LAG


Number of channel-groups in use: 1
Number of aggregators:           1

Group  Port-channel  Protocol    Ports
------+-------------+-----------+-----------------------------------------------
10     Po10(SU)        LACP      Gi0/0(P)    Gi0/1(P)    

SW1_Core-F0#!
SW1_Core-F0#
```

## Switch 2: Distribution

```
!
!
enable
configure terminal
!
hostname SW2_Distr-F0
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                       "
"              I can read people's minds...             "
"      I have read the pasts, presents and futures      "
"            And each mind that I peered into           "
" was stuffed with the same single object of obssesion  "
"                                                       "
"                -- HECHO EN MEXICO --                  "
"                                                       "
"                 Twitter:  @fz3r0_OPs                  "
"                 GitHub :  Fz3r0                       " 
"                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

$
!
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 30
name VLAN_30_YELLOW 
vlan 88
name VLAN_88_Management  
vlan 99
name VLAN_99_TrunkNative
!
interface vlan 10
ip address 192.168.10.2 255.255.255.0
no shutdown
exit
interface vlan 20
ip address 192.168.20.2 255.255.255.0
no shutdown
exit
interface vlan 30
ip address 192.168.30.2 255.255.255.0
no shutdown
exit
interface vlan 88
ip address 192.168.88.2 255.255.255.0
no shutdown
exit
interface vlan 99
ip address 192.168.99.2 255.255.255.0
no shutdown
exit
!
interface Gi 0/0
description VLAN_10_Gi_SW
switchport mode access
switchport access vlan 10
no shutdown
exit
interface Gi 0/1
description VLAN_20_Gi_SW
switchport mode access
switchport access vlan 20
no shutdown
exit
interface Gi 0/2
description VLAN_30_Gi_SW
switchport mode access
switchport access vlan 30
no shutdown
exit
interface Gi 0/3
description VLAN_88_Gi_SW
switchport mode access
switchport access vlan 88
no shutdown
exit
!
interface gi 3/3
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,88
no shutdown 
exit
!
end
!
wr
!
!
!
```

- CLI view

```
Switch>
Switch>!
Switch>enable
Switch#configure terminal
Enter configuration commands, one per line.  End with CNTL/Z.
Switch(config)#!
Switch(config)#hostname SW2_Distr-F0
SW2_Distr-F0(config)#banner motd $
Enter TEXT message.  End with the character '$'.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                       "
"              I can read people's minds...             "
"      I have read the pasts, presents and futures      "
"            And each mind that I peered into           "
" was stuffed with the same single object of obssesion  "
"                                                       "
"                -- HECHO EN MEXICO --                  "
"                                                       "
"                 Twitter:  @fz3r0_OPs                  "
"                 GitHub :  Fz3r0                       " 
"                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

$
SW2_Distr-F0(config)#!
SW2_Distr-F0(config)#!
SW2_Distr-F0(config)#vlan 10
SW2_Distr-F0(config-vlan)#name VLAN_10_RED 
SW2_Distr-F0(config-vlan)#vlan 20
SW2_Distr-F0(config-vlan)#name VLAN_20_BLUE 
SW2_Distr-F0(config-vlan)#vlan 30
SW2_Distr-F0(config-vlan)#name VLAN_30_YELLOW 
SW2_Distr-F0(config-vlan)#vlan 88
SW2_Distr-F0(config-vlan)#name VLAN_88_Management  
SW2_Distr-F0(config-vlan)#vlan 99
SW2_Distr-F0(config-vlan)#name VLAN_99_TrunkNative
SW2_Distr-F0(config-vlan)#!
SW2_Distr-F0(config-vlan)#interface vlan 10
SW2_Distr-F0(config-if)#ip address 192.168.10.2 255.255.255.0
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface vlan 20
SW2_Distr-F0(config-if)#ip address 192.168.20.2 255.255.255.0
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface vlan 30
SW2_Distr-F0(config-if)#ip address 192.168.30.2 255.255.255.0
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface vlan 88
SW2_Distr-F0(config-if)#ip address 192.168.88.2 255.255.255.0
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface vlan 99
SW2_Distr-F0(config-if)#ip address 192.168.99.2 255.255.255.0
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#!
SW2_Distr-F0(config)#interface Gi 0/0
SW2_Distr-F0(config-if)#description VLAN_10_Gi_SW
SW2_Distr-F0(config-if)#switchport mode access
SW2_Distr-F0(config-if)#switchport access vlan 10
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface Gi 0/1
SW2_Distr-F0(config-if)#description VLAN_20_Gi_SW
SW2_Distr-F0(config-if)#switchport mode access
SW2_Distr-F0(config-if)#switchport access vlan 20
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface Gi 0/2
SW2_Distr-F0(config-if)#description VLAN_30_Gi_SW
SW2_Distr-F0(config-if)#switchport mode access
SW2_Distr-F0(config-if)#switchport access vlan 30
SW2_Distr-F0(
*Sep  4 22:07:51.733: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to up
*Sep  4 22:07:52.043: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to up
*Sep  4 22:07:52.141: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan30, changed state to up
*Sep  4 22:07:52.227: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan88, changed state to up
*Sep  4 22:07:52.312: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan99, changed state to up
*Sep  4 22:07:53.018: %LINK-3-UPDOWN: Interface Vlan10, changed state to up
*Sep  4 22:07:53.113: %LINK-3-UPDOWN: Interface Vlan20, changed state to up
*Sep  4 22:07:53.202: %LINK-3-UPDOWN: Interface Vlan30, changed state to up
*Sep  4 22:07:53.289: %LINK-3-UPDOWN: Interface Vlan88, changed state to up
*Sep  4 22:07:53.374: %LINK-3-UPDOWN: Interface Vlan99, changed state to upconfig-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface Gi 0/3
SW2_Distr-F0(config-if)#description VLAN_88_Gi_SW
SW2_Distr-F0(config-if)#switchport mode access
SW2_Distr-F0(config-if)#switchport access vlan 88
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#!
SW2_Distr-F0(config)#interface gi 3/3
SW2_Distr-F0(config-if)#switchport trunk encapsulation dot1q
SW2_Distr-F0(config-if)#switchport mode trunk
SW2_Distr-F0(config-if)#switchport trunk native vlan 99
SW2_Distr-F0(config-if)#switchport trunk allowed vlan 10,20,30,88
SW2_Distr-F0(config-if)#no shutdown 
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#!
SW2_Distr-F0(config)#end
SW2_Distr-F0#!
SW2_Distr-F0#wr
Building configuration...

*Sep  4 22:07:55.772: %SYS-5-CONFIG_I: Configured from console by consoleCompressed configuration from 5021 bytes to 2201 bytes[OK]
SW2_Distr-F0#!
SW2_Distr-F0#!
SW2_Distr-F0#!
SW2_Distr-F0#
*Sep  4 22:07:57.824: %GRUB-5-CONFIG_WRITING: GRUB configuration is being updated on disk. Please wait...
*Sep  4 22:07:58.501: %GRUB-5-CONFIG_WRITTEN: GRUB configuration was written to disk successfully.
SW2_Distr-F0#
```

## Fortigate Config

### Fortigate Backup CLI

```
#config-version=FGVMK6-6.2.0-FW-build0866-190328:opmode=0:vdom=0:user=admin
#conf_file_ver=185495342590113
#buildno=0866
#global_vdom=1
config system global
    set alias "Fz3r0-Fortigate"
    set hostname "Fz3r0-Fortigate"
    set timezone 04
end
config system accprofile
    edit "super_admin"
        set secfabgrp read-write
        set ftviewgrp read-write
        set authgrp read-write
        set sysgrp read-write
        set netgrp read-write
        set loggrp read-write
        set fwgrp read-write
        set vpngrp read-write
        set utmgrp read-write
        set wanoptgrp read-write
        set wifi read-write
    next
    edit "prof_admin"
        set secfabgrp read-write
        set ftviewgrp read-write
        set authgrp read-write
        set sysgrp read-write
        set netgrp read-write
        set loggrp read-write
        set fwgrp read-write
        set vpngrp read-write
        set utmgrp read-write
        set wanoptgrp read-write
        set wifi read-write
    next
end
config system interface
    edit "port1"
        set vdom "root"
        set mode dhcp
        set allowaccess ping https ssh http fgfm radius-acct capwap
        set type physical
        set alias "Internerd_Site1"
        set fortiheartbeat enable
        set snmp-index 1
    next
    edit "port2"
        set vdom "root"
        set ip 190.204.108.1 255.255.255.252
        set allowaccess ping
        set type physical
        set alias "WAN1"
        set lldp-reception enable
        set role wan
        set snmp-index 2
    next
    edit "port3"
        set vdom "root"
        set ip 60.120.211.1 255.255.255.252
        set allowaccess ping
        set type physical
        set alias "WAN2"
        set lldp-reception enable
        set role wan
        set snmp-index 3
    next
    edit "port4"
        set vdom "root"
        set type physical
        set snmp-index 4
    next
    edit "port5"
        set vdom "root"
        set type physical
        set snmp-index 5
    next
    edit "port6"
        set vdom "root"
        set type physical
        set snmp-index 6
    next
    edit "ssl.root"
        set vdom "root"
        set type tunnel
        set alias "SSL VPN interface"
        set snmp-index 7
    next
    edit "LAG_LAN_Site1"
        set vdom "root"
        set allowaccess ping https capwap
        set type aggregate
        set member "port5" "port6"
        set alias "LAG_LAN_Site1_LACP"
        set device-identification enable
        set lldp-transmission enable
        set role lan
        set snmp-index 8
    next
    edit "VLAN_10_FG"
        set vdom "root"
        set ip 192.168.10.10 255.255.255.0
        set allowaccess ping https capwap
        set alias "VLAN_10_FG"
        set device-identification enable
        set role lan
        set snmp-index 9
        set interface "LAG_LAN_Site1"
        set vlanid 10
    next
    edit "VLAN_20_FG"
        set vdom "root"
        set ip 192.168.20.10 255.255.255.0
        set allowaccess ping https capwap
        set alias "VLAN_20_FG"
        set device-identification enable
        set role lan
        set snmp-index 10
        set interface "LAG_LAN_Site1"
        set vlanid 20
    next
    edit "VLAN_30_FG"
        set vdom "root"
        set ip 192.168.30.10 255.255.255.0
        set allowaccess ping https capwap
        set alias "VLAN_30_FG"
        set device-identification enable
        set role lan
        set snmp-index 11
        set interface "LAG_LAN_Site1"
        set vlanid 30
    next
    edit "VLAN_40_FG"
        set vdom "root"
        set ip 192.168.40.10 255.255.255.0
        set allowaccess ping https capwap
        set alias "VLAN_40_FG"
        set device-identification enable
        set role lan
        set snmp-index 12
        set interface "LAG_LAN_Site1"
        set vlanid 40
    next
    edit "VLAN_88_MGMT_FG"
        set vdom "root"
        set ip 192.168.88.10 255.255.255.0
        set allowaccess ping https capwap
        set alias "VLAN_88_MGMT_FG"
        set device-identification enable
        set role lan
        set snmp-index 13
        set interface "LAG_LAN_Site1"
        set vlanid 88
    next
end
config system custom-language
    edit "en"
        set filename "en"
    next
    edit "fr"
        set filename "fr"
    next
    edit "sp"
        set filename "sp"
    next
    edit "pg"
        set filename "pg"
    next
    edit "x-sjis"
        set filename "x-sjis"
    next
    edit "big5"
        set filename "big5"
    next
    edit "GB2312"
        set filename "GB2312"
    next
    edit "euc-kr"
        set filename "euc-kr"
    next
end
config system admin
    edit "admin"
        set accprofile "super_admin"
        set vdom "root"
        config gui-dashboard
            edit 1
                set name "Status"
                set vdom "root"
                set permanent enable
                config widget
                    edit 1
                        set width 1
                        set height 1
                    next
                    edit 2
                        set type licinfo
                        set x-pos 1
                        set width 1
                        set height 1
                    next
                    edit 3
                        set type vminfo
                        set x-pos 2
                        set width 1
                        set height 1
                    next
                    edit 4
                        set type forticloud
                        set x-pos 3
                        set width 1
                        set height 1
                    next
                    edit 5
                        set type security-fabric
                        set x-pos 4
                        set width 1
                        set height 1
                    next
                    edit 6
                        set type security-fabric-ranking
                        set x-pos 5
                        set width 1
                        set height 1
                    next
                    edit 7
                        set type admins
                        set x-pos 6
                        set width 1
                        set height 1
                    next
                    edit 8
                        set type cpu-usage
                        set x-pos 7
                        set width 2
                        set height 1
                    next
                    edit 9
                        set type memory-usage
                        set x-pos 8
                        set width 2
                        set height 1
                    next
                    edit 10
                        set type sessions
                        set x-pos 9
                        set width 2
                        set height 1
                    next
                end
            next
            edit 2
                set name "Top Usage LAN/DMZ"
                set vdom "root"
                set layout-type fixed
                set columns 12
                config widget
                    edit 1
                        set type fortiview
                        set width 6
                        set height 3
                        set fortiview-type "source"
                        set fortiview-sort-by "bytes"
                        set fortiview-timeframe "hour"
                        set fortiview-visualization "table"
                    next
                    edit 2
                        set type fortiview
                        set x-pos 1
                        set width 6
                        set height 3
                        set fortiview-type "destination"
                        set fortiview-sort-by "sessions"
                        set fortiview-timeframe "hour"
                        set fortiview-visualization "table"
                    next
                    edit 3
                        set type fortiview
                        set x-pos 2
                        set width 6
                        set height 3
                        set fortiview-type "application"
                        set fortiview-sort-by "bytes"
                        set fortiview-timeframe "hour"
                        set fortiview-visualization "table"
                    next
                    edit 4
                        set type fortiview
                        set x-pos 3
                        set width 6
                        set height 3
                        set fortiview-type "website"
                        set fortiview-sort-by "sessions"
                        set fortiview-timeframe "hour"
                        set fortiview-visualization "table"
                    next
                end
            next
            edit 3
                set name "Security"
                set vdom "root"
                set layout-type fixed
                set columns 12
                config widget
                    edit 1
                        set type fortiview
                        set width 6
                        set height 3
                        set fortiview-type "compromisedHosts"
                        set fortiview-sort-by "verdict"
                        set fortiview-timeframe "hour"
                        set fortiview-visualization "table"
                    next
                    edit 2
                        set type fortiview
                        set x-pos 1
                        set width 6
                        set height 3
                        set fortiview-type "threats"
                        set fortiview-sort-by "threatLevel"
                        set fortiview-timeframe "hour"
                        set fortiview-visualization "table"
                    next
                    edit 3
                        set type vulnerability-summary
                        set x-pos 2
                        set width 3
                        set height 3
                    next
                    edit 4
                        set type host-scan-summary
                        set x-pos 3
                        set width 3
                        set height 3
                    next
                    edit 5
                        set type fortiview
                        set x-pos 4
                        set width 6
                        set height 3
                        set fortiview-type "endpointDevices"
                        set fortiview-sort-by "vulnerabilities"
                        set fortiview-timeframe "hour"
                        set fortiview-visualization "table"
                    next
                end
            next
        end
    next
end
config system sso-admin
end
config system ha
    set override disable
end
config system storage
    edit "Virtual-Disk"
        set status enable
        set media-status enable
        set order 1
        set partition "LOGUSEDXDC47A175"
        set device "/dev/vdb1"
        set size 8062
        set usage log
    next
end
config system dns
    set primary 8.8.8.8
    set secondary 8.8.4.4
end
config system replacemsg-image
    edit "logo_fnet"
        set image-type gif
        set image-base64 ''
    next
    edit "logo_fguard_wf"
        set image-type gif
        set image-base64 ''
    next
    edit "logo_fw_auth"
        set image-base64 ''
    next
    edit "logo_v2_fnet"
        set image-base64 ''
    next
    edit "logo_v2_fguard_wf"
        set image-base64 ''
    next
    edit "logo_v2_fguard_app"
        set image-base64 ''
    next
end
config system replacemsg mail "email-av-fail"
end
config system replacemsg mail "email-block"
end
config system replacemsg mail "email-dlp-subject"
end
config system replacemsg mail "email-dlp-ban"
end
config system replacemsg mail "email-filesize"
end
config system replacemsg mail "email-file-filter"
end
config system replacemsg mail "partial"
end
config system replacemsg mail "smtp-block"
end
config system replacemsg mail "smtp-filesize"
end
config system replacemsg mail "email-decompress-limit"
end
config system replacemsg mail "smtp-decompress-limit"
end
config system replacemsg http "bannedword"
end
config system replacemsg http "url-block"
end
config system replacemsg http "urlfilter-err"
end
config system replacemsg http "infcache-block"
end
config system replacemsg http "http-block"
end
config system replacemsg http "http-filesize"
end
config system replacemsg http "http-dlp-ban"
end
config system replacemsg http "http-archive-block"
end
config system replacemsg http "http-contenttypeblock"
end
config system replacemsg http "https-invalid-cert-block"
end
config system replacemsg http "https-untrusted-cert-block"
end
config system replacemsg http "https-blacklisted-cert-block"
end
config system replacemsg http "http-client-block"
end
config system replacemsg http "http-client-filesize"
end
config system replacemsg http "http-client-bannedword"
end
config system replacemsg http "http-post-block"
end
config system replacemsg http "http-client-archive-block"
end
config system replacemsg http "switching-protocols-block"
end
config system replacemsg webproxy "deny"
end
config system replacemsg webproxy "user-limit"
end
config system replacemsg webproxy "auth-challenge"
end
config system replacemsg webproxy "auth-login-fail"
end
config system replacemsg webproxy "auth-group-info-fail"
end
config system replacemsg webproxy "http-err"
end
config system replacemsg webproxy "auth-ip-blackout"
end
config system replacemsg ftp "ftp-av-fail"
end
config system replacemsg ftp "ftp-dl-blocked"
end
config system replacemsg ftp "ftp-dl-filesize"
end
config system replacemsg ftp "ftp-dl-dlp-ban"
end
config system replacemsg ftp "ftp-explicit-banner"
end
config system replacemsg ftp "ftp-dl-archive-block"
end
config system replacemsg nntp "nntp-av-fail"
end
config system replacemsg nntp "nntp-dl-blocked"
end
config system replacemsg nntp "nntp-dl-filesize"
end
config system replacemsg nntp "nntp-dlp-subject"
end
config system replacemsg nntp "nntp-dlp-ban"
end
config system replacemsg nntp "email-decompress-limit"
end
config system replacemsg fortiguard-wf "ftgd-block"
end
config system replacemsg fortiguard-wf "http-err"
end
config system replacemsg fortiguard-wf "ftgd-ovrd"
end
config system replacemsg fortiguard-wf "ftgd-quota"
end
config system replacemsg fortiguard-wf "ftgd-warning"
end
config system replacemsg spam "ipblocklist"
end
config system replacemsg spam "smtp-spam-dnsbl"
end
config system replacemsg spam "smtp-spam-feip"
end
config system replacemsg spam "smtp-spam-helo"
end
config system replacemsg spam "smtp-spam-emailblack"
end
config system replacemsg spam "smtp-spam-mimeheader"
end
config system replacemsg spam "reversedns"
end
config system replacemsg spam "smtp-spam-bannedword"
end
config system replacemsg spam "smtp-spam-ase"
end
config system replacemsg spam "submit"
end
config system replacemsg alertmail "alertmail-virus"
end
config system replacemsg alertmail "alertmail-block"
end
config system replacemsg alertmail "alertmail-nids-event"
end
config system replacemsg alertmail "alertmail-crit-event"
end
config system replacemsg alertmail "alertmail-disk-full"
end
config system replacemsg admin "pre_admin-disclaimer-text"
end
config system replacemsg admin "post_admin-disclaimer-text"
end
config system replacemsg auth "auth-disclaimer-page-1"
end
config system replacemsg auth "auth-disclaimer-page-2"
end
config system replacemsg auth "auth-disclaimer-page-3"
end
config system replacemsg auth "auth-reject-page"
end
config system replacemsg auth "auth-login-page"
end
config system replacemsg auth "auth-login-failed-page"
end
config system replacemsg auth "auth-token-login-page"
end
config system replacemsg auth "auth-token-login-failed-page"
end
config system replacemsg auth "auth-success-msg"
end
config system replacemsg auth "auth-challenge-page"
end
config system replacemsg auth "auth-keepalive-page"
end
config system replacemsg auth "auth-portal-page"
end
config system replacemsg auth "auth-password-page"
end
config system replacemsg auth "auth-fortitoken-page"
end
config system replacemsg auth "auth-next-fortitoken-page"
end
config system replacemsg auth "auth-email-token-page"
end
config system replacemsg auth "auth-sms-token-page"
end
config system replacemsg auth "auth-email-harvesting-page"
end
config system replacemsg auth "auth-email-failed-page"
end
config system replacemsg auth "auth-cert-passwd-page"
end
config system replacemsg auth "auth-guest-print-page"
end
config system replacemsg auth "auth-guest-email-page"
end
config system replacemsg auth "auth-success-page"
end
config system replacemsg auth "auth-block-notification-page"
end
config system replacemsg auth "auth-quarantine-page"
end
config system replacemsg auth "auth-qtn-reject-page"
end
config system replacemsg sslvpn "sslvpn-login"
end
config system replacemsg sslvpn "sslvpn-header"
end
config system replacemsg sslvpn "sslvpn-limit"
end
config system replacemsg sslvpn "hostcheck-error"
end
config system replacemsg device-detection-portal "device-detection-failure"
end
config system replacemsg nac-quar "nac-quar-virus"
end
config system replacemsg nac-quar "nac-quar-dos"
end
config system replacemsg nac-quar "nac-quar-ips"
end
config system replacemsg nac-quar "nac-quar-dlp"
end
config system replacemsg nac-quar "nac-quar-admin"
end
config system replacemsg nac-quar "nac-quar-app"
end
config system replacemsg traffic-quota "per-ip-shaper-block"
end
config system replacemsg utm "virus-html"
end
config system replacemsg utm "client-virus-html"
end
config system replacemsg utm "virus-text"
end
config system replacemsg utm "dlp-html"
end
config system replacemsg utm "dlp-text"
end
config system replacemsg utm "appblk-html"
end
config system replacemsg utm "ipsblk-html"
end
config system replacemsg utm "ipsfail-html"
end
config system replacemsg utm "exe-text"
end
config system replacemsg utm "waf-html"
end
config system replacemsg utm "outbreak-prevention-html"
end
config system replacemsg utm "outbreak-prevention-text"
end
config system replacemsg icap "icap-req-resp"
end
config system snmp sysinfo
end
config firewall internet-service-definition
end
config firewall internet-service-cat-definition
end
config system cluster-sync
end
config system fortiguard
    set update-server-location usa
    set sdns-server-ip "208.91.112.220" 
end
config ips global
end
config system email-server
    set server "notification.fortinet.net"
    set port 465
    set security smtps
end
config system session-helper
    edit 1
        set name pptp
        set protocol 6
        set port 1723
    next
    edit 2
        set name h323
        set protocol 6
        set port 1720
    next
    edit 3
        set name ras
        set protocol 17
        set port 1719
    next
    edit 4
        set name tns
        set protocol 6
        set port 1521
    next
    edit 5
        set name tftp
        set protocol 17
        set port 69
    next
    edit 6
        set name rtsp
        set protocol 6
        set port 554
    next
    edit 7
        set name rtsp
        set protocol 6
        set port 7070
    next
    edit 8
        set name rtsp
        set protocol 6
        set port 8554
    next
    edit 9
        set name ftp
        set protocol 6
        set port 21
    next
    edit 10
        set name mms
        set protocol 6
        set port 1863
    next
    edit 11
        set name pmap
        set protocol 6
        set port 111
    next
    edit 12
        set name pmap
        set protocol 17
        set port 111
    next
    edit 13
        set name sip
        set protocol 17
        set port 5060
    next
    edit 14
        set name dns-udp
        set protocol 17
        set port 53
    next
    edit 15
        set name rsh
        set protocol 6
        set port 514
    next
    edit 16
        set name rsh
        set protocol 6
        set port 512
    next
    edit 17
        set name dcerpc
        set protocol 6
        set port 135
    next
    edit 18
        set name dcerpc
        set protocol 17
        set port 135
    next
    edit 19
        set name mgcp
        set protocol 17
        set port 2427
    next
    edit 20
        set name mgcp
        set protocol 17
        set port 2727
    next
end
config system auto-install
    set auto-install-config enable
    set auto-install-image enable
end
config system ntp
    set ntpsync enable
end
config system object-tagging
    edit "default"
    next
end
config switch-controller traffic-policy
    edit "quarantine"
        set description "Rate control for quarantined traffic"
        set guaranteed-bandwidth 163840
        set guaranteed-burst 8192
        set maximum-burst 163840
        set cos-queue 0
        set id 1
    next
    edit "sniffer"
        set description "Rate control for sniffer mirrored traffic"
        set guaranteed-bandwidth 50000
        set guaranteed-burst 8192
        set maximum-burst 163840
        set cos-queue 0
        set id 2
    next
end
config system settings
end
config system dhcp server
    edit 1
        set dns-service default
        set default-gateway 192.168.10.10
        set netmask 255.255.255.0
        set interface "VLAN_10_FG"
        config ip-range
            edit 1
                set start-ip 192.168.10.50
                set end-ip 192.168.10.79
            next
        end
        set timezone-option default
    next
    edit 2
        set dns-service default
        set default-gateway 192.168.20.10
        set netmask 255.255.255.0
        set interface "VLAN_20_FG"
        config ip-range
            edit 1
                set start-ip 192.168.20.50
                set end-ip 192.168.20.79
            next
        end
        set timezone-option default
    next
    edit 3
        set dns-service default
        set default-gateway 192.168.30.10
        set netmask 255.255.255.0
        set interface "VLAN_30_FG"
        config ip-range
            edit 1
                set start-ip 192.168.30.50
                set end-ip 192.168.30.79
            next
        end
        set timezone-option default
    next
    edit 4
        set dns-service default
        set default-gateway 192.168.40.10
        set netmask 255.255.255.0
        set interface "VLAN_40_FG"
        config ip-range
            edit 1
                set start-ip 192.168.40.50
                set end-ip 192.168.40.79
            next
        end
        set timezone-option default
    next
    edit 5
        set dns-service default
        set default-gateway 192.168.88.10
        set netmask 255.255.255.0
        set interface "VLAN_88_MGMT_FG"
        config ip-range
            edit 1
                set start-ip 192.168.88.50
                set end-ip 192.168.88.79
            next
        end
        set timezone-option default
    next
end
config firewall address
    edit "none"
        set uuid 7cde7e30-2717-51ed-3b80-995198ff0a13
        set subnet 0.0.0.0 255.255.255.255
    next
    edit "login.microsoftonline.com"
        set uuid 7cde8344-2717-51ed-0d70-86f59d61536f
        set type fqdn
        set fqdn "login.microsoftonline.com"
    next
    edit "login.microsoft.com"
        set uuid 7cde863c-2717-51ed-ed48-be3219a629e0
        set type fqdn
        set fqdn "login.microsoft.com"
    next
    edit "login.windows.net"
        set uuid 7cde87e0-2717-51ed-606c-ded58183e516
        set type fqdn
        set fqdn "login.windows.net"
    next
    edit "gmail.com"
        set uuid 7cde8966-2717-51ed-1787-3e39d61c4b6a
        set type fqdn
        set fqdn "gmail.com"
    next
    edit "wildcard.google.com"
        set uuid 7cde8ae2-2717-51ed-7f13-6e0d15142b3c
        set type wildcard-fqdn
        set wildcard-fqdn "*.google.com"
    next
    edit "wildcard.dropbox.com"
        set uuid 7cde8c54-2717-51ed-4b9c-d9d8b497ee5c
        set type wildcard-fqdn
        set wildcard-fqdn "*.dropbox.com"
    next
    edit "all"
        set uuid 7ce1ec3c-2717-51ed-fac3-5238ee4c4f5a
    next
    edit "FIREWALL_AUTH_PORTAL_ADDRESS"
        set uuid 7ce1ed36-2717-51ed-5a6d-c02b88efd95d
        set visibility disable
    next
    edit "FABRIC_DEVICE"
        set uuid 7ce1ede0-2717-51ed-4694-42480b614fe3
        set comment "IPv4 addresses of Fabric Devices."
    next
    edit "SSLVPN_TUNNEL_ADDR1"
        set uuid 7ce235de-2717-51ed-3b6a-30910864b82a
        set type iprange
        set associated-interface "ssl.root"
        set start-ip 10.212.134.200
        set end-ip 10.212.134.210
    next
    edit "LAG_LAN_Site1 address"
        set uuid e33e81ea-2c8d-51ed-ff25-4483958313c0
        set type interface-subnet
        set interface "LAG_LAN_Site1"
    next
    edit "VLAN_10_FG address"
        set uuid 401f75a4-2c8e-51ed-abd3-3803a951f337
        set type interface-subnet
        set subnet 192.168.10.10 255.255.255.0
        set interface "VLAN_10_FG"
    next
    edit "VLAN_20_FG address"
        set uuid 62bf4b7a-2c8e-51ed-fe40-2f905e42537d
        set type interface-subnet
        set subnet 192.168.20.10 255.255.255.0
        set interface "VLAN_20_FG"
    next
    edit "VLAN_30_FG address"
        set uuid 74d63850-2c8e-51ed-91ad-2e8175662724
        set type interface-subnet
        set subnet 192.168.30.10 255.255.255.0
        set interface "VLAN_30_FG"
    next
    edit "VLAN_40_FG address"
        set uuid 8753d9f6-2c8e-51ed-ef05-30e23d2b8812
        set type interface-subnet
        set subnet 192.168.40.10 255.255.255.0
        set interface "VLAN_40_FG"
    next
    edit "VLAN_88_MGMT_FG address"
        set uuid a54f2618-2c8e-51ed-8d88-97fa19e5e458
        set type interface-subnet
        set subnet 192.168.88.10 255.255.255.0
        set interface "VLAN_88_MGMT_FG"
    next
end
config firewall multicast-address
    edit "all"
        set start-ip 224.0.0.0
        set end-ip 239.255.255.255
    next
    edit "all_hosts"
        set start-ip 224.0.0.1
        set end-ip 224.0.0.1
    next
    edit "all_routers"
        set start-ip 224.0.0.2
        set end-ip 224.0.0.2
    next
    edit "Bonjour"
        set start-ip 224.0.0.251
        set end-ip 224.0.0.251
    next
    edit "EIGRP"
        set start-ip 224.0.0.10
        set end-ip 224.0.0.10
    next
    edit "OSPF"
        set start-ip 224.0.0.5
        set end-ip 224.0.0.6
    next
end
config firewall address6
    edit "SSLVPN_TUNNEL_IPv6_ADDR1"
        set uuid 7ce2373c-2717-51ed-60b3-75995d291fd5
        set ip6 fdff:ffff::/120
    next
    edit "all"
        set uuid 7d6658a0-2717-51ed-e7bd-0b26789664e5
    next
    edit "none"
        set uuid 7d665d28-2717-51ed-6db7-387233fbdb45
        set ip6 ::/128
    next
end
config firewall multicast-address6
    edit "all"
        set ip6 ff00::/8
    next
end
config firewall addrgrp
    edit "G Suite"
        set uuid 7cde8e8e-2717-51ed-4584-a821782923dd
        set member "gmail.com" "wildcard.google.com"
    next
    edit "Microsoft Office 365"
        set uuid 7cde9230-2717-51ed-2520-b2a7232d0e8e
        set member "login.microsoftonline.com" "login.microsoft.com" "login.windows.net"
    next
end
config firewall wildcard-fqdn custom
    edit "adobe"
        set uuid 7cf2f13a-2717-51ed-dcdf-24d7f45293c2
        set wildcard-fqdn "*.adobe.com"
    next
    edit "Adobe Login"
        set uuid 7cf2f1e4-2717-51ed-2b76-9414140adb55
        set wildcard-fqdn "*.adobelogin.com"
    next
    edit "android"
        set uuid 7cf2f284-2717-51ed-1659-7323326db4d8
        set wildcard-fqdn "*.android.com"
    next
    edit "apple"
        set uuid 7cf2f31a-2717-51ed-55d6-191b0194fc29
        set wildcard-fqdn "*.apple.com"
    next
    edit "appstore"
        set uuid 7cf2f3b0-2717-51ed-4cfd-c799beb36eff
        set wildcard-fqdn "*.appstore.com"
    next
    edit "auth.gfx.ms"
        set uuid 7cf2f450-2717-51ed-beb0-1ed61ceb0852
        set wildcard-fqdn "*.auth.gfx.ms"
    next
    edit "citrix"
        set uuid 7cf2f4f0-2717-51ed-91a4-c781705a05f1
        set wildcard-fqdn "*.citrixonline.com"
    next
    edit "dropbox.com"
        set uuid 7cf2f590-2717-51ed-2e4e-174fabede9af
        set wildcard-fqdn "*.dropbox.com"
    next
    edit "eease"
        set uuid 7cf2f630-2717-51ed-3efc-f0b9e296a18d
        set wildcard-fqdn "*.eease.com"
    next
    edit "firefox update server"
        set uuid 7cf2f6d0-2717-51ed-5e81-79186875971f
        set wildcard-fqdn "aus*.mozilla.org"
    next
    edit "fortinet"
        set uuid 7cf2f770-2717-51ed-a1d8-602a595aa145
        set wildcard-fqdn "*.fortinet.com"
    next
    edit "googleapis.com"
        set uuid 7cf2f806-2717-51ed-f9db-bdfecbe19898
        set wildcard-fqdn "*.googleapis.com"
    next
    edit "google-drive"
        set uuid 7cf2f89c-2717-51ed-1cad-02689868a97e
        set wildcard-fqdn "*drive.google.com"
    next
    edit "google-play2"
        set uuid 7cf2f946-2717-51ed-5928-d5c363402c84
        set wildcard-fqdn "*.ggpht.com"
    next
    edit "google-play3"
        set uuid 7cf2f9e6-2717-51ed-c9ba-385b0a5c3ea8
        set wildcard-fqdn "*.books.google.com"
    next
    edit "Gotomeeting"
        set uuid 7cf2fa90-2717-51ed-cc42-d77672024e07
        set wildcard-fqdn "*.gotomeeting.com"
    next
    edit "icloud"
        set uuid 7cf2fb94-2717-51ed-6aae-ac01c7af0747
        set wildcard-fqdn "*.icloud.com"
    next
    edit "itunes"
        set uuid 7cf2fc3e-2717-51ed-b212-5dc40cf84a9f
        set wildcard-fqdn "*itunes.apple.com"
    next
    edit "microsoft"
        set uuid 7cf2fce8-2717-51ed-8aa0-7dd87ffbeede
        set wildcard-fqdn "*.microsoft.com"
    next
    edit "skype"
        set uuid 7cf2fd92-2717-51ed-285e-3183d7997330
        set wildcard-fqdn "*.messenger.live.com"
    next
    edit "softwareupdate.vmware.com"
        set uuid 7cf2fe28-2717-51ed-8c95-13dce369cb92
        set wildcard-fqdn "*.softwareupdate.vmware.com"
    next
    edit "verisign"
        set uuid 7cf2fec8-2717-51ed-dd22-be84e90be905
        set wildcard-fqdn "*.verisign.com"
    next
    edit "Windows update 2"
        set uuid 7cf2ff72-2717-51ed-3f94-7d6b3000f8a8
        set wildcard-fqdn "*.windowsupdate.com"
    next
    edit "live.com"
        set uuid 7cf30026-2717-51ed-2ae5-0b02a50a501a
        set wildcard-fqdn "*.live.com"
    next
    edit "google-play"
        set uuid 7cf300c6-2717-51ed-65dd-5ed782ad7c42
        set wildcard-fqdn "*play.google.com"
    next
    edit "update.microsoft.com"
        set uuid 7cf30170-2717-51ed-38cc-6a6e5fdc36c9
        set wildcard-fqdn "*update.microsoft.com"
    next
    edit "swscan.apple.com"
        set uuid 7cf30210-2717-51ed-5a0f-97b61d5fe545
        set wildcard-fqdn "*swscan.apple.com"
    next
    edit "autoupdate.opera.com"
        set uuid 7cf30300-2717-51ed-d4e9-7b6fca197045
        set wildcard-fqdn "*autoupdate.opera.com"
    next
end
config firewall service category
    edit "General"
        set comment "General services."
    next
    edit "Web Access"
        set comment "Web access."
    next
    edit "File Access"
        set comment "File access."
    next
    edit "Email"
        set comment "Email services."
    next
    edit "Network Services"
        set comment "Network services."
    next
    edit "Authentication"
        set comment "Authentication service."
    next
    edit "Remote Access"
        set comment "Remote access."
    next
    edit "Tunneling"
        set comment "Tunneling service."
    next
    edit "VoIP, Messaging & Other Applications"
        set comment "VoIP, messaging, and other applications."
    next
    edit "Web Proxy"
        set comment "Explicit web proxy."
    next
end
config firewall service custom
    edit "ALL"
        set category "General"
        set protocol IP
    next
    edit "ALL_TCP"
        set category "General"
        set tcp-portrange 1-65535
    next
    edit "ALL_UDP"
        set category "General"
        set udp-portrange 1-65535
    next
    edit "ALL_ICMP"
        set category "General"
        set protocol ICMP
        unset icmptype
    next
    edit "ALL_ICMP6"
        set category "General"
        set protocol ICMP6
        unset icmptype
    next
    edit "GRE"
        set category "Tunneling"
        set protocol IP
        set protocol-number 47
    next
    edit "AH"
        set category "Tunneling"
        set protocol IP
        set protocol-number 51
    next
    edit "ESP"
        set category "Tunneling"
        set protocol IP
        set protocol-number 50
    next
    edit "AOL"
        set visibility disable
        set tcp-portrange 5190-5194
    next
    edit "BGP"
        set category "Network Services"
        set tcp-portrange 179
    next
    edit "DHCP"
        set category "Network Services"
        set udp-portrange 67-68
    next
    edit "DNS"
        set category "Network Services"
        set tcp-portrange 53
        set udp-portrange 53
    next
    edit "FINGER"
        set visibility disable
        set tcp-portrange 79
    next
    edit "FTP"
        set category "File Access"
        set tcp-portrange 21
    next
    edit "FTP_GET"
        set category "File Access"
        set tcp-portrange 21
    next
    edit "FTP_PUT"
        set category "File Access"
        set tcp-portrange 21
    next
    edit "GOPHER"
        set visibility disable
        set tcp-portrange 70
    next
    edit "H323"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 1720 1503
        set udp-portrange 1719
    next
    edit "HTTP"
        set category "Web Access"
        set tcp-portrange 80
    next
    edit "HTTPS"
        set category "Web Access"
        set tcp-portrange 443
    next
    edit "IKE"
        set category "Tunneling"
        set udp-portrange 500 4500
    next
    edit "IMAP"
        set category "Email"
        set tcp-portrange 143
    next
    edit "IMAPS"
        set category "Email"
        set tcp-portrange 993
    next
    edit "Internet-Locator-Service"
        set visibility disable
        set tcp-portrange 389
    next
    edit "IRC"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 6660-6669
    next
    edit "L2TP"
        set category "Tunneling"
        set tcp-portrange 1701
        set udp-portrange 1701
    next
    edit "LDAP"
        set category "Authentication"
        set tcp-portrange 389
    next
    edit "NetMeeting"
        set visibility disable
        set tcp-portrange 1720
    next
    edit "NFS"
        set category "File Access"
        set tcp-portrange 111 2049
        set udp-portrange 111 2049
    next
    edit "NNTP"
        set visibility disable
        set tcp-portrange 119
    next
    edit "NTP"
        set category "Network Services"
        set tcp-portrange 123
        set udp-portrange 123
    next
    edit "OSPF"
        set category "Network Services"
        set protocol IP
        set protocol-number 89
    next
    edit "PC-Anywhere"
        set category "Remote Access"
        set tcp-portrange 5631
        set udp-portrange 5632
    next
    edit "PING"
        set category "Network Services"
        set protocol ICMP
        set icmptype 8
        unset icmpcode
    next
    edit "TIMESTAMP"
        set protocol ICMP
        set visibility disable
        set icmptype 13
        unset icmpcode
    next
    edit "INFO_REQUEST"
        set protocol ICMP
        set visibility disable
        set icmptype 15
        unset icmpcode
    next
    edit "INFO_ADDRESS"
        set protocol ICMP
        set visibility disable
        set icmptype 17
        unset icmpcode
    next
    edit "ONC-RPC"
        set category "Remote Access"
        set tcp-portrange 111
        set udp-portrange 111
    next
    edit "DCE-RPC"
        set category "Remote Access"
        set tcp-portrange 135
        set udp-portrange 135
    next
    edit "POP3"
        set category "Email"
        set tcp-portrange 110
    next
    edit "POP3S"
        set category "Email"
        set tcp-portrange 995
    next
    edit "PPTP"
        set category "Tunneling"
        set tcp-portrange 1723
    next
    edit "QUAKE"
        set visibility disable
        set udp-portrange 26000 27000 27910 27960
    next
    edit "RAUDIO"
        set visibility disable
        set udp-portrange 7070
    next
    edit "REXEC"
        set visibility disable
        set tcp-portrange 512
    next
    edit "RIP"
        set category "Network Services"
        set udp-portrange 520
    next
    edit "RLOGIN"
        set visibility disable
        set tcp-portrange 513:512-1023
    next
    edit "RSH"
        set visibility disable
        set tcp-portrange 514:512-1023
    next
    edit "SCCP"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 2000
    next
    edit "SIP"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 5060
        set udp-portrange 5060
    next
    edit "SIP-MSNmessenger"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 1863
    next
    edit "SAMBA"
        set category "File Access"
        set tcp-portrange 139
    next
    edit "SMTP"
        set category "Email"
        set tcp-portrange 25
    next
    edit "SMTPS"
        set category "Email"
        set tcp-portrange 465
    next
    edit "SNMP"
        set category "Network Services"
        set tcp-portrange 161-162
        set udp-portrange 161-162
    next
    edit "SSH"
        set category "Remote Access"
        set tcp-portrange 22
    next
    edit "SYSLOG"
        set category "Network Services"
        set udp-portrange 514
    next
    edit "TALK"
        set visibility disable
        set udp-portrange 517-518
    next
    edit "TELNET"
        set category "Remote Access"
        set tcp-portrange 23
    next
    edit "TFTP"
        set category "File Access"
        set udp-portrange 69
    next
    edit "MGCP"
        set visibility disable
        set udp-portrange 2427 2727
    next
    edit "UUCP"
        set visibility disable
        set tcp-portrange 540
    next
    edit "VDOLIVE"
        set visibility disable
        set tcp-portrange 7000-7010
    next
    edit "WAIS"
        set visibility disable
        set tcp-portrange 210
    next
    edit "WINFRAME"
        set visibility disable
        set tcp-portrange 1494 2598
    next
    edit "X-WINDOWS"
        set category "Remote Access"
        set tcp-portrange 6000-6063
    next
    edit "PING6"
        set protocol ICMP6
        set visibility disable
        set icmptype 128
        unset icmpcode
    next
    edit "MS-SQL"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 1433 1434
    next
    edit "MYSQL"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 3306
    next
    edit "RDP"
        set category "Remote Access"
        set tcp-portrange 3389
    next
    edit "VNC"
        set category "Remote Access"
        set tcp-portrange 5900
    next
    edit "DHCP6"
        set category "Network Services"
        set udp-portrange 546 547
    next
    edit "SQUID"
        set category "Tunneling"
        set tcp-portrange 3128
    next
    edit "SOCKS"
        set category "Tunneling"
        set tcp-portrange 1080
        set udp-portrange 1080
    next
    edit "WINS"
        set category "Remote Access"
        set tcp-portrange 1512
        set udp-portrange 1512
    next
    edit "RADIUS"
        set category "Authentication"
        set udp-portrange 1812 1813
    next
    edit "RADIUS-OLD"
        set visibility disable
        set udp-portrange 1645 1646
    next
    edit "CVSPSERVER"
        set visibility disable
        set tcp-portrange 2401
        set udp-portrange 2401
    next
    edit "AFS3"
        set category "File Access"
        set tcp-portrange 7000-7009
        set udp-portrange 7000-7009
    next
    edit "TRACEROUTE"
        set category "Network Services"
        set udp-portrange 33434-33535
    next
    edit "RTSP"
        set category "VoIP, Messaging & Other Applications"
        set tcp-portrange 554 7070 8554
        set udp-portrange 554
    next
    edit "MMS"
        set visibility disable
        set tcp-portrange 1755
        set udp-portrange 1024-5000
    next
    edit "KERBEROS"
        set category "Authentication"
        set tcp-portrange 88 464
        set udp-portrange 88 464
    next
    edit "LDAP_UDP"
        set category "Authentication"
        set udp-portrange 389
    next
    edit "SMB"
        set category "File Access"
        set tcp-portrange 445
    next
    edit "NONE"
        set visibility disable
        set tcp-portrange 0
    next
    edit "webproxy"
        set proxy enable
        set category "Web Proxy"
        set protocol ALL
        set tcp-portrange 0-65535:0-65535
    next
end
config firewall service group
    edit "Email Access"
        set member "DNS" "IMAP" "IMAPS" "POP3" "POP3S" "SMTP" "SMTPS"
    next
    edit "Web Access"
        set member "DNS" "HTTP" "HTTPS"
    next
    edit "Windows AD"
        set member "DCE-RPC" "DNS" "KERBEROS" "LDAP" "LDAP_UDP" "SAMBA" "SMB"
    next
    edit "Exchange Server"
        set member "DCE-RPC" "DNS" "HTTPS"
    next
end
config vpn certificate ca
end
config vpn certificate local
    edit "Fortinet_CA_SSL"
        set password ENC c59xfBvv5giNERqdXIiYxvVGJ566VlXX1qs476c8JpYYr8WcIbVVbK0s32olg9bsxZslLSsBKDHOEw6UPvPeqw8rGNuixUTNH5OLOO68wuxfZNqvKK+0U+tV8kzogiCJllDggji+v4jpFaQa+L7uR46THSmcHSaFsQbF/9rGogy7IHfPrb6enmhfkCLxbWvrFQK/6g==
        set comments "This is the default CA certificate the SSL Inspection will use when generating new server certificates."
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBtDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIZybEZhcEafICAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECOg788S/bvozBIIBYKVkvtbsrGmK
7rhfIP2krVOivlNx5p8D+EGMOhSNZAUHjov/qWdAcgrnzv/+ROg5ySZC+XYa7VO2
I6XPNHM89o/0cT/BTRwbitqxY6THCwTHp7xA4zSCi8dXq4CajeZ6/A3oS4PyLcVR
ziukUKkj2qp5BhQnZUV2KCqfOaJEKuzWqMZQNeFCufeC+7Db3p6wby9hkqyj739w
7Kdwlttuu7mzr0CYkZSJQbXNIpIlOPHWGfG3VlQMFwHZOsoE6HaLTIkETyQZ6XAp
bL3O6aODvsXhFkxkqmu/ybuVXmPs76giw1gmS56fmkvjC1ep5leGT3JpNlEzeqHX
qo2wMU2qoAVclvrYZ8vRFt4Rm0m7vyJdiLwdcmlhqDBgjZxtqxfIQR/FKPrt27jh
GymVdg47WXGcFGTKm6+xkfOn+imywWoliG0Oqu5gH3hY7ESOE6ZJMATEFDylgO1K
B+sJ00SJ/N0=
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICXDCCAgagAwIBAgIIBGk6LJLbQNwwDQYJKoZIhvcNAQELBQAwgakxCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MR4wHAYDVQQLDBVDZXJ0aWZpY2F0ZSBBdXRob3Jp
dHkxGTAXBgNVBAMMEEZHVk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1
cHBvcnRAZm9ydGluZXQuY29tMB4XDTIyMDkwNDE3MDUyMloXDTMyMDkwNDE3MDUy
MlowgakxCzAJBgNVBAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQH
DAlTdW5ueXZhbGUxETAPBgNVBAoMCEZvcnRpbmV0MR4wHAYDVQQLDBVDZXJ0aWZp
Y2F0ZSBBdXRob3JpdHkxGTAXBgNVBAMMEEZHVk1FVlZBRERTS0hWMUExIzAhBgkq
hkiG9w0BCQEWFHN1cHBvcnRAZm9ydGluZXQuY29tMFwwDQYJKoZIhvcNAQEBBQAD
SwAwSAJBAMP8aW8nLHK5FgYNahg/O/ASsQWh1l8bvLwpropjZ0ZO861DAh8xQ9HL
3SR9P9id8eMOtlB7HpapktA3/Qt6IWECAwEAAaMQMA4wDAYDVR0TBAUwAwEB/zAN
BgkqhkiG9w0BAQsFAANBAD2Ka5HexkaiGUoD4VMfvxCfsXlY9/wlWdCahduKFlG+
26VGwHR77iHcbndKN7sCYzDCtA042zSsIcFBPTCbXfc=
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_CA_Untrusted"
        set password ENC 8NmFUqFL13+jeRno4ZzOtI+yo+Dqf3grRJhwMKJ+9qU6O+ANpiMSLR26HmsMqx7yeWIi6sUspAPui8CyR8dG/QG16bHq1zuAGkZQYO5mP24cstBOmu0x62ilHvUii8qbKixynxfJgS5nLifdDra6ULj2ksQSUm47Zo++ZQ9rFklgrVl4Z0s9gLT1+h/lDyLo2RxYlw==
        set comments "This is the default CA certificate the SSL Inspection will use when generating new server certificates."
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBtDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIocWhGACApRwCAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECAiQWplsHKz3BIIBYMPpbX0DOfwX
XkRhnLbSizH9Ke+oWSIstUryey03J7i1ElzFc42m3RTirAJTceNSktKL66jZPSGD
thBYgiR5fwAGK/6Q/+uwa+evfhj80Np3SWqyjKaPfAWt4d4CccAoY4i8YOXGWCT1
OxdZnrx7m5VP0EyAyWvrqOfQZqI2lznkdHMHsLy+SCZLOpPbhwmgCmrJMfwom8gZ
UUlB44qT0pB7sxKH65h00l7kOLm/Hd9WPzl7qoeh/Fq895L3LzHfY87hhIV8uwPi
v+kragbu0u6ZUNenANqhYw3m5SvX0ur2dfpLk72IKXmXdbpdeoiBwXbbOjjqpwRC
kSzVjjzke6ob1OLrT6l5vsae2qYQ9p7FuR+KbJUKpso+jD7oOLzjYCvrV9GO1TMl
eq/3okH5ucsaPSpTtB1t7Uo24O0uuTswtrZkAY0oww+k0is1gS1lhBdP9B9NpLxd
2YSGRqTChpI=
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICZjCCAhCgAwIBAgIIdVfN+zufTjgwDQYJKoZIhvcNAQELBQAwga4xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MR4wHAYDVQQLDBVDZXJ0aWZpY2F0ZSBBdXRob3Jp
dHkxHjAcBgNVBAMMFUZvcnRpbmV0IFVudHJ1c3RlZCBDQTEjMCEGCSqGSIb3DQEJ
ARYUc3VwcG9ydEBmb3J0aW5ldC5jb20wHhcNMjIwOTA0MTcwNTIyWhcNMzIwOTA0
MTcwNTIyWjCBrjELMAkGA1UEBhMCVVMxEzARBgNVBAgMCkNhbGlmb3JuaWExEjAQ
BgNVBAcMCVN1bm55dmFsZTERMA8GA1UECgwIRm9ydGluZXQxHjAcBgNVBAsMFUNl
cnRpZmljYXRlIEF1dGhvcml0eTEeMBwGA1UEAwwVRm9ydGluZXQgVW50cnVzdGVk
IENBMSMwIQYJKoZIhvcNAQkBFhRzdXBwb3J0QGZvcnRpbmV0LmNvbTBcMA0GCSqG
SIb3DQEBAQUAA0sAMEgCQQDxkptPYXffZDNglGj0z5QIINgynQjk0Zqz3aAFyeJg
/parRUG7hAKc3KcXH4AttvXnqtxXTAB/Q2hgHNFbd+GLAgMBAAGjEDAOMAwGA1Ud
EwQFMAMBAf8wDQYJKoZIhvcNAQELBQADQQCbK3t++ra/WIHFy3Y5pZRuJ7VsCQIJ
LCZMP5Vh3L4J/vkuBv8/Fsc2pKXuQrRT0bNH7D+5Xpv6NIwHCejg84+9
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_SSL"
        set password ENC nmXgEyXt74f28scPWLEOnlPsU8/VAeVunRrXS6pK55maK9GfnXy9ydxLqKW5S0BTkLbwpELrG0KtEa5WkSDmah+4iPOGYe393Y8eEXY1P/RIiVSs0phTqGjNpzEfyRuODK/1bi7DBrmqbeCtQ1fYxDHX9PGiaOjJkkl3IZTEdz9Eb8R1fWqv4jz0RFtbo/lh8ZcIWw==
        set comments "This certificate is embedded in the hardware at the factory and is unique to this unit. "
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBtDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIMwsveE9ibIsCAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECNn6psavyIRTBIIBYGG/Yo0Tm0lW
e0+ndeqD/k/Cz7OcyE4jU/PnuuWOCka/vi3Lde2Oa0yYSQJp4w4+wudtM4u9TncX
N+NYc7YgSRi2FBB3DgpUIOHrhlTZYYOvqjcQdyoc27qiNKFO6rerl8ePTYj4PbNm
By0z+ObUfdFW1fLAGLMTm7fT9ZDyBkn6oWq8m8DQXEdID4VGmbaTWZASdFutavwb
jSOg3vilmveyi66/nyy5cgpZFC8+FSu7jvx87Y/5YIOnXcH37EEtXQaz6HNuQqz/
IGFTlpCSf1+++my3Ryrx1n2B66Qbf/AkcG3ImNr06pGEM6lQr8QDqIDfTXAR+p80
5BJWEwEGR15mn2A5yRZWcSK+7+WOBirUP+CKn29kKCxkHcByqBLzT+fR8VD51No9
RWnYhrh7WTuji0E8X4AIOCHqLFSR6jkhgC9QAkfPoIHPsoP+X/wZXWFlzwam2e5h
WdgYR68Q0hs=
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICQTCCAeugAwIBAgIIHXiYDOc2o2swDQYJKoZIhvcNAQELBQAwgZ0xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMM
EEZHVk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGlu
ZXQuY29tMB4XDTIyMDkwNDE3MDUyMloXDTMyMDkwNDE3MDUyMlowgZ0xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMM
EEZHVk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGlu
ZXQuY29tMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBALa9fbA4gkm5c94H5L5+L+xr
Bfj4DgjTEgZpk6c1Ehmm84Omokkt0+g86m1dCQTAahcv2UDEMnUE8JPEcPRzE+MC
AwEAAaMNMAswCQYDVR0TBAIwADANBgkqhkiG9w0BAQsFAANBAJdGt2Gvhd1f0P+L
UdXXmohEw+ATOX40Ikl+BdWHbjklZwTvbugC3rJqXIkcz41UCC5oZK7CUb0tXkUR
a6VzkJ8=
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_SSL_RSA1024"
        set password ENC zmixZF21eXlkEUarrXOznptLbl0HHcHrJuebGDymb3WUwAC1DUC+yzDbuCThIke8cN9remeIV4N7uCbOpcWtnMklxNrMhg8CfrzgTKKxL4i0IM7P6NK6DZ1oWHylPGtuSJKtgbPFKZkfBXUh3RohlUAnUJrw31F2si/BEIV/kb0dHYE1cIUHVEBN7bvJSFHWLbngVQ==
        set comments "This certificate is embedded in the hardware at the factory and is unique to this unit. "
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBtDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQIq7nVduK/RtwCAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECHIQzDN1JI2RBIIBYC45fyPozSrr
OZqWrMo8rfJhgiprTogcdqrtoSEnpXtzflOAl/Futciz2nT9md4CHsEwshkNB1MU
dMEvUYt8V/jaZQRvzSf2Anmkc1uZhBCn6Dl+NMXPxJrMtDSA70Feblze8i2gy8J9
u0Q8lF3unQQRtTsvkyq/VD/s3INcO2+wXLjE3Md7j3nlKcMb+Y4O62WRGV02pcRH
AEXMFHGoauoGsqc9iYUb71v/efg75gscjA9vscwG15iUvQnAqzex2d+1pGm/fnHN
EQ7Ri8VaXRpmTCLOqUVmK4Eyfk9FfSg7wrPck8mA8YS0v/GPFhTwS4bwDCWaDpo5
5tObPs17+l12mszNXPb97VBDs5w2UG4JC9GY7fQf6wlW0QgVBQhUGgm+7A2RMQNH
rFDZYz2aRSRUWHJLvPWHuqAICqN3gAYuUDH7YWm8csauMIQ9mMoGr6efreVv+MZd
uW4LAzBdZns=
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICQTCCAeugAwIBAgIIbLWWFuCytSQwDQYJKoZIhvcNAQELBQAwgZ0xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMM
EEZHVk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGlu
ZXQuY29tMB4XDTIyMDkwNDE3MDUyMloXDTMyMDkwNDE3MDUyMlowgZ0xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMM
EEZHVk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGlu
ZXQuY29tMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAM5jlvmWKbHECSMQyTbZ5B+J
QsizKLaTEjXx8fVYVRjH8nqK7iaWBflzxvdtw5bVaFdv2kTvAP1VT8oYY5hxLV8C
AwEAAaMNMAswCQYDVR0TBAIwADANBgkqhkiG9w0BAQsFAANBAFcTC1JT2HHDZHAb
Jht78zLcJqP57DFRCPdNbq79CM+f+2t2Z9ARs7at6u4Du3wy+yuOnFweBA+i3MQM
AmkM22A=
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_SSL_RSA2048"
        set password ENC UV9Zq/L11lygOLxFjg/jPfLQT+mejGcCOg2EJ1hRGFCzIGo4DuPQOI5/ibulaHxEk2sET8LhCynWdm60wycYWQMpnX/XNdguaqZhpBifVNfchX4VzIbVNIzvxUjWAuTEVLo2Rt/KuH9sxB+fYKI8VCN4RH+wxZrnSKIu7BudA78+1ev0Sz06GD++Eu47iVSWhW9W3Q==
        set comments "This certificate is embedded in the hardware at the factory and is unique to this unit. "
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBrDBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQINVWOXORApM4CAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECOA7OQIRr3ThBIIBWO0CS7SBVR/x
twhBXAdqpCI2rzOynea34si8mzljyrWfX768iIhhDm/nHW09rM4V0qrUoJQsCtrC
lvRDkxReUP00pkxEAwRT1/OxZNqnoPYK9FAe7Va55HxOe0Cxs1PjcJcnwiDxNQuc
tUEP0fLt1QM0zMU86V9+OHb/qwv+HlzpxKZ8XD0uA0YA+i70x8TyVaH5tq15+LGx
T6ATnaQXwZYo3wXpe+Rx3vhdxXMCltpKgq+0V1RqSU+UICDDOfd8JJJ1qe/nu6ZU
3DNP1jbTfbRL/7YQqK/8oOkOfsuU2O7+8onKBayQ1zP6MHs+kgnGYzktDyaJs11m
yCnBFv//xN9CkwGcMaEiC31vuV7ASpVdHRoGAMIjT13tmyYEZPBEIR3h4Vvl9lLu
WN5itngK14oR9GC5Sfwu9JQjriS9kTdbnzU9ESR1QXgkbbD/Txn2zTXp8SDbF3tp
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICQTCCAeugAwIBAgIIbDymOQjhn2owDQYJKoZIhvcNAQELBQAwgZ0xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMM
EEZHVk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGlu
ZXQuY29tMB4XDTIyMDkwNDE3MDUyMloXDTMyMDkwNDE3MDUyMlowgZ0xCzAJBgNV
BAYTAlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUx
ETAPBgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMM
EEZHVk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGlu
ZXQuY29tMFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKHmJxW8mjqIIGDQKUhQiCIA
dkElO7S4AmzxN+weu1BTDmTQJT7wjLCLntVkNpMqo8fz2kpYOzdvYrpHXAMjji0C
AwEAAaMNMAswCQYDVR0TBAIwADANBgkqhkiG9w0BAQsFAANBAHt9v0KP5P9BmZas
y/xcmqpJgROn1+kDATCtgw/NHsGLYL0Ikxul9zYCC8ftaZpVVB4esiJStqpumT4J
6Rk5Tk8=
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_SSL_DSA1024"
        set password ENC nnnkjXjI/O+MUPZVFpXSWZOV4wJnNPnoNAmtx8UZHMrkFYcX3RkLRAncJKPpMaUw1bIdGn/8noOljbi7VlvkgqhKjipsgZTUma7cTcMAiiaIZJc8q0dieEJSvEtX2vAj7Ci4h7v0om4s89G9RQ0Kb2yDt5knhPougC6V6D7h5p4SGQM6qkBPLY1WdOwE58NBTaqe6A==
        set comments "This certificate is embedded in the hardware at the factory and is unique to this unit. "
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBIzBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQICl5QDnQb04ICAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECN7R1ONh+HgdBIHQT0MKYOFftWSF
eKOfA+vIwoZGM3NUbPpMoz4GEjTuQnijci5+XTGDce0yAVPdPmH0mgCEODkZ6NuD
/hoeI60wTK5Kfq+wKKtZsyur0kR4jlr1+BgNzAiWLi984vUfwkOvEUxYKWU+QKU3
a9ldsr7GVAIeLd0xWZ5zDe6MOdrbZ8torOxmp+NDUrRTMarNj/zGEnne8tn3YtNZ
7MvjRXUFVKtMgorCLiJKnPIVVuzTuTWM17zrYaE8MhwbsFmk42KbuAZTXn0kvlo4
InnIw2rl9Q==
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICwzCCAoCgAwIBAgIIX7wTtB617IMwCwYJYIZIAWUDBAMCMIGdMQswCQYDVQQG
EwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTESMBAGA1UEBwwJU3Vubnl2YWxlMREw
DwYDVQQKDAhGb3J0aW5ldDESMBAGA1UECwwJRm9ydGlHYXRlMRkwFwYDVQQDDBBG
R1ZNRVZWQUREU0tIVjFBMSMwIQYJKoZIhvcNAQkBFhRzdXBwb3J0QGZvcnRpbmV0
LmNvbTAeFw0yMjA5MDQxNzA1MjJaFw0zMjA5MDQxNzA1MjJaMIGdMQswCQYDVQQG
EwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTESMBAGA1UEBwwJU3Vubnl2YWxlMREw
DwYDVQQKDAhGb3J0aW5ldDESMBAGA1UECwwJRm9ydGlHYXRlMRkwFwYDVQQDDBBG
R1ZNRVZWQUREU0tIVjFBMSMwIQYJKoZIhvcNAQkBFhRzdXBwb3J0QGZvcnRpbmV0
LmNvbTCB8jCBqQYHKoZIzjgEATCBnQJBAKCBkVEX+9qjWm0G0Dnh6uXwg1K2iumI
6Xcj4gkxfJezqtIV3YE7y0LG9jpvq6CNUMw0LFjcQ1KjEsUvHMST6vECFQDmB8+7
jGIXwW1O344WIQu7Jb7gXQJBAJDIZJp4oT336zW48I+cwmdSww42lO2vv+19Nopa
StThYloG906FPQpFvLJnz5yPldZsHoYX8MRmRYZUaXWooREDRAACQQCd141UIj7U
fW4i7FO9IOoA/vgch5p6XXnjCw0grck7uTzJ20tBUJB4fNr0/MM3fOffoPt+iTpf
mY0trQ9aa2Iqow0wCzAJBgNVHRMEAjAAMAsGCWCGSAFlAwQDAgMwADAtAhUA5R0y
L6xcMokSrFRBJBmieSnWXV0CFBo6X0RfXCI36yhxG0cfoxnfrMgM
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_SSL_DSA2048"
        set password ENC mg76UkZvlZe7mq81fUmR6/KhBU9NA4jTHwnKFtf1SqUQ74FVEJWGzwJ3MXrcTwM1qjqrAPy8mlviXcjGKsgF3Nchs3M81HzvWTF+td9OOBoIK5noxPvYX3GRoAvYEmhAxkksUaSZ+WkbWH+67CzntOgVH/2dnE7DrcEZ6i+AVDVclkk10KrwUWuwjq/gcIZF07Wgdw==
        set comments "This certificate is embedded in the hardware at the factory and is unique to this unit. "
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBIzBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQI5lUs/h1xiFcCAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECP5o9WzDxhvGBIHQSf0ByDxTGCfK
wtJxfy3AK5WAmGXsN0xOpEcVRGDS1ieAESCiZt9t16xUFuDT8KfS/KbsooooECqL
B0TfXPk/zfgN+00wojxRrph4dPgbb2IpRXqewOrxDHHudvskLutiztbMnpBbmjUo
4Ap1KqBKq33ei+W0pvnpyzIA4oqe7H1qJWkS7nKrSZTpfGxVo4W2f+tMvxJ6Jf51
C+6PYdzX3kGuX0v3PbExb+npGFpiDldJJQB/AfR3KrqTvlK1Ao+1Lt1IsLw+d6yv
TP+ImtOPJg==
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICwTCCAn6gAwIBAgIIVBDw087P7eIwCwYJYIZIAWUDBAMCMIGdMQswCQYDVQQG
EwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTESMBAGA1UEBwwJU3Vubnl2YWxlMREw
DwYDVQQKDAhGb3J0aW5ldDESMBAGA1UECwwJRm9ydGlHYXRlMRkwFwYDVQQDDBBG
R1ZNRVZWQUREU0tIVjFBMSMwIQYJKoZIhvcNAQkBFhRzdXBwb3J0QGZvcnRpbmV0
LmNvbTAeFw0yMjA5MDQxNzA1MjJaFw0zMjA5MDQxNzA1MjJaMIGdMQswCQYDVQQG
EwJVUzETMBEGA1UECAwKQ2FsaWZvcm5pYTESMBAGA1UEBwwJU3Vubnl2YWxlMREw
DwYDVQQKDAhGb3J0aW5ldDESMBAGA1UECwwJRm9ydGlHYXRlMRkwFwYDVQQDDBBG
R1ZNRVZWQUREU0tIVjFBMSMwIQYJKoZIhvcNAQkBFhRzdXBwb3J0QGZvcnRpbmV0
LmNvbTCB8DCBqAYHKoZIzjgEATCBnAJBALa9TyZXHPUCf8Wb7TSpGu4pIHLPMVt7
RCoAnHe/WIVtu0YSSs+tzPuxfKkVLJXQ4PH1pbe75ANi6JCJfgctohECFQDcthFQ
A7MlaPZwKj3Pefz9kGNMYwJAT6q8YBDkIlXPJmJ9UdmNqLzM9ZGuNSfQXzDHRmll
hhhc03XCy+gmXt9FXNoWONnc1/Nr34xiYhqMISiTvGBjGQNDAAJADj4gOzvZ069R
eqfsLPQN+7LyUfDkH2RRkY9iQvQhTriCXkZjWUnugleZVyCi5tg9vsJMZO/vRkNh
MW3r95O9/KMNMAswCQYDVR0TBAIwADALBglghkgBZQMEAwIDMAAwLQIVANSYSuqO
LDuiOoadtQYR1DkQ4LU8AhQlGngkYB9T8CccnYv1DQi9Oy6Lvg==
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_SSL_ECDSA256"
        set password ENC KbLMDa1FYwMRkxl7MpaVaXk/xigFAbFFfikFe//6jwjVbhcRrvSgSgVqOGgqy9fAWmC5btQOU3flyK9GJo/iyTVykch0qhvU7UTHzmlDdsK6VGHl6M4jIZItBLWN+uxJ2Jg3HDNwMZ5c62DtpPjru0MvbjA/Fe3jOQuwemXTmDJCLNvrJE+4onB8ii0hmAq6miMikg==
        set comments "This certificate is embedded in the hardware at the factory and is unique to this unit. "
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIHjME4GCSqGSIb3DQEFDTBBMCkGCSqGSIb3DQEFDDAcBAhgW0UQRHZyWQICCAAw
DAYIKoZIhvcNAgkFADAUBggqhkiG9w0DBwQIpoWgOQlouh8EgZBhPM7yJ2yx8qL+
p5fxyHEHYswJQR4fwyNpaJu0KjGdmsKaSOgZoRP22t9JJTHk2/jljzVFu1FX9kGW
cpGpVFHT3qHTzRwHtUGcqVFNyl2a0dZyl2yi4MBPT+Jx7ohnrdCi2h5c1Z3v3rIs
2QEBh1s7akP1KrH9naChbU+a0ZQo+CZh17UxxYhLnscvQR8fYRw=
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICQDCCAeWgAwIBAgIIZvWTXaL46PkwCgYIKoZIzj0EAwIwgZ0xCzAJBgNVBAYT
AlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUxETAP
BgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMMEEZH
Vk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGluZXQu
Y29tMB4XDTIyMDkwNDE3MDUyMloXDTMyMDkwNDE3MDUyMlowgZ0xCzAJBgNVBAYT
AlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUxETAP
BgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMMEEZH
Vk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGluZXQu
Y29tMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEggJ9H4BVv28gkRhhJQNnvSrI
O4EwwU20yxSERMY7iYfYRDt+k9FTEHMNepAyUNVl3o63cZAb7OoBHNd1BKYcqqMN
MAswCQYDVR0TBAIwADAKBggqhkjOPQQDAgNJADBGAiEAjTpvJw/5TDi66RLpUtcZ
AAN9a8nwSHoXH6lbVuOcaGQCIQDL6deUPoq3cBTlSwfEwViqVBAmdM1ZHYChC5X2
rtKdnw==
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
    edit "Fortinet_SSL_ECDSA384"
        set password ENC jI4UTmPNADanjYqNlNVHJ6cFuOtw3YW6X7tD2qDFsZ996lyS5JvhCPCidVWoD6t2kl1tGo/z8A861xuwx6uwJkMvMlfEq+RZ7l07tpJmdcgWFWrf33XVOcJ9M1Cm7WJsN+RQj0hortANIS1clpqJrsmLY4l4P0xAvqg83/t1ZxIufXL3PvhFATdDil1QnRtFeg8P9Q==
        set comments "This certificate is embedded in the hardware at the factory and is unique to this unit. "
        set private-key "-----BEGIN ENCRYPTED PRIVATE KEY-----
MIIBEzBOBgkqhkiG9w0BBQ0wQTApBgkqhkiG9w0BBQwwHAQITTynfcRi4hACAggA
MAwGCCqGSIb3DQIJBQAwFAYIKoZIhvcNAwcECJ4hTE7VwuO2BIHA5WuyQRvfl312
9V7ognhRqUeW8Bro7sLLKZ+wdJYhcg5Cy09mJwYfAQnMF+M0+wS5k01zjIWc1sWq
nIkh+zg3I2pOGeMCqcbjlzOeYkFZMI16b4ByxUQ6ybuRK7uy1GvIga1kSw+XXW39
R50sTOvQJj6T4IU8DA/5PPpYg2y834SQ6Hf4Gs5ee1LJFDoCorYlsttgjRwxkxrx
lHnYtDdcvkyLSMXXixuV9L7U7myTHBnfhxica/MBf+qi6KNmZQLo
-----END ENCRYPTED PRIVATE KEY-----"
        set certificate "-----BEGIN CERTIFICATE-----
MIICezCCAgKgAwIBAgIIQ4xzLIq5jkUwCgYIKoZIzj0EAwIwgZ0xCzAJBgNVBAYT
AlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUxETAP
BgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMMEEZH
Vk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGluZXQu
Y29tMB4XDTIyMDkwNDE3MDUyMloXDTMyMDkwNDE3MDUyMlowgZ0xCzAJBgNVBAYT
AlVTMRMwEQYDVQQIDApDYWxpZm9ybmlhMRIwEAYDVQQHDAlTdW5ueXZhbGUxETAP
BgNVBAoMCEZvcnRpbmV0MRIwEAYDVQQLDAlGb3J0aUdhdGUxGTAXBgNVBAMMEEZH
Vk1FVlZBRERTS0hWMUExIzAhBgkqhkiG9w0BCQEWFHN1cHBvcnRAZm9ydGluZXQu
Y29tMHYwEAYHKoZIzj0CAQYFK4EEACIDYgAE8FoeNGAuNJ3bwcwe6+GYneJncowN
PB9tey2iVLBQc6Q82yMvsrAzoVGrwnN82sYUj9em2OKG1ybtbyieIaUI6ijtOtb3
JTP4kk6faUnZuQV6oaXWDBKUTB5R4wYtVksTow0wCzAJBgNVHRMEAjAAMAoGCCqG
SM49BAMCA2cAMGQCMDt1fBlvgKxwY70cCjKuCLUynHBfPpYmlwaF0lud2/OneU+4
6ckPtZufPo4WcN4agQIwMw5ZOVwonIS9npd6DEbYAiD740XOa/2FBb4YojHlcisu
9XWLWc26ZIwSvWGk36jl
-----END CERTIFICATE-----"
        set range global
        set source factory
        set last-updated 1661721735
    next
end
config webfilter ftgd-local-cat
    edit "custom1"
        set id 140
    next
    edit "custom2"
        set id 141
    next
end
config ips sensor
    edit "default"
        set comment "Prevent critical attacks."
        config entries
            edit 1
                set severity medium high critical 
            next
        end
    next
    edit "sniffer-profile"
        set comment "Monitor IPS attacks."
        config entries
            edit 1
                set severity medium high critical 
            next
        end
    next
    edit "wifi-default"
        set comment "Default configuration for offloading WiFi traffic."
        config entries
            edit 1
                set severity medium high critical 
            next
        end
    next
    edit "all_default"
        set comment "All predefined signatures with default setting."
        config entries
            edit 1
            next
        end
    next
    edit "all_default_pass"
        set comment "All predefined signatures with PASS action."
        config entries
            edit 1
                set action pass
            next
        end
    next
    edit "protect_http_server"
        set comment "Protect against HTTP server-side vulnerabilities."
        config entries
            edit 1
                set location server 
                set protocol HTTP 
            next
        end
    next
    edit "protect_email_server"
        set comment "Protect against email server-side vulnerabilities."
        config entries
            edit 1
                set location server 
                set protocol SMTP POP3 IMAP 
            next
        end
    next
    edit "protect_client"
        set comment "Protect against client-side vulnerabilities."
        config entries
            edit 1
                set location client 
            next
        end
    next
    edit "high_security"
        set comment "Blocks all Critical/High/Medium and some Low severity vulnerabilities"
        set block-malicious-url enable
        config entries
            edit 1
                set severity medium high critical 
                set status enable
                set action block
            next
            edit 2
                set severity low 
            next
        end
    next
end
config firewall shaper traffic-shaper
    edit "high-priority"
        set maximum-bandwidth 1048576
        set per-policy enable
    next
    edit "medium-priority"
        set maximum-bandwidth 1048576
        set priority medium
        set per-policy enable
    next
    edit "low-priority"
        set maximum-bandwidth 1048576
        set priority low
        set per-policy enable
    next
    edit "guarantee-100kbps"
        set guaranteed-bandwidth 100
        set maximum-bandwidth 1048576
        set per-policy enable
    next
    edit "shared-1M-pipe"
        set maximum-bandwidth 1024
    next
end
config web-proxy global
    set proxy-fqdn "default.fqdn"
end
config application list
    edit "default"
        set comment "Monitor all applications."
        config entries
            edit 1
                set action pass
            next
        end
    next
    edit "sniffer-profile"
        set comment "Monitor all applications."
        unset options
        config entries
            edit 1
                set action pass
            next
        end
    next
    edit "wifi-default"
        set comment "Default configuration for offloading WiFi traffic."
        set deep-app-inspection disable
        config entries
            edit 1
                set action pass
                set log disable
            next
        end
    next
    edit "block-high-risk"
        config entries
            edit 1
                set category 2 6
            next
            edit 2
                set action pass
            next
        end
    next
end
config dlp filepattern
    edit 1
        set name "builtin-patterns"
        config entries
            edit "*.bat"
            next
            edit "*.com"
            next
            edit "*.dll"
            next
            edit "*.doc"
            next
            edit "*.exe"
            next
            edit "*.gz"
            next
            edit "*.hta"
            next
            edit "*.ppt"
            next
            edit "*.rar"
            next
            edit "*.scr"
            next
            edit "*.tar"
            next
            edit "*.tgz"
            next
            edit "*.vb?"
            next
            edit "*.wps"
            next
            edit "*.xl?"
            next
            edit "*.zip"
            next
            edit "*.pif"
            next
            edit "*.cpl"
            next
        end
    next
    edit 2
        set name "all_executables"
        config entries
            edit "bat"
                set filter-type type
                set file-type bat
            next
            edit "exe"
                set filter-type type
                set file-type exe
            next
            edit "elf"
                set filter-type type
                set file-type elf
            next
            edit "hta"
                set filter-type type
                set file-type hta
            next
        end
    next
end
config dlp sensitivity
    edit "Private"
    next
    edit "Critical"
    next
    edit "Warning"
    next
end
config dlp sensor
    edit "default"
        set comment "Default sensor."
    next
    edit "sniffer-profile"
        set comment "Log a summary of email and web traffic."
        set summary-proto smtp pop3 imap http-get http-post
    next
end
config webfilter ips-urlfilter-setting
end
config webfilter ips-urlfilter-setting6
end
config log threat-weight
    config web
        edit 1
            set category 26
            set level high
        next
        edit 2
            set category 61
            set level high
        next
        edit 3
            set category 86
            set level high
        next
        edit 4
            set category 1
            set level medium
        next
        edit 5
            set category 3
            set level medium
        next
        edit 6
            set category 4
            set level medium
        next
        edit 7
            set category 5
            set level medium
        next
        edit 8
            set category 6
            set level medium
        next
        edit 9
            set category 12
            set level medium
        next
        edit 10
            set category 59
            set level medium
        next
        edit 11
            set category 62
            set level medium
        next
        edit 12
            set category 83
            set level medium
        next
        edit 13
            set category 72
        next
        edit 14
            set category 14
        next
    end
    config application
        edit 1
            set category 2
        next
        edit 2
            set category 6
            set level medium
        next
    end
end
config icap profile
    edit "default"
        config icap-headers
            edit 1
                set name "X-Authenticated-User"
                set content "$user"
            next
            edit 2
                set name "X-Authenticated-Groups"
                set content "$local_grp"
            next
        end
    next
end
config user local
    edit "guest"
        set type password
        set passwd ENC mO8959eJi5hXa6OiQjt8iJExopZh/3bnjPqJK6alHZusqZOrB6Hoj6+xzOhKgW/cOyC7SlewVq/AO5fTdHM+db5g+MpYia5+w7mLmIKPGWVlJxogr587F2diSBRFrrtY4UY2fQx6el3OQQRB1NO3fi2+PiHAA99YTltOtRrUudQlEzfn6QU8zwGcY/hZCPa1YzpkcA==
    next
end
config user setting
    set auth-cert "Fortinet_Factory"
end
config user group
    edit "SSO_Guest_Users"
    next
    edit "Guest-group"
        set member "guest"
    next
end
config vpn ssl web host-check-software
    edit "FortiClient-AV"
        set guid "C86EC76D-5A4C-40E7-BD94-59358E544D81"
    next
    edit "FortiClient-FW"
        set type fw
        set guid "528CB157-D384-4593-AAAA-E42DFF111CED"
    next
    edit "FortiClient-AV-Vista"
        set guid "385618A6-2256-708E-3FB9-7E98B93F91F9"
    next
    edit "FortiClient-FW-Vista"
        set type fw
        set guid "006D9983-6839-71D6-14E6-D7AD47ECD682"
    next
    edit "FortiClient-AV-Win7"
        set guid "71629DC5-BE6F-CCD3-C5A5-014980643264"
    next
    edit "AVG-Internet-Security-AV"
        set guid "17DDD097-36FF-435F-9E1B-52D74245D6BF"
    next
    edit "AVG-Internet-Security-FW"
        set type fw
        set guid "8DECF618-9569-4340-B34A-D78D28969B66"
    next
    edit "AVG-Internet-Security-AV-Vista-Win7"
        set guid "0C939084-9E57-CBDB-EA61-0B0C7F62AF82"
    next
    edit "AVG-Internet-Security-FW-Vista-Win7"
        set type fw
        set guid "34A811A1-D438-CA83-C13E-A23981B1E8F9"
    next
    edit "CA-Anti-Virus"
        set guid "17CFD1EA-56CF-40B5-A06B-BD3A27397C93"
    next
    edit "CA-Internet-Security-AV"
        set guid "6B98D35F-BB76-41C0-876B-A50645ED099A"
    next
    edit "CA-Internet-Security-FW"
        set type fw
        set guid "38102F93-1B6E-4922-90E1-A35D8DC6DAA3"
    next
    edit "CA-Internet-Security-AV-Vista-Win7"
        set guid "3EED0195-0A4B-4EF3-CC4F-4F401BDC245F"
    next
    edit "CA-Internet-Security-FW-Vista-Win7"
        set type fw
        set guid "06D680B0-4024-4FAB-E710-E675E50F6324"
    next
    edit "CA-Personal-Firewall"
        set type fw
        set guid "14CB4B80-8E52-45EA-905E-67C1267B4160"
    next
    edit "F-Secure-Internet-Security-AV"
        set guid "E7512ED5-4245-4B4D-AF3A-382D3F313F15"
    next
    edit "F-Secure-Internet-Security-FW"
        set type fw
        set guid "D4747503-0346-49EB-9262-997542F79BF4"
    next
    edit "F-Secure-Internet-Security-AV-Vista-Win7"
        set guid "15414183-282E-D62C-CA37-EF24860A2F17"
    next
    edit "F-Secure-Internet-Security-FW-Vista-Win7"
        set type fw
        set guid "2D7AC0A6-6241-D774-E168-461178D9686C"
    next
    edit "Kaspersky-AV"
        set guid "2C4D4BC6-0793-4956-A9F9-E252435469C0"
    next
    edit "Kaspersky-FW"
        set type fw
        set guid "2C4D4BC6-0793-4956-A9F9-E252435469C0"
    next
    edit "Kaspersky-AV-Vista-Win7"
        set guid "AE1D740B-8F0F-D137-211D-873D44B3F4AE"
    next
    edit "Kaspersky-FW-Vista-Win7"
        set type fw
        set guid "9626F52E-C560-D06F-0A42-2E08BA60B3D5"
    next
    edit "McAfee-Internet-Security-Suite-AV"
        set guid "84B5EE75-6421-4CDE-A33A-DD43BA9FAD83"
    next
    edit "McAfee-Internet-Security-Suite-FW"
        set type fw
        set guid "94894B63-8C7F-4050-BDA4-813CA00DA3E8"
    next
    edit "McAfee-Internet-Security-Suite-AV-Vista-Win7"
        set guid "86355677-4064-3EA7-ABB3-1B136EB04637"
    next
    edit "McAfee-Internet-Security-Suite-FW-Vista-Win7"
        set type fw
        set guid "BE0ED752-0A0B-3FFF-80EC-B2269063014C"
    next
    edit "McAfee-Virus-Scan-Enterprise"
        set guid "918A2B0B-2C60-4016-A4AB-E868DEABF7F0"
    next
    edit "Norton-360-2.0-AV"
        set guid "A5F1BC7C-EA33-4247-961C-0217208396C4"
    next
    edit "Norton-360-2.0-FW"
        set type fw
        set guid "371C0A40-5A0C-4AD2-A6E5-69C02037FBF3"
    next
    edit "Norton-360-3.0-AV"
        set guid "E10A9785-9598-4754-B552-92431C1C35F8"
    next
    edit "Norton-360-3.0-FW"
        set type fw
        set guid "7C21A4C9-F61F-4AC4-B722-A6E19C16F220"
    next
    edit "Norton-Internet-Security-AV"
        set guid "E10A9785-9598-4754-B552-92431C1C35F8"
    next
    edit "Norton-Internet-Security-FW"
        set type fw
        set guid "7C21A4C9-F61F-4AC4-B722-A6E19C16F220"
    next
    edit "Norton-Internet-Security-AV-Vista-Win7"
        set guid "88C95A36-8C3B-2F2C-1B8B-30FCCFDC4855"
    next
    edit "Norton-Internet-Security-FW-Vista-Win7"
        set type fw
        set guid "B0F2DB13-C654-2E74-30D4-99C9310F0F2E"
    next
    edit "Symantec-Endpoint-Protection-AV"
        set guid "FB06448E-52B8-493A-90F3-E43226D3305C"
    next
    edit "Symantec-Endpoint-Protection-FW"
        set type fw
        set guid "BE898FE3-CD0B-4014-85A9-03DB9923DDB6"
    next
    edit "Symantec-Endpoint-Protection-AV-Vista-Win7"
        set guid "88C95A36-8C3B-2F2C-1B8B-30FCCFDC4855"
    next
    edit "Symantec-Endpoint-Protection-FW-Vista-Win7"
        set type fw
        set guid "B0F2DB13-C654-2E74-30D4-99C9310F0F2E"
    next
    edit "Panda-Antivirus+Firewall-2008-AV"
        set guid "EEE2D94A-D4C1-421A-AB2C-2CE8FE51747A"
    next
    edit "Panda-Antivirus+Firewall-2008-FW"
        set type fw
        set guid "7B090DC0-8905-4BAF-8040-FD98A41C8FB8"
    next
    edit "Panda-Internet-Security-AV"
        set guid "4570FB70-5C9E-47E9-B16C-A3A6A06C4BF0"
    next
    edit "Panda-Internet-Security-2006~2007-FW"
        set type fw
        set guid "4570FB70-5C9E-47E9-B16C-A3A6A06C4BF0"
    next
    edit "Panda-Internet-Security-2008~2009-FW"
        set type fw
        set guid "7B090DC0-8905-4BAF-8040-FD98A41C8FB8"
    next
    edit "Sophos-Anti-Virus"
        set guid "3F13C776-3CBE-4DE9-8BF6-09E5183CA2BD"
    next
    edit "Sophos-Enpoint-Secuirty-and-Control-FW"
        set type fw
        set guid "0786E95E-326A-4524-9691-41EF88FB52EA"
    next
    edit "Sophos-Enpoint-Secuirty-and-Control-AV-Vista-Win7"
        set guid "479CCF92-4960-B3E0-7373-BF453B467D2C"
    next
    edit "Sophos-Enpoint-Secuirty-and-Control-FW-Vista-Win7"
        set type fw
        set guid "7FA74EB7-030F-B2B8-582C-1670C5953A57"
    next
    edit "Trend-Micro-AV"
        set guid "7D2296BC-32CC-4519-917E-52E652474AF5"
    next
    edit "Trend-Micro-FW"
        set type fw
        set guid "3E790E9E-6A5D-4303-A7F9-185EC20F3EB6"
    next
    edit "Trend-Micro-AV-Vista-Win7"
        set guid "48929DFC-7A52-A34F-8351-C4DBEDBD9C50"
    next
    edit "Trend-Micro-FW-Vista-Win7"
        set type fw
        set guid "70A91CD9-303D-A217-A80E-6DEE136EDB2B"
    next
    edit "ZoneAlarm-AV"
        set guid "5D467B10-818C-4CAB-9FF7-6893B5B8F3CF"
    next
    edit "ZoneAlarm-FW"
        set type fw
        set guid "829BDA32-94B3-44F4-8446-F8FCFF809F8B"
    next
    edit "ZoneAlarm-AV-Vista-Win7"
        set guid "D61596DF-D219-341C-49B3-AD30538CBC5B"
    next
    edit "ZoneAlarm-FW-Vista-Win7"
        set type fw
        set guid "EE2E17FA-9876-3544-62EC-0405AD5FFB20"
    next
    edit "ESET-Smart-Security-AV"
        set guid "19259FAE-8396-A113-46DB-15B0E7DFA289"
    next
    edit "ESET-Smart-Security-FW"
        set type fw
        set guid "211E1E8B-C9F9-A04B-6D84-BC85190CE5F2"
    next
end
config vpn ssl web portal
    edit "full-access"
        set tunnel-mode enable
        set ipv6-tunnel-mode enable
        set web-mode enable
        set ip-pools "SSLVPN_TUNNEL_ADDR1"
        set ipv6-pools "SSLVPN_TUNNEL_IPv6_ADDR1"
    next
end
config vpn ssl settings
    set servercert "self-sign"
    set port 443
end
config voip profile
    edit "default"
        set comment "Default VoIP profile."
    next
    edit "strict"
        config sip
            set malformed-request-line discard
            set malformed-header-via discard
            set malformed-header-from discard
            set malformed-header-to discard
            set malformed-header-call-id discard
            set malformed-header-cseq discard
            set malformed-header-rack discard
            set malformed-header-rseq discard
            set malformed-header-contact discard
            set malformed-header-record-route discard
            set malformed-header-route discard
            set malformed-header-expires discard
            set malformed-header-content-type discard
            set malformed-header-content-length discard
            set malformed-header-max-forwards discard
            set malformed-header-allow discard
            set malformed-header-p-asserted-identity discard
            set malformed-header-sdp-v discard
            set malformed-header-sdp-o discard
            set malformed-header-sdp-s discard
            set malformed-header-sdp-i discard
            set malformed-header-sdp-c discard
            set malformed-header-sdp-b discard
            set malformed-header-sdp-z discard
            set malformed-header-sdp-k discard
            set malformed-header-sdp-a discard
            set malformed-header-sdp-t discard
            set malformed-header-sdp-r discard
            set malformed-header-sdp-m discard
        end
    next
end
config dnsfilter profile
    edit "default"
        set comment "Default dns filtering."
        config ftgd-dns
            config filters
                edit 1
                    set category 2
                next
                edit 2
                    set category 7
                next
                edit 3
                    set category 8
                next
                edit 4
                    set category 9
                next
                edit 5
                    set category 11
                next
                edit 6
                    set category 12
                next
                edit 7
                    set category 13
                next
                edit 8
                    set category 14
                next
                edit 9
                    set category 15
                next
                edit 10
                    set category 16
                next
                edit 11
                next
                edit 12
                    set category 57
                next
                edit 13
                    set category 63
                next
                edit 14
                    set category 64
                next
                edit 15
                    set category 65
                next
                edit 16
                    set category 66
                next
                edit 17
                    set category 67
                next
                edit 18
                    set category 26
                    set action block
                next
                edit 19
                    set category 61
                    set action block
                next
                edit 20
                    set category 86
                    set action block
                next
                edit 21
                    set category 88
                    set action block
                next
                edit 22
                    set category 90
                    set action block
                next
                edit 23
                    set category 91
                    set action block
                next
            end
        end
        set block-botnet enable
    next
end
config antivirus settings
    set grayware enable
end
config antivirus profile
    edit "default"
        set comment "Scan files and block viruses."
        config http
            set options scan
        end
        config ftp
            set options scan
        end
        config imap
            set options scan
            set executables virus
        end
        config pop3
            set options scan
            set executables virus
        end
        config smtp
            set options scan
            set executables virus
        end
    next
    edit "sniffer-profile"
        set comment "Scan files and monitor viruses."
        config http
            set options scan
        end
        config ftp
            set options scan
        end
        config imap
            set options scan
            set executables virus
        end
        config pop3
            set options scan
            set executables virus
        end
        config smtp
            set options scan
            set executables virus
        end
    next
    edit "wifi-default"
        set comment "Default configuration for offloading WiFi traffic."
        config http
            set options scan
        end
        config ftp
            set options scan
        end
        config imap
            set options scan
            set executables virus
        end
        config pop3
            set options scan
            set executables virus
        end
        config smtp
            set options scan
            set executables virus
        end
    next
end
config webfilter profile
    edit "default"
        set comment "Default web filtering."
        config ftgd-wf
            unset options
            config filters
                edit 1
                    set action block
                next
                edit 2
                    set category 2
                    set action block
                next
                edit 3
                    set category 7
                    set action block
                next
                edit 4
                    set category 8
                    set action block
                next
                edit 5
                    set category 9
                    set action block
                next
                edit 6
                    set category 11
                    set action block
                next
                edit 7
                    set category 12
                    set action block
                next
                edit 8
                    set category 13
                    set action block
                next
                edit 9
                    set category 14
                    set action block
                next
                edit 10
                    set category 15
                    set action block
                next
                edit 11
                    set category 16
                    set action block
                next
                edit 12
                    set category 26
                    set action block
                next
                edit 13
                    set category 57
                    set action block
                next
                edit 14
                    set category 61
                    set action block
                next
                edit 15
                    set category 63
                    set action block
                next
                edit 16
                    set category 64
                    set action block
                next
                edit 17
                    set category 65
                    set action block
                next
                edit 18
                    set category 66
                    set action block
                next
                edit 19
                    set category 67
                    set action block
                next
                edit 20
                    set category 86
                    set action block
                next
                edit 21
                    set category 88
                    set action block
                next
                edit 22
                    set category 90
                    set action block
                next
                edit 23
                    set category 91
                    set action block
                next
            end
        end
    next
    edit "sniffer-profile"
        set comment "Monitor web traffic."
        config ftgd-wf
            config filters
                edit 1
                next
                edit 2
                    set category 1
                next
                edit 3
                    set category 2
                next
                edit 4
                    set category 3
                next
                edit 5
                    set category 4
                next
                edit 6
                    set category 5
                next
                edit 7
                    set category 6
                next
                edit 8
                    set category 7
                next
                edit 9
                    set category 8
                next
                edit 10
                    set category 9
                next
                edit 11
                    set category 11
                next
                edit 12
                    set category 12
                next
                edit 13
                    set category 13
                next
                edit 14
                    set category 14
                next
                edit 15
                    set category 15
                next
                edit 16
                    set category 16
                next
                edit 17
                    set category 17
                next
                edit 18
                    set category 18
                next
                edit 19
                    set category 19
                next
                edit 20
                    set category 20
                next
                edit 21
                    set category 23
                next
                edit 22
                    set category 24
                next
                edit 23
                    set category 25
                next
                edit 24
                    set category 26
                next
                edit 25
                    set category 28
                next
                edit 26
                    set category 29
                next
                edit 27
                    set category 30
                next
                edit 28
                    set category 31
                next
                edit 29
                    set category 33
                next
                edit 30
                    set category 34
                next
                edit 31
                    set category 35
                next
                edit 32
                    set category 36
                next
                edit 33
                    set category 37
                next
                edit 34
                    set category 38
                next
                edit 35
                    set category 39
                next
                edit 36
                    set category 40
                next
                edit 37
                    set category 41
                next
                edit 38
                    set category 42
                next
                edit 39
                    set category 43
                next
                edit 40
                    set category 44
                next
                edit 41
                    set category 46
                next
                edit 42
                    set category 47
                next
                edit 43
                    set category 48
                next
                edit 44
                    set category 49
                next
                edit 45
                    set category 50
                next
                edit 46
                    set category 51
                next
                edit 47
                    set category 52
                next
                edit 48
                    set category 53
                next
                edit 49
                    set category 54
                next
                edit 50
                    set category 55
                next
                edit 51
                    set category 56
                next
                edit 52
                    set category 57
                next
                edit 53
                    set category 58
                next
                edit 54
                    set category 59
                next
                edit 55
                    set category 61
                next
                edit 56
                    set category 62
                next
                edit 57
                    set category 63
                next
                edit 58
                    set category 64
                next
                edit 59
                    set category 65
                next
                edit 60
                    set category 66
                next
                edit 61
                    set category 67
                next
                edit 62
                    set category 68
                next
                edit 63
                    set category 69
                next
                edit 64
                    set category 70
                next
                edit 65
                    set category 71
                next
                edit 66
                    set category 72
                next
                edit 67
                    set category 75
                next
                edit 68
                    set category 76
                next
                edit 69
                    set category 77
                next
                edit 70
                    set category 78
                next
                edit 71
                    set category 79
                next
                edit 72
                    set category 80
                next
                edit 73
                    set category 81
                next
                edit 74
                    set category 82
                next
                edit 75
                    set category 83
                next
                edit 76
                    set category 84
                next
                edit 77
                    set category 85
                next
                edit 78
                    set category 86
                next
                edit 79
                    set category 87
                next
                edit 80
                    set category 88
                next
                edit 81
                    set category 89
                next
                edit 82
                    set category 90
                next
                edit 83
                    set category 91
                next
                edit 84
                    set category 92
                next
                edit 85
                    set category 93
                next
                edit 86
                    set category 94
                next
                edit 87
                    set category 95
                next
            end
        end
    next
    edit "wifi-default"
        set comment "Default configuration for offloading WiFi traffic."
        set options block-invalid-url
        config ftgd-wf
            unset options
            config filters
                edit 1
                next
                edit 2
                    set category 2
                    set action block
                next
                edit 3
                    set category 7
                    set action block
                next
                edit 4
                    set category 8
                    set action block
                next
                edit 5
                    set category 9
                    set action block
                next
                edit 6
                    set category 11
                    set action block
                next
                edit 7
                    set category 12
                    set action block
                next
                edit 8
                    set category 13
                    set action block
                next
                edit 9
                    set category 14
                    set action block
                next
                edit 10
                    set category 15
                    set action block
                next
                edit 11
                    set category 16
                    set action block
                next
                edit 12
                    set category 26
                    set action block
                next
                edit 13
                    set category 57
                    set action block
                next
                edit 14
                    set category 61
                    set action block
                next
                edit 15
                    set category 63
                    set action block
                next
                edit 16
                    set category 64
                    set action block
                next
                edit 17
                    set category 65
                    set action block
                next
                edit 18
                    set category 66
                    set action block
                next
                edit 19
                    set category 67
                    set action block
                next
                edit 20
                    set category 86
                    set action block
                next
                edit 21
                    set category 88
                    set action block
                next
                edit 22
                    set category 90
                    set action block
                next
                edit 23
                    set category 91
                    set action block
                next
            end
        end
    next
    edit "monitor-all"
        set comment "Monitor and log all visited URLs, flow-based."
        config ftgd-wf
            unset options
            config filters
                edit 1
                    set category 1
                next
                edit 2
                    set category 3
                next
                edit 3
                    set category 4
                next
                edit 4
                    set category 5
                next
                edit 5
                    set category 6
                next
                edit 6
                    set category 12
                next
                edit 7
                    set category 59
                next
                edit 8
                    set category 62
                next
                edit 9
                    set category 83
                next
                edit 10
                    set category 2
                next
                edit 11
                    set category 7
                next
                edit 12
                    set category 8
                next
                edit 13
                    set category 9
                next
                edit 14
                    set category 11
                next
                edit 15
                    set category 13
                next
                edit 16
                    set category 14
                next
                edit 17
                    set category 15
                next
                edit 18
                    set category 16
                next
                edit 19
                    set category 57
                next
                edit 20
                    set category 63
                next
                edit 21
                    set category 64
                next
                edit 22
                    set category 65
                next
                edit 23
                    set category 66
                next
                edit 24
                    set category 67
                next
                edit 25
                    set category 19
                next
                edit 26
                    set category 24
                next
                edit 27
                    set category 25
                next
                edit 28
                    set category 72
                next
                edit 29
                    set category 75
                next
                edit 30
                    set category 76
                next
                edit 31
                    set category 26
                next
                edit 32
                    set category 61
                next
                edit 33
                    set category 86
                next
                edit 34
                    set category 17
                next
                edit 35
                    set category 18
                next
                edit 36
                    set category 20
                next
                edit 37
                    set category 23
                next
                edit 38
                    set category 28
                next
                edit 39
                    set category 29
                next
                edit 40
                    set category 30
                next
                edit 41
                    set category 33
                next
                edit 42
                    set category 34
                next
                edit 43
                    set category 35
                next
                edit 44
                    set category 36
                next
                edit 45
                    set category 37
                next
                edit 46
                    set category 38
                next
                edit 47
                    set category 39
                next
                edit 48
                    set category 40
                next
                edit 49
                    set category 42
                next
                edit 50
                    set category 44
                next
                edit 51
                    set category 46
                next
                edit 52
                    set category 47
                next
                edit 53
                    set category 48
                next
                edit 54
                    set category 54
                next
                edit 55
                    set category 55
                next
                edit 56
                    set category 58
                next
                edit 57
                    set category 68
                next
                edit 58
                    set category 69
                next
                edit 59
                    set category 70
                next
                edit 60
                    set category 71
                next
                edit 61
                    set category 77
                next
                edit 62
                    set category 78
                next
                edit 63
                    set category 79
                next
                edit 64
                    set category 80
                next
                edit 65
                    set category 82
                next
                edit 66
                    set category 85
                next
                edit 67
                    set category 87
                next
                edit 68
                    set category 31
                next
                edit 69
                    set category 41
                next
                edit 70
                    set category 43
                next
                edit 71
                    set category 49
                next
                edit 72
                    set category 50
                next
                edit 73
                    set category 51
                next
                edit 74
                    set category 52
                next
                edit 75
                    set category 53
                next
                edit 76
                    set category 56
                next
                edit 77
                    set category 81
                next
                edit 78
                    set category 84
                next
                edit 79
                next
                edit 80
                    set category 88
                next
                edit 81
                    set category 89
                next
                edit 82
                    set category 90
                next
                edit 83
                    set category 91
                next
                edit 84
                    set category 92
                next
                edit 85
                    set category 93
                next
                edit 86
                    set category 94
                next
                edit 87
                    set category 95
                next
            end
        end
        set log-all-url enable
        set web-content-log disable
        set web-filter-activex-log disable
        set web-filter-command-block-log disable
        set web-filter-cookie-log disable
        set web-filter-applet-log disable
        set web-filter-jscript-log disable
        set web-filter-js-log disable
        set web-filter-vbs-log disable
        set web-filter-unknown-log disable
        set web-filter-referer-log disable
        set web-filter-cookie-removal-log disable
        set web-url-log disable
        set web-invalid-domain-log disable
        set web-ftgd-err-log disable
        set web-ftgd-quota-usage disable
    next
end
config webfilter search-engine
    edit "google"
        set hostname ".*\\.google\\..*"
        set url "^\\/((custom|search|images|videosearch|webhp)\\?)"
        set query "q="
        set safesearch url
        set safesearch-str "&safe=active"
    next
    edit "yahoo"
        set hostname ".*\\.yahoo\\..*"
        set url "^\\/search(\\/video|\\/images){0,1}(\\?|;)"
        set query "p="
        set safesearch url
        set safesearch-str "&vm=r"
    next
    edit "bing"
        set hostname ".*\\.bing\\..*"
        set url "^(\\/images|\\/videos)?(\\/search|\\/async|\\/asyncv2)\\?"
        set query "q="
        set safesearch header
    next
    edit "yandex"
        set hostname "yandex\\..*"
        set url "^\\/((yand|images\\/|video\\/)(search)|search\\/)\\?"
        set query "text="
        set safesearch url
        set safesearch-str "&family=yes"
    next
    edit "youtube"
        set hostname ".*youtube.*"
        set safesearch header
    next
    edit "baidu"
        set hostname ".*\\.baidu\\.com"
        set url "^\\/s?\\?"
        set query "wd="
    next
    edit "baidu2"
        set hostname ".*\\.baidu\\.com"
        set url "^\\/(ns|q|m|i|v)\\?"
        set query "word="
    next
    edit "baidu3"
        set hostname "tieba\\.baidu\\.com"
        set url "^\\/f\\?"
        set query "kw="
    next
end
config emailfilter profile
    edit "sniffer-profile"
        set comment "Malware and phishing URL monitoring."
    next
    edit "default"
        set comment "Malware and phishing URL filtering."
    next
end
config report layout
    edit "default"
        set title "FortiGate System Analysis Report"
        set style-theme "default-report"
        set options include-table-of-content view-chart-as-heading
        config page
            set paper letter
            set page-break-before heading1
            config header
                config header-item
                    edit 1
                        set type image
                        set style "header-image"
                        set img-src "fortinet_logo_small.png"
                    next
                end
            end
            config footer
                config footer-item
                    edit 1
                        set style "footer-text"
                        set content "FortiGate ${schedule_type} Security Report - Host Name: ${hostname}"
                    next
                    edit 2
                        set style "footer-pageno"
                    next
                end
            end
        end
        config body-item
            edit 101
                set type image
                set style "report-cover1"
                set img-src "fortigate_log.png"
            next
            edit 103
                set style "report-cover2"
                set content "FortiGate ${schedule_type} Security Report"
            next
            edit 105
                set style "report-cover3"
                set content "Report Date: ${started_time}"
            next
            edit 107
                set style "report-cover3"
                set content "Data Range: ${report_data_range}  (${hostname})"
            next
            edit 109
                set style "report-cover3"
                set content "${vdom}"
            next
            edit 111
                set type image
                set style "report-cover4"
                set img-src "fortinet_logo_small.png"
            next
            edit 121
                set type misc
                set misc-component page-break
            next
            edit 301
                set text-component heading1
                set content "Bandwidth and Applications"
            next
            edit 311
                set type chart
                set chart "traffic.bandwidth.history_c"
            next
            edit 321
                set type chart
                set chart "traffic.sessions.history_c"
            next
            edit 331
                set type chart
                set chart "traffic.statistics"
            next
            edit 411
                set type chart
                set chart "traffic.bandwidth.apps_c"
            next
            edit 421
                set type chart
                set chart "traffic.bandwidth.cats_c"
            next
            edit 511
                set type chart
                set chart "traffic.bandwidth.users_c"
            next
            edit 521
                set type chart
                set chart "traffic.users.history.hour_c"
            next
            edit 611
                set type chart
                set chart "traffic.bandwidth.destinations_tab"
            next
            edit 1001
                set text-component heading1
                set content "Web Usage"
            next
            edit 1011
                set type chart
                set chart "web.allowed-request.sites_c"
            next
            edit 1021
                set type chart
                set chart "web.bandwidth.sites_c"
            next
            edit 1031
                set type chart
                set chart "web.blocked-request.sites_c"
            next
            edit 1041
                set type chart
                set chart "web.blocked-request.users_c"
            next
            edit 1051
                set type chart
                set chart "web.requests.users_c"
            next
            edit 1061
                set type chart
                set chart "web.bandwidth.users_c"
            next
            edit 1071
                set type chart
                set chart "web.bandwidth.stream-sites_c"
            next
            edit 1301
                set text-component heading1
                set content "Emails"
            next
            edit 1311
                set type chart
                set chart "email.request.senders_c"
            next
            edit 1321
                set type chart
                set chart "email.bandwidth.senders_c"
            next
            edit 1331
                set type chart
                set chart "email.request.recipients_c"
            next
            edit 1341
                set type chart
                set chart "email.bandwidth.recipients_c"
            next
            edit 1501
                set text-component heading1
                set content "Threats"
            next
            edit 1511
                set type chart
                set top-n 80
                set chart "virus.count.viruses_c"
            next
            edit 1531
                set type chart
                set top-n 80
                set chart "virus.count.users_c"
            next
            edit 1541
                set type chart
                set top-n 80
                set chart "virus.count.sources_c"
            next
            edit 1551
                set type chart
                set chart "virus.count.history_c"
            next
            edit 1561
                set type chart
                set top-n 80
                set chart "botnet.count_c"
            next
            edit 1571
                set type chart
                set top-n 80
                set chart "botnet.count.users_c"
            next
            edit 1581
                set type chart
                set top-n 80
                set chart "botnet.count.sources_c"
            next
            edit 1591
                set type chart
                set chart "botnet.count.history_c"
            next
            edit 1601
                set type chart
                set top-n 80
                set chart "attack.count.attacks_c"
            next
            edit 1611
                set type chart
                set top-n 80
                set chart "attack.count.victims_c"
            next
            edit 1621
                set type chart
                set top-n 80
                set chart "attack.count.source_bar_c"
            next
            edit 1631
                set type chart
                set chart "attack.count.blocked_attacks_c"
            next
            edit 1641
                set type chart
                set chart "attack.count.severity_c"
            next
            edit 1651
                set type chart
                set chart "attack.count.history_c"
            next
            edit 1701
                set text-component heading1
                set content "VPN Usage"
            next
            edit 1711
                set type chart
                set top-n 80
                set chart "vpn.bandwidth.static-tunnels_c"
            next
            edit 1721
                set type chart
                set top-n 80
                set chart "vpn.bandwidth.dynamic-tunnels_c"
            next
            edit 1731
                set type chart
                set top-n 80
                set chart "vpn.bandwidth.ssl-tunnel.users_c"
            next
            edit 1741
                set type chart
                set top-n 80
                set chart "vpn.bandwidth.ssl-web.users_c"
            next
            edit 1901
                set text-component heading1
                set content "Admin Login and System Events"
            next
            edit 1911
                set type chart
                set top-n 80
                set chart "event.login.summary_c"
            next
            edit 1931
                set type chart
                set top-n 80
                set chart "event.failed.login_c"
            next
            edit 1961
                set type chart
                set top-n 80
                set chart "event.system.group_events_c"
            next
        end
    next
end
config wanopt settings
    set host-id "default-id"
end
config wanopt profile
    edit "default"
        set comments "Default WANopt profile."
    next
end
config firewall schedule recurring
    edit "always"
        set day sunday monday tuesday wednesday thursday friday saturday
    next
    edit "none"
    next
end
config firewall profile-protocol-options
    edit "default"
        set comment "All default services."
        config http
            set ports 80
            unset options
            unset post-lang
        end
        config ftp
            set ports 21
            set options splice
        end
        config imap
            set ports 143
            set options fragmail
        end
        config mapi
            set ports 135
            set options fragmail
        end
        config pop3
            set ports 110
            set options fragmail
        end
        config smtp
            set ports 25
            set options fragmail splice
        end
        config nntp
            set ports 119
            set options splice
        end
        config dns
            set ports 53
        end
        config cifs
            set ports 445
        end
    next
end
config firewall ssl-ssh-profile
    edit "deep-inspection"
        set comment "Read-only deep inspection profile."
        config https
            set ports 443
            set status deep-inspection
        end
        config ftps
            set ports 990
            set status deep-inspection
        end
        config imaps
            set ports 993
            set status deep-inspection
        end
        config pop3s
            set ports 995
            set status deep-inspection
        end
        config smtps
            set ports 465
            set status deep-inspection
        end
        config ssh
            set ports 22
            set status disable
        end
        config ssl-exempt
            edit 1
                set fortiguard-category 31
            next
            edit 2
                set fortiguard-category 33
            next
            edit 3
                set type wildcard-fqdn
                set wildcard-fqdn "adobe"
            next
            edit 4
                set type wildcard-fqdn
                set wildcard-fqdn "Adobe Login"
            next
            edit 5
                set type wildcard-fqdn
                set wildcard-fqdn "android"
            next
            edit 6
                set type wildcard-fqdn
                set wildcard-fqdn "apple"
            next
            edit 7
                set type wildcard-fqdn
                set wildcard-fqdn "appstore"
            next
            edit 8
                set type wildcard-fqdn
                set wildcard-fqdn "auth.gfx.ms"
            next
            edit 9
                set type wildcard-fqdn
                set wildcard-fqdn "citrix"
            next
            edit 10
                set type wildcard-fqdn
                set wildcard-fqdn "dropbox.com"
            next
            edit 11
                set type wildcard-fqdn
                set wildcard-fqdn "eease"
            next
            edit 12
                set type wildcard-fqdn
                set wildcard-fqdn "firefox update server"
            next
            edit 13
                set type wildcard-fqdn
                set wildcard-fqdn "fortinet"
            next
            edit 14
                set type wildcard-fqdn
                set wildcard-fqdn "googleapis.com"
            next
            edit 15
                set type wildcard-fqdn
                set wildcard-fqdn "google-drive"
            next
            edit 16
                set type wildcard-fqdn
                set wildcard-fqdn "google-play2"
            next
            edit 17
                set type wildcard-fqdn
                set wildcard-fqdn "google-play3"
            next
            edit 18
                set type wildcard-fqdn
                set wildcard-fqdn "Gotomeeting"
            next
            edit 19
                set type wildcard-fqdn
                set wildcard-fqdn "icloud"
            next
            edit 20
                set type wildcard-fqdn
                set wildcard-fqdn "itunes"
            next
            edit 21
                set type wildcard-fqdn
                set wildcard-fqdn "microsoft"
            next
            edit 22
                set type wildcard-fqdn
                set wildcard-fqdn "skype"
            next
            edit 23
                set type wildcard-fqdn
                set wildcard-fqdn "softwareupdate.vmware.com"
            next
            edit 24
                set type wildcard-fqdn
                set wildcard-fqdn "verisign"
            next
            edit 25
                set type wildcard-fqdn
                set wildcard-fqdn "Windows update 2"
            next
            edit 26
                set type wildcard-fqdn
                set wildcard-fqdn "live.com"
            next
            edit 27
                set type wildcard-fqdn
                set wildcard-fqdn "google-play"
            next
            edit 28
                set type wildcard-fqdn
                set wildcard-fqdn "update.microsoft.com"
            next
            edit 29
                set type wildcard-fqdn
                set wildcard-fqdn "swscan.apple.com"
            next
            edit 30
                set type wildcard-fqdn
                set wildcard-fqdn "autoupdate.opera.com"
            next
        end
    next
    edit "custom-deep-inspection"
        set comment "Customizable deep inspection profile."
        config https
            set ports 443
            set status deep-inspection
        end
        config ftps
            set ports 990
            set status deep-inspection
        end
        config imaps
            set ports 993
            set status deep-inspection
        end
        config pop3s
            set ports 995
            set status deep-inspection
        end
        config smtps
            set ports 465
            set status deep-inspection
        end
        config ssh
            set ports 22
            set status disable
        end
        config ssl-exempt
            edit 1
                set fortiguard-category 31
            next
            edit 2
                set fortiguard-category 33
            next
            edit 3
                set type wildcard-fqdn
                set wildcard-fqdn "adobe"
            next
            edit 4
                set type wildcard-fqdn
                set wildcard-fqdn "Adobe Login"
            next
            edit 5
                set type wildcard-fqdn
                set wildcard-fqdn "android"
            next
            edit 6
                set type wildcard-fqdn
                set wildcard-fqdn "apple"
            next
            edit 7
                set type wildcard-fqdn
                set wildcard-fqdn "appstore"
            next
            edit 8
                set type wildcard-fqdn
                set wildcard-fqdn "auth.gfx.ms"
            next
            edit 9
                set type wildcard-fqdn
                set wildcard-fqdn "citrix"
            next
            edit 10
                set type wildcard-fqdn
                set wildcard-fqdn "dropbox.com"
            next
            edit 11
                set type wildcard-fqdn
                set wildcard-fqdn "eease"
            next
            edit 12
                set type wildcard-fqdn
                set wildcard-fqdn "firefox update server"
            next
            edit 13
                set type wildcard-fqdn
                set wildcard-fqdn "fortinet"
            next
            edit 14
                set type wildcard-fqdn
                set wildcard-fqdn "googleapis.com"
            next
            edit 15
                set type wildcard-fqdn
                set wildcard-fqdn "google-drive"
            next
            edit 16
                set type wildcard-fqdn
                set wildcard-fqdn "google-play2"
            next
            edit 17
                set type wildcard-fqdn
                set wildcard-fqdn "google-play3"
            next
            edit 18
                set type wildcard-fqdn
                set wildcard-fqdn "Gotomeeting"
            next
            edit 19
                set type wildcard-fqdn
                set wildcard-fqdn "icloud"
            next
            edit 20
                set type wildcard-fqdn
                set wildcard-fqdn "itunes"
            next
            edit 21
                set type wildcard-fqdn
                set wildcard-fqdn "microsoft"
            next
            edit 22
                set type wildcard-fqdn
                set wildcard-fqdn "skype"
            next
            edit 23
                set type wildcard-fqdn
                set wildcard-fqdn "softwareupdate.vmware.com"
            next
            edit 24
                set type wildcard-fqdn
                set wildcard-fqdn "verisign"
            next
            edit 25
                set type wildcard-fqdn
                set wildcard-fqdn "Windows update 2"
            next
            edit 26
                set type wildcard-fqdn
                set wildcard-fqdn "live.com"
            next
            edit 27
                set type wildcard-fqdn
                set wildcard-fqdn "google-play"
            next
            edit 28
                set type wildcard-fqdn
                set wildcard-fqdn "update.microsoft.com"
            next
            edit 29
                set type wildcard-fqdn
                set wildcard-fqdn "swscan.apple.com"
            next
            edit 30
                set type wildcard-fqdn
                set wildcard-fqdn "autoupdate.opera.com"
            next
        end
    next
    edit "no-inspection"
        set comment "Read-only profile that does no inspection."
        config https
            set status disable
        end
        config ftps
            set status disable
        end
        config imaps
            set status disable
        end
        config pop3s
            set status disable
        end
        config smtps
            set status disable
        end
        config ssh
            set ports 22
            set status disable
        end
    next
    edit "certificate-inspection"
        set comment "Read-only SSL handshake inspection profile."
        config https
            set ports 443
            set status certificate-inspection
        end
        config ftps
            set status disable
        end
        config imaps
            set status disable
        end
        config pop3s
            set status disable
        end
        config smtps
            set status disable
        end
        config ssh
            set ports 22
            set status disable
        end
    next
end
config waf profile
    edit "default"
        config signature
            config main-class 100000000
                set action block
                set severity high
            end
            config main-class 20000000
            end
            config main-class 30000000
                set status enable
                set action block
                set severity high
            end
            config main-class 40000000
            end
            config main-class 50000000
                set status enable
                set action block
                set severity high
            end
            config main-class 60000000
            end
            config main-class 70000000
                set status enable
                set action block
                set severity high
            end
            config main-class 80000000
                set status enable
                set severity low
            end
            config main-class 110000000
                set status enable
                set severity high
            end
            config main-class 90000000
                set status enable
                set action block
                set severity high
            end
            set disabled-signature 80080005 80200001 60030001 60120001 80080003 90410001 90410002
        end
        config constraint
            config header-length
                set status enable
                set log enable
                set severity low
            end
            config content-length
                set status enable
                set log enable
                set severity low
            end
            config param-length
                set status enable
                set log enable
                set severity low
            end
            config line-length
                set status enable
                set log enable
                set severity low
            end
            config url-param-length
                set status enable
                set log enable
                set severity low
            end
            config version
                set log enable
            end
            config method
                set action block
                set log enable
            end
            config hostname
                set action block
                set log enable
            end
            config malformed
                set log enable
            end
            config max-cookie
                set status enable
                set log enable
                set severity low
            end
            config max-header-line
                set status enable
                set log enable
                set severity low
            end
            config max-url-param
                set status enable
                set log enable
                set severity low
            end
            config max-range-segment
                set status enable
                set log enable
                set severity high
            end
        end
    next
end
config firewall policy
    edit 1
        set name "Internet"
        set uuid ae9bf56c-275b-51ed-46ca-fa89600259bf
        set srcintf "port4"
        set dstintf "port1"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set fsso disable
        set nat enable
    next
    edit 2
        set name "INTERNET_VLAN10"
        set uuid 3352f36e-2c93-51ed-7e15-9eb13796aa2f
        set srcintf "VLAN_10_FG"
        set dstintf "port1"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set fsso disable
        set nat enable
    next
    edit 3
        set name "INTERNET_VLAN20"
        set uuid 30d3b8a6-2c95-51ed-e6a5-3b77265f8f7b
        set srcintf "VLAN_20_FG"
        set dstintf "port1"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set fsso disable
        set nat enable
    next
    edit 4
        set name "INTERNET_VLAN30"
        set uuid 4b90e4ac-2c95-51ed-f196-d4358552bf9e
        set srcintf "VLAN_30_FG"
        set dstintf "port1"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set fsso disable
        set nat enable
    next
    edit 5
        set name "INTERNET_VLAN88"
        set uuid 84cf6338-2c95-51ed-6ebd-68335a5b3a91
        set srcintf "VLAN_88_MGMT_FG"
        set dstintf "port1"
        set srcaddr "all"
        set dstaddr "all"
        set action accept
        set schedule "always"
        set service "ALL"
        set fsso disable
        set nat enable
    next
end
config firewall ssh local-key
    edit "Fortinet_SSH_RSA2048"
        set password ENC fwAAAH8l3Hl1bNmVzBXe5ZJUriBpYk+IEJAjYoENdMTF5B/n0LNHQi49O92d/q1Di5jTtpALtBM/CAJCiauNDlsdsKgHm4p97sgdmcgrk+P6ESp2TeXyx4+Iq83U6Lrj14cN9K++PscBEsRmIsQVd9fRmGwigCHBps+dTJeF4R/5F5H23FL0e+1mmZ1N+w+AN73++A==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABA83tHVwU
lc4xiQGe8pf35oAAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQDD0K6hD1pW
+0JeDNVsch7AGdhdaaDSxRHTN7tt6IOq/e9Gc7TIm8c2nqs4Bu3xk2EUHoshKAfSVjRUv1
x45lQVBc9R03eEf1OnfC9c59l3qN+gjiA1uR8Uh/5FqofwfqAYrMgSZBLp2vA8VUuHOX4W
Sb6sBP8ribOMkX8lsu0tq3sNX0Vhl5RuLRqsVV+SmjIs3c3sEli8nBrEEQBqa1/U5AaRsK
apZc7oyFDhV1xCEC81muVrS44MsNiURCXoRDPtJhxLYp/GgzaIjkGPkt+mXDzKMQLy53Pq
wXM5xpbMJ+aaCEBCodzV8dp8OHFika1n6nW7M5jV+sI6957RlzXHAAADwJbSJivbapU3e4
VjkwtczVoYUywbvcNyyqO1B+I0QUh3QHeDE+QypmGEFL9zpBy8T5M3Lml3TWK8gXCdDHBb
iVHmrPDbM3iD2mTlidSVav6pHznIV2D6vpNDrDjHpk0q4ep5gQjkAfEp1y5GpI1mvA1gEa
koW+Fsmek+xnOL3E75NOmEqIeZWGiDSH8f34s2U6QXOuwpZ0gYoMNxQJO76aDDpV5aeNYx
GvMMT+YwGv/DdOXVueRqfADYRBQ+WZ0+OxZPBn9w0YVUq+oT+XFzjVl/DdOu5Opjh8qOeZ
AZXyh232zau1dKRqorMlnO01CDCoFzb4ZAnVoKt/NZd9DIY835UicEVy+HM/OFYrNEPgTI
i8jqRXZdZc1/+ViXNSqRWGCTssWxMkpMpdfWafWn/AN9HLPUikMo+YBSKYnuOVLksoU1zW
0Cf8kY/fR8qmoH4TlHs6kfsYNHQlaG+4j+1+TT1mNvSjcjxeiA4verKZaFyWR5MktPicli
YJfa1ITwY1Hckp1JwsfLBTc2KctuBH2v2gbte0iE5BvxH1pI72cxK2VGdtj2cHs6hfTRR2
nT8A1rb0PJnDrbGYlr4Bin6Ay2beTohTrdfcKgTAG1xYBT9rFO0lozTKYQweJvEew03TOy
sMnfFWPPlFWCcBCwjCOjmy+goTFmABCbckI34Nx4A8cnMRaeHu68uenoQZrvNG/G3dewRE
KhBtlk+9fM+9DIbN8btYSnaNF4NgJplD51ZqI+aV1HF2cdkzF1Y0iEqdHbagHoECbcWywN
+PwtnorTYBhAA47yEhMTHZhGj2h6fDz0AelnjGaIqdrfOkEanH7B2ubz7IAyp55uuqCdw0
7w2aOYVy7w5kyYUUwTxFhKb0ZblYmVVwAYY2UacSSNvI2BDfFLVkTsUCd1OWPJ8YEt2AfX
YRV8Y3yxft3OagZ5NFZXJ366KMqHEwNUu5sS8KgMDAiT+SpghyDwwNp33p85Te3kh1C9dk
4iIGCIMaWj+eRYIgo81xf2RNgqOvU2kzMZE27vEN86cfGZ4iXpBgX8ja1eKTOXrtSYfaHC
fy5KD/ine7GH6EOiqgH+U+aEnqn0/P3AOMir7TXjWi+7zZ/DnghyMTYtGVx9Gspy2Aqpo9
5qDpb+RRfTipS6y7dPnchmKEdMrtLit+sRKVRBsK5TobqQTWJFEtCQi9zbZL037x6b4y5j
GG8uDO6EVzXEuMujEHmc3qcHMag7IHQKNW5ZoKAwTxlY67wR1OEEwKI9QoUHQOp4U6K00q
Wl8BjRfg==
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDD0K6hD1pW+0JeDNVsch7AGdhdaaDSxRHTN7tt6IOq/e9Gc7TIm8c2nqs4Bu3xk2EUHoshKAfSVjRUv1x45lQVBc9R03eEf1OnfC9c59l3qN+gjiA1uR8Uh/5FqofwfqAYrMgSZBLp2vA8VUuHOX4WSb6sBP8ribOMkX8lsu0tq3sNX0Vhl5RuLRqsVV+SmjIs3c3sEli8nBrEEQBqa1/U5AaRsKapZc7oyFDhV1xCEC81muVrS44MsNiURCXoRDPtJhxLYp/GgzaIjkGPkt+mXDzKMQLy53PqwXM5xpbMJ+aaCEBCodzV8dp8OHFika1n6nW7M5jV+sI6957RlzXH"
        set source built-in
    next
    edit "Fortinet_SSH_DSA1024"
        set password ENC fwAAAH9TRPcoGPTyj4T02HecFYowrP4BR3wuXPLzf65Yg6n+bGpa7O3+drSR0YzfQA33Vz0Wa2+uSMYejfSvjxByIp8NxCyCxeShsgv6yDm6FU28cHOYOBoMJX+7jUMFBimoKYed+gtGiOdUKNIuMZNyebZTUcFWAs7MZGPESW0APUjjvRJ9sX+ok8iWzGXRxYrCPg==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABA7dhUlpq
zMSk9+s+yUG/WXAAAAEAAAAAEAAAGxAAAAB3NzaC1kc3MAAACBAOh3iwMBFGlBgPdpLYwV
IheW45OURhSUKrKVpsMr4nGfojiPUP6/ZimAAXvCk69vrm0ROQLAKZVlvoazh8oShz+TDK
6/lmlqz72eVpSlUB3iK6w/OR2XoM37Hnbrq8Fh1yK9Pc8muJMN52/m1/GShcXocWF+wpt0
gnURx29PDPEDAAAAFQDGd2NMWituoN8Gde8k55+4/jijLQAAAIAeSpDtVMjceHBzHH3zmY
qzBn92U8c7Xg4Oc9MtArZ8+qAewbN6Rok3iW+ITAe0WUgdj0Bbb61Tz1XtsWYwabAEyBZ0
ff6HvrpnksNxjPwTHUzsi9L6YnVsu3lgIcTm9/7VNHKGFy07Tffx46hLPDI0F6nnZeQWwF
jdOSVmP/YhBgAAAIAdvrTsABSzkAHnBSkdDeZa6UljQ3U8GXKYLozTK0wrVnIvEdJaOk3y
Wow9moECv+rBLa/jmGdpC3kfhRR507FxvrIWb5iA8hidRgZCqhYfJZK/b4q1wNJmPbulOT
kQr56GOWFlKbryfRD1ocRS/FMrQJyv3ItGCfy43KN/K8lQ7wAAAeCZHTcr7YKDrYAyTCWc
hPdUsInOTm3rUbgEewVfwi3rtQp15GRhHZQQ52+oI+SyDU80WoIl27nsPJIW9wOiB7UIHL
6Vacqh30WOP1DHoIevVymz0Mw/O9b0ugG0FqScfEatIIUX7yZkVKl5IoL4nMmVvVFZ6Kyk
iNgs+N2412r2Y75rRyaFqbtbtBjMWDKi80AUT/Hl92cUR3+vOGljjGHnLTogzIt4J3pm1C
bfbdGGZhGa+eo5R5Kpo3G/zWlUjWZDo2Z7NG5h0Jm/T1xsoTlbiI1WYIvTqdQZZ3CfHrJG
bcfHDYxKUoRwfonhapd9DKxARCZB/E6eLtOO/VDDwG9gkqLfhhekSQfzcEv111Q5zfppZ2
Io5vZLkawan1HspxovqgLZDRy7KA6JCoz1B36uEGamDlDCvAN47MNct4JHejsYUYR6VQa5
aYAtVC2jrH+Bd3SBVmkNWi/FglcTMQHC/3biepZme6gDK17B+XkMVR5tskaHgVls92oGrA
HprHvY6dyoIr5F1JsQ7FHGhNOZmkwjFQp1vkhXXoz2Gckv8ZUT5hLnkcxRBUuLDHfvxcFZ
gg78Yt8COZTzQgQX0LUFGZVnyV+izru3wTy/deI7PJ3SOywRtaTelj0Cp6Wc280=
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ssh-dss AAAAB3NzaC1kc3MAAACBAOh3iwMBFGlBgPdpLYwVIheW45OURhSUKrKVpsMr4nGfojiPUP6/ZimAAXvCk69vrm0ROQLAKZVlvoazh8oShz+TDK6/lmlqz72eVpSlUB3iK6w/OR2XoM37Hnbrq8Fh1yK9Pc8muJMN52/m1/GShcXocWF+wpt0gnURx29PDPEDAAAAFQDGd2NMWituoN8Gde8k55+4/jijLQAAAIAeSpDtVMjceHBzHH3zmYqzBn92U8c7Xg4Oc9MtArZ8+qAewbN6Rok3iW+ITAe0WUgdj0Bbb61Tz1XtsWYwabAEyBZ0ff6HvrpnksNxjPwTHUzsi9L6YnVsu3lgIcTm9/7VNHKGFy07Tffx46hLPDI0F6nnZeQWwFjdOSVmP/YhBgAAAIAdvrTsABSzkAHnBSkdDeZa6UljQ3U8GXKYLozTK0wrVnIvEdJaOk3yWow9moECv+rBLa/jmGdpC3kfhRR507FxvrIWb5iA8hidRgZCqhYfJZK/b4q1wNJmPbulOTkQr56GOWFlKbryfRD1ocRS/FMrQJyv3ItGCfy43KN/K8lQ7w=="
        set source built-in
    next
    edit "Fortinet_SSH_ECDSA256"
        set password ENC fwAAAB9Lax5Lfx6VIUXOsZplAcOqrnUC1ThUj7Aeg9Z8rgGrH8ksQcYpNG4OWvYMBMdREGgr6LZE/YcuLZjXE4g1XHILqaozYRJcQiLOIhJfZRfrGvHSK8dURbcjKjERZzsp5nqFCxFK4KMTTiYAtyzad/17m59KNf50hmQfC/5swY3BziLp9+S5cTPiPLGbL4J50w==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABCfB8bHXV
myWyX7EZmOnJgSAAAAEAAAAAEAAABoAAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlz
dHAyNTYAAABBBMwVSy5WAm0ED2v3VZMlQzPsMs/BUvHOhld1G5E//7tVmW+I/mk+gBAvpq
XASEfI0KjZEXDS6fHB4ymqME9N/fsAAACg3qhR6w3AarEEHdRlT8YFLTDA0n8HEm9UztKv
g6EAyrUtc5TSIGNeClh7yGveNXsFsdIYSjGkDlVPmvwJXuBPYLNxaHkuugoU+nBmbEp6Xe
1S5UQMrcgCaGqE5SNQ9FjkbhonxMXL1zIB/GTv8BGolsf+6nEqrGlWDTNYT8cL0ybKadfV
DY40qdRZkcQl90TePjqH1KQ5Qcpk7vl9tGPmlQ==
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ecdsa-sha2-nistp256 AAAAE2VjZHNhLXNoYTItbmlzdHAyNTYAAAAIbmlzdHAyNTYAAABBBMwVSy5WAm0ED2v3VZMlQzPsMs/BUvHOhld1G5E//7tVmW+I/mk+gBAvpqXASEfI0KjZEXDS6fHB4ymqME9N/fs="
        set source built-in
    next
    edit "Fortinet_SSH_ECDSA384"
        set password ENC fwAAAFPYprLeZ5M+htV9Qq/B8TVPUNTX/pTGW8vOWWCAe+1PsWU5nCXqPJBbNKyU9kE51aIfZu9AQhNPBHf7P9LyGX2wxtnHpA4fJMa0GM5xgp+l1BdMv9iOJd4w7r6CjzIs2GHu8hnC6Uy8s8XcScgD9nQsFXKgAP1RZkHK0GR47scsb1rhW9sdkwZVPxxGGnmcSA==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABAaMUrYj5
oiUiZkVf4moIXZAAAAEAAAAAEAAACIAAAAE2VjZHNhLXNoYTItbmlzdHAzODQAAAAIbmlz
dHAzODQAAABhBJefbJ0DJn2wyuvja0El03eX7J7ViMmQ+57JCbvujyt8Lj30ZecoRieTPk
dbaUkIoQqMJobHBcfGZM8/4WSKUq4GjQ2YfiqUswEEedW51zjDo2ZsqJAph+RvOVZcqHkP
EwAAANDQQgxxdIV5HlWGvtaJx/PzqO6xrhpGPm8ZibpYcoF4U9XV1hPsuFhYpW4MJbI14d
X/FL8fqUITa3giAsZyNhdu2NK3DBdex8hXes0MtsIFKuZ16Q9iBqnM3CKxQflPhzCUUtVG
HakqGs+6CFeua8x3aPTpsolWcZrSgHOKpkYc+Uk+ubCcRrQsfStQdkU/guD0pA97j31ykH
tKrWO0jE2LY/HMcxhVG+5RakgGGmAJ6e9o+89FQqSQp9asjY1+pQOmoPcALaHMqoN7BNXA
Bx8g
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ecdsa-sha2-nistp384 AAAAE2VjZHNhLXNoYTItbmlzdHAzODQAAAAIbmlzdHAzODQAAABhBJefbJ0DJn2wyuvja0El03eX7J7ViMmQ+57JCbvujyt8Lj30ZecoRieTPkdbaUkIoQqMJobHBcfGZM8/4WSKUq4GjQ2YfiqUswEEedW51zjDo2ZsqJAph+RvOVZcqHkPEw=="
        set source built-in
    next
    edit "Fortinet_SSH_ECDSA521"
        set password ENC fwAAAIUCPlKVnHP1bcx/QuDaqe8iO6YGnjizImN6Qo9Xi5Iu7E0Y4rN6IpkHklswfN7678UAwhsuVTur3+OQUFSUKdwuoUTw+WRUjtV3skOh+hLPksBeGMffDS5gyVct1lLqINh5YS8dfdoK7PWfqacV79V0HGLWsKoAbNgiD7s9AaK2kCl//28H96kIdP/4pf0stA==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABBbn38ja9
rk1+MObGahm3fiAAAAEAAAAAEAAACsAAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlz
dHA1MjEAAACFBAH8jyw6/dk7Fa64/AWSUpmxAGVznnujFo+UEyv6NzY3Bg1ZO4iltpQBlI
ce4Rx31Qb4SxryLGKJyZFg0z9ZJzazEgCqKAiRbMEdtlQaYS23i1OMsRVeDRPX5wdItVpU
ofV8VAd8SWwIWsMHQREtxJTCnBXcZLxHbI/s13s1S9CqfLwAtAAAAQAsckWYzO6dhOXUFY
xU8aTmBNabDeK/OsZz5fQ1NXlaiP0lCFAkiRauV8ZUo+lnpgR1T0beTg4cpobr+L/OvXqH
JkVFvGrDAEudEeoHRT/3zItmP3B8czZgqXWJi7PQmEy2FgpCtRSJEkxQpyvbqNsZWBAzLj
G0cVid/ubb4g3vsiqXNIgQvFfHBerdER77lBnA8PiECLLY5fnPTsdg+KgMLhGEYptB6yf0
/duiZOILtGi419QtvZYEfGj32/8wx44cHergcZ2NV1b6OmGPbcOrMbkmmQFQDqeNbTtAFW
i3LlhHaoE81DoKHtxYMq4UJyQn62Nq4+4707/6SFcFikKj
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ecdsa-sha2-nistp521 AAAAE2VjZHNhLXNoYTItbmlzdHA1MjEAAAAIbmlzdHA1MjEAAACFBAH8jyw6/dk7Fa64/AWSUpmxAGVznnujFo+UEyv6NzY3Bg1ZO4iltpQBlIce4Rx31Qb4SxryLGKJyZFg0z9ZJzazEgCqKAiRbMEdtlQaYS23i1OMsRVeDRPX5wdItVpUofV8VAd8SWwIWsMHQREtxJTCnBXcZLxHbI/s13s1S9CqfLwAtA=="
        set source built-in
    next
    edit "Fortinet_SSH_ED25519"
        set password ENC Zo3R2hjaWBq12vl0HwUfFQMMknsQTNViDnvTlRnnsAWNS7YBLGBDsWwtIMPi533GUhSzfjmTrsP3uenbxPWA1ARXenO6g2Crh7izT7OkhQH3PTFxZvyrXlY0ZI4fKZeMbMswALQyxHejs/Ra4WiS0sSL5XWMRyQbVP89GSR8NjUHA/0AGEVnCKnmCwFExvnXAJ3Y5w==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABCO6P8VlX
1Z4H849vf7rt/aAAAAEAAAAAEAAAAzAAAAC3NzaC1lZDI1NTE5AAAAIEaaKXZ5MSNhdrHU
g9BEHp1dBMz8Sx6RqD5DqCAWJT4WAAAAkJnLQD+6hBOWy6YAB0Tl91Mwq1liyzzu/Mql+8
VWDBTZh3OiEPEV2sKCzkajeVnN7yAfLwy06wJb96Xalsb5xTUY9Z9flfOQacVpaBlqdd9v
sdisDbGSv4NarVMZsGUYF12GEkmf0TRxp9XE5jryZIwbQhBjk1Y2ULGgpd3f3j69SLbQph
KpuSE2VHqHvE9XUw==
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ssh-ed25519 AAAAC3NzaC1lZDI1NTE5AAAAIEaaKXZ5MSNhdrHUg9BEHp1dBMz8Sx6RqD5DqCAWJT4W"
        set source built-in
    next
end
config firewall ssh local-ca
    edit "Fortinet_SSH_CA"
        set password ENC AAAAAWadQA+C1DIoPFC9lbvTK8P98EtFjA0n27+oGQzKL30kzpPNzWEiZWts4o12hxw2ugz1LMn4qISIxRwu3qjjZ4ZPqN+Y5CGNpNCqGNT5ZkAI0gyr8374i5D83dOCLxGjwMRkDtkM4Z+DxQPgo3S4+RFpTofvtQ9ZYDkt8cFolU7cIADUxpDQQPHPr2KxlpljHg==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABDw8udGTS
i9G1I/kDU3FtleAAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQC988UGkKkK
9irsqq34VtzMLgoelIBb8Mpuo7lbOCiwGa7QPm1rZTDL0kdcFLz8KQc7ANRcHn5F2nFjrG
nNSCj3MCR1gD6ExX+WYx/zsAl3ypj0h+a2wRNr4vre0nS+eDIKXiqMbf9D/R8kg0/lkuOX
SeYgCMz/Fa/o9iQu99RakU6ff5jwCtLA54fFAmbal1Fj51oII4njF8ZfPgVZSj2LvodW8c
I4lYuXnyElpJpNhgCv1oEAssJZOy7VjtbA9bxETj3rwNbOlY8i8oZcvEfXP7iAvhWfwB9R
3blEWEjgbXYlxAjUrX7ss1uXjQTOYmfGaLFezxoC2rlTpv0uDXrfAAADwKN8RjfuTvLd2H
favS58nIhce19LUR82Din2D23OzAK0B/G9C3J264mgvEtcZ1YrPSUUN94qJFgAGLi4QulD
DAQiufMsZ9e6sHs8rO6DxaKcaPSKLeLfY+pT9yemufQPJHcYre11dLZS2pEEELjsqb9BGX
18qfJwP/sriRs5dcqfqN9UfnX0e73DSOhN98WQtfZ4O/LbupUdwTKQr+SBY2R07XfKY0XE
yAw/zimcM31DuyPeE/7hFnk/Njz8FsyQWdcJLVRwQe1ak+ocQF8Y7Wj4Av8X+Z1Bq32uJW
vusnxMx41CWCIYGSk242LXYvrk8ZqZAhNNeePEnED9CfEUJ/aMJ8HALColBbhzPzXWIDFG
6LDqEHIukKGuAFQl1oqiPG4LHezBQ1G+pcLchngE0Aqq9msFI7+v9imxRhBTrIM8DhE5Sa
X3KpOhciVCteSDpmKblqP/urEVFUNmFEpPJL1voP/c/0+AMmQlcbOruqtkF4IZ/+4h7L7x
N5PmBn59YzigrvKWCkkHYo17QzNf5b/gasDY7gmPpJC76VvrfQZXNMwP4GHkH94xeOX8aB
TYxonksS09O7oCsBmvOX0HskUlyTFjojXJ46YGeTtuUCa1IpUHDzWMJl0pSrAhAqMPNqB/
IZ+lEM3nIWHPDH1T1EFnJgBwhqOh/osMmbwAr2phc254bk2rBgGr+BhmiHamIYA+KbmLxB
LqM0JgSv0t1q9hs7Wy9ihoJj1a7RQKDfTCfJTB2Rhmh1qoJkRyudmsnkRVLv2oDkjwaXIB
wzYMxF9FmH1I/9YGgUMZcWI8+APgaNP4D8FjY+D+I5e9zIOolb0Yfk0deA18rtgPHJf7k+
cQAl+2/FiAOXgzlzCqjiKRlwMRY4tbc0kMIUFKefiXg/CN53MFGN2HsBEa+14JwuD8Dt7P
TRfg+xrv6+OMzUUUGqx5f3h4X/GycM2rnEmmp8tNmVyfEGCAgd6K/CnDoA03KD5ns7z47V
RFItl2aXPazRKuI28gLPZjvkdKYZRPkge0jQHPzUWRuOjIuCzdzvpuYKmYwg+J1OQn05gV
69kXxNZj8ZMyy+pdRifbmxPN1W5tMN0J7mqynk4dTIwr4shtqolyYp+fxCvZTiI/yzq0RN
6XSh26f3fnQDrdOtW49DnnpCcKrUQkfKFUYkj1bl3lvBFZcp4VS28Wl0V7mhKJvrQmxy3V
R4u/fdbA+1+510KO0dU8uxgGgWAC0PSqa0mbqvkbDTFzkEgb+C/l95hvKVZzDiTbgMLNjN
Sd04H7oQ==
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC988UGkKkK9irsqq34VtzMLgoelIBb8Mpuo7lbOCiwGa7QPm1rZTDL0kdcFLz8KQc7ANRcHn5F2nFjrGnNSCj3MCR1gD6ExX+WYx/zsAl3ypj0h+a2wRNr4vre0nS+eDIKXiqMbf9D/R8kg0/lkuOXSeYgCMz/Fa/o9iQu99RakU6ff5jwCtLA54fFAmbal1Fj51oII4njF8ZfPgVZSj2LvodW8cI4lYuXnyElpJpNhgCv1oEAssJZOy7VjtbA9bxETj3rwNbOlY8i8oZcvEfXP7iAvhWfwB9R3blEWEjgbXYlxAjUrX7ss1uXjQTOYmfGaLFezxoC2rlTpv0uDXrf"
        set source built-in
    next
    edit "Fortinet_SSH_CA_Untrusted"
        set password ENC AAAAAS6reRF/FnPMYLRCXeW7ehND9DamehNu+YU2SS5hw1ZJlF9VBOYfYnmoaroLb3xotobmbmXxQEODPY0m13rcvrWpU4W5WlKsCvmJBT+q2+/Ns/yXohZu84kC5kjRGsesuaEBntVSKTUP1yre4s+4vBo0o1zsto48u7MeXT35t8Wy8S8Wd/ra2Fj3belxuBnnUQ==
        set private-key "-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAACmFlczI1Ni1jdHIAAAAGYmNyeXB0AAAAGAAAABAPDuNz1N
qUDNis/aKtnm/8AAAAEAAAAAEAAAEXAAAAB3NzaC1yc2EAAAADAQABAAABAQC+CAkKg8lA
lh8hXRgwNtPE+81ro/hgzPShACCDr1uYBzRG7X84lzdSR598/DQUiKlGchZmAH3cthdKQk
gBkLQIyUYHs7x3XQSiTHfyFpi1uORolQ16zQWe4SLZs6h0ym8lIEcCFnJmZ0R8D8WhXVRM
5kFHNGBYChTcEbpWEwm+A2LRESNVwg6E7gDoTV55wPE6G/aVSBjwDTiHIiwHk5lFOu3xHX
Keo6VTinXbF0oEXw7P21tXRc+R2Xyf7Kqb8DqWjbU9Ixs9842IGhamU9pBGXqz97QuwTQp
dXaSSxjHvFRVvYojdIfK56lNI1RH1wkFa78mWtLoY7OcNpxFojLtAAADwFm2GaYARnxAbm
X8pAbDxgNvSORR155hw1mshI7sQv5ZIrOUBq2KgIMdQKrDwu1pXjFQEStsIeDxUT1mYc5W
SRRBZ72zYeJzhHE3XpNMeJgyh5SOmXgFh+8nwk43VT9yTpo/6vSqCaAcLyWeyAg5tJQ2w6
04w6oIo2cUsAmLitZkdwq0DDCnhFwsy0LC8k5L2efrOPh/GcT1+vDD2ZjOILspyj8eNKDP
eYM5jauxEgNHdSkSi8tfU3zKG/aSg4eEMtPELeLc9JbMhs0nxkBK5NUs1vCVA2V9fvV9FQ
WfKVZwQoRPhkRDHVBxZJlOL148hlXEpp21ckSUMTyto3uMMxafc9cq9pfDT9CEZ0iLnBG3
ljOVIwM03B/5/iLGw5nHRnhwvqkUgSCsFx47H7/OwHmYmQmNXOHZoLE8WDFoVbF/4deUsf
8glXlFAA/Phy0tZEJ1wYfvbLbp5LJ0j+jP0vtnUC0Ob7DYz1cwDIIeGnb3pLPL5aqPgZXJ
/K1dwnktLrjvlzCphqEjSyiGYbDE9aIE5OJjU5EHO2TC+rzZ4D3Khn10pWYv2kVNlJpEII
UdIUeZiZG0umvNYSJSOzrFd+usT0WA4rQeVCg0n9SIag6CsIWh64kHI4pS+JdbRQhj3Z+M
bqEovQKthi5RFtKiwRjNlS1D5HdT2OY05ZhXF+pz1cLsTKN6usa3nSBpKuIwrQcYrPV/0x
ypfHeGHppEGj8gKJXpBEYt4+VKxhJ2dvCNmiPDUl0za4/45KlF6OQVilVArSRLMJrxZl5w
/HPdFdpowFxiOxfKgk1frHkwlCHGW/M0/hvCjH/DQn4IqYBgvAcwCZIai0QI4RYcl0SN2W
Ek+x6kXmcLcNIYXFWWZXbC0urHEfP2u05rbbBs1R2Ks7WQ4cvLMoKb16almsvLOiFVAOtx
sGvILMYTLybMtZ5OlVO23AEw8SYa/dtMnNOZWG1gKEiD59mYLRtQZPhn8G8HlFBoZTGSks
cBU8QQF09DjhSOvh5XP5wZtDin4g8u1aRZXw5PnP7u0l1LPN4LFpHrE0RBa+sy153IQbME
BgKI6ulYXRkYOaAnoDMfPkinZ3Qtn4fmRboUXmjIlssF2xYPJyKLBreQTpIcJDTVy2cDdr
weOydORAXunkxcZ7BvoYSqFKKxqs3sm98LRAiYSfBv1pT9TGq1XqnwlZoqJeoRn3R9oUHf
ofDUWvBLlN28QXyPxdDVCPVtDOUR3WYjwWYIImhbiwzb7eofghuMLwM+qr0URK7ZbM4eLB
1QLzgwMQ==
-----END OPENSSH PRIVATE KEY-----
"
        set public-key "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQC+CAkKg8lAlh8hXRgwNtPE+81ro/hgzPShACCDr1uYBzRG7X84lzdSR598/DQUiKlGchZmAH3cthdKQkgBkLQIyUYHs7x3XQSiTHfyFpi1uORolQ16zQWe4SLZs6h0ym8lIEcCFnJmZ0R8D8WhXVRM5kFHNGBYChTcEbpWEwm+A2LRESNVwg6E7gDoTV55wPE6G/aVSBjwDTiHIiwHk5lFOu3xHXKeo6VTinXbF0oEXw7P21tXRc+R2Xyf7Kqb8DqWjbU9Ixs9842IGhamU9pBGXqz97QuwTQpdXaSSxjHvFRVvYojdIfK56lNI1RH1wkFa78mWtLoY7OcNpxFojLt"
        set source built-in
    next
end
config firewall ssh setting
    set caname "Fortinet_SSH_CA"
    set untrusted-caname "Fortinet_SSH_CA_Untrusted"
    set hostkey-rsa2048 "Fortinet_SSH_RSA2048"
    set hostkey-dsa1024 "Fortinet_SSH_DSA1024"
    set hostkey-ecdsa256 "Fortinet_SSH_ECDSA256"
    set hostkey-ecdsa384 "Fortinet_SSH_ECDSA384"
    set hostkey-ecdsa521 "Fortinet_SSH_ECDSA521"
    set hostkey-ed25519 "Fortinet_SSH_ED25519"
end
config switch-controller security-policy 802-1X
    edit "802-1X-policy-default"
        set user-group "SSO_Guest_Users"
        set mac-auth-bypass disable
        set open-auth disable
        set eap-passthru enable
        set guest-vlan disable
        set auth-fail-vlan disable
        set framevid-apply enable
        set radius-timeout-overwrite disable
    next
end
config switch-controller security-policy local-access
    edit "default"
        set mgmt-allowaccess https ping ssh
        set internal-allowaccess https ping ssh
    next
end
config switch-controller lldp-profile
    edit "default"
        set med-tlvs inventory-management network-policy location-identification
        set auto-isl disable
    next
    edit "default-auto-isl"
    next
end
config switch-controller qos dot1p-map
    edit "voice-dot1p"
        set priority-0 queue-4
        set priority-1 queue-4
        set priority-2 queue-3
        set priority-3 queue-2
        set priority-4 queue-3
        set priority-5 queue-1
        set priority-6 queue-2
        set priority-7 queue-2
    next
end
config switch-controller qos ip-dscp-map
    edit "voice-dscp"
        config map
            edit "1"
                set cos-queue 1
                set value 46
            next
            edit "2"
                set cos-queue 2
                set value 24,26,48,56
            next
            edit "5"
                set cos-queue 3
                set value 34
            next
        end
    next
end
config switch-controller qos queue-policy
    edit "default"
        set schedule round-robin
        set rate-by kbps
        config cos-queue
            edit "queue-0"
            next
            edit "queue-1"
            next
            edit "queue-2"
            next
            edit "queue-3"
            next
            edit "queue-4"
            next
            edit "queue-5"
            next
            edit "queue-6"
            next
            edit "queue-7"
            next
        end
    next
    edit "voice-egress"
        set schedule weighted
        set rate-by kbps
        config cos-queue
            edit "queue-0"
            next
            edit "queue-1"
                set weight 0
            next
            edit "queue-2"
                set weight 6
            next
            edit "queue-3"
                set weight 37
            next
            edit "queue-4"
                set weight 12
            next
            edit "queue-5"
            next
            edit "queue-6"
            next
            edit "queue-7"
            next
        end
    next
end
config switch-controller qos qos-policy
    edit "default"
    next
    edit "voice-qos"
        set trust-dot1p-map "voice-dot1p"
        set trust-ip-dscp-map "voice-dscp"
        set queue-policy "voice-egress"
    next
end
config switch-controller storm-control-policy
    edit "default"
        set description "default storm control on all port"
    next
    edit "auto-config"
        set description "storm control policy for fortilink-isl-icl port"
        set storm-control-mode disabled
    next
end
config switch-controller auto-config policy
    edit "default"
    next
end
config switch-controller auto-config default
    set fgt-policy "default"
    set isl-policy "default"
    set icl-policy "default"
end
config switch-controller switch-profile
    edit "default"
    next
end
config wireless-controller wids-profile
    edit "default"
        set comment "Default WIDS profile."
        set ap-scan enable
        set wireless-bridge enable
        set deauth-broadcast enable
        set null-ssid-probe-resp enable
        set long-duration-attack enable
        set invalid-mac-oui enable
        set weak-wep-iv enable
        set auth-frame-flood enable
        set assoc-frame-flood enable
        set spoofed-deauth enable
        set asleap-attack enable
        set eapol-start-flood enable
        set eapol-logoff-flood enable
        set eapol-succ-flood enable
        set eapol-fail-flood enable
        set eapol-pre-succ-flood enable
        set eapol-pre-fail-flood enable
    next
    edit "default-wids-apscan-enabled"
        set ap-scan enable
    next
end
config wireless-controller wtp-profile
    edit "FAPU323EV-default"
        config platform
            set type U323EV
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPU321EV-default"
        config platform
            set type U321EV
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPU24JEV-default"
        config platform
            set type U24JEV
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPU223EV-default"
        config platform
            set type U223EV
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPU221EV-default"
        config platform
            set type U221EV
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPU423E-default"
        config platform
            set type U423E
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPU422EV-default"
        config platform
            set type U422EV
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPU421E-default"
        config platform
            set type U421E
        end
        config radio-1
            set band 802.11n
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP321E-default"
        config platform
            set type 321E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS223E-default"
        config platform
            set type S223E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS221E-default"
        config platform
            set type S221E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP224E-default"
        config platform
            set type 224E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP223E-default"
        config platform
            set type 223E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP222E-default"
        config platform
            set type 222E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP221E-default"
        config platform
            set type 221E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP423E-default"
        config platform
            set type 423E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP421E-default"
        config platform
            set type 421E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS423E-default"
        config platform
            set type S423E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS422E-default"
        config platform
            set type S422E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS421E-default"
        config platform
            set type S421E
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS323CR-default"
        config platform
            set type S323CR
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS322CR-default"
        config platform
            set type S322CR
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS321CR-default"
        config platform
            set type S321CR
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS313C-default"
        config platform
            set type S313C
        end
        config radio-1
            set band 802.11ac
        end
    next
    edit "FAPS311C-default"
        config platform
            set type S311C
        end
        config radio-1
            set band 802.11ac
        end
    next
    edit "FAPS323C-default"
        config platform
            set type S323C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS322C-default"
        config platform
            set type S322C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAPS321C-default"
        config platform
            set type S321C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP321C-default"
        config platform
            set type 321C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP223C-default"
        config platform
            set type 223C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP112D-default"
        config platform
            set type 112D
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP24D-default"
        config platform
            set type 24D
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP21D-default"
        config platform
            set type 21D
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FK214B-default"
        config platform
            set type 214B
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP224D-default"
        config platform
            set type 224D
        end
        config radio-1
            set band 802.11n-5G
        end
        config radio-2
            set band 802.11n,g-only
        end
    next
    edit "FAP222C-default"
        config platform
            set type 222C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP25D-default"
        config platform
            set type 25D
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP221C-default"
        config platform
            set type 221C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP320C-default"
        config platform
            set type 320C
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11ac
        end
    next
    edit "FAP28C-default"
        config platform
            set type 28C
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP223B-default"
        config platform
            set type 223B
        end
        config radio-1
            set band 802.11n-5G
        end
        config radio-2
            set band 802.11n,g-only
        end
    next
    edit "FAP14C-default"
        config platform
            set type 14C
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP11C-default"
        config platform
            set type 11C
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP320B-default"
        config platform
            set type 320B
        end
        config radio-1
            set band 802.11n-5G
        end
        config radio-2
            set band 802.11n,g-only
        end
    next
    edit "FAP112B-default"
        config platform
            set type 112B
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP222B-default"
        config platform
            set type 222B
        end
        config radio-1
            set band 802.11n,g-only
        end
        config radio-2
            set band 802.11n-5G
        end
    next
    edit "FAP210B-default"
        config platform
            set type 210B
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
    edit "FAP220B-default"
        config radio-1
            set band 802.11n-5G
        end
        config radio-2
            set band 802.11n,g-only
        end
    next
    edit "AP-11N-default"
        config platform
            set type AP-11N
        end
        config radio-1
            set band 802.11n,g-only
        end
    next
end
config wireless-controller utm-profile
    edit "wifi-default"
        set comment "Default configuration for offloading WiFi traffic."
        set ips-sensor "wifi-default"
        set application-list "wifi-default"
        set antivirus-profile "wifi-default"
        set webfilter-profile "wifi-default"
    next
end
config log memory setting
    set status enable
end
config log disk setting
    set status enable
end
config log null-device setting
    set status disable
end
config router rip
    config redistribute "connected"
    end
    config redistribute "static"
    end
    config redistribute "ospf"
    end
    config redistribute "bgp"
    end
    config redistribute "isis"
    end
end
config router ripng
    config redistribute "connected"
    end
    config redistribute "static"
    end
    config redistribute "ospf"
    end
    config redistribute "bgp"
    end
    config redistribute "isis"
    end
end
config router static
    edit 1
        set gateway 192.168.1.254
        set device "port1"
    next
end
config router ospf
    config redistribute "connected"
    end
    config redistribute "static"
    end
    config redistribute "rip"
    end
    config redistribute "bgp"
    end
    config redistribute "isis"
    end
end
config router ospf6
    config redistribute "connected"
    end
    config redistribute "static"
    end
    config redistribute "rip"
    end
    config redistribute "bgp"
    end
    config redistribute "isis"
    end
end
config router bgp
    config redistribute "connected"
    end
    config redistribute "rip"
    end
    config redistribute "ospf"
    end
    config redistribute "static"
    end
    config redistribute "isis"
    end
    config redistribute6 "connected"
    end
    config redistribute6 "rip"
    end
    config redistribute6 "ospf"
    end
    config redistribute6 "static"
    end
    config redistribute6 "isis"
    end
end
config router isis
    config redistribute "connected"
    end
    config redistribute "rip"
    end
    config redistribute "ospf"
    end
    config redistribute "bgp"
    end
    config redistribute "static"
    end
    config redistribute6 "connected"
    end
    config redistribute6 "rip"
    end
    config redistribute6 "ospf"
    end
    config redistribute6 "bgp"
    end
    config redistribute6 "static"
    end
end
config router multicast
end
```


## Probar funcionamiento

- Del lado del fortigate en CLI se puede sniffear ICMP (ping)

    - **`diagnose sniffer packet any 'icmp' 4`**

- Del lado del Switch tirar pings hacia cada una de las interfaces VLAN

    - `ping 192.168.10.10`
    - `ping 192.168.20.10`    
    - `ping 192.168.30.10`      
    - `ping 192.168.88.10`   

- Asignar IP a cada PC via DHCP, se debe asignar un segmento de su VLAN correspondiente
- También debe hacer ping a Internet como 1.1.1.1, google.com, 8.8.8.8, cisco.com, etc. 

    - `ip dhcp`    

### Ejemplo:

- Fortigate:

```
FortiGate-VM64-KVM # diagnose sniffer packet any 'icmp' 4
.
.
.
(tirar ping del lado del switch)
.
.
.

interfaces=[any]
filters=[icmp]
43.652999 VLAN_10_RED in 192.168.10.1 -> 192.168.10.10: icmp: echo request
43.653107 VLAN_10_RED out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.653109 LAG_LACP out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.653110 port3 out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.654804 VLAN_10_RED in 192.168.10.1 -> 192.168.10.10: icmp: echo request
43.654809 VLAN_10_RED out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.654810 LAG_LACP out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.654810 port3 out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.656326 VLAN_10_RED in 192.168.10.1 -> 192.168.10.10: icmp: echo request
43.656336 VLAN_10_RED out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.656336 LAG_LACP out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.656337 port3 out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.657731 VLAN_10_RED in 192.168.10.1 -> 192.168.10.10: icmp: echo request
43.657745 VLAN_10_RED out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.657746 LAG_LACP out 192.168.10.10 -> 192.168.10.1: icmp: echo reply
43.657746 port3 out 192.168.10.10 -> 192.168.10.1: icmp: echo reply

```

- Switch:

```
SW1_Core-F0#
SW1_Core-F0#ping 192.168.10.10
Type escape sequence to abort.
Sending 5, 100-byte ICMP Echos to 192.168.10.10, timeout is 2 seconds:
.!!!!
Success rate is 80 percent (4/5), round-trip min/avg/max = 1/1/1 ms
SW1_Core-F0#
```

- Lo mismo con todas las VLANs (_excepto la 99 que se quedó como Native para no usar la Defoult 1_)

---

- Dudas

    - No se debe asignar una nativa en la troncal del fortigate??? En este caso la 99??? O usa la default 1??? o no importa???
    - Routing entre diferentes subnets, como se abre?



