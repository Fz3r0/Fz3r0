
# Configure WLAN on WLC like a sir!

![My Video](https://user-images.githubusercontent.com/94720207/165892585-b830998d-d7c5-43b4-a3ad-f71a07b9077e.gif)

## Fz3r0 Operations: `Networking`

##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Networking` `Routing & Switching` `Wireless` `WLAN` `WLC` `CCNA` `CCNP` 
  
## Index

- < **Before anything else!!!** >

- < **Option1**: Straight to the point Configuration >

- < **Option2**: Step by Step Configuration >

- < **Troubleshooting** & **show commands** for this configuration >** 

### Background Knowledge about this config:

- < **Nerd Pocket-Bible about this configuration** >

## Configure a Basic WLAN on the WLC

### WLC Topology

- WLC Topology Example:

    - ![image](https://user-images.githubusercontent.com/94720207/172299671-b0336dea-5fec-427b-996a-43cce68c9da2.png)
 
- The access point `AP` is a `controller-based AP` as opposed to an `autonomous AP`. 

    - Recall that controller-based APs require no initial configuration and are often called lightweight APs (LAPs). 
    
    - `LAPs` use the `Lightweight Access Point Protocol` `LWAPP` to communicate with a `WLAN controller` `WLC`. 
    
    - Controller-based APs are useful in situations where many APs are required in the network. 
    
    - As more APs are added, each AP is automatically configured and managed by the WLC.

- The previous figure shows a wireless LAN controller (WLC) topology. 

    - `PC-A` is a `RADIUS/SNMP Server` connected to `R1` on `Gi 0/0` interface. 

    - `PC-B` is connected to `S1` on S1s `F0/6` port. 
    
    - `R1` and `S1` are connected together on `R1s Gi 0/1` interface and on `S1s F0/5` interface. 
    
    - `S1` is connected to a `WLC` on its `F0/18` port. 
    
    - On `S1s F0/1` port its connected to an access point, `AP1`. 
    
    - A `laptop` is wirelessly connected to `AP1`.

- Addressing Table: 

| **Device**      | **Interface** | **IP Address**  | **Subnet Mask**  |
|-----------------|---------------|-----------------|------------------|
| R1              | Gi0/0         | 172.31.1.1      | 255.255.255.0    |
| R1              | Gi0/1.5       | 192.168.5.1     | 255.255.255.0    |
| R1              | Gi0/1.200     | 192.168.200.1   | 255.255.255.0    |
| SW1             | VLAN 200      | 192.168.200.100 | 255.255.255.0    |
| LAP-1           | G0	          | DHCP            |                  |
| WLC             | Management    | 192.168.200.254 | 255.255.255.0    |
| AP1             | Wired 0       | 192.168.200.3   | 255.255.255.0    |
| Server          | NIC           | 172.31.1.254    | 255.255.255.0    |
| Admin PC        | NIC           | 192.168.200.200 | 255.255.255.0    |
| Wireless Laptop | Wireless NIC  | DHCP            |                  |

- Objectives:

1. Connect to a wireless LAN controller GUI.
2. Explain some of the information that is available on the WLC Monitor screen.
3. Configure a WLAN on a wireless LAN controller.
4. Implement security on a WLAN.
5. Configure a wireless host to connect to a wireless LAN.

## Part1: Monitor WLC:

- Go the desktop of Admin PC and open a browser. 

- Enter the management IP address of WLC-1 from the addressing table into the address bar. 

- You must specify the `HTTPS` protocol.

    - ![image](https://user-images.githubusercontent.com/94720207/172300557-30b63ce3-d8d5-4370-ac47-0dce015373aa.png)

- Click Login and enter these credentials: 

    - User Name: `admin`
    
    - Password: `Cisco123`
    
    - ![image](https://user-images.githubusercontent.com/94720207/172300785-64fe6db2-44a9-48dd-8e9c-281b484abda3.png)
 
- After a short delay, you will see the WLC Monitor Summary screen.

    - ![image](https://user-images.githubusercontent.com/94720207/172300904-155d1974-7641-4b0f-bfb2-29fcf89fd2ea.png)

- Click Detail next to the All APs entry in the Access Point Summary section of the page.

- Information shown on the WLC includes the name of the AP, the IP address of the AP, the device model, MAC, software version, operational status, power source, etc.

    - ![image](https://user-images.githubusercontent.com/94720207/172301143-e7b39d71-21d1-482c-aa12-94266234d950.png)

    - ![image](https://user-images.githubusercontent.com/94720207/172301294-bf12f30c-9f80-4b90-85d1-695a42bb1e91.png)

## Part 2: Create a Wireless LAN







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
