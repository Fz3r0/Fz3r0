
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
    - Cisco Router as a DHCP Server
    - Generic _(Windows/Linux)_ Server as a DHCP Server
    - Home Router _(WiFi Modem)_ as a DHCP Server

3. Configure DHCP Relay
    - Cisco Routers as a DHCP Relay Agent

5. Configure DHCP Clients:
    - Cisco Router as a DHCP Client
    - Home Router _(WiFi Modem)_ as a DHCP Client
    - Generic DHCP Clients as PCs, Laptops, Smartphones, Printers, Tablets

---

### Scenario

1. Configuring a Cisco router as a DHCP server to provide dynamic allocation of addresses to clients on the network. 
2. Configure the **edge router as a DHCP client** so that it receives an IP address from the ISP network. 
3. Since the server is centralized, configure the two LAN routers to relay DHCP traffic between the LANs and the router that is serving as the DHCP server.

---

### Configuration

---

### R2 - Router 2 - `DHCP SERVER` 

1. Configure **R2** to **exclude the IPs** you need to take out
2. Create 2 different pools for 2 different VLANs (VLAN10 & VLAN20)
3. Configure the DHCP Pools including:
    - Network Address
    - Default Gateway
    - DNS Server IP
4. R2 needs to be configured to receive addressing from the ISP.

- **Note: R2 Will be the DHCP Server for the 2 different networks _(VLAN10 & VLAN20)_, and at the same time R2 will be recieving DHCP from the ISP Router _(Internet Cloud)_.**

```

enable
configure terminal
!
!
hostname < R2 - DHCP Server for VLAN-10 & VLAN-20 >
domain-name fz3r0_domain.DHCP_labs
!
!
!
ip dhcp excluded-address 192.168.10.1 192.168.10.100
ip dhcp excluded-address 192.168.10.200 192.168.10.254
ip dhcp excluded-address 192.168.10.99
ip dhcp excluded-address 192.168.10.66
ip dhcp excluded-address 192.168.10.69
!
ip dhcp pool fz3r0_DHCP_Pool1_<< R1-VLAN-20 >>
!
network 192.168.10.0 255.255.255.0
default-router 192.168.10.254
dns-server 1.1.1.1
!
!
!
ip dhcp excluded-address 192.168.20.1 192.168.20.100
ip dhcp excluded-address 192.168.20.200 192.168.20.254
ip dhcp excluded-address 192.168.20.99
ip dhcp excluded-address 192.168.20.66
ip dhcp excluded-address 192.168.20.69
!
ip dhcp pool fz3r0_DHCP_Pool2_<< R3-VLAN-30 >>
!
network 192.168.20.0 255.255.255.0
default-router 192.168.20.254
dns-server 1.1.1.1
!
!
!
interface Gi 0/1
ip address dhcp
no shut down
exit
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




---

### References

- https://contenthub.netacad.com/srwe-dl/6.2.3

---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
