## Link Aggregation

### Topology

![image](https://user-images.githubusercontent.com/94720207/188337555-66b19a28-6ece-4849-8815-ad55cd552bc6.png)

```
==========================================================

                          (_.- Fz3r0 -._)
          
          Secure Network Labs

          Fortigate LACP (LAG) + Cisco Switch
          VLANs + Trunks
          DHCP
          Internet Access

          Github : Fz3r0
          Twitter: Fz3r0_OPs

==========================================================
```

#### Puertos/Interfaces a utilizar:

```
<<< FortiGate >>>

    - WAN | INTERNET

        - Port1

    + LAG:

        - Port4 + Port5

<<< Cisco Switch >>>

    + LAG:

        - Gi 0/0 + Gi 0/1
```

#### VLANs

- VLAN_10_RED
- VLAN_20_BLUE
- VLAN_30_YELLOW
- VLAN_88_Management
- VLAN_99_TrunkNative

### Intro

- El Fortigate solo tiene configurada una interfaz via DHCP para entra rpor UI.
- El Cisco Switch no tiene nada, está por defecto. 

## Configuraciones

- En este ejemplo empezaré por los switches y después el Forti, en realidad no importa el orden anyways...

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

### Interfaces

- Objetivo:

![image](https://user-images.githubusercontent.com/94720207/188336095-5fcbbc7d-a542-4bfe-a580-e92b8a905dd2.png)

- Port1: Internet

![image](https://user-images.githubusercontent.com/94720207/188336130-b800a0c7-0435-4403-a7c8-44637f052f5e.png)

- Port4 & Port5: Link Aggregation (LAG/LACP)

![image](https://user-images.githubusercontent.com/94720207/188336160-2bbe4444-f483-4309-be05-7e0417b2bd34.png)

- VLANs (Ejemplo con solo una, solo cambiar lo correspondiente a las demás)

![image](https://user-images.githubusercontent.com/94720207/188336202-40f638b5-4c2d-487e-9b2d-b17945c6d2de.png)

### DNS

![image](https://user-images.githubusercontent.com/94720207/188336264-5fac4157-0d06-4df0-b324-0bdd2bb28891.png)

### Static Route

![image](https://user-images.githubusercontent.com/94720207/188336284-98972207-a42c-4ebd-ae8b-da5339e3fdba.png)

### IPv4 Policy

- Salida a Internet para cada VLAN e Interfaz física

- Objetivo:

![image](https://user-images.githubusercontent.com/94720207/188336310-5cf84372-4951-44fa-9f94-e5d474ee6048.png)

- Ejemplo (Ejemplo con solo una, solo cambiar lo correspondiente a las demás)

![image](https://user-images.githubusercontent.com/94720207/188336338-cc4abe4c-4ea5-4a50-ab87-6e4ae31c75ac.png)

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

- Pruebas desdee las PCs con DHCP y acceso a Internet:

```
Test-VPCS> 
Test-VPCS> ip dhcp
DDORA IP 192.168.88.51/24 GW 192.168.88.10      <<<<---- RECIBE DHCP DE LA SUBNET/VLAN CORRESPONDIENTE AL PUERTO ;)

Test-VPCS> ping 1.1.1.1                         <<<<---- HACE PING HACIA INTERNET/WAN ;)

84 bytes from 1.1.1.1 icmp_seq=1 ttl=127 time=79.783 ms
84 bytes from 1.1.1.1 icmp_seq=2 ttl=127 time=421.692 ms
84 bytes from 1.1.1.1 icmp_seq=3 ttl=127 time=80.371 ms
84 bytes from 1.1.1.1 icmp_seq=4 ttl=127 time=78.660 ms
84 bytes from 1.1.1.1 icmp_seq=5 ttl=127 time=80.230 ms

Test-VPCS> ping google.com
google.com resolved to 142.250.217.206         <<<<---- RESUELVE DNS A GOOGLE.COM ;)

84 bytes from 142.250.217.206 icmp_seq=1 ttl=127 time=48.258 ms
84 bytes from 142.250.217.206 icmp_seq=2 ttl=127 time=227.230 ms
84 bytes from 142.250.217.206 icmp_seq=3 ttl=127 time=195.798 ms
84 bytes from 142.250.217.206 icmp_seq=4 ttl=127 time=26.935 ms
84 bytes from 142.250.217.206 icmp_seq=5 ttl=127 time=23.096 ms

Test-VPCS> ping 192.168.88.50                  <<<<---- HACE PING A OTRA PC DE MISMA VLAN/SUBNET ;)

84 bytes from 192.168.88.50 icmp_seq=1 ttl=64 time=5.519 ms
84 bytes from 192.168.88.50 icmp_seq=2 ttl=64 time=3.192 ms
84 bytes from 192.168.88.50 icmp_seq=3 ttl=64 time=3.317 ms
84 bytes from 192.168.88.50 icmp_seq=4 ttl=64 time=4.277 ms
84 bytes from 192.168.88.50 icmp_seq=5 ttl=64 time=4.585 ms

Test-VPCS> 
```

---

- I am the darkness:

![image](https://user-images.githubusercontent.com/94720207/188338444-5435d38e-3c05-47e6-a9ae-b1738d101403.png)

---

![image](https://user-images.githubusercontent.com/94720207/188338515-83afd81d-acb1-4476-bece-8a5a1090e0b3.png)

![image](https://user-images.githubusercontent.com/94720207/188338584-453cad31-d6ff-4bc1-aa68-b3617f6c1fd6.png)

![image](https://user-images.githubusercontent.com/94720207/188338616-9d539904-9e19-45c1-a094-9a1e829a70fa.png)

---

- Dudas

    - No se debe asignar una nativa en la troncal del fortigate??? En este caso la 99??? O usa la default 1??? o no importa???
    - Routing entre diferentes subnets, como se abre?



