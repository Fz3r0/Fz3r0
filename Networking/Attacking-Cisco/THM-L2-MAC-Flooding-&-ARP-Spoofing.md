
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

- < **Option2**: Step by Step Configuration >s

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
        
- **Topology of the GNS3 Lab:**

![image](https://user-images.githubusercontent.com/94720207/166299318-bd8ac75a-92b6-4847-a2f4-2433197606ab.png)
        
- **Login & Root:**

![image](https://user-images.githubusercontent.com/94720207/166289827-3062f316-1057-4f90-9dd9-ce03cf603571.png)
![image](https://user-images.githubusercontent.com/94720207/166290085-b08e918d-f03a-4f26-99e4-a415b0e373c0.png)

- **OK...let's keep going...**

---

### Network Discovery

- As mentioned previously, the host is connected to one or more additional networks. You are currently connected to the machine via SSH on Ethernet adapter eth0. The network of interest is connected with Ethernet adapter eth1.

![image](https://user-images.githubusercontent.com/94720207/166306269-e37da4c6-7e21-4cda-bec2-8d9f098635d7.png)

1. First, have a look at the adapter:

    - `ip address show eth1` or the shorthand version: `ip a s eth1`

![image](https://user-images.githubusercontent.com/94720207/166290765-190266f9-0234-40ae-ad23-2bab0a5af312.png)

2. Now I will scan the Network using NMap to discover more hosts _(It's supposed that I don't know the topology at this point, so let's just rol play...)._

    - First I will use the IPv4 Address of the target machine (The machine I'm already in!) to check for more hosts in the Network who share the same `Network ID`.
     
    - The IP that we are using have the default Subnet Mask /24 Class C and is the typical "192.168.x.x", so it's very easy to figure out the Network ID and more:
    
        - PWNED host: `192.168.12.66/24`
        
        - Network ID: `192.168.12.0`
        - SubnetMask: `255.255.255.0` 
        - CIDR      : `/24`
        - Min Host  : `192.168.0.1`
        - Max Host  : `192.168.0.254`
        - Broadcast : `192.168.0.255`
        - Wildcard  : `0.0.0.255`
        
    - Fire in the hole:      

![image](https://user-images.githubusercontent.com/94720207/166302924-fffd0a0b-13a4-4bc1-b97c-62f315f941c8.png)

- There are a total of 3 hosts in the Network:

    1. alice (192.168.12.1) MAC Address: 00:50:79:66:68:00 (Private)
    2. bob (192.168.12.2) MAC Address: 00:50:79:66:68:01 (Private)
    3. eve (192.168.12.66) _We are in this machine_
 
- I will scan each host:

1. First, I will scan "myself" `eve` (the machine where I logon with ssh & "gained" root privileges, it's supposed that we already have compromised that machine... but i don't know where i'm steping up, so!)

![image](https://user-images.githubusercontent.com/94720207/166293441-32e43138-a1b4-41b3-9bd8-667747c6dbf8.png)

- There are some virtual Cisco Devices using a GNS3 setup for a Network Lab, and we are connected via SSH to the target, think it as a "pivot" to the cisco virtual devices & hosts configured as a network, but actually everything is just simulated inside the target machine, so we can experiment with it. (Beautiful work made by the author of this room! salute to you sir).

- Notice how 2 devices are using Telnet protocol, that means all the traffic sent between both hosts will be in plain text and we can sniff it, I think the room is going that way, I will continue to scan the other 2 hosts: 

2. Host: `alice` (192.168.12.1) MAC Address: 00:50:79:66:68:00 (Private)

![image](https://user-images.githubusercontent.com/94720207/166314063-f84ab825-a76f-4de8-acd6-95d2f79a5946.png)

3. Host: `bob` (192.168.12.2) MAC Address: 00:50:79:66:68:01 (Private)

![image](https://user-images.githubusercontent.com/94720207/166314835-1c7304f1-b55c-4ed9-af1f-00cc98d2a0e4.png)




- OK we have recognized all the hosts, we did't find something useful in last 2 hosts using NMap.

- However, **now we know the physical and logical topology of the Network and we can try to sniff the new broadcast domain we have discovered.**

---

### Passive Network Sniffing

- Simply scanning those hosts won't help us gather any useful information, and you may be asking, what could a pentester do in this situation? Depending on the rules of engagement and scope, you could try sniffing traffic on this network.

- The diagram below describes your current situation where you are the Attacker and have persistent access to eve.

![image](https://user-images.githubusercontent.com/94720207/166329055-98178c61-af51-4703-89e9-374447f490f7.png)

- As you can see, from `Eve` we can "see" 2 different Broadcast Domains for 2 different LANs, 

- **I found in my old write ups of Networking something very useful for the next tasks, it talks about Layer 2 types of comunication and how devices at Layer 2 uses MAC Addresses to identify who is every host inside the LAN:

![image](https://user-images.githubusercontent.com/94720207/166326956-69553eaf-4a36-4494-9f37-9e19753ed742.png)

- _(I promise i will upload more of my networking writeups to my github, I have some mor good stuff! :D)_ 
    
    - Here's the deal! We can "hear" any broadcast sent inside the network 192.168.12.0 or if there's someone trying to connect with us `eve`: 
        
        - Imagine we are inside a "room", if someone scream everyone inside will hear that person, including us. That's `broadcast`
    
        - But! If 2 persons whisper together, even if we are in the same room we CAN NOT hear them. That's `unicast`
    
             - **At this point, we can only "hear" if someone is screaming to everyone (broadcasting) or whispering tu us (unicast)**  
             - **We can't hear if `bob` or `alice` are whispering together!

- So, we will sniff on ETH1 as shown in the diagram:

![image](https://user-images.githubusercontent.com/94720207/166329870-6b0ff09a-56d9-4a11-93c4-afa87ef0c2f1.png)

- Let's try running tcpdump on the eth1 network interface:

    - `tcpdump -i eth1`

- Optionally, for a more verbose output that prints each packet (minus its link level header) in ASCII format:

    - `tcpdump -A -i eth1`

![image](https://user-images.githubusercontent.com/94720207/166315229-f1f193e1-10d0-44a4-be99-074d354502cc.png)

- **Now, let's take a closer look at the captured packets! We can redirect them into a pcap file providing a destination file via the `-w` argument:**

    - `tcpdump -A -i eth1 -w /tmp/tcpdump.pcap`

![image](https://user-images.githubusercontent.com/94720207/166315748-7d74eb1b-cd7e-4a01-8658-c836198bb91b.png)

- Capture traffic for about a minute, then transfer the pcap to either your machine or the AttackBox to open it in `Wireshark`.

![image](https://user-images.githubusercontent.com/94720207/166316424-4a33587f-97d7-45fa-8434-972f41085fa8.png)

- I will use SCP to transfer the file but it could be done in many ways, mounting a python HTTP server is another easy way.
    
    - SCP - `scp admin@$ip_target:/tmp/Fz3r0_NetSec_PCap1.pcap .` 

![image](https://user-images.githubusercontent.com/94720207/166317931-def6931f-c8b3-488e-8f8b-7031236c330e.png)

- `Wireshark` PCAP:

    - Note: If you receive an error _"tcpdump: /tmp/tcpdump.pcap: Permission denied"_ and cannot overwrite the existing /tmp/tcpdump.pcap file, specify a new filename such as `tcpdump2.pcap`, or run `rm -f /tmp/*.pcap` then re-run tcpdump. 

![image](https://user-images.githubusercontent.com/94720207/166318386-720217fb-8bfc-4548-a5bb-1424e0c5409e.png)

- This is a very easy PCAP to read, I captured a little bit more than 1 minute and I got just 68 packets.

- Even without filters we can notice that there are only traffic betweet 2 hosts: `eve` (us / 192.168.12.66) `bob` (192.168.12.2)

- The type of packets sent are `ICMP`, that means `bob` is the `source` who is sending ping to us `eve`, we are the `destination`

- Then, `eve` send back ACKs to respond those ICMP. 

![image](https://user-images.githubusercontent.com/94720207/166323557-81003b11-b587-4267-b473-c1c2c906ff33.png)

- We can also analyze the data sent throught ICMP, we can identify is in plain text...and is nothing useful.

    - **At this point, we can't do very much with that packets, those are only ICMPs (ping) with random data "abcdefghij.... but! we have the IP & MAC address from `bob`, we can use that MAC!**   

        - **Remember that I said: "WE CAN'T HEAR IF BOB AND ALICE ARE "WHISPERING" (UNICAST) TO EACH OTHER")**
    
            - **Maybe we can! We can "disguse" as `bob` because now we have something that only that user have...`MAC address` from `bob`!!! 
    
            - **As the diagram of Layer 2 I uploaded says, MAC Address is used in Layer 2 Transmission to identify hosts, if we take that MAC, then we become `bob` for the other devices, just like Agent 47, easy! let's go:** 

---

### Sniffing while MAC Flooding

- Unfortunately, we weren't able to capture any interesting traffic so far. However, we're not going to give up this easily! So, how can we capture more network traffic? As mentioned in the room description, we could try to launch a MAC flooding attack against the L2-Switch.

    - **Beware: MAC flooding could trigger an alarm in a SOC. No, seriously, suspicious layer 2 traffic can easily be detected and reported by state-of-the-art and properly configured network devices.** 
    - Even worse, your network port could even get blocked by the network device altogether, rendering your machine locked out of the network. 
    - In case of production services running on or production traffic being routed through that network connection, **this could even result in an effective Denial-of-Service!**














---

### References

- https://tryhackme.com/room/layer2

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 

