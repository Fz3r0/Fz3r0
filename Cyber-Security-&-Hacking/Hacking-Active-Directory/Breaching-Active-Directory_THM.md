
# Breaching Active Directory 

![image](https://user-images.githubusercontent.com/94720207/177055475-de773174-ab76-48d5-9038-d04979204068.png)

_This network covers techniques and tools that can be used to acquire that first set of AD credentials that can then be used to enumerate AD._

##  Introduction to AD Breaches

Active Directory (AD) is used by approximately 90% of the Global Fortune 1000 companies. If an organisation's estate uses Microsoft Windows, you are almost guaranteed to find AD. Microsoft AD is the dominant suite used to manage Windows domain networks. However, since AD is used for Identity and Access Management of the entire estate, it holds the keys to the kingdom, making it a very likely target for attackers.

For a more in-depth understanding of AD and how it works, please complete this room on AD basics first.

### Breaching Active Directory

Before we can exploit AD misconfigurations for privilege escalation, lateral movement, and goal execution, you need initial access first. You need to acquire an initial set of valid AD credentials. Due to the number of AD services and features, the attack surface for gaining an initial set of AD credentials is usually significant. In this room, we will discuss several avenues, but this is by no means an exhaustive list.

When looking for that first set of credentials, we don't focus on the permissions associated with the account; thus, even a low-privileged account would be sufficient. We are just looking for a way to authenticate to AD, allowing us to do further enumeration on AD itself.

### Learning Objectives

In this network, we will cover several methods that can be used to breach AD. This is by no means a complete list as new methods and techniques are discovered every day. However, we will  cover the following techniques to recover AD credentials in this network:

**- NTLM Authenticated Services**
**- LDAP Bind Credentials**
**- Authentication Relays**
**- Microsoft Deployment Toolkit**
**- Configuration Files**

We can use these techniques on a security assessment either by targeting systems of an organisation that are internet-facing or by implanting a rogue device on the organisation's network.

## Connecting to the Network

### AttackBox

If you are using the Web-based AttackBox, you will be connected to the network automatically if you start the AttackBox from the room's page. You can verify this by running the ping command against the IP of the THMDC.za.tryhackme.com host. We do still need to configure DNS, however. **Windows Networks use the Domain Name Service (DNS) to resolve hostnames to IPs. Throughout this network, DNS will be used for the tasks. You will have to configure DNS on the host on which you are running the VPN connection. In order to configure our DNS, we must edit the/etc/systemd/resolved.conf file. Uncomment the DNS line and add the IP of THMDC:**

```sh
#  This file is part of systemd.
#
#  systemd is free software; you can redistribute it and/or modify it
#  under the terms of the GNU Lesser General Public License as published by
#  the Free Software Foundation; either version 2.1 of the License, or
#  (at your option) any later version.
#
# Entries in this file show the compile time defaults.
# You can change settings by editing this file.
# Defaults can be restored by simply deleting this file.
#
# See resolved.conf(5) for details

[Resolve]
DNS=<THMDC IP>
#FallbackDNS=
#Domains=
#LLMNR=no
#MulticastDNS=no
#DNSSEC=no
#Cache=yes
#DNSStubListener=yes
```

- Save the file and restart the service:

```sh
[thm@thm]$ systemctl restart systemd-resolved
```

You can test that DNS is working by running:

`nslookup thmdc.za.tryhackme.com`

This should resolve to the IP of your DC.

**Note: DNS may be reset on the AttackBox roughly every 3 hours. If this occurs, you will have to restart the systemd-resolved service. If your AttackBox terminates and you continue with the room at a later stage, you will have to redo all the DNS steps.**

You should also take the time to make note of your VPN IP. Using `ifconfig` or `ip a`, make note of the 10.50.x.x or 10.51.x.x IP. This is your IP and the associated interface that you should use when performing the attacks in the tasks.

### Other Hosts

If you are going to use your own attack machine, an OpenVPN configuration file will have been generated for you once you join the room. [Go to your access page](https://tryhackme.com/access). Select 'BreachingAD' from the VPN servers (under the network tab) and download your configuration file.

![image](https://user-images.githubusercontent.com/94720207/177055562-58980c65-1847-46ef-9041-4ae8d213a6e4.png)

Use an OpenVPN client to connect. This example is shown on the Linux machine; use this guide to connect using Windows or macOS.

```sh
[thm@thm]$ sudo openvpn breachingad.ovpn
Fri Mar 11 15:06:20 2022 OpenVPN 2.4.9 x86_64-redhat-linux-gnu [SSL (OpenSSL)] [LZO] [LZ4] [EPOLL] [PKCS11] [MH/PKTINFO] [AEAD] built on Apr 19 2020
Fri Mar 11 15:06:20 2022 library versions: OpenSSL 1.1.1g FIPS  21 Apr 2020, LZO 2.08
[....]
Fri Mar 11 15:06:22 2022 /sbin/ip link set dev tun0 up mtu 1500
Fri Mar 11 15:06:22 2022 /sbin/ip addr add dev tun0 10.50.2.3/24 broadcast 10.50.2.255
Fri Mar 11 15:06:22 2022 /sbin/ip route add 10.200.4.0/24 metric 1000 via 10.50.2.1
Fri Mar 11 15:06:22 2022 WARNING: this configuration may cache passwords in memory -- use the auth-nocache option to prevent this
Fri Mar 11 15:06:22 2022 Initialization Sequence Completed
```

The message "Initialization Sequence Completed" tells you that you are now connected to the network. Return to your access page. You can verify you are connected by looking on your access page. Refresh the page, and you should see a green tick next to Connected. It will also show you your internal IP address.

![image](https://user-images.githubusercontent.com/94720207/177055617-8e64ce9e-f425-47a9-bd3e-7e8ece54d80f.png)

Note: You still have to configure DNS similar to what was shown above. It is important to note that although not used, the DC does log DNS requests. If you are using your own machine, these logs may include the hostname of your device. For example, if you run the VPN on your kali machine with the hostname of kali, this will be logged.

#### Kali

If you are using a Kali VM, Network Manager is most likely used as DNS manager. You can use GUI Menu to configure DNS:

- Network Manager -> Advanced Network Configuration -> Your Connection -> IPv4 Settings
- Set your DNS IP here to the IP for THMDC in the network diagram above
- Add another DNS such as 1.1.1.1 or similar to ensure you still have internet access
- Run `sudo systemctl restart NetworkManager` and test your DNS similar to the steps above.

## Pre-Config Fz3r0

- MKDIR:

    - ![image](https://user-images.githubusercontent.com/94720207/177063864-6199fa2e-0829-49d0-b797-1d0bec787e9b.png)

- VPN: `sudo openvpn /home/kali/Documents/5_____VPN_THM/fz3r0.carlos-breachingad.ovpn`

    - ![image](https://user-images.githubusercontent.com/94720207/177064365-24c874ba-10ae-4f7a-a6ca-fa77e882f079.png)

- DNS Config:

    - Network Manager -> Advanced Network Configuration -> Your Connection -> IPv4 Settings
    - Set your DNS IP here to the IP for THMDC in the network diagram above
    - Add another DNS such as 1.1.1.1 or similar to ensure you still have internet access
    - Run `sudo systemctl restart NetworkManager` and test your DNS similar to the steps above.

    - ![image](https://user-images.githubusercontent.com/94720207/177064107-394be2b9-dbcd-45bf-afdf-f0c0b1c8f014.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/177064206-5901b0b4-7970-452b-a935-e3c460da4158.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/177064436-c316403a-84d8-4f12-9383-c6e7cd0bf85a.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/177064638-f21bd4b8-124d-4366-b328-1619cd1c7e1f.png)
 
## OSINT and Phishing

_Two popular methods for gaining access to that first set of AD credentials is Open Source Intelligence (OSINT) and Phishing. We will only briefly mention the two methods here, as they are already covered more in-depth in other rooms._

### OSINT

OSINT is used to discover information that has been publicly disclosed. In terms of AD credentials, this can happen for several reasons, such as:

- Users who ask questions on public forums such as Stack Overflow but disclose sensitive information such as their credentials in the question.
 
- Developers that upload scripts to services such as Github with credentials hardcoded.
 
- Credentials being disclosed in past breaches since employees used their work accounts to sign up for other external websites. Websites such as HaveIBeenPwned and DeHashed provide excellent platforms to determine if someone's information, such as work email, was ever involved in a publicly known data breach.

By using OSINT techniques, it may be possible to recover publicly disclosed credentials. If we are lucky enough to find credentials, we will still need to find a way to test whether they are valid or not since OSINT information can be outdated. In Task 3, we will talk about NTLM Authenticated Services, which may provide an excellent avenue to test credentials to see if they are still valid.

A detailed room on Red Team OSINT can be found [here](https://tryhackme.com/room/redteamrecon).

### PHISHING

Phishing is another excellent method to breach AD. Phishing usually entices users to either provide their credentials on a malicious web page or ask them to run a specific application that would install a Remote Access Trojan (RAT) in the background. This is a prevalent method since the RAT would execute in the user's context, immediately allowing you to impersonate that user's AD account. This is why phishing is such a big topic for both Red and Blue teams.

A detailed room on phishing can be found [here](https://tryhackme.com/module/phishing).

## NTLM and NetNTLM

![image](https://user-images.githubusercontent.com/94720207/177065933-a87d7184-65a5-4db6-af80-d83152e19ab3.png)

New Technology LAN Manager (NTLM) is the suite of security protocols used to authenticate users' identities in AD. NTLM can be used for authentication by using a challenge-response-based scheme called NetNTLM. This authentication mechanism is heavily used by the services on a network. However, services that use NetNTLM can also be exposed to the internet. The following are some of the popular examples:

- Internally-hosted Exchange (Mail) servers that expose an Outlook Web App (OWA) login portal.
- Remote Desktop Protocol (RDP) service of a server being exposed to the internet.
- Exposed VPN endpoints that were integrated with AD.
- Web applications that are internet-facing and make use of NetNTLM.

NetNTLM, also often referred to as Windows Authentication or just NTLM Authentication, allows the application to play the role of a middle man between the client and AD. All authentication material is forwarded to a Domain Controller in the form of a challenge, and if completed successfully, the application will authenticate the user.

This means that the application is authenticating on behalf of the user and not authenticating the user directly on the application itself. This prevents the application from storing AD credentials, which should only be stored on a Domain Controller. This process is shown in the diagram below:

![image](https://user-images.githubusercontent.com/94720207/177066003-bab1e498-f3cc-48e1-ada3-69ca9170a026.png)




---

### References

- https://tryhackme.com/room/breachingad
- https://tryhackme.com/room/activedirectorybasics
- https://tryhackme.com/room/redteamrecon
- https://tryhackme.com/module/phishing





