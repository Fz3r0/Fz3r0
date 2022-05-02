
# Fz3r0 Operations  [Network Security (NetSec)]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### THM - Layer 2 MAC Flooding & ARP Spoofing 

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---
 
#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Layer 2 Attack` `Hacking` `Pentesting` `MAC Flooding` `ARP Spoofing`

---
   
### Configure on Cisco Routers FHRP (First Hop Redundancy) & HSRP (Hot Standby Router) like a Sir! 

- < **Before anything else!!!** >

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

- < **Troubleshooting** & **show commands** for this configuration >** 

### Background Knowledge about this config:

- < **Nerd Pocket-Bible about this configuration** >

---

### Layer 2 MAC Flooding & ARP Spoofing

- **Before anything else!**

    - For the sake of this room, let's assume the following:

        - While conducting a pentest, you have gained initial access to a network and escalated privileges to root on a Linux machine. 
        - During your routine OS enumeration, you realize it's a dual-homed host, meaning it is connected to two (or more) networks. 
        - Being the curious hacker you are, you decided to explore this network to see if you can move laterally.
        
        - After having established persistence, you can access the compromised host via SSH:
        
            - `ssh -o StrictHostKeyChecking=accept-new admin:Layer2$ip_target`
            
        - Note: The admin user is in the sudo group. I suggest using the root user to complete this room: `sudo su -` 
        
- **OK...let's keep going...**

![image](https://user-images.githubusercontent.com/94720207/166289827-3062f316-1057-4f90-9dd9-ce03cf603571.png)
![image](https://user-images.githubusercontent.com/94720207/166290085-b08e918d-f03a-4f26-99e4-a415b0e373c0.png)




---

### Network Discovery

- As mentioned previously, the host is connected to one or more additional networks. You are currently connected to the machine via SSH on Ethernet adapter eth0. The network of interest is connected with Ethernet adapter eth1.

1. First, have a look at the adapter:

    - `ip address show eth1` or the shorthand version: `ip a s eth1`

![image](https://user-images.githubusercontent.com/94720207/166290765-190266f9-0234-40ae-ad23-2bab0a5af312.png)

2. Now I will scan "myself" (the machine where i logon with ssh, it's supposes it's already compromised but i don't know where i'm steping up, so!)

![image](https://user-images.githubusercontent.com/94720207/166293441-32e43138-a1b4-41b3-9bd8-667747c6dbf8.png)

- There are some virtual Cisco devices using a GNS3 setup for a Network Lab, and we are connected via SSH to the target, think it as a "pivot" to the cisco virtual devices configured as a network, but actually everything is just simulated inside the target machine, so we can experiment with it. (Beautiful work made by the author of this room! salute to you sir)

3. Now I will scan the Network using NMap (This Network Scan is installed on the Linux machine I'm attacking _(I also can send to the target any other scanner or even my super python scripts for NetScans)_ .

    - First I will use the Network ID of the target machine (The machine I'm already in!) to check for more hosts in the Network who share my Network ID.
     
    - The IP have the default Subnet Mask /24 so it's very easy to figure out the Network ID:
    
        - PWNED host: `192.168.12.66/24`
        - Network ID: `192.168.12.0/24`
        
    - Fire in the hole:      

![image](https://user-images.githubusercontent.com/94720207/166294518-59320c43-ba96-4453-a44a-5cc14e80448d.png)

- There are 3 total hosts in the Network:

    1. alice (192.168.12.1) MAC Address: 00:50:79:66:68:00 (Private)
    2. bob (192.168.12.2) MAC Address: 00:50:79:66:68:01 (Private)
    3. eve (192.168.12.66) _We are in this machine_
 
- _It smells like alice and bob could be the simulated cisco devices, this room is about layer 2 so...they must be 2 switches, but let's keep rol playing..._

- 


Now, use the network enumeration tool of your choice, e.g., ping, a bash or python script, or Nmap (pre-installed) to discover other hosts in the network and answer question #3.










---

### References

- https://tryhackme.com/room/layer2

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 

