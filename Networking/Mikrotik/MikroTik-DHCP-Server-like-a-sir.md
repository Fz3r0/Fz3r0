
# Config `MikroTik DHCP Server`... Like A sir! 💀🎩
![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)
_by [Fz3r0 💀](https://github.com/Fz3r0/)_


---

##### Twitter  : [@Fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---
 
#### Keywords: `Networking` `Routing & Switching` `MikroTik` `DHCP Server`

---

## Topology

![image](https://user-images.githubusercontent.com/94720207/201570663-0ad85193-b008-4585-99e5-87d9d8d3b177.png)

## Security

- User y Pass utilizados en este laboratorrio:

    - **User: `Fz3r0`** 
    - **Pass: `Fz3r0.12345`** 

## IP-Address Table & DHCP Configs

| VLAN ID  | VLAN NAME | NETWORK ID  | CIDR | MASK          | SUBNET HOST RANGE           | TOTAL HOSTS | IP POOLS                                            | POOLs TOTAL IPs | RESERVED IP LEASES (STATIC)              |
|:--------:|:---------:|:-----------:|:----:|:-------------:|:---------------------------:|:-----------:|:---------------------------------------------------:|:---------------:|:----------------------------------------:|
| VLAN 10  | RED       | 172.10.0.0  | /16  | 255.255.0.0   | 172.10.0.1 - 172.10.255.254 | 65,536 - 2  | 172.10.0.10 - 172.10.1.255                          | 510             | 172.10.0.1, 172.10.0.254                 |
| VLAN 20  | BLUE      | 172.20.0.0  | /17  | 255.255.128.0 | 172.20.0.1 - 172.20.127.254 | 32,768 - 2  | 172.20.0.10 - 172.20.5.255                          | 1534            | 172.20.0.1, 172.20.0.254                 |
| VLAN 30  | GREEN     | 172.30.0.0  | /18  | 255.255.192.0 | 172.30.0.1 - 172.30.63.254  | 16,384 - 2  | 172.30.0.10 - 172.30.63.254                         | 16382           | 172.30.0.1, 172.30.0.254                 |
| VLAN 88  | MGMT      | 172.88.0.0  | /20  | 255.255.240.0 | 172.88.0.1 - 172.88.15.254  | 4,096 - 2   | 172.99.1.10 - 172.99.10.255                         | 5118            | 172.88.0.1, 172.88.0.5, 172.88.0.254     |
| VLAN 100 | SERVICE1  | 172.100.0.0 | /22  | 255.255.252.0 | 172.100.0.1 - 172.100.3.254 | 1,024 - 2   | 172.100.3.11 - 172.100.3.254                        | 255             | 172.100.0.1, 172.100.0.10, 172.100.0.254 |
| VLAN 200 | SERVICE2  | 172.200.0.0 | /24  | 255.255.255.0 | 172.200.0.1 - 172.200.0.254 | 256 - 2     | 172.200.0.2 - 172.200.0.9, 172.200.11 - 172.200.253 | 251             | 172.200.0.1, 172.200.0.10, 172.200.0.254 |

### Lista de IPs `Management`

- Switch-CORE: `MGMT` - `172.88.0.1`
- MikroTik (VLAN88): `MGMT` - `172.88.0.5`
- Gateway: `MGMT` - `172.88.0.254`

## `Switch Core` - Config

- **Notas:**

    - Ojo que el Trunk hacia el DHCP Server utilizo el `Default VLAN 99 Native` (Los noobs usan VLAN 1 jeje), sin embargo, las Trunks de Management por ejemplo hacia un AP o la PC de Administrador ya utilizan una `Native VLAN 88`. **Si utilizara la MGMT 88 también para el MikroTik no repartiría DHCP esa Network!!! Cuidado!!!**

    - La seguridad que utilizo se puede estudiar más a fondo en mi tutorial "Fz3r0 Layer 2 Top Security"
    
    - Ojo a la IP del Switch y en general a toda la subnet de management

![image](https://user-images.githubusercontent.com/94720207/201709512-7e351f7d-a021-478b-959a-db49e1b4656a.png)

```
!
!
enable
configure terminal
!
hostname SW1-CORE_Fz3r0
no ip domain-lookup
ip domain-name Fz3r0.DHCP.MikroTik
!
banner motd %




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                                       "
"          /$$$$$$$$               /$$$$$$             /$$$$$$          "
"         | $$_____/              /$$__  $$           /$$$_  $$         "
"         | $$          /$$$$$$$$|__/  \ $$  /$$$$$$ | $$$$\ $$         "
"         | $$$$$ /$$$$|____ /$$/   /$$$$$/ /$$__  $$| $$ $$ $$         "
"         | $$__/|____/   /$$$$/   |___  $$| $$  \__/| $$\ $$$$         "
"         | $$           /$$__/   /$$  \ $$| $$      | $$ \ $$$         "
"         | $$          /$$$$$$$$|  $$$$$$/| $$      |  $$$$$$/         "
"         |__/         |________/ \______/ |__/       \______/          "
"                                                                       "
"                        @@@@@@@@@@@@@@@@@@                             "
"                      @@@@@@@@@@@@@@@@@@@@@@@                          "
"                    @@@@@@@@@@@@@@@@@@@@@@@@@@@                        "
"                   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@                       "
"                  @@@@@@@@@@@@@@@/      \@@@/   @                      "
"                 @@@@@@@@@@@@@@@@\      @@  @___@                      "
"                 @@@@@@@@@@@@@ @@@@@@@@@@  | \@@@@@                    "
"                 @@@@@@@@@@@@@ @@@@@@@@@\__@_/@@@@@                    "
"                  @@@@@@@@@@@@@@@/,/,/./'/_|.\'\,\                     "
"                    @@@@@@@@@@@@@|  | | | | | | | |                    "  
"                                  \_|_|_|_|_|_|_|_|                    "
"                                                                       "
"          <<<  Config MikroTik DHCP Server... Like A sir!  >>>         "
"                                                                       "
"                        -- HECHO EN MEXICO --                          "
"                                                                       "
"                         Twitter:  @Fz3r0_OPs                          "
"                         GitHub :  Fz3r0                               "
"                                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
%
!
banner exec %

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                                       "
"             Welcome to my house! Enter freely. Go safely,             "
"           and leave something of the happiness you bring...           "
"                                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

%
!
banner incoming %
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                                       "
"                       <<<  SW1-CISCO-CORE >>>                         "
"                                                                       "
"              User:  Fz3r0             Pass:   Fz3r0.12345             "
"                                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

%
!
banner login %
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
"                                                                       "
"                       <<<  SW1-CISCO-CORE >>>                         "
"                                                                       "
"              User:  Fz3r0             Pass:   Fz3r0.12345             "
"                                                                       "
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

%
!
!
vlan 10
name VLAN_10_RED 
vlan 20
name VLAN_20_BLUE 
vlan 30
name VLAN_10_GREEN
vlan 88
name VLAN_88_MGMT_&_TRUNKS
vlan 100
name VLAN_100_SERVICE1 
vlan 200
name VLAN_200_SERVICE2
!
!
!
interface vlan 88
description <<_MGMT_VLAN_88_INTERFACE(VR)_>>
ip address 172.88.0.1 255.255.240.0
no shutdown
exit
!
ip default-gateway 172.88.0.254
ip http server
!
lldp run
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,30,88,100,200
ip arp inspection vlan 1,10,20,30,88,100,200
!
!
interface gi 3/3
description <<_-_TRUNK--->>>-MikroTik_DHCP_Server_-_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 1,10,20,30,88,100,200
switchport nonegotiate
ip dhcp snooping TRUST
ip arp inspection TRUST
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
lldp TRANSMIT
lldp RECEIVE
no CDP ENABLE
shutdown
no shutdown 
exit
!
!
interface gi 3/2
description <<_-_TRUNK--->>>-MGMT-ADMIN-FZ3R0-WIN10_-_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 99
switchport trunk allowed vlan 1,10,20,30,88,100,200
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
interface gi 3/2
description <<<---HOST_-_ACCESS_VLAN_88_RED--->>>
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
interface gi 3/2
errdisable recovery cause psecure-violation
!
interface range gi 0/0 - 1
description <<<---HOST_-_ACCESS_VLAN_10_RED--->>>
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
interface range gi 0/0 - 1
errdisable recovery cause psecure-violation
!
!
interface range gi 0/2 - 3
description <<<---HOST_-_ACCESS_VLAN_20_BLUE--->>>
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
interface range gi 0/2 - 3
errdisable recovery cause psecure-violation
!
!
interface range gi 1/0 - 1
description <<<---HOST_-_ACCESS_VLAN_30_GREEN--->>>
switchport mode access
switchport access vlan 30
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
interface range gi 1/0 - 1
errdisable recovery cause psecure-violation
!
!
!
interface range gi 2/0 - 1
description <<<---SERVICE1_-_ACCESS_VLAN_100--->>>
switchport mode access
switchport access vlan 100
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
interface range gi 2/0 - 1
errdisable recovery cause psecure-violation
!
interface range gi 2/2 - 3
description <<_-_SERVICE2_-_TRUNK_SERVICE_CARRIER_VLAN200_-_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 200
switchport trunk allowed vlan 1,10,20,30,88,100,200
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
interface range gi 3/0 - 1
description <<_-_TRUNK--->>>-MNGMT_-_>>
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk native vlan 88
switchport trunk allowed vlan 1,10,20,30,88,100,200
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

## Windows VM

### 4 Pasos para entrar al Winbox:

**1. La interface en VMWare se pone en `Bridge (Automatic)`, así le asignará una VMnet automáticamente al encender la VM**

![image](https://user-images.githubusercontent.com/94720207/201561959-96391314-a1eb-45a5-b721-71e36e180bbe.png)

- Ojo!!! Después de encender la VM, se le asignará automáticamente una VMnet, en este caso le asignó la VMnet3

![image](https://user-images.githubusercontent.com/94720207/201561554-f2131574-c2fe-4125-a9c3-dd4fc733efd1.png)

**2. Conectar la PC que administrará el MikroTik a la interface `ether1` _(Debe ser esa ya que es la WAN por default)_.** 

- Ojo!!! Se puede usar un switch como en este laboratiorio o como en muchos casos en un deploy real:

    - **NOTA IMPORTANTE RESPECTO A LAS TRUNKS**

    - Obviamente ambos dispositivos deben estar en la misma VLAN o con políticas de inter-comunicación desde un principio.
    - En el caso de este laboratiorio, al final hice unos cambios de VLAN para tener un resultado donde mi Admin reciba DHCP de la VLAN 88 y al mismo tiempo sea Trunk, además de haber sido quien configuró al DHCP desde un principio... Es algo enredado lo sé, pero solo es importante recordar lo siguiente:

        1. Al configurar desde 0 ambos dispositivos (Pc y MikroTik) deben estar en la misma VLAN (para poderse ver aunque sea Layer 2 MAC)
        2. Para que pueda recibir DHCP una Trunk de Management, la Native VLAN no puede ser la misma que transporta las VLANs (Native / Untagged) desde el DHCP server, por eso al final se la cambié por la `Default 99` y dejé los Trunk de Management con `Native 88`

![image](https://user-images.githubusercontent.com/94720207/201557603-0b4d32d0-b9aa-45c7-a8ec-03ea89553a35.png)


**3. Ya dentro del Windows se podrá ver como neighbor desde winbox**

![image](https://user-images.githubusercontent.com/94720207/201543853-c587c9c0-d378-43a7-8da6-3235ba2e21f2.png)

- Default user: `admin`
- Pass: _(vacío)_
- Connect!

![image](https://user-images.githubusercontent.com/94720207/201544152-12829ac7-a2a1-4d74-854c-286fd7791aff.png)

- Nota:

    - Ojo!!! Nótese como la PC no tiene IPv4 asignada y de todos modos alcanzó al MikroTik, esto se debe a que se conectaron via MAC-Address con la función de búsqueda del MikroTik en la Interfaz `ether 1`. 
    - También se le podríar una IP estática a ambos dispositivos y conectarse por ese medio ;). Por ahora lo dejaré así y esperaré a que la PC recibe DHCP después. 

# WinBox DHCP Config:

## 1. Configurar IP-Address Local (Management) & System ID

- **Via CLI:**

```
/interface bridge add name=Local_Management
/interface bridge port add interface=ether1 bridge=Local_Management
/ip address add address=172.88.0.2/20 interface=Local_Management
```

- **Via WinBox:**

1. Crear el `Bridge` para acceso `local`:

![image](https://user-images.githubusercontent.com/94720207/201568831-f8f461a7-7b0c-47ed-99b2-b5e5baf3d155.png)

![image](https://user-images.githubusercontent.com/94720207/201569025-c531090c-9bf2-4a7f-a997-c8cb665a9efa.png)

2. Asignar la IP a esa `interface local` en mi caso `172.88.0.5/20`:

![image](https://user-images.githubusercontent.com/94720207/201570515-df34847d-785a-4c1a-a2d4-d771d013c08f.png)

![image](https://user-images.githubusercontent.com/94720207/201570865-1b8937e8-9eee-45f0-b880-f04be7d1a8e7.png)

3. Reiniciar RouterOS:

![image](https://user-images.githubusercontent.com/94720207/201571644-b67d9e50-3d7d-43c1-8061-8883f97783fc.png)

---

- Nombre y Password de Dispositivo:

![image](https://user-images.githubusercontent.com/94720207/201545830-21780c82-27fe-46cc-8834-003e8fcf112f.png)

## 2. Configurar nuevo Admin

- `System` > `Users`

![image](https://user-images.githubusercontent.com/94720207/201546150-277a2bf2-c12a-4737-b31a-e8204a2f228e.png)

![image](https://user-images.githubusercontent.com/94720207/201546093-1f23339d-0039-4bdf-a525-bccdccd3fe94.png)

- Se puede cambiar el password de admin o modificarlo para mayor seguridad

![image](https://user-images.githubusercontent.com/94720207/201546642-7e61f5a9-0d16-4021-800c-816983e25071.png)

## 2. Configurar VLANs en Interface `ether1`

- `Interfaces` > `+`

![image](https://user-images.githubusercontent.com/94720207/201544666-d0400058-ab13-4dba-9f83-eb80306e6125.png)

- Configurar las VLANs (sub-interfaces), hacer lo mismo para todas las VLANs que necesitemos.

![image](https://user-images.githubusercontent.com/94720207/201545057-f14c90c0-9df0-46ca-8a12-857795baa5e1.png)

- Al final se verá algo así:

![image](https://user-images.githubusercontent.com/94720207/201545210-d676b4cf-37ba-423c-85e5-c98c5ba6c84e.png)

## 3. Crear Subnets / Direcciones IPv4

- Comando `ip address print` _(para revisión)_

![image](https://user-images.githubusercontent.com/94720207/201546992-7c93ab43-8019-44c7-82a8-a83d6706c0bb.png)

- `IP` > `Addresses` > `+`

![image](https://user-images.githubusercontent.com/94720207/201546840-2782c91c-0b9e-446d-9837-86699ff30824.png)

- Primero puedo aprovechar para seleccionar el ether1 como la Interfaz de MGMT y ponerle su IP al DHCP Server

![image](https://user-images.githubusercontent.com/94720207/201547071-47cdfa0b-c584-4416-b96a-1c53b84524e5.png)

- Despúes creo todas las demás dubmet para cada VLAN respectivamente, por ejemplo:

    - En este Lab utilizamos las IP que acaban en `0.1` para identificar las Sub-Interfaces del DHCP
    - En este Lab utilizamos las IP que acaban en `0.254` para identificar las Sub-Interfaces o Interfaces de los Gateways
    - En el caso de la Interfaz física `ether1` decidí ponerle la `0.2` de la `vlan 88` que le corresponde 

![image](https://user-images.githubusercontent.com/94720207/201547886-1e1eeb7a-23a7-495d-8a65-7481019a72a8.png)

- Al final quedaría algo así: _(lo verde son las VLANs y lo rosa es la ether1 física)_

![image](https://user-images.githubusercontent.com/94720207/201548134-09c55fea-6220-45f3-951a-2f654538bbc3.png)

- Comando `ip address print` _(para revisión)_

![image](https://user-images.githubusercontent.com/94720207/201555754-fcf3ab59-458c-4e3d-bcee-0c9a1998f0e4.png)

## 4. Configurar DHCP Server

- `IP` > `DHCP Server` > `+`

![image](https://user-images.githubusercontent.com/94720207/201546720-9d06d028-ae7d-42fa-8c33-eda0c58e8af6.png)

- **Opción 1: Usando `DHCP Setup` (Wizard)**

![image](https://user-images.githubusercontent.com/94720207/201548393-a3ee9758-22a2-4730-8b58-fcdda20188e9.png)

![image](https://user-images.githubusercontent.com/94720207/201548416-acf29c6d-803b-4f5a-8619-c1992131df56.png)

![image](https://user-images.githubusercontent.com/94720207/201548430-c62bb6be-08ed-4a2b-8737-daad5b25144a.png)

![image](https://user-images.githubusercontent.com/94720207/201549912-ce5231a7-ed27-416f-b2e8-28830abeff5d.png)

![image](https://user-images.githubusercontent.com/94720207/201548940-5816bfa8-1a8f-415d-bc37-fc958e0a1c41.png)

![image](https://user-images.githubusercontent.com/94720207/201549011-9afd45cc-dfd1-49bd-9694-e357e2c17808.png)

![image](https://user-images.githubusercontent.com/94720207/201549025-b37e0dad-3f99-4ea3-ba35-bbf6a228d126.png)

![image](https://user-images.githubusercontent.com/94720207/201549052-ba012011-8b00-4987-a182-9a928486c96d.png)

![image](https://user-images.githubusercontent.com/94720207/201549087-be56d01d-eb70-43b9-ac71-875825b72604.png)

- **Opción 2: de manera `Manual`**

- `IP` > `Pool`

![image](https://user-images.githubusercontent.com/94720207/201549205-054b46b9-9c04-4adb-b7a4-73cfc2866066.png)

- Crear la Pool:

![image](https://user-images.githubusercontent.com/94720207/201550023-85f70dd0-e27c-46a0-8d45-843276876da8.png)

- Diferencias (el nombre del Wizard también se puede cambiar desde aquí y todo más fácil :D)

![image](https://user-images.githubusercontent.com/94720207/201550084-58bdf6f2-8d6c-4937-8918-74c4fdaf4ef3.png)

![image](https://user-images.githubusercontent.com/94720207/201550105-81c02650-7041-458d-8b1d-0e69d1b57f60.png)

- Asignar la Pool a la VLAN (en este ejemplo la 20)

![image](https://user-images.githubusercontent.com/94720207/201550288-0ff7fd03-2660-4782-b4af-12d0de2e284e.png)

- Aquí también se puede cambiar de nombre lo que se hizo con el Wizard

![image](https://user-images.githubusercontent.com/94720207/201550355-0ea53fe0-9386-4edb-a20a-c837445550dc.png)

- Crear la DHCP Network

![image](https://user-images.githubusercontent.com/94720207/201550678-078d6f9e-9f44-4ae0-8046-0cc543a0b59e.png)

![image](https://user-images.githubusercontent.com/94720207/201550791-15dec35c-2fc3-437a-9d88-ea4491a27f01.png)

## 5. Revisión de configuración de DHCP Server

- Ya sea que se haya realizado Wizard o Manual al final se verá algo así:

### Interface List

![image](https://user-images.githubusercontent.com/94720207/201551611-76cb6495-6b5a-4ac5-bfff-efd394ff051f.png)

### DHCP Server

![image](https://user-images.githubusercontent.com/94720207/201551523-4d131deb-4358-403e-b1e7-4ebabc98e0e0.png)

### DHCP Networks

![image](https://user-images.githubusercontent.com/94720207/201551535-98caf034-86ce-4375-99a6-115a20dfb6bc.png)

### IP Pool

![image](https://user-images.githubusercontent.com/94720207/201551499-fa85c714-5f19-4045-8a2c-770f4e0a3de7.png)

### `export compact` desde MikroTik RouterOS CLI

![image](https://user-images.githubusercontent.com/94720207/201565010-69f536cf-1445-413d-9e65-3a47fa1367d1.png)

## 6. Revisión desde los Hosts

- PC-Admin Fz3r0 `ipconfig`:

![image](https://user-images.githubusercontent.com/94720207/201556276-2ab7e398-8642-40b2-9d78-2537e69fcca7.png)

- Ping Hacia la Sub-Interfaz del DHCP Server de `VLAN 88 Management` - `172.88.0.2`

![image](https://user-images.githubusercontent.com/94720207/201555332-dc20233c-afe9-4b12-9543-52738cdce888.png)

- Revisión en los demás hosts y cada VLAN, por ejemplo:

- **`VLAN 10 RED` - `172.10.0.0/16`**

![image](https://user-images.githubusercontent.com/94720207/201556442-b5a19784-95af-49e5-bd3a-5b8bd02c1c38.png)

- Lo mismo para la asignación DHCP de cualquier Host y VLAN necesarios.

---

- Finalmente, se pueden hacer pruebas de ping, tráfico, troughput, etc.

![image](https://user-images.githubusercontent.com/94720207/201557093-a42674ae-6838-4ba0-9c16-01a68581f354.png)

- Nota: En este Lab no hice ninguna salida a Internet o WAN, pero también se debería probar la salida a Internet como en mi otro tutorial "Barad-Dur".

- También podemos revisar los `logs`, `leases`, `IP Pools` o `Used IPs` utilizados desde el Winbox:

![image](https://user-images.githubusercontent.com/94720207/201559399-925e449a-f698-47c2-95ae-2756050f2f5d.png)

![image](https://user-images.githubusercontent.com/94720207/201559569-b4e94303-8679-4887-968f-d9700ea51d90.png)

![image](https://user-images.githubusercontent.com/94720207/201581860-1ff7b3f0-1106-4d43-ae98-59f673db3f0d.png)

![image](https://user-images.githubusercontent.com/94720207/201581803-50e85654-7de9-4b37-885d-30f70560dbb0.png)


- También desde la PC podemos hacer un Packet Analysis con `Wireshark` y se podrían ver los PDU de DHCP (pendiente)

## Conclusiones

- En realidad está de volada padrino... Solo ojo con: 

    - Los detalles de las troncales que reciban DHCP no sean la misma que la troncal del DHCP server.
    
    - Siempre tener bien identificadas las IP estáticas y reservadas y no usarlas en la Pool (O asignarlas estáticas desde el MikroTik), por ejemplo:
    
        - `0.1` (DHCP Server Interface)
        - `0.254` (Gateway)
        - Cualquier otro Host o Servicio con IP Reservada
    
    - En caso de usar seguridad del lado del switch como DHCP snooping hacerlo a mucha conciencia. 

- En este caso no usamos salida a WAN ni desde el MikroTik ni desde otro Router o Firewall, en caso de realizarlo desde el MikroTik se debe configurar una `NAT` con `Masquerade`, aunque el verdadero propósito de este laboratorio es replicar el uso de un MikroTik **únicamente como DHCP Server**. Por ejemplo, un `FortiGate` podría estar sirviendo de Gateway hacia la WAN (Internet).

## Recursos

### DHCP SERVER

- https://www.youtube.com/watch?v=4VPqFfLdhKg (manual)
- https://www.youtube.com/watch?v=3m6AsMdZgOE
- https://www.youtube.com/watch?v=OVDQLD_VC7I
- https://www.youtube.com/watch?v=yxASqrhP18Q

### RESERVED IP LEASES

- https://www.youtube.com/watch?v=fiNOPC8BBhI

### Configuring IP Access

- https://help.mikrotik.com/docs/display/ROS/First+Time+Configuration

---

<span align="center"> <p align="center"> ![giphy](https://user-images.githubusercontent.com/94720207/166587250-292d9a9f-e590-4c25-a678-d457e2268e85.gif) </p> </span> 

&nbsp;

<span align="center"> <p align="center"> _Don't forget to enjoy your days..._ </p> </span> 
<span align="center"> <p align="center"> _...It's getting dark... so dark..._ </p> </span> 
<span align="center"> <p align="center"> _I am [Fz3r0 💀](https://github.com/Fz3r0/) and the Sun no longer rises..._ </p> </span> 
 
---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_  
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 

