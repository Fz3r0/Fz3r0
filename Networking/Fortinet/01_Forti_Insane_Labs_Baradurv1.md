


## IPv4 Addressing Table

| **Device**            | **Interface** | **IP Address**  | **Subnet Mask** | **CIDR** | **Gateway**     | **VLAN**    | **Notes**                                   |
|-----------------------|---------------|-----------------|-----------------|----------|-----------------|-------------|---------------------------------------------|
| **WAN1 (Cloud)**      | eth1          | 000.000.000.000 | 255.255.255.255 | 16       | 255.255.255.255 | N/A         | Internet Telmex (Cloud GNS3) this is a note |
| **WAN2 (NAT)**        | eth0          | 000.000.000.000 | 255.255.255.255 | 16       | 255.255.255.255 | N/A         |                                             |
| **FortiGate1**        | Port1         | 000.000.000.000 | 255.255.255.255 | 16       | 255.255.255.255 | 1           |                                             |
| **FortiGate2**        | Port1         | 000.000.000.000 | 255.255.255.255 | 16       | 255.255.255.255 | 1           |                                             |
| **MikroTik - DHCP**   | Port1         | 000.000.000.000 | 255.255.255.255 | 16       | 255.255.255.255 | 99 (Native) |                                             |
| **WLC Zone Director** | Port1         |                 |                 |          |                 |             |                                             |
| **SW0**               | Gi 3/3        |                 |                 |          |                 |             |                                             |
| **SW1**               |               |                 |                 |          |                 |             |                                             |
| **SW2**               |               |                 |                 |          |                 |             |                                             |
| **SW3**               |               |                 |                 |          |                 |             |                                             |
| **SW4**               |               |                 |                 |          |                 |             |                                             |
| **SW5**               |               |                 |                 |          |                 |             |                                             |
| **SW6**               |               |                 |                 |          |                 |             |                                             |
| **null**              |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |



## Switches Configurations

### SW1-Cisco-CORE - Switch Core

```
!
!
enable
configure terminal
!
hostname SW1_Core-F0
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"  Rising black, blacker and darker than the vast shades  "
"  amid which it stood, immeasurably strong, mountain of  "
"  iron, gate of steel, tower of adamant...               "
"                                                         "
"  ...The cruel pinnacles and iron crown of the topmost   "
"  tower of Barad-dûr. Fortress of Sauron.                "
"                                                         "
"                  -- HECHO EN MEXICO --                  "
"                                                         "
"                   Twitter:  @Fz3r0_OPs                  "
"                   GitHub :  Fz3r0                       "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"           <<<  Barad-dûr "The Dark Tower"  >>>          "
"                                                         "
"                 <<<  SW1-CISCO-CORE  >>>                "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
$
!
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 88
name VLAN_88_MAMAGEMENT
vlan 99
name VLAN_99_TrunkNative
!
interface vlan 10
description <<_VLAN_10_RED>>
ip address 172.10.0.11 255.255.0.0
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE>>
ip address 172.20.0.11 255.255.0.0
no shutdown
exit
interface vlan 88
description <<_MANAGEMENT_VLAN_88_>>
ip address 172.88.0.11 255.255.0.0
no shutdown
exit
!
ip default-gateway 172.88.0.254 
ip http server
!
!
interface range gi 3/0 - 1
description <<CHANNEL_L_fg_MASTER_PORTS_0-1>>
channel-group 10 mode active
no shutdown 
exit
!
interface port-channel 10
description <<LAG1_LAN_L_MASTER_FORTI<>SWITCH>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
no shutdown 
exit
!
!
interface range gi 3/2 - 3
description CHANNEL_R_fg_SLAVE_PORTS_2-3
channel-group 20 mode active
no shutdown 
exit
!
interface port-channel 20
description LAG2_LAN_R_SLAVE_FORTI<>SWITCH
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
no shutdown 
exit
!
!
interface gi 0/0
description TRUNK--->>>SWITCH_DISTRIBUTION_GI3/3
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
no shutdown 
exit
!
!
!
interface gi 1/0
description <<<-MikroTik-RouterBoard-DHCP-Server->>>
switchport mode access
switchport access vlan 88
no shutdown 
exit
!
end
!
interface gi 1/1
description <<<-WLC-Ruckus-ZoneDirector->>>
switchport mode access
switchport access vlan 88
no shutdown 
exit
!
end
!
interface gi 1/2
description <<<---TEST_CORE_PC--->>>
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

### SW2-Cisco-DISTRIBUTION - Switch Distribution

```
!
!
enable
configure terminal
!
hostname SW2_Distribution-F0
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"  Rising black, blacker and darker than the vast shades  "
"  amid which it stood, immeasurably strong, mountain of  "
"  iron, gate of steel, tower of adamant...               "
"                                                         "
"  ...The cruel pinnacles and iron crown of the topmost   "
"  tower of Barad-dûr. Fortress of Sauron.                "
"                                                         "
"                  -- HECHO EN MEXICO --                  "
"                                                         "
"                   Twitter:  @Fz3r0_OPs                  "
"                   GitHub :  Fz3r0                       "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"           <<<  Barad-dûr "The Dark Tower"  >>>          "
"                                                         "
"             <<<  SW2-CISCO-DISTRIBUTION  >>>            "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
$
!
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 88
name VLAN_88_MAMAGEMENT
vlan 99
name VLAN_99_TrunkNative
!
interface vlan 10
description <<_VLAN_10_RED>>
ip address 172.10.0.11 255.255.0.0
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE>>
ip address 172.20.0.11 255.255.0.0
no shutdown
exit
interface vlan 88
description <<_MANAGEMENT_VLAN_88_>>
ip address 172.88.0.12 255.255.0.0
no shutdown
exit
!
ip default-gateway 172.88.0.254
ip http server
!
!
interface range gi 0/0 - 3, gi 1/0
description <<Trunk--->>ACCESS_SWITCHES>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
no shutdown 
exit
!
!
interface gi 3/3
description <<Trunk--->>CORE>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
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

