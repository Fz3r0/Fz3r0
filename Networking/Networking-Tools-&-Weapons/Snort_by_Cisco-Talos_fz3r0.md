Hello moto


---

### Intro

- **SNORT** is an open-source, rule-based **Network Intrusion Detection and Prevention System (NIDS/NIPS)**. 

- It was developed and still maintained by Martin Roesch, open-source contributors, and the **Cisco Talos team**. 

- The official description: 

    - "Snort is the foremost Open Source Intrusion Prevention System (IPS) in the world. Snort IPS uses a series of rules that help define malicious network activity and uses those rules to find packets that match against them and generate alerts for users."

### Traffic Generator 

- The machine is offline, but there is a script `traffic-generator.sh` for you to generate traffic to your `snort` interface.

    - Bash script: 

```bash
#!/bin/bash
selection=$(zenity --list \
"1) ICMP Traffic" \
"2) HTTP Traffic" \
"3) TASK-6 Exercise" \
"4) TASK-7 Exercise" \
"5) TASK-10 IPS Exercise - Port 4444 Traffic" \
"6) TASK-10 IPS Exercise - Torrent Traffic" \
 --column="" --text="Select a traffic pattern to feed the pig!" --title="Traffic Generator" --width=450 --height=450)
case "$selection" in
"1) ICMP Traffic")gnome-terminal --hide-menubar --title="ICMP Traffic" --geometry=120x32 -e 'tcpreplay -v --mbps=0.005 -i eth0 /home/ubuntu/Desktop/Task-Exercises/.traffic-generator-source/icmp-test.pcap';;
"2) HTTP Traffic")gnome-terminal --hide-menubar --title="HTTP Traffic" --geometry=120x32 -e 'tcpreplay -v --mbps=0.03 -i eth0 /home/ubuntu/Desktop/Task-Exercises/.traffic-generator-source/mx-1.pcap';;
"3) TASK-6 Exercise")gnome-terminal --hide-menubar --title="TASK-6 Exercise" --geometry=120x32 -e 'tcpreplay -v --mbps=0.03 -i eth0 /home/ubuntu/Desktop/Task-Exercises/.traffic-generator-source/mx-1.pcap';;
"4) TASK-7 Exercise")gnome-terminal --hide-menubar --title="TASK-7 Exercise" --geometry=120x32 -e 'tcpreplay -v --mbps=0.03 -i eth0 /home/ubuntu/Desktop/Task-Exercises/.traffic-generator-source/mx-1.pcap';;
"5) TASK-10 IPS Exercise - Port 4444 Traffic")gnome-terminal --hide-menubar --title="TASK-10 IPS - ICMP Traffic" --geometry=120x32 -e 'tcpreplay -v --mbps=0.007 -i eth0 /home/ubuntu/Desktop/Task-Exercises/.traffic-generator-source/44m.pcap';;
"6) TASK-10 IPS Exercise - Torrent Traffic")gnome-terminal --hide-menubar --title="TASK-10 IPS - Torrent Traffic" --geometry=120x32 -e 'tcpreplay -v --mbps=0.009 -i eth0 /home/ubuntu/Desktop/Task-Exercises/.traffic-generator-source/torrent.pcap';;
esac
```

- You will use this script to trigger traffic to the snort interface. 

- Once you run the script, it will ask you to choose the exercise type and then automatically open another terminal to show you the output of the selected action. 

- Run the `traffic generator.sh` file by executing it as `sudo`. 

```
user@ubuntu$ sudo ./traffic-generator.sh
```

- General desktop overview. Traffic generator script in action.

![image](https://user-images.githubusercontent.com/94720207/167321690-020469ea-0297-4361-b70d-eb46d253e7a7.png)

- Once you choose an action, the menu disappears and opens a terminal instance to show you the output of the action.

![image](https://user-images.githubusercontent.com/94720207/167321703-d3816047-ea9c-49fb-849e-f5c50250e063.png)

---

### Introduction to IDS & IPS

![image](https://user-images.githubusercontent.com/94720207/167321847-1d8c926b-936b-4c88-8316-a4834e0228ec.png)

- Before diving into `Snort` and **analysing traffic**, let's have a brief overview of what an **Intrusion Detection System (IDS) and Intrusion Prevention System (IPS)** is. 

- It is possible to configure your network infrastructure and use both of them, but before starting to use any of them, let's learn the differences.

### Intrusion Detection System (IDS)

- **IDS is a passive monitoring solution** for detecting possible malicious activities/patterns, abnormal incidents, and policy violations. 

- It is responsible for generating alerts for each suspicious event.

    - **There are two main types of IDS systems:**

        1. **Network Intrusion Detection System (NIDS)**
            
            - NIDS monitors the traffic flow from various areas of the network. 
            - The aim is to investigate the traffic on the entire subnet. 
            - If a signature is identified, an alert is created.

        2. **Host-based Intrusion Detection System (HIDS)**
        
            - HIDS monitors the traffic flow from a single endpoint device. 
            - The aim is to investigate the traffic on a particular device. 
            - If a signature is identified, an alert is created.  

### Intrusion Prevention System (IPS)

- **IPS is an active protecting solution** for preventing possible malicious activities/patterns, abnormal incidents, and policy violations. 

- It is responsible for stopping/preventing/terminating the suspicious event as soon as the detection is performed.

    - **There are four main types of IPS systems:**

        1. Network Intrusion Prevention System (NIPS)
        
            - NIPS monitors the traffic flow from various areas of the network. 
            - The aim is to protect the traffic on the entire subnet. 
            - If a signature is identified, the connection is terminated.

        2. Behaviour-based Intrusion Prevention System (Network Behaviour Analysis - NBA):
        
            - Behaviour-based systems monitor the traffic flow from various areas of the network. 
            - The aim is to protect the traffic on the entire subnet. 
            - If a signature is identified, the connection is terminated.
        
    - Network Behaviour Analysis System works similar to NIPS. 
    - The difference between NIPS and Behaviour-based is; behaviour based systems require a training period (also known as "baselining") to learn the normal traffic and differentiate the malicious traffic and threats. This model provides more efficient results against new threats.
    - The system is trained to know the "normal" to detect "abnormal". 
    - The training period is crucial to avoid any false positives. 
    - In case of any security breach during the training period, the results will be highly problematic. 
    - Another critical point is to ensure that the system is well trained to recognise benign activities. 
    
        3. Wireless Intrusion Prevention System (WIPS)
        
            - WIPS monitors the traffic flow from of wireless network. 
            - The aim is to protect the wireless traffic and stop possible attacks launched from there. 
            - If a signature is identified, the connection is terminated.

        4. Host-based Intrusion Prevention System (HIPS)
        
            - HIPS actively protects the traffic flow from a single endpoint device. 
            - The aim is to investigate the traffic on a particular device. 
            - If a signature is identified, the connection is terminated.
    
    - **HIPS working mechanism is similar to HIDS.** 
    - **The difference between them is that while HIDS creates alerts for threats, HIPS stops the threats by terminating the connection.**

---

### Detection/Prevention Techniques

- There are three main detection and prevention techniques used in IDS and IPS solutions:

    1. Signature-Based
        - This technique relies on rules that identify the specific patterns of the known malicious behaviour. 
        - This model helps detect known threats. 
    
    2. Behaviour-Based
        - This technique identifies new threats with new patterns that pass through signatures. 
        - The model compares the known/normal with unknown/abnormal behaviours. 
        - This model helps detect previously unknown or new threats.
    
    3. Policy-Based  
        - This technique compares detected activities with system configuration and security policies. 
        - This model helps detect policy violations.
        
---
