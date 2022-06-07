
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

- Now you will create a new wireless LAN on the WLC. 

- You will configure the settings that are required for hosts to join the WLAN.

    - ## Step 1: Create and enable the WLAN

        - Click WLANs in the WLC menu bar. 
        
        - Locate the dropdown box in the upper right had corner of the WLANs screen. 
        
        - It will say Create New. 
        
        - Click Go to create a new WLAN.
        
            - ![image](https://user-images.githubusercontent.com/94720207/172306153-03dfe76c-e604-4ea5-b50a-e90c08826e38.png)

        - Enter the **Profile Name of the new WLAN**. 
        
        - Use the profile name `Floor 2 Employees`. 
        
        - Assign an `SSID` of `SSID-5` to the **WLAN**. 
        
            - **Hosts will need to use this `SSID` to join the network.**

        - Select the `ID` for the **WLAN**. 
        
            - **This `ID` value is a label that will be used to identify the WLAN is other displays.** 
        
            - Select a value of `5` to **keep it consistent with the VLAN number and SSID**. 
            
            - **This is not a requirement but it helps with understanding the topology.**
                
            - ![image](https://user-images.githubusercontent.com/94720207/172305916-4c8a32c8-9fd9-4235-853a-3158ed47542e.png)

        - Click Apply so that the settings go into effect.
        
            - ![image](https://user-images.githubusercontent.com/94720207/172306258-77a031f9-0f90-4ec6-a147-85edce9ad16f.png)
 
- Now that the WLAN has been created, you can configure features of the network.

- Click Enabled to make the WLAN functional. 

    - **CAUTION! It is a common mistake to accidentally skip this step.**

- Choose the VLAN interface that will be used for the WLAN. 

    - The WLC will use this interface for user traffic on the network. 
    
    - Click the `drop-down box` for `Interface/Interface Group (G)`.
    
    -  Select the `WLAN-5` interface. (This interface was previously configured on the WLC for this activity).
    
        - ![image](https://user-images.githubusercontent.com/94720207/172306660-5782bd51-314b-4bcf-8931-b8f1899e7c50.png)

- **Click the Advanced tab.**

    - Scroll down to the `FlexConnect` portion of the page. 
    
    - Click to `enable` `FlexConnect Local Switching` and `FlexConnect Local Auth`.

    - Click `Apply` to enable the new WLAN. **If you forget to do this, the WLAN will not operate.**
    
        - ![image](https://user-images.githubusercontent.com/94720207/172307552-e1cb3343-e1a8-43a8-bc22-7665443b3d36.png)
    
        - ![image](https://user-images.githubusercontent.com/94720207/172307612-7ea96ed4-0fba-4150-8c78-ca3a4bb6b864.png)

    - ## Step 2: Secure the WLAN

- **The new WLAN currently has no security in place.** 

    - **This WLAN will initially use `WPA2-PSK` security.** 

    - In another activity, you will configure the WLAN to use `WPA2-Enterprise`, **a much better solution for larger wireless networks.**

- In the WLANs Edit screen for the `Floor 2 Employees WLAN`, click the `Security tab`. 

    - Under the `Layer 2` tab, select `WPA+WPA2` from the `Layer 2 Security` drop down box. 
    
        - This will reveal the `WPA` parameters.

-  Click the checkbox next to `WPA2 Policy`. 

    -  This will reveal additional security settings. 
    
    -  Under Authentication `Key Management`, enable `PSK`.

    - Now you can enter the `pre-shared key` that will be used by hosts to join the WLAN. 
    
    - Use `Cisco123` as the `passphrase`.
    
        - ![image](https://user-images.githubusercontent.com/94720207/172310081-1573fc75-a182-4cb2-b7ee-64f0ef86db2d.png)
        
    - Apply configs:
    
        - ![image](https://user-images.githubusercontent.com/94720207/172310621-44d7d0bf-2d38-4efe-b4ed-e2efbd8348c5.png)
  
            - **Note: It is not a good practice to reuse passwords when configuring security. We have reused passwords in this activity to simplify configuration.**

   - ## Step 3: Verify the Settings
   
       - After Applying the configuration, click Back. This will take you back to the WLANs screen.  
  
           - ![image](https://user-images.githubusercontent.com/94720207/172310681-94fd5e21-eae5-43b2-a354-e9da17ee3cd1.png)

       - The WLAN name, SSID, security policy and admin status are available here. 
       
       - The Admin Status value indicates whether WLAN is in operational or not. 
       
       - If you click the `WLAN ID`, you will be taken to the `WLANs Edit screen`. 
       
       - Use this to verify and change the details of the settings. 
       
           - ![image](https://user-images.githubusercontent.com/94720207/172311093-f387b05c-e4c4-416e-b7b3-7770a7b4b3d6.png)

       - **Don't forget to Save Global WLC Configurations!!!**
       
           - ![image](https://user-images.githubusercontent.com/94720207/172311345-a7584dde-69b4-42bd-ac24-d87c3969f382.png)
 
## Part 3: Connect a Host to the WLAN

- In this step I will configure the laptop, most of wireless devices can configure very similar to Packet Tracer example: 

    - ## Step 1: Connect to the network and verify connectivity
    
        - Go to the `desktop` of `Wireless Host` or `laptop` or `smartphone` and click the PC `Wireless` tile
        
        - Click the `Connect` tab. 
        
        - After a brief delay you should see the SSID for the WLAN appear in the table of wireless network names. 
        
        - Select the `SSID-5` network and click the `Connect` button. 

            - ![image](https://user-images.githubusercontent.com/94720207/172314125-3d61ce04-cf9b-477f-ad1a-e001494d614c.png)

            - ![image](https://user-images.githubusercontent.com/94720207/172314228-a72858a9-8a89-4557-a9f6-bdb853c425b8.png)
            
            - ![image](https://user-images.githubusercontent.com/94720207/172314379-f6e6a8f9-0307-4070-a3f2-c00b3f5bb13f.png)
        
        - Enter the `pre-shared key` that you configured for the WLAN (`Cisco123`) and click `Connect`.  

 






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
