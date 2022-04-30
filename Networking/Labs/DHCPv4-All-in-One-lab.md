
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
!
!
!
ip dhcp excluded-address 192.168.30.1 192.168.30.100
ip dhcp excluded-address 192.168.30.151 192.168.30.254
ip dhcp excluded-address 192.168.30.113
ip dhcp excluded-address 192.168.30.114
ip dhcp excluded-address 192.168.30.115
!
ip dhcp pool fz3r0_DHCP_Pool2_<<for:R3-VLAN-30___PUBLIC_DNS>>
!
network 192.168.30.0 255.255.255.0
default-router 192.168.30.254
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
ip helper-address 10.1.1.2
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
ip address 192.168.30.254 255.255.255.0
ip helper-address 10.2.2.2
duplex auto
speed auto
no shutdown
!
!

```

---

### INTERNET WWW > SERVER1(`twitter.com`), SERVER2(`github.com`), SERVER3(`cloudflare.com`)

- Server1: twitter.com

```



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

### References

- https://contenthub.netacad.com/srwe-dl/6.2.3

---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
