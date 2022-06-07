

# Fz3r0 Operations  [Networking]

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## Configure Remote Site Wireless like a Sir! 

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `Wireless` `WLAN` `CCNA` `CCNP` 
  
## Index

- < **Before anything else!!!** >

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

- < **Troubleshooting** & **show commands** for this configuration >** 

### Background Knowledge about this config:

- < **Nerd Pocket-Bible about this configuration** >

## Remote Site Wireless Configuration

### The Wireless Router

- Remote workers, small branch offices, and home networks often use a **small office and home router**. 

- These routers are sometimes called an integrated router because they **typically include a switch for wired clients, a port for an internet connection (sometimes labeled “WAN”), and wireless components for wireless client access**. For example `Cisco Meraki MX64W`

    - For the rest of this module, **small office and home routers are referred to as wireless routers.**

- The next figure shows a topology depicting the physical connection of a wired laptop to the wireless router, which is then connected to a cable or DSL modem for internet connectivity.

    - ![image](https://user-images.githubusercontent.com/94720207/172261039-79988ce3-8fcc-4a36-9ac3-f90f05207ba1.png)

- These wireless routers typically provide WLAN security, DHCP services, integrated Name Address Translation (NAT), quality of service (QoS), as well as a variety of other features. (The feature set will vary based on the router model.)

    - **NOTE:** Cable or DSL modem configuration is usually done by the **service provider’s representative either on-site or remotely through a walkthrough with you on the phone**. 
    - If you buy the modem, it will come with documentation for how to connect it to your service provider which will most likely include contacting your service provider for more information.
    - For example...Telmex send a technician to do all the job for you ;)

---

### Log in to the Wireless Router

- Most wireless routers are ready for service out of the box. 

- They are preconfigured to be connected to the network and provide services. 

    - For example, the wireless router uses DHCP to automatically provide addressing information to connected devices. 
    
    - However, **wireless router default IP addresses, usernames, and passwords can easily be found on the internet.**
    
        - Just enter the search phrase `default wireless router IP address` or `default wireless router passwords` to see a listing of many websites that provide this information. 
    
        - For example, username and password for the wireless router in the figure is `admin`. 
        - **Therefore, your first priority should be to change these defaults for security reasons.**

1. To gain access to the wireless router’s configuration GUI, open a web browser.

2. In the address field, enter the default IP address for your wireless router. 
    
    - The default IP address can be found in the documentation that came with the wireless router or you can search the internet. 
    
    - The figure shows the IPv4 address `192.168.0.1`, which is a common default for many manufacturers. 

