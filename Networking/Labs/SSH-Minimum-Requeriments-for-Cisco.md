
---

### Fz3r0 Operations  [Networking]

### Fz3r0 Secure Networking Labs - EtherChannel Like a Sir

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `EtherChannel` `PortChannel`

---

```

enable
configure terminal 
!
no ip domain-lookup
ip domain-name Fz3r0.domain
!
hostname << Device-Name Fz3r0 >>
!
enable secret cisco12345
service password-encryption
security passwords min-length 10
login block-for 120 attempts 3 within 60
!
username root privilege 15 secret cisco12345
username user privilege 10 secret cisco12345
!
line console 0
password cisco12345
login
exit
!
line aux 0
password cisco12345
login
exit
!
line vty 0 8
access-class 8 in
exec-timeout 5 30
transport input ssh
login local
exit
!
crypto key generate rsa
2048
ip ssh version 2
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

         Fz3r0 Cisco CCNA Labs!!!
         
         SSH Minimum requeriments
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  

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

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
