# MikroTik DHCP Server Config Lab
_by [Fz3r0 💀](https://github.com/Fz3r0/)_

## Topology

![image](https://user-images.githubusercontent.com/94720207/201542945-eb1cd274-f02d-4058-8b87-df159cf6d20a.png)

## Security

- User y Pass utilizados en este laboratorrio:

    - **User: `Fz3r0`** 
    - **Pass: `Fz3r0.12345`** 

## IP-Address Table & DHCP Configs

| VLAN ID  | VLAN NAME | NETWORK ID  | CIDR | MASK          | SUBNET HOST RANGE           | TOTAL HOSTS | IP POOLS                                            | POOL IPs | RESERVED IP LEASES (STATIC)              |
|:--------:|:---------:|:-----------:|:----:|:-------------:|:---------------------------:|:-----------:|:---------------------------------------------------:|:--------:|:----------------------------------------:|
| VLAN 1   | DEFAULT   | 172.1.0.0   | /24  | 255.255.255.0 | 172.1.0.1 - 172.200.0.254   | 256 - 2     | 172.1.0.1 - 172.200.0.254                           | 254      | N/A                                      |
| VLAN 10  | RED       | 172.10.0.0  | /16  | 255.255.0.0   | 172.10.0.1 - 172.10.255.254 | 65,536 - 2  | 172.10.0.1 - 172.10.1.255                           | 510      | N/A                                      |
| VLAN 20  | BLUE      | 172.20.0.0  | /17  | 255.255.128.0 | 172.20.0.1 - 172.20.127.254 | 32,768 - 2  | 172.20.0.1 - 172.20.5.255                           | 1534     | N/A                                      |
| VLAN 30  | GREEN     | 172.30.0.0  | /18  | 255.255.192.0 | 172.30.0.1 - 172.30.63.254  | 16,384 - 2  | 172.30.0.1 - 172.30.63.254                          | 16382    | N/A                                      |
| VLAN 88  | MGMT      | 172.88.0.0  | /20  | 255.255.240.0 | 172.88.0.1 - 172.88.15.254  | 4,096 - 2   | 172.99.1.0 - 172.99.10.255                          | 5118     | 172.88.0.1, 172.88.0.2, 172.88.0.254     |
| VLAN 100 | SERVICE1  | 172.100.0.0 | /22  | 255.255.252.0 | 172.100.0.1 - 172.100.3.254 | 1,024 - 2   | 172.100.3.0 - 172.100.3.254                         | 255      | 172.100.0.10                             |
| VLAN 200 | SERVICE2  | 172.200.0.0 | /24  | 255.255.255.0 | 172.200.0.1 - 172.200.0.254 | 256 - 2     | 172.200.0.2 - 172.200.0.9, 172.200.11 - 172.200.253 | 251      | 172.200.0.1, 172.200.0.10, 172.200.0.254 |





## Switch Core Configuration

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
"              <<<  MikroTik DHCP Server Easy as-ass!  >>>              "
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
switchport trunk native vlan 88
switchport trunk allowed vlan 10,20,30,88,100,200
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
switchport trunk native vlan 88
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

### 4 Pasos para entrar al Winbox

**1. La interface en VMWare se pone en `Bridge Automatic`, así la detectará dentro del laboratiorio virtual.**

**2. Conectar la PC que administrará el MikroTik a la interface X1 _(eth0 en este lab)_.** 

- Se puede usar un switch como en este laboratiorio o como en muchos casos en un deploy real _(obviamente ambos dispositivos deben estar en la misma VLAN o con políticas de inter-comunicación...En mi caso usé mi Standard VLAN 88 Nativa para management)**_

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

- `Quickset` > `Local Network` & `System`

![image](https://user-images.githubusercontent.com/94720207/201544405-6a2711fa-0e93-4761-af7c-54e0de87a7b3.png)
![image](https://user-images.githubusercontent.com/94720207/201545830-21780c82-27fe-46cc-8834-003e8fcf112f.png)

## 2. Configurar nuevo Admin

- `System` > `Users`

![image](https://user-images.githubusercontent.com/94720207/201546150-277a2bf2-c12a-4737-b31a-e8204a2f228e.png)

![image](https://user-images.githubusercontent.com/94720207/201546093-1f23339d-0039-4bdf-a525-bccdccd3fe94.png)

**2. Configurar VLANs en Interface `ether1`**

- `Interfaces` > `+`

![image](https://user-images.githubusercontent.com/94720207/201544666-d0400058-ab13-4dba-9f83-eb80306e6125.png)

- Configurar las VLANs (sub-interfaces), hacer lo mismo para todas las VLANs que necesitemos.

![image](https://user-images.githubusercontent.com/94720207/201545057-f14c90c0-9df0-46ca-8a12-857795baa5e1.png)

- Al final se verá algo así:

![image](https://user-images.githubusercontent.com/94720207/201545210-d676b4cf-37ba-423c-85e5-c98c5ba6c84e.png)


## Resources

### DHCP SERVER

- https://www.youtube.com/watch?v=OVDQLD_VC7I
- https://www.youtube.com/watch?v=yxASqrhP18Q

### RESERVED IP LEASES

- https://www.youtube.com/watch?v=fiNOPC8BBhI
