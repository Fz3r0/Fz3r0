

## Introducción

### Notas Generales

- FortiGate V7
- 

- Siempre verificar las `release notes` del dispositivo y versión a utilizar y ajustar cualquier detalle adicional que mencione el fabricante. 



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
| **SW6**              |               |                 |                 |          |                 |             |                                             |
| **SW6**                 |               |                 |                 |          |                 |             |                                             |
| **SW6**                  |               |                 |                 |          |                 |             |                                             |
| **SW6**                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |



## Switches Configurations

- **Layer 2 Fz3r0 Top Security Configuration:** 

    - [> Para más detalles acerca del `Fz3r0: Layer2 Security Pro-Config!` Click aquí <](https://github.com/Fz3r0/Fz3r0/blob/main/Networking/Labs/Security_&_Best-Practices_VS_Layer2_Attack_FULL_PRO_CONFIG.md)

    - [> Para más detalles acerca del `Fz3r0: SSH Pro-Config for Cisco Devices!` Click aquí <](https://github.com/Fz3r0/Fz3r0/blob/main/Networking/Labs/SSH-Minimum-Requeriments-for-Cisco.md)

    - **Nota Security 1:** Todas las interfaces utilizadas en `SW1-Core` van a transmitir y recibir LLDP y CDP, esto debido a que se encuentra en el MDF y todas las interfaces de acceso son de administrador, servidores o equipo confiable y resguardado solo para acceso autorizado, el bloqueo de paquetes de anuncios paquetes serán únicamente en los switches de acceso e interfaces de acceso _(o HoneyPots/Down)_.  

    - **Nota Security 2:** Ojo a la interfaz del MikroTik DHCP server, esta es la única que debe ser configurada como un `Trusted DHCP server` en Layer 2. 

    - **Nota Security 3:** "_The recommended rate limit for each untrusted port is 15 packets per second_" Las recomendaciones de Cisco marcan 15 paquetes por segundo para el Rate Limit de DHCP snooping, será lo que se usará en el laboratorio. 

        - **IMPORTANTE!!!** Al crear el Channel-Group del LAG en el switch, he tenido que agregar los comandos de DHCP y ARP trust **ANTES** y **DESPUÉS** de crear el port-channel, es decir, tanto las interfaces por separado como ya el port-channel creado se agregan los comandos para confiar en el DHCP, de lo contrario se bloquearán los paquetes DHCP. 

    - **Nota Security 4:**: En la VLAN e interfaces `HoneyPots` no modifico nada de DHCP Snooping ni ARP inspection, esto porque ya los active en global config, y al ser una interfaz totalmente bloqueada no creo ninguna regla. Así no permito pasar ni un solo paquete DHCP o ARP.         

### SW1-Cisco-CORE - Switch Core

- En este modelo no se puede LLDP ni CDP en port-channel LAG, pero aquí hay un turoial para modelos Cisco que lo soportan: https://www.cisco.com/c/en/us/td/docs/switches/datacenter/nexus9000/sw/7-x/system_management/configuration/guide/b_Cisco_Nexus_9000_Series_NX-OS_System_Management_Configuration_Guide_7x/b_Cisco_Nexus_9000_Series_NX-OS_System_Management_Configuration_Guide_7x_chapter_010010.pdf

- **El truco de maquinita!!!** _Ojo cuando se configura el port security en interfaces `access` (por ejemplo PC Core Test), en las ultimas lineas de err-disable te regresará automáticamente a `global-config`, es por ello de debe volver a entrar a la interface para seguir configurando el port security y ya tampoco existe el `exit` ;)_  

- `security passwords min-length 10` no está soportado en este switch como parte de security, pero se podría agregar en el nombre de usuario/admin local en algún switch soportado. 

- En todas las interfaces `access` (como en default trunk) se pondra `ip ARP INSPECTION TRUST` para confiar en todos los paquetes arp de quien sea (sin necesidad de configurar), pero verificar al final los comandos:

```
arp access-list H2
S1(config-arp-nacl)# permit ip host 1.1.1.1 mac host 1.1.1
S1(config-arp-nacl)# end
S1# show arp access-list
```

```
!
!
enable
configure terminal
!
hostname SW1-CORE_Fz3r0
no ip domain-lookup
ip domain-name <<_Fz3r0.Barad-dur_>>
!
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"  Rising black, blacker and darker than the vast shades  "
"  amid which it stood, immeasurably strong, mountain of  "
"  iron, gate of steel, tower of adamant...               "
"                                                         "
"  ...The cruel pinnacles and iron crown of the topmost   "
"  tower of Barad-dur. Fortress of Sauron.                "
"                                                         "
"                  -- HECHO EN MEXICO --                  "
"                                                         "
"                   Twitter:  @Fz3r0_OPs                  "
"                   GitHub :  Fz3r0                       "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"           <<<  Barad-dur "The Dark Tower"  >>>          "
"                                                         "
"                 <<<  SW1-CISCO-CORE  >>>                "
"                                                         "
"           User:  Fz3r0     Pass:   Fz3r0.12345          "
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
vlan 666
name VLAN_666-DownPorts
!
interface vlan 10
description <<_VLAN_10_RED>>
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE>>
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
lldp run
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,88,99,666
ip arp inspection vlan 1,10,20,88,99,666
!
!
!
interface range gi 3/0 - 1
shutdown
description >>>_-_CHANNEL_L_LAG1_FG-MASTER_PORTS_0-1_-_<<<
ip DHCP SNOOPING TRUST
ip ARP INSPECTION TRUST
switchport nonegotiate
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
lldp TRANSMIT
lldp RECEIVE
CDP ENABLE
channel-group 10 mode active
no shutdown 
exit
!
interface port-channel 10
shutdown
description <<_LAG1_LAN_L_MASTER_FORTI<>SWITCH_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
switchport nonegotiate
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
ip DHCP SNOOPING TRUST
ip ARP INSPECTION TRUST
shutdown
no shutdown 
exit
!
!
interface range gi 3/2 - 3
shutdown
description >>>_-_CHANNEL_R_LAG2_FG-SLAVE_PORTS_2-3_-_<<<
ip DHCP SNOOPING TRUST
ip ARP INSPECTION TRUST
switchport nonegotiate
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
lldp TRANSMIT
lldp RECEIVE
CDP ENABLE
channel-group 20 mode active
no shutdown 
exit
!
interface port-channel 20
shutdown
description <<_LAG2_LAN_R_SLAVE_FORTI<>SWITCH_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
switchport nonegotiate
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
ip DHCP SNOOPING TRUST
ip ARP INSPECTION TRUST
shutdown
no shutdown 
exit
!
!
interface gi 0/0
description <<_TRUNK--->>>SWITCH_DISTRIBUTION_GI3/3_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
switchport nonegotiate
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
ip DHCP SNOOPING TRUST
ip ARP INSPECTION TRUST
lldp TRANSMIT
lldp RECEIVE
CDP ENABLE
shutdown
no shutdown 
exit
!
!
!
interface gi 1/0
description <<<-MikroTik-RouterBoard-DHCP-Server-->Ether1->>>
switchport mode access
switchport access vlan 10
ip DHCP SNOOPING TRUST
ip ARP INSPECTION TRUST
spanning-tree portfast
spanning-tree bpduguard enable
lldp transmit
lldp receive
CDP enable
shutdown
no shutdown 
exit
!
!
interface gi 1/1
description <<<-WLC-Ruckus-ZoneDirector->>>
switchport mode access
switchport access vlan 20
no shutdown 
exit
!
!
interface gi 1/2
description <<<---TEST_CORE_PC_-_Fz3r0-Adm1n--->>>
switchport mode access
switchport access vlan 88
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address FF:FF:FF:00:00:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 15
ip ARP INSPECTION TRUST
spanning-tree portfast
spanning-tree bpduguard enable
lldp transmit
lldp receive
CDP enable
no shutdown 
errdisable recovery interval 60
interface gi 1/2
errdisable recovery cause psecure-violation
!
!
!
enable secret Fz3r0.12345
service password-encryption
login block-for 120 attempts 3 within 60
username root privilege 15 secret Fz3r0.12345
username Fz3r0 privilege 15 secret Fz3r0.12345
username user privilege 1 secret Fz3r0.12345
!
line console 0
password Fz3r0.12345
login local
logging synchronous
exec-timeout 5 30
exit
!
line aux 0
privilege level 1
transport input none
transport output none
login local
no exec
exit
!
line vty 0 8
access-class 8 in
transport input ssh
login local
logging synchronous
exec-timeout 5 30
exit
!
crypto key generate rsa
2048
ip ssh version 2
!
!
!
end
!
wr
!
reload
!
exit
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
hostname SW2-DIST_Fz3r0
no ip domain-lookup
ip domain-name <<_Fz3r0.Barad-dur_>>
!
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"  Rising black, blacker and darker than the vast shades  "
"  amid which it stood, immeasurably strong, mountain of  "
"  iron, gate of steel, tower of adamant...               "
"                                                         "
"  ...The cruel pinnacles and iron crown of the topmost   "
"  tower of Barad-dur. Fortress of Sauron.                "
"                                                         "
"                  -- HECHO EN MEXICO --                  "
"                                                         "
"                   Twitter:  @Fz3r0_OPs                  "
"                   GitHub :  Fz3r0                       "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"           <<<  Barad-dur "The Dark Tower"  >>>          "
"                                                         "
"             <<<  SW2-CISCO-DISTRIBUTION >>>             "
"                                                         "
"           User:  Fz3r0     Pass:   Fz3r0.12345          "
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
vlan 666
name VLAN_666-DownPorts
!
interface vlan 10
description <<_VLAN_10_RED>>
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE>>
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
lldp run
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,88,99,666
ip arp inspection vlan 1,10,20,88,99,666
!
!
!
interface range gi 0/0 - 3, gi 1/0
description <<_Trunk_to-->>ALL_ACCESS_SWITCHES_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
switchport nonegotiate
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
ip dhcp snooping TRUST
ip arp inspection TRUST
lldp TRANSMIT
lldp RECEIVE
CDP ENABLE
shutdown
no shutdown 
exit
!
interface gi 3/3
description <<_Trunk--->>CORE_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
switchport nonegotiate
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
ip dhcp snooping TRUST
ip arp inspection TRUST
lldp TRANSMIT
lldp RECEIVE
CDP ENABLE
shutdown
no shutdown 
exit
!
!
interface range gi 1/1 - 3, gi 3/1 - 2 
description <<_VLAN666-HoneyPot_DownPorts-HOLE-TO-HELL_>>
shutdown
switchport mode access
switchport access vlan 666
switchport port-security
switchport port-security maximum 1
switchport port-security mac-address FF:FF:FF:00:00:00
switchport port-security aging time 5
switchport port-security violation shutdown
switchport port-security aging type inactivity
switchport nonegotiate
spanning-tree portfast
spanning-tree bpduguard enable
no lldp transmit
no lldp receive
no CDP enable
shutdown
errdisable recovery interval 60
interface range gi 1/1 - 3, gi 3/1 - 2 
errdisable recovery cause psecure-violation
!
!
!
enable secret Fz3r0.12345
service password-encryption
login block-for 120 attempts 3 within 60
username root privilege 15 secret Fz3r0.12345
username Fz3r0 privilege 15 secret Fz3r0.12345
username user privilege 1 secret Fz3r0.12345
!
line console 0
password Fz3r0.12345
login local
logging synchronous
exec-timeout 5 30
exit
!
line aux 0
privilege level 1
transport input none
transport output none
login local
no exec
exit
!
line vty 0 8
access-class 8 in
transport input ssh
login local
logging synchronous
exec-timeout 5 30
exit
!
crypto key generate rsa
2048
ip ssh version 2
!
!
!
end
!
wr
!
reload
!
exit
!
!
!

```

### SW3 TO SW 10-Cisco-ACCESS - Switch Access

- **NOTA1:** El IP DHCP snooping esta´ra en modo Trust en las interfaces como vlan88 (a pesar de ser access) esto debido a que son APs que además de ser confiables, es posible necesiten un rate limit mayor de dhcp, es por eso que mejor se decide no limitar la cantidad de paquetes DHCP por segundo.

- **NOTA2:** El LLDP y CDP será apagado en VLAN 10 RED y VLAN 20 BLUE por estándares de seguridad al ser Host Access Untrust, sin embargo si recibirán LLDP para leer información de los neighbors. 

    - En el caso de la `VLAN 88 MGMT + APs` si se mantendrá de ambos sintidos `LLDP` aunque se apagará el `CDP` al no ser necesario y así limpiar lo más posible la red. _(En el caso de switch a switch se mantiene CDP ya que ambos vendors sin cisco, en management va a otros dispositivos como PCs o APs que no necesitan CDP realmente)_

- **NOTA3:** Este Switch tiene todos los puertos utilizados, por eso **no será necesario apagar puertos y configurarlos con VLAN de `HoneyPot`.**

- **NOTA4:** En las interfaces `Access` que usan la `VLAN 88 Management` (Utilizadas para los Access Points)

    - **IMPORTANTE!!!** **Los `Access Points Ruckus` utilizan `Access VLAN` y pueden transportar `varias VLANs` sin necesidad de una `Trunk` debido a que se reporta a la `Controladora WLC Zone Director` por medio de `SSH Tunnel`.** 

- **NOTA5:** Para lograr la estandarización de configuración en todos los switches:

    - Los puertos 3/0 - 3 (los últimos 4) siempre serán configurados como Trunks para hacer trunks, haya o no cascadeo. 
    - Los puertos del 0/0 - 3, 1/0 - 3, 2/0 - 3 siempre serán access para esperar algún host.

        - **0/0 - 3 (4 puertos)** = Para **VLAN 10 Red** `Access`
        - **1/0 - 3 (4 puertos)** = Para **VLAN 20 Blue** `Access`
        - **2/0 - 3 (4 puertos)** = Para **VLAN 88 Management** `Access`
        - **3/0 - 3 (4 puertos)** = Para **Trunks, Native 99** `standard de Native VLAN[Trunk] en sitio`

- **IMPORTANTE!!!** En cada uno de los Access Switches hay que modificar lo siguiente para que el script funcione bien:

1. La IP Address de cada una de las VLANs con la secuencia correspondiente al switch para el host (por ejemplo su IP de `VLAN 88 Management`, donde de ejemplo está la `0.20`, pero cada switch cambia: `0.21`, `0.22`, `0.23`, etc.)

2. El HostName con el nombre que haga referencia al switch. (Ahora viene con `xxx`)

3. La descripción de la troncal en caso de ser un cascade con puerto diferente (por ejemplo el SW-ACCESS7)

- **TIP:** Copiar y pegar el script en un editor de texto primero, hacer las modificaciones necesarias y después pegarlo uno por uno en cada switch _(o automatizar :O)_.   

- Cosas a cambiar:

1. El Hostname

```
hostname SWxxx_Access_Fz3r0     <<<--- CAMBIAR
no ip domain-lookup
ip domain-name <<_Fz3r0.Barad-dur_>>
```

2. La IPv4 de la VLAN de Management (21, 22, 23, 24, etc...)   

```
interface vlan 88
description <<_MANAGEMENT_VLAN_88_>>
ip address 172.88.0.21 255.255.0.0    <<<--- CAMBIAR
no shutdown
exit
```  

3. (opcional) Descripción/nombre de la troncal exacta

```
interface range gi 3/0 - 3
description <<_Trunk--->>DISTRIBUTION_or_CASCADE_>>    <<<--- CAMBIAR
```

- Ejemplo con Switch 3 - 172.0.88.20.

```
!
!
enable
configure terminal
!
hostname SW3_ACCESS_Fz3r0
no ip domain-lookup
ip domain-name <<_Fz3r0.Barad-dur_>>
!
banner motd $

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"  Rising black, blacker and darker than the vast shades  "
"  amid which it stood, immeasurably strong, mountain of  "
"  iron, gate of steel, tower of adamant...               "
"                                                         "
"  ...The cruel pinnacles and iron crown of the topmost   "
"  tower of Barad-dur. Fortress of Sauron.                "
"                                                         "
"                  -- HECHO EN MEXICO --                  "
"                                                         "
"                   Twitter:  @Fz3r0_OPs                  "
"                   GitHub :  Fz3r0                       "
"                                                         "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                         "
"           <<<  Barad-dur "The Dark Tower"  >>>          "
"                                                         "
"                <<<  SW3-CISCO-ACCESS >>>                "
"                                                         "
"           User:  Fz3r0     Pass:   Fz3r0.12345          "
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
vlan 666
name VLAN_666-DownPorts
!
interface vlan 10
description <<_VLAN_10_RED>>
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE>>
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
lldp run
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,88,99,666
ip arp inspection vlan 1,10,20,88,99,666
!
!
!
interface range gi 0/0 - 3
description <<_ACCESS_VLAN_10_RED_-_HOST_INTERFACES_>>
switchport mode access
switchport access vlan 10
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address FF:FF:FF:00:00:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 15
ip ARP INSPECTION TRUST
spanning-tree portfast
spanning-tree bpduguard enable
lldp transmit
lldp receive
CDP enable
no shutdown 
errdisable recovery interval 60
interface gi 1/2
errdisable recovery cause psecure-violation
!
!
interface range gi 1/0 - 3
description <<_ACCESS_VLAN_20_BLUE_-_HOST_INTERFACES_>>
switchport mode access
switchport access vlan 20
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address FF:FF:FF:00:00:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 15
ip ARP INSPECTION TRUST
spanning-tree portfast
spanning-tree bpduguard enable
lldp transmit
lldp receive
CDP enable
no shutdown 
errdisable recovery interval 60
interface gi 1/2
errdisable recovery cause psecure-violation
!
!
interface range gi 2/0 - 3
description <<_ACCESS_VLAN_88_MGMT_&_AccessPoints_-_AP+Admin_>>
switchport mode access
switchport access vlan 88
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address FF:FF:FF:00:00:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping TRUST
ip ARP INSPECTION TRUST
spanning-tree portfast
spanning-tree bpduguard enable
lldp transmit
lldp receive
CDP enable
no shutdown 
errdisable recovery interval 60
interface gi 1/2
errdisable recovery cause psecure-violation
!
!
!
interface range gi 3/0 - 3
description <<_Trunk--->>DISTRIBUTION_or_CASCADE_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 10,20,88
switchport nonegotiate
ip dhcp snooping TRUST
ip arp inspection TRUST
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
lldp TRANSMIT
lldp RECEIVE
CDP ENABLE
shutdown
no shutdown 
exit
!
!
!
enable secret Fz3r0.12345
service password-encryption
login block-for 120 attempts 3 within 60
username root privilege 15 secret Fz3r0.12345
username Fz3r0 privilege 15 secret Fz3r0.12345
username user privilege 1 secret Fz3r0.12345
!
line console 0
password Fz3r0.12345
login local
logging synchronous
exec-timeout 5 30
exit
!
line aux 0
privilege level 1
transport input none
transport output none
login local
no exec
exit
!
line vty 0 8
access-class 8 in
transport input ssh
login local
logging synchronous
exec-timeout 5 30
exit
!
crypto key generate rsa
2048
ip ssh version 2
!
!
!
end
!
wr
!
reload
!
exit
!
!
!

```



## FortiGates (Edge Firewalls/Router/Gateways) Configurations

- **NOTA1:** Como en cualquier configuración inicial de FortiGate comenzaré por asignar una IP `Port1` via consola `CLI` para posteriormente entrar por `UI`.

- **NOTA2:** Este lab lo enfoqué en configuración por `UI`, pero haré lo posible por adjuntar el script en CLI de cada configuración realizada. 

- **NOTA3:** Agregué 2 opciones de configuración incial para `Port1` (`A `y `B`), una en caso de querer configurar la interfaz `WAN` por `DHCP`, yo lo hice `Static` en este laboratiorio.

### FortiGate1-MASTER

- **Opción A** `Static`

- **CLI Basic Init Config:**    

```
config system interface
edit port1
set description "WAN1-TELMEX-LEFT-ISP"
set alias "WAN1-TELMEX"
set mode static
set ip 192.168.143.100 255.255.255.0
select allowaccess ping https ssh http
set lldp-reception enable
end

config system global
set hostname "Fz3r0_FortiGate1_MASTER"
set alias "Fz3r0_FortiGate1_MASTER_alias"
set gui-theme onyx
set pre-login-banner enable
set post-login-banner enable
set admintimeout 60
set timezone 04  
end

config system admin
edit "Fz3r0"
set accprofile "super_admin"
set comments "Fz3r0:Fz3r0.12345"
set vdom "root"
config gui-dashboard



```

- **Opción B** `DHCP`

- **CLI Basic Init Config:**  

```
config system interface
edit port1
set description "WAN1-TELMEX-LEFT-ISP"
set alias "WAN1-TELMEX"
set mode dhcp
select allowaccess ping https ssh http
set lldp-reception enable
end

config system global
set hostname "Fz3r0_FortiGate1_MASTER"
set alias "Fz3r0_FortiGate1_MASTER_alias"
set gui-theme onyx
set pre-login-banner enable
set post-login-banner enable
set admintimeout 60
set timezone 04  
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

### FortiGate2-SLAVE

```
config system interface
edit port1
set mode static
set ip 192.168.143.200 255.255.255.0
select allowaccess ping https ssh http
end


```

#### RADIUS Authentication

##### Free RADIUS config @ `Kali Linux`

- [Ejemplo en Video](https://www.youtube.com/watch?v=C92x-0Cbxk8&t=1503s)

- **Instalar:**

```sh
sudo apt-get install freeradius
```

- **Verificar Instalación:**

```sh
ls /etc/freeradius/3.0/
```

- **Editar `User DB` con `Nano`:**

    - **TIP:** Buscar por el ejemplo de `bob` y hacer más usuarios con la misma sintaxis. 
    - Para guardar `CTRL + X` > `Y` > Enter!

```sh
nano /etc/freeradius/3.0/users

```

- **Verificar `User DB`:**

```sh
cat /etc/freeradius/3.0/users

```

- **Agregar `clients`**

    - **NOTA:** Los `clients` son los dispositivos que se conectan al RADIUS server y tienen permiso para consultar la DB, por ejemplo: mi FortiGate en este caso _(Ya que es el que solicitará las credenciales al servidor para verificar que hagan match y se cumpla el **AAA**)_.

    - **TIP:** Buscar por el ejemplo de `clients per_socket_clients` hasta el final del documento, no hay pierde! ;) 
    - Para guardar `CTRL + X` > `Y` > Enter! 

```sh
cat /etc/freeradius/3.0/clients.conf

```

- **IMPORTANTE!!!** 

- El GateWay del cliente correponde en realidad a la IP del mi Edge Router, FireWall, etc..

    - **En este caso la IP de mi FortiGate1 sería el GaeWay del cliente RADIUS: `0.0.0.0`**

```
client 0.0.0.0 {
 secret = C1sco.12345 
 shortname = FG1
 nastype = fortinet

}   

```    


















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

```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

(_.-Fz3r0-._)

Rising black, blacker and darker than the vast shades 
amid which it stood, immeasurably strong, mountain of 
iron, gate of steel, tower of adamant... 

...The cruel pinnacles and iron crown of the topmost 
tower of Barad-dûr. Fortress of Sauron. 

-- HECHO EN MEXICO -- 

Twitter: @Fz3r0_OPs 
GitHub : Fz3r0 

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

<<< Barad-dûr "The Dark Tower" >>> 

<<< FortiGate1-MASTER UI - PreLogin >>> 

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

<<< USER & PASSWORD: >>> 


Fz3r0
Fz3r0.12345


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
```


POST

```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

(_.-Fz3r0-._)

Welcome to my house! Enter freely. Go safely, 
and leave something of the happiness you bring...

We are in Transylvania, and Transylvania is not England. 
Our ways are not your ways, and there shall be to you 
many strange things. 

Nay, from what you have told me of your experiences 
already, you know something of what strange things there 
may be.

-- HECHO EN MEXICO -- 

Twitter: @Fz3r0_OPs 
GitHub : Fz3r0 

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

<<< Barad-dûr "The Dark Tower" >>> 

<<< FortiGate1-MASTER UI - PostLogin >>> 


WELCOME!!!


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

%%LAST_SUCCESSFUL_LOGIN%%
%%LAST_FAILED_LOGIN%%
```



===


shows

show lldp interface
port-channel 10
show lldp interface
port-channel 20


show ip arp inspection vlan 1
show ip arp inspection statistics vlan 1

arp inspection full
S1# conf t
Enter configuration commands, one per line. End with CNTL/Z.
S1(config)# arp access-list H2
S1(config-arp-nacl)# permit ip host 1.1.1.1 mac host 1.1.1
S1(config-arp-nacl)# end
S1# show arp access-list
ARP access list H2
permit ip host 1.1.1.1 mac host 0001.0001.0001


Duda:

- Cómo alcanzar el SW0 por la WAN int? se crea tmb la VLAN ahi?
- Es Trunk hacia el MikroTik DHCP server?

- ip helper mikrotik para multiples vlans? usan dhcp relay?

https://www.youtube.com/watch?v=SekPxtUUR68
https://www.youtube.com/shorts/aYEzFzLGuaQ

-->




https://www.computernetworkingnotes.com/ccna-study-guide/configure-dhcp-snooping-on-cisco-switches.html#:~:text=By%20default%2C%20DHCP%20snooping%20does,is%2015%20packets%20per%20second.
