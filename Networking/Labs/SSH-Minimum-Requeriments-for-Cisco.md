
---

### Fz3r0 Operations  [Networking]

### Fz3r0 Secure Networking Labs - Cisco Devices Config for Best Practices, Security Standards, Secure Logins & SSH

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `SSH` `TLS/SSL`

---

1. [Secure Login & SSH configuration on Cisco Devices]

3. [Cisco Auto Secure Configuration]

    - Manual Secure:
        - DHCP Snooping
        - Dynamic ARP Inspection
        - Port Security 
      
4. [Disable Unused Services]

6. [Aditional Security Configuration for Cisco Devices & Network]

---

### Secure Login & SSH configuration for Cisco Devices

- SSH is the method to use, period, Telnet is for noobs. 

- Telnet example (**NEVER use it!**):

```

NOOB(config)# line vty 0 4
NOOB(config-line)# password ci5c0
NOOB(config-line)# login

```

- SSH example (**SECURE! use it! :D**)

```

PRO(config)# ip domain-name << fz3r0_domain.gov >>
PRO(config)# crypto key generate rsa general-keys modulus 2048
PRO(config)# username Fz3r0_Adm1n secret Str0ng3rPa55w0rd
PRO(config)# ssh version 2
PRO(config)# line vty 0 4
PRO(config-line)# transport input ssh
PRO(config-line)# login local

```

- Full SSH like a Sir!

```

enable
configure terminal 
!
no ip domain-lookup
ip domain-name Fz3r0.domain
!
hostname << Device-Name Fz3r0 >>
!
enable secret fz3r012345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60
!
username root privilege 15 secret cisco12345
username user privilege 10 secret cisco12345
!
line console 0
password fz3r012345
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
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Fz3r0 Cisco CCNA Labs
         
         Configure SSH like a Sir!
           
         Twitter: @fz3r0_Ops
         Github : Fz3r0  

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
end
wr
!
reload
!
exit
!
!
!

```

- **NOTE: ADD MANUALLY A DEFAULT GATEWAY AND SVI IN CASE OF A SWITCH:**

```

interface vlan 100
description << Switch SVI (Virtual Interface) | Admin/SSH >>
ip address 192.168.100.1 255.255.255.0
no shutdown 
exit

```

```

ip default-gateway 192.168.100.254

```

- **NOTE: USE LOOPBACK, INTERFACES OR SUB-INTERFACES ON ROUTERS AS DEFAULT GATEWAY:**

```

interface gigabitEthernet 0/0.100
description << Connect to Subnet 100 >>
encapsulation dot1Q 100
ip address 192.168.100.254 255.255.255.0
no shutdown 
exit

```
```
interface loopback 0
description << loopback 10.10.10.10 >>
ip address 10.10.10.10 255.255.255.255
exit

```

---

### Cisco Auto Secure Configuration

```
```

---

### Disable Unused Services

```
```

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
