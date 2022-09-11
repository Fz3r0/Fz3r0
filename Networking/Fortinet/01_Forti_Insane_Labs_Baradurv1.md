

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
| **null**              |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |
| ****                  |               |                 |                 |          |                 |             |                                             |



## Switches Configurations

- **Layer 2 Fz3r0 Top Security Configuration:** 

    - [> Para más detalles acerca del `Fz3r0: Layer2 Security Pro-Config!` Click aquí <](https://github.com/Fz3r0/Fz3r0/blob/main/Networking/Labs/Security_&_Best-Practices_VS_Layer2_Attack_FULL_PRO_CONFIG.md)

    - [> Para más detalles acerca del `Fz3r0: SSH Pro-Config for Cisco Devices!` Click aquí <](https://github.com/Fz3r0/Fz3r0/blob/main/Networking/Labs/SSH-Minimum-Requeriments-for-Cisco.md)

    - **Nota Security 1:** Todas las interfaces utilizadas en `SW1-Core` van a transmitir y recibir LLDP y CDP, esto debido a que se encuentra en el MDF y todas las interfaces de acceso son de administrador, servidores o equipo confiable y resguardado solo para acceso autorizado, el bloqueo de paquetes de anuncios paquetes serán únicamente en los switches de acceso e interfaces de acceso _(o HoneyPots/Down)_.  

    - **Nota Security 2:** Ojo a la interfaz del MikroTik DHCP server, esta es la única que debe ser configurada como un `Trusted DHCP server` en Layer 2. 

### SW1-Cisco-CORE - Switch Core



```
!
!
enable
configure terminal
!
no ip domain-lookup
ip domain-name <<_Fz3r0.Barad-dûr_>>
!
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
vlan 666
name VLAN_666-DownPorts-HoneyPot
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
shutdown
description >>>_-_CHANNEL_L_LAG1_FG-MASTER_PORTS_0-1_-_<<<
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
interface range gi 3/2 - 3
shutdown
description >>>_-_CHANNEL_R_LAG2_FG-SLAVE_PORTS_2-3_-_<<<
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
interface gi 0/0
description <<_TRUNK--->>>SWITCH_DISTRIBUTION_GI3/3_>>
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
interface gi 1/0
description <<<-MikroTik-RouterBoard-DHCP-Server-->Ether1->>>
switchport mode access
switchport access vlan 88
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
switchport access vlan 88
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
switchport port-security mac-address FF:zz:33:rr:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 6
spanning-tree portfast
spanning-tree bpduguard enable
lldp transmit
lldp receive
CDP enable
no shutdown 
exit
!
!
!
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,88,99,666
ip arp inspection vlan 1,10,20,88,99,666
!
!
!
enable secret Fz3r0.12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60
!
username root privilege 15 secret Fz3r0.12345
username user privilege 10 secret Fz3r0.12345
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
hostname SW2_Distribution-F0
!
no ip domain-lookup
ip domain-name <<_Fz3r0.Barad-dûr_>>
!
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
vlan 666
name VLAN_666-DownPorts-HoneyPot
!
interface vlan 10
description <<_VLAN_10_RED_>>
ip address 172.10.0.12 255.255.0.0
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE_>>
ip address 172.20.0.12 255.255.0.0
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
description <<_Trunk--->>ACCESS_SWITCHES_>>
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
interface gi 3/3
description <<_Trunk--->>CORE_>>
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
interface range gi 1/1 - 3, gi 3/1 - 2 
description <<_VLAN666-HoneyPot_DownPorts-HOLE-TO-HELL_>>
shutdown
switchport mode access
switchport access vlan 666
switchport port-security
switchport port-security maximum 1
switchport port-security mac-address FF:zz:33:rr:00
switchport port-security aging time 5
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 6
spanning-tree portfast
spanning-tree bpduguard enable
no lldp transmit
no lldp receive
no CDP enable
shutdown
exit
!
!
!
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,88,99,666
ip arp inspection vlan 1,10,20,88,99,666
!
!
!
enable secret Fz3r0.12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60
!
username root privilege 15 secret Fz3r0.12345
username user privilege 10 secret Fz3r0.12345
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

- **NOTA1:** El LLDP y CDP será apagado en VLAN 10 RED y VLAN 20 BLUE por estándares de seguridad al ser Host Access Untrust, sin embargo si recibirán LLDP para leer información de los neighbors. 

    - En el caso de la `VLAN 88 MGMT + APs` si se mantendrá de ambos sintidos `LLDP` aunque se apagará el `CDP` al no ser necesario y así limpiar lo más posible la red. _(En el caso de switch a switch se mantiene CDP ya que ambos vendors sin cisco, en management va a otros dispositivos como PCs o APs que no necesitan CDP realmente)_

- **NOTA2:** Este Switch tiene todos los puertos utilizados, por eso **no será necesario apagar puertos y configurarlos con VLAN de `HoneyPot`.**

- **NOTA3:** En las interfaces `Access` que usan la `VLAN 88 Management` (Utilizadas para los Access Points)

    - **IMPORTANTE!!!** **Los `Access Points Ruckus` utilizan `Access VLAN` y pueden transportar `varias VLANs` sin necesidad de una `Trunk` debido a que se reporta a la `Controladora WLC Zone Director` por medio de `SSH Tunnel`.** 

- **NOTA4:** Para lograr la estandarización de configuración en todos los switches:

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

```
!
!
enable
configure terminal
!
hostname SWxxx_Access-F0
no ip domain-lookup
ip domain-name <<_Fz3r0.Barad-dûr_>>
!
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
"              <<<  SWxx-CISCO-ACCESS-XX >>>              "
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
name VLAN_666-DownPorts-HoneyPot
!
interface vlan 10
description <<_VLAN_10_RED_>>
ip address 172.10.0.12 255.255.0.0
no shutdown
exit
interface vlan 20
description <<_VLAN_20_BLUE_>>
ip address 172.20.0.12 255.255.0.0
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
interface range gi 0/0 - 3
description <<_ACCESS_VLAN_10_RED_-_HOST_INTERFACES_>>
switchport mode access
switchport access vlan 10
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address FF:zz:33:rr:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 6
spanning-tree portfast
spanning-tree bpduguard enable
no lldp transmit
lldp receive
no CDP enable
shutdown
no shutdown 
exit
!
interface range gi 1/0 - 3
description <<_ACCESS_VLAN_20_BLUE_-_HOST_INTERFACES_>>
switchport mode access
switchport access vlan 20
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address FF:zz:33:rr:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 6
spanning-tree portfast
spanning-tree bpduguard enable
no lldp transmit
lldp receive
no CDP enable
shutdown
no shutdown 
exit
!
interface range gi 2/0 - 3
description <<_ACCESS_VLAN_88_MGMT_&_AccessPoints_-_AP+Admin_>>
switchport mode access
switchport access vlan 20
switchport port-security
switchport port-security maximum 2
switchport port-security mac-address FF:zz:33:rr:00
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
switchport nonegotiate
ip dhcp snooping limit rate 6
spanning-tree portfast
spanning-tree bpduguard enable
lldp transmit
lldp receive
no CDP enable
shutdown
no shutdown 
exit
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
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,88,99,666
ip arp inspection vlan 1,10,20,88,99,666
!
!
!
enable secret Fz3r0.12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60
!
username root privilege 15 secret Fz3r0.12345
username user privilege 10 secret Fz3r0.12345
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





===

Duda:

- Cómo alcanzar el SW0 por la WAN int? se crea tmb la VLAN ahi?
- Es Trunk hacia el MikroTik DHCP server?

- ip helper mikrotik para multiples vlans? usan dhcp relay?

https://www.youtube.com/watch?v=SekPxtUUR68
https://www.youtube.com/shorts/aYEzFzLGuaQ

-->
