
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

- < **Before anything else!!!** >

- < **Section 1**: Network Discovery >

- < **Section 1**: Network Discovery >

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
        
            - `ssh -o StrictHostKeyChecking=accept-new admin:Layer2@$ip_target`
            
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

![image](https://user-images.githubusercontent.com/94720207/166345518-a54c21ea-fffe-4ccf-a5d5-dc46101008fc.png)

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

![image](https://user-images.githubusercontent.com/94720207/166348275-9e96d11c-7381-45dd-ba56-0a29071ba3d0.png)

- As you can see, from `Eve` we can "see" 2 different Broadcast Domains for 2 different LANs, 

### I've found in my old write ups of Networking something very useful for the next tasks and this room in general, it talks about Layer 2 types of comunication and how devices like Switches and Hubs at Layer 2 creates Broadcast and Collision Domains, also how Layer 2 devices uses MAC Addresses to identify who is every host inside the LAN:

![image](https://user-images.githubusercontent.com/94720207/166326956-69553eaf-4a36-4494-9f37-9e19753ed742.png)

![image](https://user-images.githubusercontent.com/94720207/166402151-e29d22e6-c954-4e1d-a012-41c016e35b0c.png)

- _(I promise that I will upload more of my networking writeups to my github, I have some good stuff! :D)_ 
    
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

- However, if we're successful, the switch will resort to fail-open mode and temporarily operate similarly to a network hub – forwarding all received frames to every connected port (aside from the port the traffic originated from). 

- This would allow an adversary or pentester to sniff the network traffic between other hosts that normally wouldn't be received by their device if the switch were functioning properly.

    - **Considering such an attack vector is only recommended when you have reasons to believe that:**

        1. It is in fact a switched network (and not a virtual bridge) AND
        
        2. The switch might be a consumer or prosumer (**unmanaged**) switch OR:
            
        3. **The network admins haven't configured mitigations such as Dynamic ARP Inspection (DAI) for instance AND ARP and MAC spoofing attacks are explicitly permitted in the rules of engagement.**
            
            - **THAT'S WHY WE NEED TO CONFIGURE `DYNAMIC ARP INSPECTION (DAI)` IN OUR `CISCO SWITCHES`, JUST AS WE SAW IN CISCO CCNAV7 MODULE-2 SECURITY "LAYER 2 ATTACKS"**
            
            - I'm making a guide to achieve Best Practices & Security to our Cisco Layer 2 devices [here](https://github.com/Fz3r0/Fz3r0#-networking--1) _(I still need to update the info, meanwhile just google for Cisco DAI on IOS)_

- _- "Anyhow, let's assume you've met the well-thought decision to give it a try."_

    - For better usability, open a second SSH session. This way, you can leave the tcpdump process running in the foreground on the first SSH session:
    
        - `tcpdump -A -i eth1 -w /tmp/tcpdump2.pcap`
        
![image](https://user-images.githubusercontent.com/94720207/166393591-bb42bbb8-d3c7-4a31-8e05-719c733183d5.png)
        
- Now, on the second SSH session, buckle up and let macof run against the interface to start flooding the switch:

    - `macof -i eth1`
    
    - After around 30 seconds, stop both macof and tcpdump `(Ctrl+C)`. 

![image](https://user-images.githubusercontent.com/94720207/166393923-496a224b-2c4d-4557-b3f8-dfd34ae47489.png)

![image](https://user-images.githubusercontent.com/94720207/166394716-9f12b0d8-f06f-4c92-9a9b-afa4ea454ab8.png)

- As in the previous task, transfer the pcap to your machine _(kali/AttackBox)_ and take a look.

    - `scp admin@$ip_target:/tmp/tcpdump2.pcap .` 

![image](https://user-images.githubusercontent.com/94720207/166394524-aa7e5cad-0ff3-449b-84e1-7e4e5b27d42b.png)

- Note: If it didn't work, try to capture for 30 seconds, again (while macof is running).

    - If it still won't work, give it one last try with a capture duration of one minute.
    - As the measure of last resort, try using ettercap (introduced in the following tasks) with the `rand_flood` plugin:

        - `ettercap -T -i eth1 -P rand_flood -q -w /tmp/tcpdump3.pcap` _(Quit with q)_

- It worked for me with `tcpdump` + `macof` at first try without problems...just try to start and end both commands at same time, because `macof` will spam MACs and we are trying to trick the Network and the Switch to show us all his traffic, **`just like a hub would do`**, we need to capture at same time while we are performing the `tcpdump`. 

    - Anyways, here's how is performed with `ettercap`:

![image](https://user-images.githubusercontent.com/94720207/166396579-a7ff04b2-0236-4eea-9447-767089ab5602.png)

- You can send the file with SCP. Now, let's analize that PCAP:

    - This PCAP is HUGE! we have half million packets 😂 that's why I used the next filter:
    
        - `ip.addr == 192.168.12.1 || ip.addr == 192.168.12.2`
    
    - I'm filtering just the traffic containing IPs from `bob` (192.168.12.2) and `alice` (192.168.12.1). And maybe, we can find a "conversation" between both of them:
     
![image](https://user-images.githubusercontent.com/94720207/166396144-f37ca138-1395-46cf-aa7e-b8f653ca102d.png)

- **That's how we just performed a MAC flooding attack while sniffing the Network, and we have "listened" the "whispering" (`unicast`) betweeen `bob` and `alice`.**

- Just for a better idea this is somehow what it just happened:

![image](https://user-images.githubusercontent.com/94720207/166399966-e3b6c77b-473c-44ee-bb1d-70d767817bee.png)

- Maybe is not that "crazy" as those lines, but you can understand better the attack now! [The reality is that we just made the `switch` "go crazy" and start working as a `hub` due to evermwhelming spam of MAC address inside the CAM table of the switch](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#ive-found-in-my-old-write-ups-of-networking-something-very-useful-for-the-next-tasks-and-this-room-in-general-it-talks-about-layer-2-types-of-comunication-and-how-devices-like-switches-and-hubs-at-layer-2-creates-broadcast-and-collision-domains-also-how-layer-2-devices-uses-mac-addresses-to-identify-who-is-every-host-inside-the-lan)

- **Mitigation** Configuring `Dynamic ARP Inspection (DAI)` on our Layer 2 Devices, for example Cisco Switches.**
    - ** Port Security is also another option configuring out switchport to only hold a max of 10 MAC on the CAM table**
    
    - We can also use more defensive techniques but in this case I'm just remarking the configs of best practices and security on our Layer 2 Devices.

--- 

### Man-in-the-Middle: Intro to ARP Spoofing

- As you may have noticed, MAC Flooding can be considered a real "noisy" technique _**(making the switch go crazy and doing a DoS like attack is not so ninja)**_. 

- In order to reduce the risk of detection and DoS we will leave `macof` aside for now. 

- Instead, we are going to perform so-called `ARP cache poisoning` attacks against `Alice` and `Bob`, in an attempt to become a **fully-fledged `Man-in-the-Middle (MITM)**`.

- For a deeper understanding of this technique, [read the Wikipedia article on ARP spoofing](https://en.wikipedia.org/wiki/ARP_spoofing)

    – _"an attacker sends (spoofed) ARP messages […] to associate the attacker's MAC address with the IP address of another host […] causing any traffic meant for that IP address to be sent to the attacker instead. ARP spoofing may allow an attacker to intercept data frames on a network, modify the traffic, or stop all traffic. Often the attack is used as an opening for other attacks, such as denial of service, man in the middle, or session hijacking attacks." - Wikipedia - ARP spoofing_

![image](https://user-images.githubusercontent.com/94720207/166403377-49c6012d-6689-4763-8419-cfdd08a86387.png)
_https://commons.wikimedia.org/wiki/File:ARP_Spfing.svg_

- There are, however, measures and controls available to detect and prevent such attacks. 
    
    - **We can configure our Cisco Layer 2 Devices with `ARP Snooping`, again, just as we saw in CCNA v7 Module 2 - Security - Layer 2 Attacks.**

- In the current scenario, both hosts are running an ARP implementation that takes pains to validate incoming ARP replies. Without further ado, we are using ettercap to launch an ARP Spoofing attack against Alice and Bob and see how they react:

    - `ettercap -T -i eth1 -M arp` 

![image](https://user-images.githubusercontent.com/94720207/166403965-3e7f755f-748b-4d58-b047-aa658fbf2f6f.png)

![image](https://user-images.githubusercontent.com/94720207/166404207-8e0943c2-d525-4be7-b8b2-edfd0c94a2ab.png)

- Just to dig a little bit more about this command, let's try another MITM attack instead of `ARP` 

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

- Since we already have the IPs and MACs from `bob`, `alice` & `eve` we can try to perform an ICMP MITM attack:

![image](https://user-images.githubusercontent.com/94720207/166405349-c5ff93b3-ea39-43e6-af4d-730ea9353b78.png)

- Ethernet II Frame:

    - Src: `alice` MAC: `00:50:79:66:68:00` IP: `192.168.12.1`
    - Dst: `bob` MAC: `00:50:79:66:68:01` IP: `192.168.12.2`

- `ettercap` command:
    
    - Example: `icmp (MAC/IP)`
    
    - `ettercap -T -i eth1 -M icmp:00:50:79:66:68:00/192.168.12.1` 

![image](https://user-images.githubusercontent.com/94720207/166406256-b44e94e5-6e13-4c66-a901-33d32a91311b.png)

![image](https://user-images.githubusercontent.com/94720207/166407313-56badb53-d7b4-452f-b564-bf91a30af062.png)
  
<!--

- Surprise! We can "hear" the "whisper" (unicast) coming from `bob` with destination `alice`, that's because we are **spoofing** `alice` MAC

- But how it works? Easy! because the switch is not protected with ARP snooping, the switch don't realize that the same MAC address is comming from different switchports and now when the switch send traffic to `alice` MAC from `bob`, we can hear it!
    
    - Just as the last task, but this time was not a "crazyness" it was more like this: 

-->

---

















---

### References

- https://tryhackme.com/room/layer2

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 

