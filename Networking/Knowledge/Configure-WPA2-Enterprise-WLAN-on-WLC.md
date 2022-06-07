
# Configure a WPA2 Enterprise WLAN on the WLC like a Sir!

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## Fz3r0 Operations: `Networking`

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `Wireless` `WLAN` `WLC` `RADIUS` `AAA` `CCNA` `CCNP` 
  
## Index

- < **Before anything else!!!** >

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

- < **Troubleshooting** & **show commands** for this configuration >** 

### Background Knowledge about this config:

- < **Nerd Pocket-Bible about this configuration** >

## Configure a WPA2 Enterprise WLAN on the WLC

### WLC Topology

- Falta detallarlo:

- ![image](https://user-images.githubusercontent.com/94720207/172326073-8e9a3773-dc92-4166-b432-1ce519b1369f.png)

### Addressing Table

| **Device**         | **Interface**     | **IP Address**      |
|--------------------|-------------------|---------------------|
| R1                 | G0/0/0.5          | 192.168.5.1/24      |
| G0/0/0.200         | 192.168.200.1/24  |                     |
| G0/0/1             | 172.31.1.1/24     |                     |
| SW1                | VLAN 200          | 192.168.200.100/24  |
| LAP-1              | G0                | DHCP                |
| WLC-1              | Management        | 192.168.200.254/24  |
| RADIUS/SNMP Server | NIC               | 172.31.1.254/24     |
| Admin PC           | NIC               | 192.168.200.200/24  |

## SNMP and RADIUS

- In this lab I will use `Simple Network Management Protocol` `SNMP` and `Remote Authentication Dial-In User Service` `RADIUS` server software. 

    - `SNMP` is used to monitor the network. 
    
        - The network administrator wants the `WLC` to **forward all `SNMP log messages`, called `traps`, to the `SNMP server`**.

    - In addition, for WLAN user authentication, the network administrator wants to use a `RADIUS` server for `authentication, authorization, and accounting` `AAA` services. 
    
        - Instead of entering a publicly known pre-shared key to authenticate, as they do with `WPA2-PSK`, users will enter **their own username and password credentials**. 
    
        - **The credentials will be verified by the RADIUS server.** 
        
    - This way, individual user access can be tracked and audited if necessary and user accounts can be added or modified from a central location. 
    
    - **The `RADIUS server` is required for WLANs that are using `WPA2 Enterprise` authentication**.
    
    - **In this lab I will NOT configure the RADIUS server or SNMP, I will do that on next lab and focus now on `WPA2 Enterprise Authentication` (Both servers are previusly configured and ready to go :D)**

## Objectives

- Configure a new VLAN interface on a WLC.
- Configure a new WLAN on a WLC.
- Configure a new scope on the WLC internal DHCP server.
- Configure the WLC with SNMP settings.
- Configure the WLC to user a RADIUS server to authenticate WLAN users.
- Secure a WLAN with WPA2-Enterprise.
- Connect hosts to the new WLC.

## Part 1: Create a new WLAN

- I will create a WLAN inside the WLC dashboard like a sir, just like in the previous lab. 

    - ## Step 1: Create a new VLAN interface.

        - **Each `WLAN` requires a `virtual interface` on the `WLC`.** 
        
            - **These interfaces are known as `dynamic interfaces`**. 
            
            - The virtual interface is assigned a `VLAN ID` and traffic that uses the interface will be tagged as `VLAN traffic`. 
            
            - **This is why connections between the APs, the WLC, and the router are over trunk ports.** 
            
            - For the traffic from multiple WLANs to be transported through the network, traffic for the WLAN VLANs must be trunked.

- Open the browser from the desktop of `Admin PC`. 

    - Connect to the IP address of the WLC over HTTPS. `https://192.168.200.254`
    
    - ![image](https://user-images.githubusercontent.com/94720207/172330898-413724fc-7491-4ab0-ae00-01e11310d758.png)
 
- Login with the username `admin` and password `Cisco123`.

    - ![image](https://user-images.githubusercontent.com/94720207/172331931-d44136ad-43af-422e-9bfe-08e40c8915e1.png)

- Click the Controller `menu` and then click `Interfaces` from the menu on the left. 

    - You will see the `default virtual interface` and the `management interface` to which you are connected.

    - Click the `New` button in the upper right-hand corner of the page. 
    
        - **You may need to scroll the page to the right to see it.**
        
        - ![image](https://user-images.githubusercontent.com/94720207/172333193-70b89efb-44e4-4efb-93ab-96b9805175bc.png)
        
        - ![image](https://user-images.githubusercontent.com/94720207/172333409-7076403f-7190-47dc-917c-41af01c42b62.png)

- Enter the name of the new interface. 

    - We will call it `WLAN-5`. 
    
    - Configure the `VLAN ID` as `5`. 
    
        - **This is the `VLAN` that will carry traffic for the `WLAN` that we create later. 
        
    - Click `Apply`. 
    
        - This leads to a configuration screen for the VLAN interface.
        
        - ![image](https://user-images.githubusercontent.com/94720207/172334030-30cc4da1-1f54-4b3d-91bc-7ff58a101369.png)

        - ![image](https://user-images.githubusercontent.com/94720207/172334177-b7b90e17-ed4f-4786-af33-9b1692edc1af.png)

- First, configure the interface to use `physical port number` `1`. 

    - **Multiple VLAN interfaces can use the same physical port because the physical interfaces are like dedicated trunk ports.**
    
        - _That's why the `Fz3r0 Super Cisco Trunkin' Standard` uses `ALWAYS VLAN 99 for Trunk VLANs`_ 

- Address the interface as follows:

    - **IP Address: `192.168.5.254`**
    - **Netmask: `255.255.255.0`**
    - **Gateway: `192.168.5.1`**
    - **Primary DHCP server: `192.168.5.1`**
    
        - ![image](https://user-images.githubusercontent.com/94720207/172335214-653f1f8c-bdf2-45c5-bb40-21ade6bc8e3d.png)
 



 




 
---

### References

- https://ccna-200-301.online/configure-wlan-wlc/

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