### SW3 TO SW 10-Cisco-ACCESS - Switch Access

- NOTA: Para lograr la estandarización de configuración en todos los switches:

    - Los puertos 3/0 - 3 (los últimos 4) siempre serán configurados como Trunks para hacer trunks, haya o no cascadeo. 
    - Los puertos del 0/0 - 3, 1/0 - 3, 2/0 - 3 siempre serán access para esperar algún host.

        - 0/0 - 3 y  1/0 - 3 (8 puertos) = Para VLAN 10 Blue
        - 2/0 - 3 (4 puertos) = Para VLAN 20 Red
        - 3/0 - 3 (4 puertos) = Para Trunks, Native 99 (standard de troncal en sitio)

- **IMPORTANTE!!!** En cada uno de los Access Switches hay que modificar lo siguiente para que el script funcione bien:

1. La IP Address de cada una de las VLANs con la secuencia correspondiente al switch para el host (por ejemplo su IP de `VLAN 88 Management`, donde de ejemplo está la `0.20`, pero cada switch cambia: `0.21`, `0.22`, `0.23`, etc.)

2. El HostName con el nombre que haga referencia al switch. (Ahora viene con `xxx`)

3. La descripción de la troncal en caso de ser un cascade con puerto diferente (por ejemplo el SW-ACCESS7)        

```
!
!
enable
configure terminal
!
hostname SWxxx_Distribution-F0
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"  Rising black, blacker and darker than the vast shades  "
"  amid which it stood, immeasurably strong, mountain of  "
"  iron, gate of steel, tower of adamant...               "
"                                                         "
"  ...The cruel pinnacles and iron crown of the topmost   "
"  tower of Barad-dûr. Fortress of Sauron.                "
"                                                         "
"                  -- HECHO EN MEXICO --                  "
"                                                         "
"                   Twitter:  @Fz3r0_OPs                  "
"                   GitHub :  Fz3r0                       "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"           <<<  Barad-dûr "The Dark Tower"  >>>          "
"                                                         "
"               <<<  SWxx-CISCO-ACCESS  >>>               "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
$
!
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 88
name VLAN_88_MAMAGEMENT
vlan 99
name VLAN_99_TrunkNative
!
interface vlan 10
description <<_VLAN_10_RED>>
ip address 172.10.0.11 255.255.0.0
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE>>
ip address 172.20.0.11 255.255.0.0
no shutdown
exit
interface vlan 88
description <<_MANAGEMENT_VLAN_88_>>
ip address 172.88.0.20 255.255.0.0
no shutdown
exit
!
ip default-gateway 172.88.0.254
ip http server
!
!
interface range gi 0/0 - 3, gi 1/0
description <<Trunk--->>ACCESS_SWITCHES>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
no shutdown 
exit
!
!
interface gi 3/3
description <<Trunk--->>CORE>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
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

## FortiGates (Edge Firewalls/Router/Gateways) Configurations

### FortiGate1-MASTER

#### FortIOS CLI:

- **Opción A** `Static`

    - **Console CLI:**

```
config system interface
edit port1
set mode static
set ip 192.168.143.100 255.255.255.0
select allowaccess ping http https ssh
end

