


---

[9___fz3r0_OPs_Routing_&_Switching_SUPER_PRO__SECURE_&_BEST_PRACTICES_VS_LAYER_2_ATTACKS.zip](https://github.com/Fz3r0/Fz3r0/files/8683966/9___fz3r0_OPs_Routing_._Switching_SUPER_PRO__SECURE_._BEST_PRACTICES_VS_LAYER_2_ATTACKS.zip)

![image](https://user-images.githubusercontent.com/94720207/168204033-89002e71-4eb9-477f-a6e5-310bbc0463e4.png)

![image](https://user-images.githubusercontent.com/94720207/168204629-8b160dba-5ca2-433a-91ad-09ffca5a1117.png)

---

## SWITCH-1 >> `Fz3r0_SW1` 

- **NOTES:**

    - This switch is the main configuration for this Lab
    - The idea of this Lab is make a full configuration of security and best practices against ALL Layer 2 Attacks available
    - This switch have different variables and scenarios in its interfaces like:
        
        - Access VLANS to Hosts (PCs)
        - Access VLANS to Hosts (Servers) 
        - Access VLANS to Trusted DHCP Server 
        - Trunk VLANs to Other Switch
        - Trunk VLANs to Router / Gateway
        - Different VLANs
        - Hosts with static IPs
        - Hosts with dynamic IPs
        - SVI support
        - Multiple VLAN support
        - Used/Unused Ports
        - etc

```
enable
configure terminal 
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


         fz3r0 - Switch1:  Only authorized access!!!!


               FULL SECURITY & BEST PRACTICES CONFIGURATION
              
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  



=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=




         STARTING BASE CONFIGURATION: 

            HOSTNAME, DOMAIN, VLANS, SSH SVI & DEFAULT GATEWAY



=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
hostname Fz3r0_SW1
!
!
no ip domain-lookup
ip domain-name <<_Fz3r0.Layer2_Security_&_BestPractices.configs_>>
!
!
!
vlan 10
name VLAN10-BLUE-HOST__(access)
vlan 20
name VLAN20-RED-HOST__(access)
vlan 30
name VLAN30-YELLOW-HOST__(access)
vlan 40
name VLAN40-GREEN-HOST__(access)
!
vlan 100
name VLAN1000-BROWN-SERVERS__(access)
!
vlan 101
name VLAN1000-DHCP-TRUSTED-SERVER__(access)
!
vlan 99
name VLAN99-TRUNK__(trunk)
exit
!
vlan 69
name VLAN69-Management/SSH
exit
!
vlan 666
name VLAN666-OFF=Unused_Honeypot
exit
!
interface vlan 69
description << Switch 1 Management/SSH >>
ip address 192.168.69.1 255.255.255.0
no shutdown 
exit
!
ip default-gateway 192.168.69.254
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: GLOBAL CONFIGS FOR SECURITY & BEST PRACTICES


NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) 

      but STP Portfast & BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG, only on each interface..
      ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT JUST TO AVOID MISTAKES 



=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
ip dhcp snooping 
ip dhcp snooping vlan 1,10,20,30,40,69,99,666,100,101
ip arp inspection vlan 1,10,20,30,40,69,99,666,100,101
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: ACCESS INTERFACES (HOSTS) VLAN 10 ---INTERFACES_CONFIG_SECURITY_BEST_PRACTICES:




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface range Fa 0/1 - 4
description << VLAN 10 - BLUE - Access Ports to Hosts (PCs) >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: VLAN 10 BLUE ACCESS HOSTS>>
!
description << 1. This are Active Used Ports > no shut >>
description << 2. Port Security > Max 2 | (PC & Admin MACs: Only 2 known MACs) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > Enabled(default) + limit rate | (Not a trusted DHCP server: | Snooping=ON) >>
description << 5. DAI DynARP Inspection: Enabled | (This are ACCESS untrusted ports: | DAI=ON) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS untrusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS untrusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
no shutdown
!
switchport mode access
switchport access vlan 10
!
switchport port-security
switchport port-security maximum 2
description << NOTE: TRY TO USE ONLY MANUAL MAC IN REAL LIFE, I USED STICKY FOR HAVING BOTH OPTIONS AND AUTO-HOST-LEARNING>>
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip dhcp snooping limit rate 6
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << VLAN 10 - BLUE - Access Ports to Hosts (PCs) >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: ACCESS INTERFACES (HOSTS) VLAN 20 ---INTERFACES_CONFIG_SECURITY_BEST_PRACTICES:




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface range Fa 0/5 - 8
description << VLAN 20 - RED - Access Ports to Hosts (PCs) >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: VLAN 20 RED ACCESS HOSTS >>
!
description << 1. This are Active Used Ports > no shut >>
description << 2. Port Security > Max 2 | (PC & Admin MACs: Only 2 known MACs) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > Enabled(default) + limit rate | (Not a trusted DHCP server: | Snooping=ON) >>
description << 5. DAI DynARP Inspection: Enabled | (This are ACCESS untrusted ports: | DAI=ON) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS untrusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS untrusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
no shutdown
!
switchport mode access
switchport access vlan 20
!
switchport port-security
switchport port-security maximum 2
description << NOTE: TRY TO USE ONLY MANUAL MAC IN REAL LIFE, I USED STICKY FOR HAVING BOTH OPTIONS AND AUTO-HOST-LEARNING>>
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip dhcp snooping limit rate 6
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << VLAN 20 - RED - Access Ports to Hosts (PCs) >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: ACCESS INTERFACES (HOSTS) VLAN 30 ---INTERFACES_CONFIG_SECURITY_BEST_PRACTICES:




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface range Fa 0/9 - 12
description << VLAN 30 - YELLOW - Access Ports to Hosts (PCs) >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: VLAN 30 YELLOW ACCESS HOSTS >>
!
description << 1. This are Active Used Ports > no shut >>
description << 2. Port Security > Max 2 | (PC & Admin MACs: Only 2 known MACs) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > Enabled(default) + limit rate | (Not a trusted DHCP server: | Snooping=ON) >>
description << 5. DAI DynARP Inspection: Enabled | (This are ACCESS untrusted ports: | DAI=ON) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS untrusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS untrusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
no shutdown
!
switchport mode access
switchport access vlan 30
!
switchport port-security
switchport port-security maximum 2
description << NOTE: TRY TO USE ONLY MANUAL MAC IN REAL LIFE, I USED STICKY FOR HAVING BOTH OPTIONS AND AUTO-HOST-LEARNING>>
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip dhcp snooping limit rate 6
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << VLAN 30 - YELLOW - Access Ports to Hosts (PCs) >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: ACCESS INTERFACES (HOSTS) VLAN 40 ---INTERFACES_CONFIG_SECURITY_BEST_PRACTICES:




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface range Fa 0/13 - 14
description << VLAN 40 - GREEN - Access Ports to Hosts (PCs) >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: VLAN 40 GREEN ACCESS HOSTS >>
!
description << 1. This are Active Used Ports > no shut >>
description << 2. Port Security > Max 2 | (PC & Admin MACs: Only 2 known MACs) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > Enabled(default) + limit rate | (Not a trusted DHCP server: | Snooping=ON) >>
description << 5. DAI DynARP Inspection: Enabled | (This are ACCESS untrusted ports: | DAI=ON) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS untrusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS untrusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
no shutdown
!
switchport mode access
switchport access vlan 40
!
switchport port-security
switchport port-security maximum 2
description << NOTE: TRY TO USE ONLY MANUAL MAC IN REAL LIFE, I USED STICKY FOR HAVING BOTH OPTIONS AND AUTO-HOST-LEARNING>>
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip dhcp snooping limit rate 6
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << VLAN 40 - GREEN - Access Ports to Hosts (PCs) >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: ACCESS INTERFACES VLAN 1000 (SERVERS)---_INTERFACES_CONFIG_SECURITY_BEST_PRACTICES:




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface range Fa 0/15 - 16, Fa 0/18
description << VLAN 100 - BROWN - Access Ports to Hosts (SERVERS) >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: VLAN 100 - BROWN - Access Ports to Hosts (SERVERS) >>
!
description << 1. This are Active Used Ports > no shut >>
description << 2. Port Security > Max 2 | (PC & Admin MACs: Only 2 known MACs) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > Enabled(default) + limit rate | (Not a trusted DHCP server: | Snooping=ON) >>
description << 5. DAI DynARP Inspection: Enabled | (This are ACCESS untrusted ports: | DAI=ON) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS untrusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS untrusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
no shutdown
!
switchport mode access
switchport access vlan 100
!
switchport port-security
switchport port-security maximum 2
description << NOTE: TRY TO USE ONLY MANUAL MAC IN REAL LIFE, I USED STICKY FOR HAVING BOTH OPTIONS AND AUTO-HOST-LEARNING>>
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip dhcp snooping limit rate 6
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << VLAN 100 - BROWN - Access Ports to Hosts (SERVERS) >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: ACCESS   << TRUSTED DHCP SERVER >> DHCP_SERVICE_INTERFACE_CONFIG_SECURITY_BEST_PRACTICES




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface  Fa 0/17
description << VLAN 101 - PINK - TRUSTED DHCP SERVER >>> == Trust me!!! I'm your DHCP Server == >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: VLAN 101 - PINK - ==TRUSTED DHCP SERVER== >>
!
description << 1. This are Active Used Ports > no shut >>
description << 2. Port Security > Max 2 | (PC & Admin MACs: Only 2 known MACs) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > DISABLE!!! | THIS IS A TRUSTED DHCP SERVER! TRUST ME!!! | Snooping=OFF) >>
description << 5. DAI DynARP Inspection > DISABLE!!! | THIS IS A TRUSTED DHCP SERVER! TRUST ME!!! | DAI=OFF) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS trusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS trusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
no shutdown
!
switchport mode access
switchport access vlan 101
!
switchport port-security
switchport port-security maximum 2
description << NOTE: TRY TO USE ONLY MANUAL MAC IN REAL LIFE, I USED STICKY FOR HAVING BOTH OPTIONS AND AUTO-HOST-LEARNING>>
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security mac-address sticky 
switchport port-security aging time 1440
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip DHCP SNOOPING TRUST
ip ARP INSPECTION TRUST
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << VLAN 101 - PINK - TRUSTED DHCP SERVER >>> == Trust me!!! I'm your DHCP Server == >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: ACCESS   (OFF-UNUSED INTERFACE / HONEYPOT)    UNUSED_INTERFACES_CONFIG_SECURITY_BEST_PRACTICES




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface range Fa 0/19 - 24
description << VLAN 666 - Honeypot - UNUSED VLAN - UNUSED PORTS - TURN OFF - HOLE TO NOWHERE >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: UNUSED VLAN - UNUSED PORTS - TURN OFF - HOLE TO NOWHERE >>
!
description << 1. This are INACTIVE!!! Ports > SHUTDOWN >>
description << 2. Port Security > Max 1 | (Admin MAC: Only Admin PC can enter) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > Enabled(default) + limit rate | (Not a trusted DHCP server: | Snooping=ON) >>
description << 5. DAI DynARP Inspection: Enabled | (This are ACCESS untrusted ports: | DAI=ON) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS untrusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS untrusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
SHUTDOWN
!
switchport mode access
switchport access vlan 666
!
switchport port-security
switchport port-security maximum 1
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security aging time 5
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip dhcp snooping limit rate 6
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: UNUSED VLAN - UNUSED PORTS - TURN OFF - HOLE TO NOWHERE >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=





NEXT: TRUNKS ON INTERFACES TO SWITCHES & ROUTERS (TRUNK-INTERFACES__>>>__TO_SWITCH_AND/OR_ROUTER)---TRUNK_CONFIG_SECURITY_BEST_PRACTICES




=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
interface range Gi 0/1 - 2
description << VLAN 99 - TRUNK - TRUNK PORT CONNECTED TO A SWITCH OR ROUTER >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: VLAN 99 - TRUNK - TRUNK PORT CONNECTED TO A SWITCH OR ROUTER >>
!
description << 1. This are Active Used Ports > no shut >>
description << 2. Port Security > NO NEED FOR PORT SECURITY IN THIS TRUNKING SCENARIO >>
description << 3. DTP > nonegotiate | (This are TRUNK ports, but NOT dynamic trunks (Manual static trunk config): | DTP=OFF) >>
description << 4. DHCP snooping > Disabled | (this is a TRUSTED trunk uplink port that are connected to other switch or Router | Snooping=ON) >>
description << 5. DAI DynARP Inspection > Disabled | (this is a TRUSTED trunk uplink port that are connected to other switch or Router | DAI=OFF) >>
description << 6. STP Portfast & BPDU guard: Disabled | (This is a Trunk port!!! Disable both!!!)  >>
description << 7. CDP & LLDP: Enable | (This are TRUNK trusted ports, link discovery can be enabled | lldp=ON)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
no shutdown
!
switchport mode trunk
switchport trunk native vlan 99
!
!
description << NO NEED OF PORT SECURITY IN THIS TRUNKING SCENARIO >>
!
!
switchport nonegotiate
!
ip dhcp snooping TRUST
ip arp inspection TRUST
!
spanning-tree bpduguard DISABLE
spanning-tree portfast DISABLE
shutdown
no shutdown
!
lldp TRANSMIT
lldp RECEIVE
CDP ENABLE
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << VLAN 99 - TRUNK - TRUNK PORT CONNECTED TO A SWITCH OR ROUTER >>
exit
!
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


         fz3r0 - Switch1:  Only authorized access!!!!


               FULL SECURITY & BEST PRACTICES CONFIGURATION DONE! :D
              
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
!
!
!
end
WR
!
reload
!
exit
!
!
!

```

---

## SWITCH-2 >> `Fz3r0_SW2` 

- **NOTES:**

    - This switch is only for having a switch variable at the other side og Gi 0/1 on SW1
    - It have the same config as SW1, only copy and paste again config from SW1 and then:
    - Copy and Paste the next config (different hostname and shutdown all switchports except Gi 0/1)

```
enable
configure terminal 
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=



         STARTING BASE CONFIGURATION: 

            FIRST, COPY WHOLE SWITCH 1 SETUP INTO SWITCH 2!!! 

            THEN, COPY AND PASTE THIS CONFIG AGAIN TO SWITCH 2!!!!!



=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
hostname Fz3r0_SW2
!
!
no ip domain-lookup
ip domain-name <<_Fz3r0.Layer2_Security_&_BestPractices.configs_>>
!
!
!
vlan 10
name VLAN10-BLUE-HOST__(access)
vlan 20
name VLAN20-RED-HOST__(access)
vlan 30
name VLAN30-YELLOW-HOST__(access)
vlan 40
name VLAN40-GREEN-HOST__(access)
!
vlan 100
name VLAN100-BROWN-SERVERS__(access)
!
vlan 101
name VLAN101-DHCP-TRUSTED-SERVER__(access)
!
vlan 99
name VLAN99-TRUNK__(trunk)
exit
!
vlan 69
name VLAN69-Management/SSH
exit
!
vlan 666
name VLAN666-OFF=Unused_Honeypot
exit
!
interface vlan 69
description << Switch 2 Management/SSH >>
ip address 192.168.69.2 255.255.255.0
no shutdown 
exit
!
ip default-gateway 192.168.69.254
!
!
!
!
!
interface range Fa 0/1 - 24, Gi 0/2
description << VLAN 666 - Honeypot - UNUSED VLAN - UNUSED PORTS - TURN OFF - HOLE TO NOWHERE >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: UNUSED VLAN - UNUSED PORTS - TURN OFF - HOLE TO NOWHERE >>
!
description << 1. This are INACTIVE!!! Ports > SHUTDOWN >>
description << 2. Port Security > Max 1 | (Admin MAC: Only Admin PC can enter) >>
description << 3. DTP > nonegotiate | (This are ACCESS ports, NOT dynamic trunks: | DTP=OFF) >>
description << 4. DHCP snooping > Enabled(default) + limit rate | (Not a trusted DHCP server: | Snooping=ON) >>
description << 5. DAI DynARP Inspection: Enabled | (This are ACCESS untrusted ports: | DAI=ON) >>
description << 6. STP Portfast & BPDU guard: Enabled | (This are ACCESS untrusted ports: | Portfast & BPDUguard=ON)  >>
description << 7. CDP & LLDP: Disabled | (This are ACCESS untrusted ports, link discovery must be disabled | lldp=OFF)  >>
!
description << NOTE: DHCP snooping, DAI are configured in global config + each interface (both options) >> 
description <<       STP Portfast& BPDU guard ARE NOT CONFIFURED IN GLOBAL CONFIG... >>
description <<       ...I CONFIGURED MANUALLY ONLY ON EACH SWITCHPORT TO AVOID MISTAKES >>
!
description << SECURITY & BEST PRACTICES CHECKLIST DONE!!! >>
description << Full Configuration: >>
!
!
!
SHUTDOWN
!
switchport mode access
switchport access vlan 666
!
switchport port-security
switchport port-security maximum 1
switchport port-security mac-address AA:DD:MM:II:NN
switchport port-security aging time 5
switchport port-security violation shutdown
description << NOTE: >>
description << port-security errdisable & aging type NOT supported on packet tracer: >>
errdisable recovery cause psecure-violation
errdisable recovery interval 600
switchport port-security aging type inactivity
!
switchport nonegotiate
!
ip dhcp snooping limit rate 6
!
spanning-tree portfast
spanning-tree bpduguard enable
!
no lldp transmit
no lldp receive
no CDP enable
!
description << SECURITY & BEST PRACTICES FULL CONFIG DONE!!! FULL SECURITY ARMED >>
!
description << Fz3r0: Security & Best Practices Checklist for this scenario: UNUSED VLAN - UNUSED PORTS - TURN OFF - HOLE TO NOWHERE >>
exit
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


         fz3r0 - Switch2:  Only authorized access!!!!


               FULL SECURITY & BEST PRACTICES CONFIGURATION DONE! :D
              
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
!
!
!
!
!
end
WR
!
reload
!
exit
!
!
!

```

---

## ROUTER-1 >> `Fz3r0_R1` 

- **NOTES:**

    - Basic Setup for Routing the VLANs and subnets within this LAN
        
        - **BONUS: It support DHCP Relay Agent! :D**
            - This router is the DHCP Relay Agent for the DHCP Server in this LAN
            - This means the server can serve all the VLANs and solve DHCP for different subnets due to `ip-helper`  

```
enable
configure terminal 
!
no ip domain-lookup
ip domain-name <<_Fz3r0.Layer2_Security_&_BestPractices.configs_>>
!
hostname Fz3r0_R1
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


         fz3r0 - ROUTER 1:  Only authorized access!!!!


                 THIS IS JUST A BASIC ROUTER CONFIG FOR THIS LAB:
              

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
interface range g0/0 - 2
description << Unused Router Ports >>
shutdown
exit
!
interface gigabitEthernet 0/0
description << Connect SUB-Interfaces 10,20,30,40,69,99,100,101 >>
no shutdown
exit
!
interface gigabitEthernet 0/0.10
description << Connect to Subnet 10 >>
encapsulation dot1Q 10
ip address 192.168.10.254 255.255.255.0
ip helper-address 192.168.101.1
no shutdown 
exit
!
interface gigabitEthernet 0/0.20
description << Connect to Subnet 20 >>
encapsulation dot1Q 20
ip address 192.168.20.254 255.255.255.0
ip helper-address 192.168.101.1
no shutdown 
exit
!
interface gigabitEthernet 0/0.30
description << Connect to Subnet 30 >>
encapsulation dot1Q 30
ip address 192.168.30.254 255.255.255.0
ip helper-address 192.168.101.1
no shutdown 
exit
!
interface gigabitEthernet 0/0.40
description << Connect to Subnet 40 >>
encapsulation dot1Q 40
ip address 192.168.40.254 255.255.255.0
ip helper-address 192.168.101.1
no shutdown 
exit
!
interface gigabitEthernet 0/0.69
description << Connect to Subnet 69 >>
encapsulation dot1Q 69
ip address 192.168.69.254 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.99
description << Connect to Subnet 99 >>
encapsulation dot1Q 99
ip address 192.168.99.254 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.100
description << Connect to Subnet 100 >>
encapsulation dot1Q 100
ip address 192.168.100.254 255.255.255.0
no shutdown 
exit
!
interface gigabitEthernet 0/0.101
description << Connect to Subnet 101 >>
encapsulation dot1Q 101
ip address 192.168.101.254 255.255.255.0
no shutdown 
exit
!
interface loopback 0
description << loopback 10.10.10.10 >>
ip address 10.10.10.10 255.255.255.255
exit
!
!
interface loopback 100
description << GOOGLE SIMULATION >>
ip address 8.8.8.8 255.255.255.255
exit
!
interface loopback 101
description << CLOUDFLARE SIMULATION >>
ip address 1.1.1.1 255.255.255.255
exit
!
interface loopback 102
description << FZ3R0.GOV SIMULATION >>
ip address 6.6.6.6 255.255.255.255
exit
!
!
!
!
banner motd #

=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=


         fz3r0 - Router1:  Only authorized access!!!!


               FULL SECURITY & BEST PRACTICES CONFIGURATION DONE! :D
              
           
         Twitter @fz3r0_Ops
         Github  Fz3r0  


=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#
!
!
!
end
WR
!
reload
!
exit
!
!
!

```

---

## DHCP SERVER 

![image](https://user-images.githubusercontent.com/94720207/168209042-41b537c9-1016-4285-aade-3c93bd7ebca5.png)


---

### References

- https://www.youtube.com/watch?v=Ekr0vXDnlrM
