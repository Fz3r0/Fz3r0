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
