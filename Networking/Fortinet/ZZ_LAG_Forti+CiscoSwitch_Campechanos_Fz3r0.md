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
- VLAN_40_GREEN
- VLAN_50_PURPLE
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
name VLAN_40_GREEN 
vlan 50
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
interface vlan 40
ip address 192.168.40.1 255.255.255.0
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
switchport trunk allowed vlan 10,20,30,40,88
no shutdown 
exit
!
```

## Switch Full Command Fz3r0 God

```
!
!
enable
configure terminal
!
hostname SW1_Core-F0
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 30
name VLAN_30_YELLOW  
vlan 40
name VLAN_40_GREEN 
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
interface vlan 40
ip address 192.168.40.1 255.255.255.0
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
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,40,88
no shutdown 
exit
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
SW1_Core-F0(config)#!
SW1_Core-F0(config)#vlan 10
SW1_Core-F0(config-vlan)#name VLAN_10_RED 
SW1_Core-F0(config-vlan)#vlan 20
SW1_Core-F0(config-vlan)#name VLAN_20_BLUE 
SW1_Core-F0(config-vlan)#vlan 30
SW1_Core-F0(config-vlan)#name VLAN_30_YELLOW  
SW1_Core-F0(config-vlan)#vlan 40
SW1_Core-F0(config-vlan)#name VLAN_40_GREEN 
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
SW1_Core-F0(config)#interface vlan 40
SW1_Core-F0(config-if)#ip address 192.168.40.1 255.255.255.0
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
SW1_Core-F0(config-if)#switchport trunk encapsulation dot1q
SW1_Core-F0(config-if)#switchport mode trunk
SW1_Core-F0(config-if)#switchport trunk native vlan 99
SW1_Core-F0(config-if)#switchport trunk allowed vlan 10,20,30,40,88
SW1_Core-F0(config-if)#no shutdown 
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#end
SW1_Core-F0#!
SW1_Core-F0#wr
Building configuration...

*Sep  4 18:32:01.973: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to down
*Sep  4 18:32:02.030: %SYS-5-CONFIG_I: Configured from console by console
*Sep  4 18:32:02.320: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to down
*Sep  4 18:32:02.409: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan30, changed state to down
*Sep  4 18:32:02.482: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan40, changed state to down
*Sep  4 18:32:02.568: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan88, changed state to down
*Sep  4 18:32:02.656: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan99, changed state to downCompressed configuration from 4361 bytes to 1998 bytes[OK]
*Sep  4 18:32:03.292: %LINK-3-UPDOWN: Interface Vlan10, changed state to down
*Sep  4 18:32:03.376: %LINK-3-UPDOWN: Interface Vlan20, changed state to down
*Sep  4 18:32:03.448: %LINK-3-UPDOWN: Interface Vlan30, changed state to down
*Sep  4 18:32:03.545: %LINK-3-UPDOWN: Interface Vlan40, changed state to down
*Sep  4 18:32:03.630: %LINK-3-UPDOWN: Interface Vlan88, changed state to down
*Sep  4 18:32:03.788: %LINK-3-UPDOWN: Interface Vlan99, changed state to down
SW1_Core-F0#!
SW1_Core-F0#!
SW1_Core-F0#!
*Sep  4 18:32:04.495: %GRUB-5-CONFIG_WRITING: GRUB configuration is being updated on disk. Please wait...
*Sep  4 18:32:05.145: %GRUB-5-CONFIG_WRITTEN: GRUB configuration was written to disk successfully.
SW1_Core-F0#
*Sep  4 18:32:12.738: %EC-5-L3DONTBNDL2: Gi0/0 suspended: LACP currently not enabled on the remote port.
*Sep  4 18:32:13.564: %EC-5-L3DONTBNDL2: Gi0/1 suspended: LACP currently not enabled on the remote port.
SW1_Core-F0#
SW1_Core-F0#
SW1_Core-F0#
SW1_Core-F0#
SW1_Core-F0#
SW1_Core-F0#!
SW1_Core-F0#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/0, Gi0/1, Gi0/2, Gi0/3
                                                Gi1/0, Gi1/1, Gi1/2, Gi1/3
                                                Gi2/0, Gi2/1, Gi2/2, Gi2/3
                                                Gi3/0, Gi3/1, Gi3/2, Gi3/3
