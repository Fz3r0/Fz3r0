
# Fz3r0 Operations: Network Security

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## LAN-Security: Endpoints, Hosts, Network Security Devices & Appliances

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---
 
#### Keywords: `Networking` `Routing & Switching` `CCNA` `CCNP` `Layer 2 Attack` `Hacking` `Pentesting` `MAC Flooding` `ARP Spoofing` `Try Hack Me` `Writeup`
---
   
### Index 

- < **[Before anything else!!!]()** >

- < **Task 1**: [Network Discovery]() >

- < **Task 2**: [Passive Network Sniffing](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#passive-network-sniffing) >

- < **Task 3**: [Sniffing while MAC Flooding](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#sniffing-while-mac-flooding) >

    - < **Task 3.1**: [Mitigation of MAC Flooding Attacks on Cisco Layer 2 Devices](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#mitigation-of-mac-flooding-attacks-on-cisco-layer-2-devices) >

- < **Task 4**: [MITM Man-in-the-Middle (MITM): Intro to ARP Poisoning + Sniffing](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#man-in-the-middle-intro-to-arp-spoofing) >

- < **Task 5**: [MITM Man-in-the-Middle (MITM): ARP Posoning + MAC Spoofing + Sniffing || Reverse Shell Payload + PrivEsc](/Networking/Attacking-Cisco/THM-L2-MAC-Flooding-&-ARP-Spoofing-writeup.md#man-in-the-middle-sniffing) >

    - < **Task 5.1**: [Mitigation of ARP Poisoning + MAC Spoofing Attacks on Cisco Layer 2 Devices]() >

- [< **Conclusions & Proof of Concept** >]()

---

### Before anything else!!!



    
---

### Network Attacks Today

- The news media commonly covers attacks on enterprise networks. 
- Simply search the internet for "latest network attacks" to find up-to-date information on current attacks. 
- Most likely, these attacks will involve one or more of the following:

    - Distributed Denial of Service (DDoS)
        
        - This is a coordinated attack from many devices, called zombies, with the intention of degrading or halting public access to an organization’s website and resources.

    - Data Breach
    
        - This is an attack in which an organization’s data servers or hosts are compromised to steal confidential information.

    - Malware 
    
        - This is an attack in which an organization’s hosts are infected with malicious software that cause a variety of problems. 
        - For example, ransomware such as WannaCry, shown in the figure, encrypts the data on a host and locks access to it until a ransom is paid.

![ransom](https://www.pcrisk.com/images/stories/screenshots201703/wanna-decrypt0r-gif.gif)

---

### Network Security Devices

- Various network security devices are required to protect the network perimeter from outside access. 
- These devices could include a `virtual private network (VPN) enabled router`, a `next-generation firewall (NGFW)`, and a `network access control (NAC)` device.

    - **Virtual Private Network (VPN) enabled router**  
        - A VPN-enabled router provides a secure connection to remote users across a public network and into the enterprise network. 
        - VPN services can be integrated into the firewall.
       
    - **Next-Generation Firewall (NGFW)**
        - An NGFW provides stateful packet inspection, application visibility and control, a next-generation intrusion prevention system (NGIPS), advanced malware protection (AMP), and URL filtering.

    - **Network Access Control (NAC)**
        - A NAC device includes authentication, authorization, and accounting (AAA) services. 
        - In larger enterprises, these services might be incorporated into an appliance that can manage access policies across a wide variety of users and device types. 
        - The Cisco Identity Services Engine (ISE) is an example of a NAC device.    

---

### Endpoint Protection

- LAN devices such as switches, wireless LAN controllers (WLCs), and other access point (AP) devices interconnect endpoints. Most of these devices are susceptible to the LAN-related attacks that are covered in this module.

- But many attacks can also originate from inside the network. 
- If an internal host is infiltrated, it can become a starting point for a threat actor to gain access to critical system devices, such as servers and sensitive data.

    - **Endpoints:**

        - Endpoints are hosts which commonly consist of laptops, desktops, servers, and IP phones, as well as employee-owned devices that are typically referred to as bring your own devices (BYODs). 
        - Endpoints are particularly susceptible to malware-related attacks that originate through email or web browsing. 
        
            - **These endpoints have typically used traditional host-based security features, such as antivirus/antimalware, host-based firewalls, and host-based intrusion prevention systems (HIPSs).** 
        
            - **However, today endpoints are best protected by a combination of NAC, host-based AMP software, an email security appliance (ESA), and a web security appliance (WSA).** 
            - **Advanced Malware Protection (AMP) products include endpoint solutions such as Cisco AMP for Endpoints.**

- The figure is a simple topology representing all the network security devices and endpoint solutions discussed in this module.

![image](https://user-images.githubusercontent.com/94720207/167505669-5baa271b-6ca2-4470-8a63-1c2adea48824.png)

---

### Cisco Email Security Appliance

- https://www.cisco.com/c/en/us/products/collateral/security/email-security-appliance/data-sheet-c78-729751.html

- The Cisco ESA is a device that is designed to monitor Simple Mail Transfer Protocol (SMTP). 
- The Cisco ESA is constantly updated by real-time feeds from the Cisco Talos, which detects and correlates threats and solutions by using a worldwide database monitoring system. 
- This threat intelligence data is pulled by the Cisco ESA every three to five minutes. 

    - These are some of the functions of the Cisco ESA:

        - Block known threats.
        - Remediate against stealth malware that evaded initial detection.
        - Discard emails with bad links (as shown in the figure).
        - Block access to newly infected sites.
        - Encrypt content in outgoing email to prevent data loss.

- In the figure, the Cisco ESA discards the email with bad links.

![image](https://user-images.githubusercontent.com/94720207/167508145-fa289869-6b03-4293-b01c-0e6a202a5aca.png)

--- 

### Cisco Web Security Appliance

- https://www.cisco.com/c/en/us/products/security/web-security-appliance/index.html

- The Cisco Web Security Appliance (WSA) is a mitigation technology for web-based threats. 
- It helps organizations address the challenges of securing and controlling web traffic. 
- The Cisco WSA combines advanced malware protection, application visibility and control, acceptable use policy controls, and reporting.

    - Cisco WSA provides complete control over how users access the internet. 
    - Certain features and applications, such as chat, messaging, video and audio, can be allowed, restricted with time and bandwidth limits, or blocked, according to the organization’s requirements. 
    - The WSA can perform blacklisting of URLs, URL-filtering, malware scanning, URL categorization, Web application filtering, and encryption and decryption of web traffic.

        - In the figure, an internal corporate employee uses a smartphone to attempt to connect to a known blacklisted site.

![image](https://user-images.githubusercontent.com/94720207/167508415-99aa415b-f78b-4025-9aa0-d202bedaf9cc.png)

---

### Authentication with a Local Password

- In the previous topic, you learned that a NAC device provides AAA services. 
- Many types of authentication can be performed on networking devices, and each method offers varying levels of security. 
- The simplest method of remote access authentication is to configure a login and password combination on console, vty lines, and aux ports, as shown in the vty lines in the following example. 
- This method is the easiest to implement, but it is also the weakest and least secure. 
- This method provides no accountability and the password is sent in plaintext. 
- Anyone with the password can gain entry to the device. 

    - Insecure Config for Login **(CAUTION!)**

```
R1(config)# line vty 0 4
R1(config-line)# password ci5c0
R1(config-line)# login
```

- **SSH is a more secure form of remote access:**

- It requires a username and a password, both of which are encrypted during transmission.
- The username and password can be authenticated by the local database method.
- It provides more accountability because the username is recorded when a user logs in.
- The following example illustrates SSH and local database methods of remote access.

```
R1(config)# ip domain-name fz3r0.gov
R1(config)# crypto key generate rsa general-keys modulus 2048
R1(config)# username Admin secret Str0ng3rPa55w0rd
R1(config)# ssh version 2
R1(config)# line vty 0 4
R1(config-line)# transport input ssh
R1(config-line)# login local
```

- **The local database method has some limitations:**

    - User accounts must be configured locally on each device. 
    - In a large enterprise environment with multiple routers and switches to manage, it can take time to implement and change local databases on each device.
    - The local database configuration provides no fallback authentication method. 
        - For example: 
            - What if the administrator forgets the username and password for that device? 
            - With no backup method available for authentication, password recovery becomes the only option.

    - **A better solution is to have all devices refer to the same database of usernames and passwords from a central server (RADIUS).**

--- 

### AAA Components    

(link to AAA)

---

### 802.1X

- The **IEEE 802.1X standard** is a port-based access control and authentication protocol. 
- This protocol restricts unauthorized workstations from connecting to a LAN through publicly accessible switch ports. 
- The authentication server authenticates each workstation that is connected to a switch port before making available any services offered by the switch or the LAN.

- With 802.1X port-based authentication, the devices in the network have specific roles, as shown in the figure.

![image](https://user-images.githubusercontent.com/94720207/167523122-f5297bdd-f882-41d5-9a6b-875c2f06ba0d.png)

- **Client (Supplicant)** 
    - This is a device running 802.1X-compliant client software, which is available for wired or wireless devices.

- **Switch (Authenticator)**
    - The switch acts as an intermediary between the client and the authentication server. 
    - It requests identifying information from the client, verifies that information with the authentication server, and relays a response to the client. 
    - Another device that could act as authenticator is a **wireless access point.**
- **Authentication server**
    - The server validates the identity of the client and notifies the switch or wireless access point that the client is or is not authorized to access the LAN and switch services.

---



---

### References

- https://www.cisco.com/c/en/us/products/collateral/security/email-security-appliance/data-sheet-c78-729751.html
- https://www.cisco.com/c/en/us/products/security/web-security-appliance/index.html 
 
---

> ![hecho en mexico 5](https://user-images.githubusercontent.com/94720207/166068790-fa1f243d-2db9-4810-a6e4-eb3c4ad23700.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_  
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 



