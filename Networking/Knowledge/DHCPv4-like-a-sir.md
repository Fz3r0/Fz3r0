
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### DHCPv4 like a Sir (Dynamic Host Configuration Protocol v4)

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `DHCPv4`

---
   
### Configure Cisco IOS DHCPv4 Server like a sir:

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

### Configure Cisco IOS DHCPv4 Client like a sir:

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

### Troubleshooting & Knowledge:

- **< Nerd Pocket-Bible about this configuration >**

- **< Troubleshooting & show commands for this configuration >**

---

### Configure Cisco IOS DHCPv4 Server like a sir

### Straight to the point:

- Cisco Router IOS:

- Sintax:

```

R1(config)# ip dhcp excluded-address 192.168.1.1 192.168.1.100
R1(config)# ip dhcp excluded-address 192.168.1.254
R1(config)# ip dhcp pool fz3r0_DHCP_pool_1
R1(dhcp-config)# network 192.168.1.0 255.255.255.00
R1(dhcp-config)# default-router 192.168.1.254
R1(dhcp-config)# dns-server 1.1.1.1
R1(dhcp-config)# domain-name fz3r0_domain.gov
R1(dhcp-config)# end
R1#

```

- Copy

```
enable
configure terminal
!
!
ip dhcp excluded-address 192.168.1.1 192.168.1.100
ip dhcp excluded-address 192.168.1.254
!
ip dhcp pool fz3r0_DHCP_pool_1
!
network 192.168.1.0 255.255.255.0
default-router 192.168.1.254
dns-server 1.1.1.1
domain-name fz3r0_domain.gov
!
!
end
exit
!
!

```

Table:

| Task	                                    | IOS Command                                      |
|:------------------------------------------:|:-------------------------------------------------|
| Define the address pool                    | network network-number [mask | / prefix-length]  |
| Define the default router or gateway.	   | default-router address [ address2….address8]     |
| Define a DNS server.	                     | dns-server address [ address2…address8]          |
| Define the domain name.	                  | domain-name domain                               |
| Define the duration of the DHCP lease.	   | lease {days [hours [ minutes]] | infinite}       |
| Define the NetBIOS WINS server.	         | netbios-name-server address [ address2…address8] |

---

- Enable & Disable DHCP:

```

service dhcp

no service dhcp

```

---

### Configure Cisco IOS DHCPv4 Server like a sir

### Step by Step:

- Steps to follow:

1. **Exclude IPv4 addresses.**
2. **Define a DHCPv4 pool name.**
3. **Configure the DHCPv4 pool.**

- Config Step by Step:

1. **Exclude IPv4 addresses:**
    - Exclude all the IPs used by other devices on the network
    - Select a range (or only 1 IP) that you want to exclude _(for example a pool of 20 IPs from 1.1.1.10-1.1.1.20)_

- Sintax:

```

Router(config)# ip dhcp excluded-address low-address [high-address]

```

- Copy:

```

enable
configure terminal
!
ip dhcp excluded-address 192.168.1.1 192.168.1.100
!
ip dhcp excluded-address 192.168.1.254
!
exit
!

```

2. **Define a DHCPv4 pool name.**

    - Configuring a DHCPv4 server involves defining a pool of addresses to assign.

    - As shown in the example, the ip dhcp pool pool-name command creates a pool with the specified name and puts the router in DHCPv4 configuration mode, which is identified by the prompt Router(dhcp-config)#.

- Sintax:

```

Router(config)# ip dhcp pool pool-name
Router(dhcp-config)# 

```

- Copy:

```

enable
configure terminal
!
ip dhcp pool pool-name
!
exit
!

```

3. **Configure the DHCPv4 Pool**

- **The address pool and default gateway router must be configured:**
    
    - Use the `network` statement to define the range of available addresses.
    - Use the `default-router` command to define the default gateway router. 