config system global
set hostname Fz3r0_FortiGate1_MASTER
set pre-login-banner enable
set post-login-banner enable
set admintimeout 60
end


```

- **Opción B** `DHCP`

    - **Console CLI:**

```
config system interface
edit port1
set mode dhcp
select allowaccess ping https http ssh
end

config system global
set hostname Fz3r0_FortiGate1_MASTER
set pre-login-banner enable
set post-login-banner enable
set admintimeout 60
end


```

- Ahora entrar por UI a `192.168.143.100`

#### FortiGate v7 UI & Dashboard

- **NOTA:** Tomar en cuenta que solo será necesario configurar este FortiGate-1, el FortiGate-2 solo se tendrá que configurar la interfaz para entrar por UI, ya que solo se tendrá que acitvar el HA. 

- **NOTA2:** Hacer cuanto antes el SD-WAN, ya que al crear politicas u otras configuraciones ya sea con la interface de WAN1 o WAN2 ya no permitirá crear el SD-WAN member y habrá que borrar las políticas creadas. 

- **NOTA3:** En caso de configurar el FortiGate antes que los switches, varias interfaces (como la LAG de la LAN) se verán en rojo (apagadas), esto es porque del lado del Switch aún no existirá ningún Port-Channel/LAG/LACP. Se pondrán en verde automáticamente al configurar el switch 

    - Esto pasaría por ejemplo en casos donde haya que configurar un Firewall antes de instalarlo en sitio.

- **TIP:** Crear primero las WANs e inmediatamente después hacer el SD-WAN. (Esto para no tener que estar borrando políticas más adelante por olvidar crear la SD-WAN)

#### Interfaces

#### SD-WAN

- [Ejemplo (Video)](https://www.youtube.com/watch?v=s-Gn_1HxhrU)    


#### SSL VPN

- [Ejemplo (Video)](https://youtu.be/kRbSq3TMxxw)

#### System > Replacement Messages

- Post-Login Disclaimer Message

```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"  Rising black, blacker and darker than the vast shades  "
"  amid which it stood, immeasurably strong, mountain of  "
"  iron, gate of steel, tower of adamant...               "
"                                                         "
"  ...The cruel pinnacles and iron crown of the topmost   "
"  tower of Barad-dûr. Fortress of Sauron.                "
"                                                         "
"                  -- HECHO EN MEXICO --                  "
"                                                         "
"                   Twitter:  @Fz3r0_OPs                  "
"                   GitHub :  Fz3r0                       "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"           <<<  Barad-dûr "The Dark Tower"  >>>          "
"                                                         "
"                 <<<  FortiGate v7 UI  >>>               "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```




<! --  


 =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
 "                                                               "
 "                                                               "
 "      /$$$$$$$$               /$$$$$$             /$$$$$$      "
 "     | $$_____/              /$$__  $$           /$$$_  $$     "
 "     | $$          /$$$$$$$$|__/  \ $$  /$$$$$$ | $$$$\ $$     "
 "     | $$$$$ /$$$$|____ /$$/   /$$$$$/ /$$__  $$| $$ $$ $$     "
 "     | $$__/|____/   /$$$$/   |___  $$| $$  \__/| $$\ $$$$     "
 "     | $$           /$$__/   /$$  \ $$| $$      | $$ \ $$$     "
 "     | $$          /$$$$$$$$|  $$$$$$/| $$      |  $$$$$$/     "
 "     |__/         |________/ \______/ |__/       \______/      "
 "                                                               "
 "                                                               "
 "                    -- HECHO EN MEXICO --                      "
 "                                                               "
 "                     Twitter:  @fz3r0_OPs                      "
 "                     GitHub :  Fz3r0                           "
 ""
 "      Proyect     : Barad-dûr "The Dark Tower" v1.0 (2022)
 "
 "      Author      : Fz3r0
 "
 "      Description : 
 "
 "           - 3 Tier Topology
 "           - Firewall High Availability (HA)
 "           - ISP redundancy @ SD-WAN
 "           - Subneting & VLAN Routing & Switching
 "           - DHCP (MikroTik Appliance) & Static Addressing
 "           - LAG/LACP between FortiGate & Cisco Switch
            - Management LAN Remote Access

    "...rising black, blacker and darker than the vast shades 
     amid which it stood, immeasurably strong, mountain of iron, 
     gate of steel, tower of adamant... 
     
     The cruel pinnacles and iron crown of the topmost tower 
     of Barad-dûr...Fortress of Sauron." 





===

Duda:

- Cómo alcanzar el SW0 por la WAN int? se crea tmb la VLAN ahi?

-->
