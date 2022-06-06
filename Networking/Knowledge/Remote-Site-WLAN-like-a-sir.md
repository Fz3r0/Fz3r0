

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

### Basic Network Setup

- Basic network setup includes the following steps:

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

5. Renew the IP address.

6. Log in to the router with the new IP address.

7. Click each step for more information and an example GUI.






---

### References

- https://contenthub.netacad.com/srwe-dl/1.3.6

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