10   VLAN_10_RED                      active    
20   VLAN_20_BLUE                     active    
30   VLAN_30_YELLOW                   active    
40   VLAN_40_GREEN                    active    
88   VLAN_88_Management               active    
99   VLAN_99_TrunkNative              active    
1002 fddi-default                     act/unsup 
1003 token-ring-default               act/unsup 
1004 fddinet-default                  act/unsup 
1005 trnet-default                    act/unsup 
SW1_Core-F0#!
SW1_Core-F0#show ip interface brief
Interface              IP-Address      OK? Method Status                Protocol
GigabitEthernet0/0     unassigned      YES unset  down                  down    
GigabitEthernet0/1     unassigned      YES unset  down                  down    
GigabitEthernet0/2     unassigned      YES unset  down                  down    
GigabitEthernet0/3     unassigned      YES unset  down                  down    
GigabitEthernet1/0     unassigned      YES unset  down                  down    
GigabitEthernet1/1     unassigned      YES unset  down                  down    
GigabitEthernet1/2     unassigned      YES unset  down                  down    
GigabitEthernet1/3     unassigned      YES unset  down                  down    
GigabitEthernet2/0     unassigned      YES unset  down                  down    
GigabitEthernet2/1     unassigned      YES unset  down                  down    
GigabitEthernet2/2     unassigned      YES unset  down                  down    
GigabitEthernet2/3     unassigned      YES unset  down                  down    
GigabitEthernet3/0     unassigned      YES unset  down                  down    
GigabitEthernet3/1     unassigned      YES unset  down                  down    
GigabitEthernet3/2     unassigned      YES unset  down                  down    
GigabitEthernet3/3     unassigned      YES unset  down                  down    
Port-channel10         unassigned      YES unset  down                  down    
Vlan10                 192.168.10.1    YES manual down                  down    
Vlan20                 192.168.20.1    YES manual down                  down    
Vlan30                 192.168.30.1    YES manual down                  down    
Vlan40                 192.168.40.1    YES manual down                  down    
          
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
10     Po10(SD)        LACP      Gi0/0(s)    Gi0/1(s)    

SW1_Core-F0#!
SW1_Core-F0#
```

- **NOTA: Hasta el momento no se ha conectado físicamente el cableado ni configurado Fortigate.**
- **En el momento que se configure y se conecten ambos puertos entre Switch <> Firewall se verá automáticamente la formación del LACP Channel-Port y VLANs UP:**

```
SW1_Core-F0#!
SW1_Core-F0#show vlan brief

VLAN Name                             Status    Ports
---- -------------------------------- --------- -------------------------------
1    default                          active    Gi0/2, Gi0/3, Gi1/0, Gi1/1
                                                Gi1/2, Gi1/3, Gi2/0, Gi2/1
                                                Gi2/2, Gi2/3, Gi3/0, Gi3/1
                                                Gi3/2, Gi3/3
10   VLAN_10_RED                      active    
20   VLAN_20_BLUE                     active    
30   VLAN_30_YELLOW                   active    
40   VLAN_40_GREEN                    active    
88   VLAN_88_Management               active    
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
GigabitEthernet1/1     unassigned      YES unset  down                  down    
GigabitEthernet1/2     unassigned      YES unset  down                  down    
GigabitEthernet1/3     unassigned      YES unset  down                  down    
GigabitEthernet2/0     unassigned      YES unset  down                  down    
GigabitEthernet2/1     unassigned      YES unset  down                  down    
GigabitEthernet2/2     unassigned      YES unset  down                  down    
GigabitEthernet2/3     unassigned      YES unset  down                  down    
GigabitEthernet3/0     unassigned      YES unset  down                  down    
GigabitEthernet3/1     unassigned      YES unset  down                  down    
GigabitEthernet3/2     unassigned      YES unset  down                  down    
GigabitEthernet3/3     unassigned      YES unset  down                  down    
Port-channel10         unassigned      YES unset  up                    up      
Vlan10                 192.168.10.1    YES manual up                    up      
Vlan20                 192.168.20.1    YES manual up                    up      
Vlan30                 192.168.30.1    YES manual up                    up      
Vlan40                 192.168.40.1    YES manual up                    up      
          
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
```

## Fortigate Config


## Probar funcionamiento

- Del lado del fortigate en CLI se puede sniffear ICMP (ping)

    - **`diagnose sniffer packet any 'icmp' 4`**

- Del lado del Switch tirar pings hacia cada una de las interfaces VLAN

    - `ping 192.168.10.10`
    - `ping 192.168.20.10`    
    - `ping 192.168.30.10`    
    - `ping 192.168.40.10`    
    - `ping 192.168.88.10`   

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


- Dudas - Nativa de Fortigate