4. A security window prompts for authorization to access the router GUI. 
    
    - The word `admin` is commonly used as the default `username` and `password`. 
    
    - Again, check your wireless router’s documentation or search the internet.
    
    - ![image](https://user-images.githubusercontent.com/94720207/172261828-d574e5d6-83d3-4615-ae1f-9e7443c5609f.png)

---

### Basic Network Setup PT.1

- **Basic network setup includes the following steps:**

    - Note: For this example I will using the next Router model of Cisco Packet Tracer_
    
        - ![image](https://user-images.githubusercontent.com/94720207/172262877-d2aea6cd-ae0d-477f-9450-ec4e7356cac4.png)
 
1. Log in to the router from a web browser.

    - ![image](https://user-images.githubusercontent.com/94720207/172263529-a2e63bd1-1fec-4729-9426-11e73a95df85.png)

    
    - ![image](https://user-images.githubusercontent.com/94720207/172263208-6508f04a-b483-4d3a-9ad6-586e742f38ad.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/172263323-bad13f98-0e28-4829-851b-79056d879ba6.png)
 
        - After logging in, a GUI opens. 
    
    - ![image](https://user-images.githubusercontent.com/94720207/172263351-66d8c866-2029-4f7a-a503-7eb8f8bf31dd.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/172263723-9a1e2bd9-586f-4e2b-86ef-710dea79d132.png)
      
    - The GUI will have tabs or menus to help you navigate to various router configuration tasks. 

    - It is often necessary to save the settings changed in one window before proceeding to another window. 
    
    - At this point, it is a best practice to make changes to the default settings.

2. Change the default administrative password.

    - To change the default login password, find the administration portion of the router’s GUI. 
    
    - In this example, the Administration tab was selected. This is where the router password can be changed. 
    
    - On some devices, such as the one in the example, you can only change the password. The username remains admin or whatever the default username is for the router you are configuring.
    
    - ![image](https://user-images.githubusercontent.com/94720207/172264053-5e568d83-c1bd-4fe5-8184-f27a0db09c42.png)
 
3. Log in with the new administrative password.

    - ![image](https://user-images.githubusercontent.com/94720207/172264250-9bc80f69-3553-47c7-9036-2181bde3f4cf.png)

    - ![image](https://user-images.githubusercontent.com/94720207/172264285-8828e62b-88ac-4b56-9025-98e62f908955.png)

4. Change the default DHCP IPv4 addresses.

    - It is a best practice to use private IPv4 addressing inside your network. 
    
    - The IPv4 address `192.168.1.254` is used in the example but it could be **any private IPv4 address you choose.**
    
    - ![image](https://user-images.githubusercontent.com/94720207/172264550-7aa585c1-087d-4737-be67-687e4b14a421.png)
 
5. Renew the IP address.

    - When you click save, you will temporarily lose access to the wireless router. 
    
    - If the IP of the PC is set manual you need to change it manually again to the subnet used bu the router:
    
        - ![image](https://user-images.githubusercontent.com/94720207/172264766-5d7ba7d9-5d91-4031-b397-a4dd4dab948b.png)
     
    - If using DHCP, open a command window and renew your IP address with the `ipconfig /renew` command.
 
         - ![image](https://user-images.githubusercontent.com/94720207/172264844-a7a5c4ff-2c54-4c0f-9d66-882609096c79.png)
         
         - ![image](https://user-images.githubusercontent.com/94720207/172265474-d64cd786-ae58-4708-a345-aea71476eb8d.png)
 
6. Log in to the router with the new IP address.

    - Enter the router’s new IP address to regain access to the router configuration GUI. 
    
    - You are now ready to continue configuring the router for wireless access.

        - ![image](https://user-images.githubusercontent.com/94720207/172265661-d3f5ea71-dd4f-4dad-af78-f8f046e6cd10.png)
        
        - ![image](https://user-images.githubusercontent.com/94720207/172265730-82f7aa50-ad1b-447c-a506-ef0053ee2079.png)

### Basic Wireless Setup PT. 2

- Basic wireless setup includes the following steps:

1. View the WLAN defaults.

    - Out of the box, a wireless router provides wireless access to devices using a default wireless network name and password. 
    
    - The network name is called the **Service Set Identified (SSID).** 
    
    - Locate the basic wireless settings for your router to change these defaults.
    
    - ![image](https://user-images.githubusercontent.com/94720207/172266709-866f5cd3-bc80-4145-bad2-cb2eee2ea1b7.png)
 
2. Change the network mode. (Optional)

    - Some wireless routers allow you to select which `802.11 standard` to implement. 
    
    - The example shows that `Legacy` has been selected. 
    
        - **This means wireless devices connecting to the wireless router can have a variety of wireless NICs installed.** 
        
    - **Today’s wireless routers configured for legacy or mixed mode most likely support `802.11a`, `802.11n`, and `802.11ac` NICs.**

    - ![image](https://user-images.githubusercontent.com/94720207/172266956-38db2300-53f7-4604-bd4a-a17b2252d011.png)

3. Configure the SSID.

    - Some wireless routers allow you to select which 802.11 standard to implement. 
    
    - The example shows that “Legacy” has been selected. 
    
    - This means wireless devices connecting to the wireless router can have a variety of wireless NICs installed. 
    
    - Today’s wireless routers configured for legacy or mixed mode most likely support 802.11a, 802.11n, and 802.11ac NICs.   

    - ![image](https://user-images.githubusercontent.com/94720207/172268413-84614ff6-d07c-4fbe-ba72-34a79c9333e4.png)

4. Configure the channel.

    - Devices configured with the same channel within the `2.4GHz` band **may overlap and cause distortion**, slowing down the wireless performance and potentially break network connections. 
    
    - **The solution to avoid interference is to configure non-overlapping channels on the wireless routers and access points that are near to each other.** 
    
        - **Specifically, channels `1`, `6`, and `11` are `non-overlapping`**. 
        
        - In the example, the wireless router is configured to use `channel 11`.
    
    - ![image](https://user-images.githubusercontent.com/94720207/172268489-017f9621-3dd9-4591-bd4b-6984f703d7d3.png)

5. Configure the security mode.

    - Out of the box, **a wireless router may have no WLAN security configured.** 
    
    - In the example, the **personal version of Wi-Fi Protected Access version 2 `WPA2 Personal`** is selected for all three WLANs. 
    
        - **`WPA2` with `Advanced Encryption Standard` `AES` encryption is currently the strongest security mode.**
        
            - ![image](https://user-images.githubusercontent.com/94720207/172269174-3a610e5a-5a46-409d-a666-09cc96602d3e.png)
  
6. Configure the passphrase.

    - **`WPA2 personal` uses a `passphrase` to authenticate wireless clients.** 
    
    - `WPA2 personal` is easier to use in a **small office or home environment because it does not require an authentication server._(Like a RADIUS  server using AAA)_** 
    
        - **Larger organizations implement `WPA2 enterprise` and require wireless clients to authenticate with a username and password. _(Using RADIUS Server | AAA Standards)_**
        
            - ![image](https://user-images.githubusercontent.com/94720207/172269628-5966dc9f-9978-4317-b1b7-00e2179d016d.png)

---

### Configure a Wireless Mesh Network

- In a small office or home network, one wireless router may suffice to provide wireless access to all the clients. 

    - However, if you want to **extend the range beyond approximately 45 meters indoors and 90 meters outdoors**, you can add `wireless access points`. 

- As shown in the `wireless mesh network` in the figure, two access points are configured with the same WLAN settings from our previous example. 

- Notice that the channels selected are 1 and 11 so that the access points do not interfere with channel 6 for other new AP that it will be installed in our imagination lol. 

    - ![image](https://user-images.githubusercontent.com/94720207/172269932-20269396-1151-4340-a92e-443ac7a7808a.png)

- Extending a WLAN in a small office or home has become increasingly easier. 

- Manufacturers have made creating a `wireless mesh network` `WMN` simple through smartphone apps. 

- You buy the system, disperse the access points, plug them in, download the app, and configure your WMN in a few steps. 

- Search the internet for `wi-fi mesh network system` to find reviews of current offerings, or just click [here!](https://www.howtogeek.com/290418/what-are-mesh-wi-fi-systems-and-how-do-they-work/)

---

### NAT for IPv4

- On a wireless router, if you look for a page like the `Status` page shown in the figure, **you will find the IPv4 addressing information that the router uses to send data to the internet.** 

- Notice that the IPv4 address is `209.165.201.11` is a different network than the `192.168.1.254` address assigned to the router’s LAN interface. 

- All the devices on the router’s LAN will get assigned addresses with the `192.168.1.x` prefix.

    - ![image](https://user-images.githubusercontent.com/94720207/172270842-83638be0-5b77-4e2c-8a1d-b72b2994dad0.png)
 
- The `209.165.201.11` IPv4 address is publicly routable on the internet. 

- Any address with `192.168.x.x` is a private IPv4 address and cannot be routed on the internet. 

    - Therefore, the router will use a process called `Network Address Translation` `NAT` to convert private IPv4 addresses to internet-routable IPv4 addresses. 
    
    - With `NAT`, a private (local) source IPv4 address is translated to a public (global) address. 
    
    - The process is reversed for incoming packets. 
    
    - The router is able to translate many internal IPv4 addresses into public addresses, by using `NAT`.

- **Some ISPs use private addressing to connect to customer devices.** 

    - However, eventually, **your traffic will leave the provider’s network and be routed on the internet.** 
    
- To see the IP addresses for your devices, search the internet for `what is my IP address.` 

- Do this for other devices on the same network and you will see that they all share the same public IPv4 address. 

- NAT makes this possible by tracking the source port numbers for every session established by a device. If your ISP has IPv6 enabled, you will see a unique IPv6 address for each device.

### Quality of Service (QoS)

- Many wireless routers have an option for configuring `Quality of Service` `QoS`. 

    - By configuring `QoS`, you can guarantee that **certain traffic types, such as voice and video, are prioritized over traffic that is not as time-sensitive**, such as email and web browsing. 
    
    - On some wireless routers, traffic can also be prioritized on **specific ports**.

- **The figure is a simplified mockup of a QoS interface based on a `Netgear` GUI.**

    - ![image](https://user-images.githubusercontent.com/94720207/172276085-1fc61465-89db-447c-be1b-64b2a508b4fc.png)
 
- You will usually find the QoS settings in the advanced menus. 

    - ![image](https://user-images.githubusercontent.com/94720207/172276023-ca65269e-34b4-4c57-86da-6949cb71b864.png)

- If you have a wireless router available, investigate the QoS settings. 

    - Sometimes, these might be listed under “bandwidth control” or something similar. Consult the wireless router’s documentation or search the internet for “qos settings” for your router’s make and model.

---

### Port Forwarding

- [Explicación chida del Port Forwarding](https://wiki.teltonika-networks.com/view/Port_Forwarding)

- **Wireless routers typically block TCP and UDP ports to prevent unauthorized access in and out of a LAN.** 

- However, there are situations when specific ports must be opened so that certain programs and applications can communicate with devices on different networks. 

    - **Port forwarding is a rule-based method of directing traffic between devices on separate networks.**

    - **Port Forwarding is the process of redirecting data packets to another destination.** 
    
        - When a packet matches a port forwarding rule, the destination and/or port values are changed in the packet header.
    
        - ![Networking_rutos_faq_port_forwarding_example_2_v1](https://user-images.githubusercontent.com/94720207/172277052-5ab3bf82-e4f8-4770-8f19-70672388f82b.gif) 
        
        - This allows for access to multiple devices in a network over one device.
        
        - ![image](https://user-images.githubusercontent.com/94720207/172276962-83a5576e-a180-44b1-a14e-d8a55f59b81a.png)

- When traffic reaches the router, the router determines if the traffic should be forwarded to a certain device based on the port number found with the traffic. 

    - For example, a router might be configured to forward port `80`, which is associated with `HTTP`. 

    - When the router receives a packet with the destination port of `80`, the router forwards the traffic to the server inside the network that serves web pages. 
    
    - In the figure, port forwarding is enabled for port `80` and is associated with the `web server` at IPv4 address `192.168.1.50`.
    
    - ![image](https://user-images.githubusercontent.com/94720207/172277579-3dfbac3c-8f61-4acb-8f73-61797c6d5601.png)

### Port Triggering

- Port triggering allows the router to temporarily forward data through inbound ports to a specific device. 

- You can use port triggering to forward data to a computer only when a designated port range is used to make an outbound request. 

    - For example, a video game might use ports `27000` to `27100` for connecting with other players. 
    
    - These are the trigger ports. 
    
    - A chat client might use port `56` for connecting the same players so that they can interact with each other. 
    
        - **In this instance, if there is gaming traffic on an outbound port within the triggered port range** 
        
        - Inbound chat traffic on port `56` is forwarded to the computer that is being used to play the video game and chat with friends. 
        
        - When the game is over and the triggered ports are no longer in use, port `56` is no longer allowed to send traffic of any type to this computer.
 
---

### References

- https://ccna-200-301.online/remote-site-wlan-configuration/
- https://contenthub.netacad.com/srwe-dl/1.3.6

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
