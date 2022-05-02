
# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### Configure FHRP like a Sir! ()

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

### Configure Cisco IOS DHCPv4 Relay Agent like a sir:

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

### Troubleshooting & Knowledge:

- **< Nerd Pocket-Bible about this configuration >**

- **< Troubleshooting & show commands for this configuration >**

---

### Configure Cisco IOS DHCPv4 Server like a sir

- **Before anything else!**

    - Just as the redundancy in Layer 2 _(STP/Etherchannel in switches)_ you can configure redundancy on Layer 3 _(Routers)_ with **First Hop Redundancy Protocols (FHRPs)**. 

    - For example: 
    
        - If the gateway router (to Internet) goes down. None of your hosts can send any messages outside of the immediate network _(Internet or other VLANs)_. 
         
        - It’s going to take a while to get this default gateway router operating again, cuz you have the worst luck and the potato deosn't even turn on...RMA time... 
         
        - Tickets, calls and mails from people that doesn't even know a shit about computers are complaining because "it's you fault".
         
        - But the real problem here is that devices are not magical and sometimes shit happens... so, the solution:
         
            - We need to ask the CEO to invest in at least **other Gateway Router, so we can configure it as a "mirror" or a `Redundancy of Routers`**, that's the way we can fight back against the worst luck it can exist: _"the luck of an engineer"_ and buy some time until we can replace the faulty Router. EZ!
        
- **OK...let's keep going...**

---

### Default Gateway Limitations

- If a router or router interface (that serves as a default gateway) fails, the hosts configured with that default gateway are isolated from outside networks. 

- A mechanism is needed to **provide alternate default gateways in switched networks where two or more routers are connected to the same VLANs**. That mechanism is provided by **first hop redundancy protocols (FHRPs).**

- In a switched network, each client receives only one default gateway. There is no way to use a secondary gateway, even if a second path exists to carry packets off the local segment.

### The problem with PCs (or other device) and unique IP config

- End devices are typically configured with a single IPv4 address for a default gateway.

- This address does not change when the network topology changes. (so, how it will "know his way" to the "mirror" router?!) 

- If that default gateway IPv4 address cannot be reached, the local device is unable to send packets off the local network segment, effectively disconnecting it from other networks.

    - **Even if a redundant router exists that could serve as a default gateway for that segment, there is no dynamic method by which these devices can determine the address of a new default gateway.** 

- _Note: IPv6 devices receive their default gateway address dynamically from the ICMPv6 Router Advertisement._

### Router Redundancy

- One way to prevent a single point of failure at the default gateway is to implement a `virtual router`.

- To implement this type of router redundancy, **multiple routers are configured to work together to present the illusion of a single router to the hosts on the LAN**, as shown in the figure.

- By sharing an IP address and a MAC address, two or more routers can act as a single virtual router: 

    - That's why I called as a **"mirror"**: devices "think" that the same router stills there, even if the original router fails, the PC just notice a little "cut" of couple seconds in the connection. 

![image](https://user-images.githubusercontent.com/94720207/166179203-90598e88-e046-43df-b5d6-e4500a701a0b.png)





---

### References

- https://contenthub.netacad.com/srwe-dl/1.3.6

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
