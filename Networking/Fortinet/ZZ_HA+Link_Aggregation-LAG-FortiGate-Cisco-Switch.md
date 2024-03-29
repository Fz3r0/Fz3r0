# FortiGate - HA + Switch Cisco + LAG + DHCP + INTERNET

<!--
```
==========================================================

                          (_.- Fz3r0 -._)
          
          Secure Network Labs

          Fortigate LACP (LAG) + Cisco Switch
          VLANs + Trunks
          DHCP per VLAN
          Internet Access
          High Availability (HA)

          Github : Fz3r0
          Twitter: Fz3r0_OPs

==========================================================
```
-->

## Topology

![image](https://user-images.githubusercontent.com/94720207/188366956-cb4f4d6a-b258-4f55-8d5e-c24a8cd9431e.png)



## Downloads



## Introducción

- El Fortigate solo tiene configurada una interfaz via DHCP para entra rpor UI.
- El Cisco Switch no tiene nada, está por defecto. 

### Puertos/Interfaces a utilizar:

```
<<< FortiGate >>>

    - WAN | INTERNET

        - Port1

    + LAG-1:

        - Port2 + Port3

    + LAG-2:

        - Port4 + Port5        

<<< Cisco Switch >>>

    + LAG-1:

        - Gi 3/0 + Gi 3/1

    + LAG-1:

        - Gi 3/2 + Gi 3/3        
```

#### VLANs

- VLAN_10_RED
- VLAN_20_BLUE
- VLAN_88_Management
- VLAN_99_TrunkNative

## Configuraciones

- En este ejemplo empezaré por los switches y después el Forti, en realidad no importa el orden anyways...
- En el `Fortigate1` & `Fortigate2` solo está configurado el `Port1` con DHCP para poder entrar a UI

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
"                 Twitter:  @Fz3r0_OPs                  "
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
interface vlan 88
ip address 192.168.88.1 255.255.255.0
no shutdown
exit
interface vlan 99
ip address 192.168.99.1 255.255.255.0
no shutdown
exit
!
interface range gi 3/0 - 1
channel-group 10 mode active
no shutdown 
exit
!
interface port-channel 10
description LAG1_LAN_FORTI<>SWITCH
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,88
no shutdown 
exit
!
!
interface range gi 3/2 - 3
channel-group 20 mode active
no shutdown 
exit
!
interface port-channel 20
description LAG2_LAN_FORTI<>SWITCH
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,30,88
no shutdown 
exit
!
interface gi 0/0
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

- CLI View:

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
"                 Twitter:  @Fz3r0_OPs                  "
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
SW1_Core-F0(config)#interface vlan 88
SW1_Core-F0(config-if)#ip address 192.168.88.1 255.255.255.0
SW1_Core-F0(config-if)#no shutdown
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#interface vlan 99
SW1_Core-F0(config-if)#ip address 192.168.99.1 255.255.255.0
SW1_Core-F0(config-if)#no shutdown
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface range gi 3/0 - 1
SW1_Core-F0(config-if-range)#channel-group 10 mode active
Creating a port-channel interface Port-channel 10

SW1_Core-F0(config-if-range)#no shutdown 
SW1_Core-F0(config-if-range)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface port-channel 10
SW1_Core-F0(config-if)#description LAG1_LAN_FORTI<>SWITCH
SW1_Core-F0(config-if)#switchport trunk encapsulation dot1q
SW1_Core-F0(config-if)#switchport mode trunk
SW1_Core-F0(config-if)#switchport trunk native vlan 99
SW1_Core-F0(config-if)#switchport trunk allowed vlan 10,20,30,88
SW1_Core-F0(config-if)#no shutdown 
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface range gi 3/2 - 3
SW1_Core-F0(config-if-range)#channel-group 20 mode active
Creating a port-channel interface Port-channel 20

SW1_Core-F0(config-if-range)#no shutdown 
SW1_Core-F0(config-if-range)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(
*Sep  5 02:28:39.910: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to down
*Sep  5 02:28:40.244: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to down
*Sep  5 02:28:40.342: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan88, changed state to down
*Sep  5 02:28:40.436: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan99, changed state to down
*Sep  5 02:28:40.971: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet3/2, changed state to down
*Sep  5 02:28:40.979: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet3/3, changed state to down
*Sep  5 02:28:41.211: %LINK-3-UPDOWN: Interface Vlan10, changed state to down
*Sep  5 02:28:41.311: %LINK-3-UPDOWN: Interface Vlan20, changed state to down
*Sep  5 02:28:41.403: %LINK-3-UPDOWN: Interface Vlan88, changed state to down
*Sep  5 02:28:41.502: %LINK-3-UPDOWN: Interface Vlan99, changed state to downconfig)#interface port-channel 20
SW1_Core-F0(config-if)#description LAG2_LAN_FORTI<>SWITCH
SW1_Core-F0(config-if)#switchport trunk encapsulation dot1q
SW1_Core-F0(config-if)#switchport mode trunk
SW1_Core-F0(config-if)#switchport trunk native vlan 99
SW1_Core-F0(config-if)#switchport trunk allowed vlan 10,20,30,88
SW1_Core-F0(config-if)#no shutdown 
SW1_Core-F0(config-if)#exit
SW1_Core-F0(config)#!
SW1_Core-F0(config)#interface gi 0/0
SW1_Core-F0(config-if)#description TRUNK>>>SWITCH2_DISTRIBUTION_GI3/3
SW1_Core-F0(config-if)#switchport trunk encapsulation dot1q
SW1_Core-F0(config-if)#switchport mode trunk
SW1_Core-F0(config-if)#switchport trunk native vlan 99
SW1_Core-F0(config-if)#switchport trunk allowed vlan 10,20,30,88
SW1_Core-F0(config-if)#no shutdown 
SW1_Core-F0(config-if)#exit
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

*Sep  5 02:28:44.604: %SYS-5-CONFIG_I: Configured from console by console
*Sep  5 02:28:45.133: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet3/2, changed state to up
*Sep  5 02:28:45.136: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet3/3, changed state to upCompressed configuration from 5843 bytes to 2546 bytes[OK]
SW1_Core-F0#!
SW1_Core-F0#!
SW1_Core-F0#!
SW1_Core-F0#
*Sep  5 02:28:46.925: %GRUB-5-CONFIG_WRITING: GRUB configuration is being updated on disk. Please wait...
*Sep  5 02:28:47.584: %GRUB-5-CONFIG_WRITTEN: GRUB configuration was written to disk successfully.
SW1_Core-F0#
*Sep  5 02:28:49.707: %LINK-3-UPDOWN: Interface Port-channel10, changed state to up
*Sep  5 02:28:50.707: %LINEPROTO-5-UPDOWN: Line protocol on Interface Port-channel10, changed state to up
SW1_Core-F0#
*Sep  5 02:28:55.439: %EC-5-L3DONTBNDL2: Gi3/3 suspended: LACP currently not enabled on the remote port.
*Sep  5 02:28:55.542: %EC-5-L3DONTBNDL2: Gi3/2 suspended: LACP currently not enabled on the remote port.
*Sep  5 02:28:56.439: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet3/3, changed state to down
*Sep  5 02:28:56.542: %LINEPROTO-5-UPDOWN: Line protocol on Interface GigabitEthernet3/2, changed state to down
SW1_Core-F0#
*Sep  5 02:29:16.573: %LINK-3-UPDOWN: Interface Vlan88, changed state to up
*Sep  5 02:29:17.573: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan88, changed state to up
*Sep  5 02:29:19.394: %LINK-3-UPDOWN: Interface Vlan10, changed state to up
*Sep  5 02:29:19.395: %LINK-3-UPDOWN: Interface Vlan20, changed state to up
*Sep  5 02:29:20.394: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to up
*Sep  5 02:29:20.395: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to up

*Sep  5 02:29:18.676: %CDP-4-NATIVE_VLAN_MISMATCH: Native VLAN mismatch discovered on GigabitEthernet0/0 (99), with Switch GigabitEthernet3/3 (1).

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

<< NOTA: EL MISSMATCH QUE MARCA ES ENTRE SWITCHES Y ES NORMAL YA QUE NO HE CONFIGURADO EL OTRO, NO MALVIAJARSE!!!! >>

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

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
interface vlan 88
ip address 192.168.88.2 255.255.255.0
no shutdown
exit
interface vlan 99
ip address 192.168.99.2 255.255.255.0
no shutdown
exit
!
interface range Gi 0/0 - 1
description VLAN_10_Gi_SW
switchport mode access
switchport access vlan 10
no shutdown
exit
interface range Gi 0/2 - 3
description VLAN_20_Gi_SW
switchport mode access
switchport access vlan 20
no shutdown
exit
interface Gi 1/0
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

- CLI

```
Switch>
Switch>!
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
SW2_Distr-F0(config)#interface vlan 88
SW2_Distr-F0(config-if)#ip address 192.168.88.2 255.255.255.0
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#interface vlan 99
SW2_Distr-F0(config-if)#ip address 192.168.99.2 255.255.255.0
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#!
SW2_Distr-F0(config)#interface range Gi 0/0 - 1
SW2_Distr-F0(config-if-range)#description VLAN_10_Gi_SW
SW2_Distr-F0(config-if-range)#switchport mode access
SW2_Distr-F0(config-if-range)#switchport access vlan 10
SW2_Distr-F0(config-if-range)#no shutdown
SW2_Distr-F0(config-if-range)#exit
SW2_Distr-F0(config)#interface range Gi 0/2 - 3
SW2_Distr-F0(config-if-range)#description VLAN_20_Gi_SW
SW2_Distr-F0(config-if-range)#switchport mode access
SW2_Distr-F0(config-if-range)#switchport access vlan 20
SW2_Distr-F0(config-if-range)#no shutdown
SW2_Distr-F0(config-if-range)#exit
SW2_Distr-F0(config)#interface Gi 1/0
SW2_Distr-F0(config-if)#description VLAN_88_Gi_SW
SW2_Distr-F0(config-if)#switchport mode access
SW2_Distr-F0(config-if)#switchport access vlan 88
SW2_Distr-F0(config-if)#no shutdown
SW2_Distr-F0(config-if)#exit
SW2_Distr-F0(config)#!
SW2_Distr-F0(config)#interface 
*Sep  5 03:24:22.144: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan10, changed state to up
*Sep  5 03:24:22.494: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan20, changed state to up
*Sep  5 03:24:22.573: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan88, changed state to up
*Sep  5 03:24:22.657: %LINEPROTO-5-UPDOWN: Line protocol on Interface Vlan99, changed state to up
*Sep  5 03:24:23.460: %LINK-3-UPDOWN: Interface Vlan10, changed state to up
*Sep  5 03:24:23.552: %LINK-3-UPDOWN: Interface Vlan20, changed state to up
*Sep  5 03:24:23.637: %LINK-3-UPDOWN: Interface Vlan88, changed state to up
*Sep  5 03:24:23.714: %LINK-3-UPDOWN: Interface Vlan99, changed state to upgi 3/3
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

*Sep  5 03:24:26.022: %SYS-5-CONFIG_I: Configured from console by consoleCompressed configuration from 5041 bytes to 2212 bytes[OK]
SW2_Distr-F0#!
SW2_Distr-F0#!
SW2_Distr-F0#!
SW2_Distr-F0#
*Sep  5 03:24:28.134: %GRUB-5-CONFIG_WRITING: GRUB configuration is being updated on disk. Please wait...
*Sep  5 03:24:28.785: %GRUB-5-CONFIG_WRITTEN: GRUB configuration was written to disk successfully.
SW2_Distr-F0#
SW2_Distr-F0#
```

## LAG >>> LAN FortiGate-1

- **NOTA: El Forgtigate-2 solo tiene configurada la interfaz de Management (Port1) con DHCP para entrar a UI**
    - No es necesario configurar nadamás, ya que al activar el **HA** llevará la configuración de **MASTER**

- Debido a la nota, solo se configurará el Fortigate-1    

- Procedimiento:

### Interfaces 

- Objetivo:

![image](https://user-images.githubusercontent.com/94720207/188370090-3748a854-e836-44b4-ac39-f50ec81a534d.png)

- WAN (Internet) Port1

    - NOTA: En mi caso está por DHCP para facilidad que sea portable, pero se puede cambiar a estático. 
   
![image](https://user-images.githubusercontent.com/94720207/188370675-881702c6-a7b3-4ddb-a20e-216c3428e0c1.png)

- LAG | 802.3ad

![image](https://user-images.githubusercontent.com/94720207/188370237-521c6248-3aec-4fb9-b8ad-aa5627e9dc32.png)

- VLANs

    - NOTA: En el ejemplo solo se ve la VLAN-10, lo mismo se hace para las demás solo cambiando su subnet apropiada. 
    - OJO!!! No olvidar el DHCP Server y la Pool ;) 

![image](https://user-images.githubusercontent.com/94720207/188377624-2e570148-78b7-4d09-aaab-56d61ffc9ab9.png)

### DNS

![image](https://user-images.githubusercontent.com/94720207/188371129-181f10f1-ac62-4eb4-9978-2eccaa40454d.png)

### Static Routes

![image](https://user-images.githubusercontent.com/94720207/188371205-157ac282-9439-4e8f-87d3-9c80b13f17de.png)

![image](https://user-images.githubusercontent.com/94720207/188371295-278b54eb-1da1-47ce-8f0e-c3f82a9316af.png)

### IPv4 Policy (Salida a Internet)

- NOTA: En el ejemplo solo se ve la VLAN-10, lo mismo se hace para las demás solo cambiando la VLAN/Interface. 

![image](https://user-images.githubusercontent.com/94720207/188371420-756c2e2b-2c8a-4e6d-884c-41629085eae4.png)

![image](https://user-images.githubusercontent.com/94720207/188371575-54ce71e3-9d02-4110-93c5-3bab6776c1fc.png)


## HA + LAG FortiGate-2

1. El modo será `Active-Passive`
2. El **MASTER** (Role) tendrá priority `128` y el Secundario `127`
3. Por buena práctica se utilizan 2 cables para el `Heartbeat` del HA

- **IMPORTANTE: EN EL MOMENTO QUE AL SEGUNDO FORTI SE LE PONGA EL HA (ACTIVE-PASSIVE + CREDENCIALES DE HA) EL SLAVE (CON PRIORITY MENOR) TOMARÁ TODA LA CONFIGURACIÓN DEL MASTER, MUCHO OJO!!! NO PONER PRORITY MAYOR AL QUE NO TIENE CONFIG!!! NO MAMES!!!**

- Objetivo:

![image](https://user-images.githubusercontent.com/94720207/188372281-d94a25e3-0b7e-4eca-b51f-d1872b9247f2.png)

- Procedimiento:

    - **MASTER** (FortiGate-1)

![image](https://user-images.githubusercontent.com/94720207/188372830-0302cb5e-5376-46e6-a472-fcc71c5daf9c.png)

- Ahora, en el **SLAVE** simplemente activar el HA > Active-Passive > MENOR PRIORITY!!! > listo!!! :D 

![image](https://user-images.githubusercontent.com/94720207/188373454-c0a05d52-d415-44a7-8e85-bec29aac1074.png)

- **NOTA: En este punto reinicié tanto MASTER como SLAVE para probar el HA





### Prueba de HA

- Así se ve el MASTER al seleccionar el Cluster SLAVE, cuando está formado el HA y el SLAVE en espera:

![image](https://user-images.githubusercontent.com/94720207/188373040-e0534936-cb81-4bb8-8b72-26d1f46ee1ae.png)

- Así se ve cuando entra el SLAVE al apagar el MASTER:

![image](https://user-images.githubusercontent.com/94720207/188373260-76eede8c-f051-4f3f-a3e1-341ff9cedfd5.png)

###

### Dudas

- ¿Al final el HA toma una sola IP y no puedo entrar al UI del SLAVE a menos que apague forzosamente el MASTER?