| Task	                                    | IOS Command                                      |
|:------------------------------------------:|:-------------------------------------------------|
| Define the address pool                    | network network-number [mask | / prefix-length]  |
| Define the default router or gateway.	   | default-router address [ address2….address8]     |
| Define a DNS server.	                     | dns-server address [ address2…address8]          |
| Define the domain name.	                  | domain-name domain                               |
| Define the duration of the DHCP lease.	   | lease {days [hours [ minutes]] | infinite}       |
| Define the NetBIOS WINS server.	         | netbios-name-server address [ address2…address8] |

- Sintax:

```

R1(dhcp-config)# network 192.168.1.0 255.255.255.00
R1(dhcp-config)# default-router 192.168.1.254
R1(dhcp-config)# dns-server 1.1.1.1
R1(dhcp-config)# domain-name fz3r0_domain.gov
R1(dhcp-config)# end
R1#

```

- Copy:

```

enable
configure terminal
!
network 192.168.1.0 255.255.255.0
default-router 192.168.1.254
dns-server 1.1.1.1
domain-name fz3r0_domain.gov
!
end
exit
!
!

```

- Enable & Disable DHCP:

```

service dhcp

no service dhcp

```

---

### Configure Cisco IOS DHCPv4 Client like a sir

### Straight to the point Configuration:

1. **Cisco Router as a DHCP Client:**

- Syntax:

```

SOHO(config)# interface G0/0/1
SOHO(config-if)# ip address dhcp
SOHO(config-if)# no shutdown

Sep 12 10:01:25.773: %DHCP-6-ADDRESS_ASSIGN: Interface GigabitEthernet0/0/1 assigned DHCP address 209.165.201.12, mask 255.255.255.224, hostname SOHO

SOHO# show ip interface g0/0/1

GigabitEthernet0/0/1 is up, line protocol is up
  Internet address is 209.165.201.12/27
  Broadcast address is 255.255.255.255
  Address determined by DHCP
(output omitted)

```

- copy:

```

enable
configure terminal
!
interface G0/0/1
ip address dhcp
no shutdown
!
!
show ip interface g0/0/1
!
!
end
exit
!
!

```

---

### Cisco Router as a DHCP Client step by step:

1. To configure an Ethernet interface as a DHCP client, use the `ip address dhcp` interface configuration mode command.

- Syntax:

```

SOHO(config)# interface G0/0/1
SOHO(config-if)# ip address dhcp
SOHO(config-if)# no shutdown

Sep 12 10:01:25.773: %DHCP-6-ADDRESS_ASSIGN: Interface GigabitEthernet0/0/1 assigned DHCP address 209.165.201.12, mask 255.255.255.224, hostname SOHO

```

- Copy:

```

enable
configure terminal
!
interface G0/0/1
ip address dhcp
no shutdown
!
!

```

2. The show ip interface g0/0/1 command confirms that the interface is up and that the address was allocated by a DHCPv4 server.

- Syntax:

```

SOHO# show ip interface g0/0/1

GigabitEthernet0/0/1 is up, line protocol is up  <<<------| Up! :D 
  Internet address is 209.165.201.12/27
  Broadcast address is 255.255.255.255
  Address determined by DHCP
(output omitted)

``` 

- Copy:

```

show ip interface g0/0/1
!

```

---

### Home Router as a DHCPv4 Client

- It depends on each device, but usually located under `configuration` `DHCP` `set IP` `Dynamic`

- For example on Packet Tracer:

![image](https://user-images.githubusercontent.com/94720207/165884711-454346fa-3438-48d7-8d05-9c2cbacb5c0e.png)

---

### DHCPv4 Concepts

### DHCPv4 Server and Client

- DHCPv4 assigns IPv4 addresses and other network configuration information dynamically. 

- Because desktop clients typically make up the bulk of network nodes, DHCPv4 is an extremely useful and timesaving tool for network administrators.

- **DHCPv4 Server:**

    - A dedicated DHCPv4 server is scalable and relatively easy to manage. _(Windows Server, Thousand of linux DHCP servers, etc)_

    - **However, in a small branch or SOHO location, a Cisco router can be configured to provide DHCPv4 services without the need for a dedicated server. Cisco IOS software supports an optional, full-featured DHCPv4 server.**

    - The DHCPv4 server dynamically assigns, or leases, an IPv4 address from a pool of addresses for a limited period of time chosen by the server, or until the client no longer needs the address.
 
- **DHCPv4 Client:**

    - Could be any device with DHCP cappabilities like PCs, smartphones, IoT, etc.

    - Clients lease the information from the server for an administratively defined period. 

    - The lease is typically anywhere from 24 hours to a week or more. 

    - When the lease expires, the client must ask for another address, although the client is typically reassigned the same address.

### DHCPv4 Operation

- DHCPv4 works in a client/server mode: 

1. Client communicates with a DHCPv4 server 
2. Server assigns or leases an IPv4 address to that client. 
3. The Client connects to the network with that leased IPv4 address until the lease expires. 
    - The client must contact the DHCP server periodically to extend the lease. 
    - This lease mechanism ensures that clients that move or power off do not keep addresses that they no longer need. 
4. When a lease expires, the DHCP server returns the address to the pool where it can be reallocated as necessary.    

### Steps to Obtain a Lease

- When the client boots (or otherwise wants to join a network), it begins a four-step process to obtain a lease _(sending messages throught network)_:

1. DHCP **Discover** `DHCPDISCOVER`
    - **The client starts the process** using a broadcast DHCPDISCOVER message with its own MAC address to discover available DHCPv4 servers. 
    - The purpose of the DHCPDISCOVER message is to find DHCPv4 servers on the network.

2. DHCP **Offer** `DHCPOFFER`
    - When the DHCPv4 server receives a `DHCPDISCOVER` message, it reserves an available IPv4 address to lease to the client.
    - The server also creates an **ARP entry** consisting of the MAC address of the requesting client and the leased IPv4 address of the client. 
    - The DHCPv4 server sends the binding `DHCPOFFER` message to the requesting client.
3. DHCP **Request** `DHCPREQUEST`
    - When the client receives the `DHCPOFFER` from the server, it sends back a `DHCPREQUEST` message.
    - **This message is used for both lease origination and lease renewal. 
    - When used for lease origination, the DHCPREQUEST serves as a binding acceptance notice to the selected server for the parameters it has offered and an implicit decline to any other servers that may have provided the client a binding offer.
4. DHCP **Acknowledgment** `DHCPACK`
    - On receiving the DHCPREQUEST message, the server may verify the lease information with an ICMP ping to that address to ensure it is not being used already, it will create a new ARP entry for the client lease, and reply with a DHCPACK message.

![image](https://user-images.githubusercontent.com/94720207/165873846-78a2616b-aa7f-4c46-bb9b-218204a79534.png)

### Steps to Renew a Lease

- **Prior to lease expiration**, the client begins a two-step process to renew the lease with the DHCPv4 server

1. DHCP Request (DHCPREQUEST)
    - Before the lease expires, the client sends a `DHCPREQUEST` message directly to the DHCPv4 server that originally offered the IPv4 address. 
    - If a `DHCPACK` is not received within a specified amount of time, the client broadcasts another `DHCPREQUEST` so that one of the other DHCPv4 servers can extend the lease.

2. DHCP Acknowledgment (DHCPACK)
    - On receiving the `DHCPREQUEST` message, the server verifies the lease information by returning a `DHCPACK`.

![image](https://user-images.githubusercontent.com/94720207/165874138-d6c33bdd-6627-480a-875c-0dfe605dbbbb.png)

Note: These messages (primarily the DHCPOFFER and DHCPACK) can be sent as unicast or broadcast according to IETF RFC 2131.

---

### Troubleshooting commands

```

| Command	                      | Description                                                                                          |
|:-----------------------------------:|:----------------------------------------------------------------------------------------------------:|
| show running-config | section dhcp  | Displays the DHCPv4 commands configured on the router.                                               |
| show ip dhcp binding                | Displays a list of all IPv4 address to MAC address bindings provided by the DHCPv4 service.          | 
| show ip dhcp server statistics      | Displays count information regarding the number of DHCPv4 messages that have been sent and received. |

```

---

### References

- https://contenthub.netacad.com/srwe-dl/6.2.3

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
