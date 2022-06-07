
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

- 

## SNMP and RADIUS

- In this lab I will use `Simple Network Management Protocol` `SNMP` and `Remote Authentication Dial-In User Service` `RADIUS` server software. 

    - `SNMP` is used to monitor the network. 
    
        - The network administrator wants the `WLC` to **forward all `SNMP log messages`, called `traps`, to the `SNMP server`**.

    - In addition, for WLAN user authentication, the network administrator wants to use a `RADIUS` server for `authentication, authorization, and accounting` `AAA` services. 
    
        - Instead of entering a publicly known pre-shared key to authenticate, as they do with `WPA2-PSK`, users will enter **their own username and password credentials**. 
    
        - **The credentials will be verified by the RADIUS server.** 
        
    - This way, individual user access can be tracked and audited if necessary and user accounts can be added or modified from a central location. 
    
    - **The `RADIUS server` is required for WLANs that are using `WPA2 Enterprise` authentication**.
    
    - 


 
---

### References

- https://ccna-200-301.online/configure-wlan-wlc/

---

> ![hecho en mex3 (1)mini](https://user-images.githubusercontent.com/94720207/163919294-2754caa3-c98c-4df3-b782-00703e4d3343.png)
>
> _- Hecho en México - by [Fz3r0 💀](https://github.com/Fz3r0/)_ 
>
> _"In the mist of the night you could see me come, where shadows move and Demons lie..."_ 
