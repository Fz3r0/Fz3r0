
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### **Pro and Secure Networking Labs:** 
#### **DHCPv4** All-in-One! (Cisco Router, Home Router, Generic Server, Wireless as DHCP Servers, Clients & Relay Agents)

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `DHCPv4`

---

#### Packet Tracer Lab Files & Topology

[**<< DOWNLOAD FILES >>**](https://github.com/Fz3r0/Fz3r0/files/8578198/7___fz3r0_OPs_Routing_._Switching_EtherChannel_PAgP_LACP_Static_All_in_one.zip)

![dhcpland1](https://user-images.githubusercontent.com/94720207/166123951-8ffa1d1a-633a-4f6e-ab9d-e335a017d21d.png)

![dhcpland2](https://user-images.githubusercontent.com/94720207/166123955-a5f79007-37ab-45e0-9072-39b0ed1ae862.png)

![dhcpland3](https://user-images.githubusercontent.com/94720207/166123980-107b3980-7be6-4ed1-beb9-469391c7ad7f.jpg)



---   
### Objectives:

1. Configure DHCP Servers:
    
    - Big Enterprise:
        - `R2` - Cisco Router as a DHCP Server for Enterprise LAN (Including VLANs)
    
    - Small Business:
        - `Server1` - Generic _(Windows Server)_ as a DHCP Server
    
    - Home Sweet Home:
    - `Home WiFi1` - Home Router _(WiFi Modem)_ as a DHCP Server

3. Configure DHCP Relay:

    - `R1` & `R3` Cisco Routers (at Big enterprise) as a DHCP Relay Agent for DHCP between different Networks _(From centralized Edge Router **R2**)_

5. Configure DHCP Clients:
    - `R2` Cisco Router as a DHCP Client _(From ISP-Telmex)_
    - `Home Router` _(WiFi Modem)_ as a DHCP Client _(From ISP-Telmex)_
    - Generic DHCP Clients as PCs, Laptops, Smartphones, Printers, Tablets

---

### Scenario

1. Configuring a Cisco router as a DHCP server to provide dynamic allocation of addresses to clients on the network divided in 2 VLANs (VLAN10 & VLAN20).
 
2. Configure the **EDGE ROUTER as a DHCP client** (`R2`) so that it receives an IP address from the ISP network (Internet). 

3. Since the server is centralized, configure the two LAN routers (`R1` & `R3`) to relay DHCP traffic between the different LANs and the router that is serving as the DHCP server (`R2`).

---

### Configuration

---

### R666-ISP - Telmex (Internet Provider) INSIDE "CLOUD"!

- **This will be the Router simulating the Gateway between WWW-Internet & ISP Internet Clients**
1. Create a DHCP pool for ALL ISP Internet Clients 
    - It's simulating 1 public IP for "3 neighbors in 1 street"
    - All the clients get DHCP from ISP to their Edge Routers, Routers or Home Routers(AKA Internet Modem for home)
2. Only exclude:
    - (Gi 0/1) 209.165.202.225/27 - To Internet Clients (Home, Office, etc)
    - _Only exclude IP of the Gateway of Internet to Clients, because Internet I & II are Static._

- _Note: EIGRP will be configured as Routing Protocol (EIGRP1)_

```

enable
configure terminal
!
!
hostname <R666-ISP-TELMEX_INFRAESTRUCTURE-SIMULATION>
ip domain-name ISP_TELMEX___fz3r0_domain.DHCP_labs
!
!
!
ip dhcp excluded-address 209.165.200.225
!
!
ip dhcp pool fz3r0_DHCP_Pool1_<<for:R1-VLAN-10___PRIVATE_DNS>>
!
network 209.165.200.224 255.255.255.224
default-router 209.165.200.225
dns-server 1.1.1.1
!
!
!
interface GigabitEthernet0/0
description << Gateway to the Internet WWW - Out into the wild!) >>
ip address 209.165.202.129 255.255.255.224
duplex auto
speed auto
no shutdown
!
!
interface GigabitEthernet 0/1
description << Gateway to the Internet DNS - Cloudflare range 1.1.1.1) >>
ip address 1.1.1.254 255.255.255.0
duplex auto
speed auto
no shutdown
!
!
!
interface GigabitEthernet 0/2
description << Gateway for Internet Clients - Connect_to_ISP_Clients) >>
ip address 209.165.200.225 255.255.255.224
duplex auto
speed auto
no shutdown
!
!
!
!
!
!
router eigrp 1
network 209.165.200.224 0.0.0.31
network 209.165.202.128 0.0.0.31
network 1.1.1.0 0.0.0.255
!
!
ip flow-export version 9
!
!
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

### BIG ENTERPRISE "Y" 

- **This is a Internet Client who get DHCP from ISP DHCP service**
1. Configure **R2** to **exclude the IPs** you need to take out
2. Create 2 different pools for 2 different VLANs (VLAN10 & VLAN20)
3. Configure the DHCP Pools including:
    - Network Address
    - Default Gateway
    - DNS Server IP
4. R2 needs to be configured to receive addressing from the ISP.

- **Note: R2 Will be the DHCP Server for the 2 different networks _(VLAN10 & VLAN20)_, and at the same time R2 will be recieving DHCP from the ISP Router _(Internet Cloud)_.**

---

### BIG ENTERPRISE "Y" > R2 - Router 2 - `DHCP SERVER` 

```

enable
configure terminal
!
!
hostname <R2-DHCP_Server_for_VLAN-10_&_VLAN-30>
ip domain-name BIG_ENTERPRISE_Y___fz3r0_domain.DHCP_labs
!
!
!
ip dhcp excluded-address 192.168.10.1 192.168.10.100
ip dhcp excluded-address 192.168.10.151 192.168.10.254
ip dhcp excluded-address 192.168.10.113
ip dhcp excluded-address 192.168.10.114
ip dhcp excluded-address 192.168.10.115
!
ip dhcp pool fz3r0_DHCP_Pool1_<<for:R1-VLAN-10___PRIVATE_DNS>>
!
network 192.168.10.0 255.255.255.0
default-router 192.168.10.254
dns-server 192.168.20.201
exit
!
!
!
ip dhcp excluded-address 192.168.30.1 192.168.30.100
ip dhcp excluded-address 192.168.30.151 192.168.30.254
ip dhcp excluded-address 192.168.30.113
ip dhcp excluded-address 192.168.30.114
ip dhcp excluded-address 192.168.30.115
!
!
!
ip dhcp pool fz3r0_DHCP_Pool2_<<for:R3-VLAN-30___PUBLIC_DNS>>
!
network 192.168.30.0 255.255.255.0
default-router 192.168.30.254
dns-server 1.1.1.1
exit
!
!
!
!
interface GigabitEthernet0/1
description <<Connect_to_Internet_(DHCP-CLIENT-FROM-ISP)>>
ip address dhcp
duplex auto
speed auto
no shutdown
!
!
!
interface GigabitEthernet0/0
description <<Connect_to_VLAN-20_(DNS_Server_Static_LAN)>>
ip address 192.168.20.254 255.255.255.0
duplex auto
speed auto
no shutdown
!
interface Serial0/0/0
description <<Connect_to_DHCP_Frame_Relay_Router(R1-VLAN-10)>>
ip address 10.1.1.2 255.255.255.252
clock rate 64000
!
interface Serial0/0/1
description <<Connect_to_DHCP_Frame_Relay_Router(R2-VLAN-30)>>
ip address 10.2.2.2 255.255.255.252
clock rate 64000
!
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

### BIG ENTERPRISE "Y" > R1 - Router 1 - `DHCP CLIENT` & `DHCP Relay Agent`

- **This is a Internet Client who get DHCP from ISP DHCP service**

```

enable
configure terminal
!
!
hostname <R1-DHCP_Relay_Agent(fromR2)_for_VLAN-10>
ip domain-name BIG_ENTERPRISE_Y___fz3r0_domain.DHCP_labs
!
!
!
interface Gi 0/0
description << R1 - Gateway for VLAN10) >>
ip address 192.168.10.254 255.255.255.0
ip helper-address 10.1.1.2
duplex auto
speed auto
no shutdown
no shutdown
!
!

```

--- 

### R3 - BIG ENTERPRISE "Y" > Router 3 - `DHCP CLIENT` & `DHCP Relay Agent`

```

enable
configure terminal
!
!
hostname <R3-DHCP_Relay_Agent(fromR2)_for_VLAN-30>
ip domain-name BIG_ENTERPRISE_Y___fz3r0_domain.DHCP_labs
!
!
!
interface Gi 0/0
description << R1 - Gateway for VLAN30) >>
ip address 192.168.30.254 255.255.255.0
ip helper-address 10.2.2.2
duplex auto
speed auto
no shutdown
!
!

```

---

### BIG ENTERPRISE "Y" 

1. Configure **R2** to **exclude the IPs** you need to take out
2. Create 2 different pools for 2 different VLANs (VLAN10 & VLAN20)
3. Configure the DHCP Pools including:
    - Network Address
    - Default Gateway
    - DNS Server IP
4. R2 needs to be configured to receive addressing from the ISP.

- **Note: R2 Will be the DHCP Server for the 2 different networks _(VLAN10 & VLAN20)_, and at the same time R2 will be recieving DHCP from the ISP Router _(Internet Cloud)_.**

---

### SMALL BUSINESS "X" > R100 - Router 100 - `DHCP SERVER`

```

enable
configure terminal
!
!
hostname < R100 - DHCP Server for VLAN-200 >
ip domain-name SMALL_BUSINESS_X___fz3r0_domain.DHCP_labs
!
!
!
ip dhcp excluded-address 192.168.66.1 192.168.66.100
ip dhcp excluded-address 192.168.66.151 192.168.66.254
ip dhcp excluded-address 192.168.66.113
ip dhcp excluded-address 192.168.66.114
ip dhcp excluded-address 192.168.66.115
!
ip dhcp pool fz3r0_DHCP_Pool1_<<for:SMALL_BUSINESS_VLAN-200___PUBLIC>>
!
network 192.168.66.0 255.255.255.0
default-router 192.168.66.254
dns-server 1.1.1.1
!
!
!
!
interface GigabitEthernet0/1
description <<Connect_to_Internet_(DHCP-CLIENT-FROM-ISP)>>
ip address dhcp
duplex auto
speed auto
no shutdown
!
!
!
interface GigabitEthernet0/0
description <<Connect_to_VLAN-200_(SMALL_BUSINESS_LAN)>>
ip address 192.168.66.254 255.255.255.0
duplex auto
speed auto
no shutdown
!
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

### INTERNET WWW > SERVER1(`twitter.com`), SERVER2(`github.com`), SERVER3(`cloudflare.com`)

- Server1: twitter.com

```



```


---

### References

- https://contenthub.netacad.com/srwe-dl/6.2.3

---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
