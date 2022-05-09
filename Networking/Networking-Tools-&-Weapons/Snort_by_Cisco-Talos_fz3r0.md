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

### Summary 

- Let's summarise the overall functions of the IDS and IPS in a nutshell.

    - **`IDS` can identify threats but require user assistance to stop them.**
    
    - **`IPS` can identify and block the threats with less user assistance at the detection time.**

--- 

### Snort... snort snort! 

- Here is the rest of the official description of the snort:

    - "Snort can be deployed inline to stop these packets, as well. Snort has three primary uses: As a packet sniffer like tcpdump, as a packet logger — which is useful for network traffic debugging, or it can be used as a full-blown network intrusion prevention system. Snort can be downloaded and configured for personal and business use alike."
    
- SNORT is an open-source, rule-based Network Intrusion Detection and Prevention System (NIDS/NIPS). 

- It was developed and still maintained by Martin Roesch, open-source contributors, and the Cisco Talos team.    

![image](https://user-images.githubusercontent.com/94720207/167324514-531d74e7-a315-488d-ba61-560093f4509c.png)

### Capabilities of Snort

- Live traffic analysis
- Attack and probe detection
- Packet logging
- Protocol analysis
- Real-time alerting
- Modules & plugins
- Pre-processors
- Cross-platform support! (Linux & Windows)

    - **Snort has three main use models:**

        1. `Sniffer Mode` - Read IP packets and prompt them in the console application.

        2. `Packet Logger Mode` - Log all IP packets (inbound and outbound) that visit the network.

        3. `NIDS` (Network Intrusion Detection System) and `NIPS` (Network Intrusion Prevention System) Modes - Log/drop the packets that are deemed as malicious according to the user-defined rules.
        
---

### The First Interaction with Snort

- First, let's verify snort is installed. The following command will show you the instance version.

- `snort -V` 

```
fz3r0@kali$ snort -V

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.7.0 GRE (Build XXXXXX) 
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.9.1 (with TPACKET_V3)
           Using PCRE version: 8.39 2016-06-14
           Using ZLIB version: 1.2.11
```           

- **Before getting your hands dirty, we should ensure our configuration file is valid.**

    - Here `-T` is used for testing configuration, and `-c` is identifying the configuration file **(snort.conf)**.
    - Note that it is possible to use an additional configuration file by pointing it with `-c`.  

```
fz3r0@kali$ sudo snort -c /etc/snort/snort.conf -T 

        --== Initializing Snort ==--
Initializing Output Plugins!
Initializing Preprocessors!
Initializing Plug-ins!
... [Output truncated]
        --== Initialization Complete ==--

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.7.0 GRE (Build XXXX) 
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.9.1 (with TPACKET_V3)
           Using PCRE version: 8.39 2016-06-14
           Using ZLIB version: 1.2.11

           Rules Engine: SF_SNORT_DETECTION_ENGINE  Version 2.4  
           Preprocessor Object: SF_GTP  Version 1.1  
           Preprocessor Object: SF_SIP  Version 1.1  
           Preprocessor Object: SF_SSH  Version 1.1  
           Preprocessor Object: SF_SMTP  Version 1.1  
           Preprocessor Object: SF_POP  Version 1.0  
           Preprocessor Object: SF_DCERPC2  Version 1.0  
           Preprocessor Object: SF_IMAP  Version 1.0  
           Preprocessor Object: SF_DNP3  Version 1.1  
           Preprocessor Object: SF_SSLPP  Version 1.1  
           Preprocessor Object: SF_MODBUS  Version 1.1  
           Preprocessor Object: SF_SDF  Version 1.1  
           Preprocessor Object: SF_REPUTATION  Version 1.1  
           Preprocessor Object: SF_DNS  Version 1.1  
           Preprocessor Object: SF_FTPTELNET  Version 1.2  
... [Output truncated]
Snort successfully validated the configuration!
Snort exiting
```

- Once we use a configuration file, snort got much more power! 
- The configuration file is an all-in-one management file of the snort. 
- Rules, plugins, detection mechanisms, default actions and output settings are identified here. 
- It is possible to have multiple configuration files for different purposes and cases but can only use one at runtime.

- Note that every time you start the Snort, it will automatically show the default banner and initial information about your setup. 
- You can prevent this by using the `-q` parameter.

| **Parameter**      | **Description**                                                                                        |
|--------------------|--------------------------------------------------------------------------------------------------------|
| **-V / --version** | This parameter provides information about your instance version.                                       |
| **-c**             | Identifying the configuration file                                                                     |
| **-T**             | Snort's self-test parameter, you can test your setup with this parameter.                              |
| **-q**             | Quiet mode prevents snort from displaying the default banner and initial information about your setup. |

- `snort -V` This parameter provides information about your instance version.
 
```
ubuntu@ip-10-10-39-43:/$ sudo snort -V

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.7.0 GRE (Build 149) 
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.9.1 (with TPACKET_V3)
           Using PCRE version: 8.39 2016-06-14
           Using ZLIB version: 1.2.11
```

- `snort -c /etc/snort/snort.conf -T` Test the current instance with "/etc/snort/snort.conf" file and check how many rules are loaded with the current build. 

```
ubuntu@ip-10-10-39-43:/$ snort -c /etc/snort/snortv2.conf -T
Running in Test mode

        --== Initializing Snort ==--
Initializing Output Plugins!
Initializing Preprocessors!
Initializing Plug-ins!
Parsing Rules file "/etc/snort/snortv2.conf"
PortVar 'HTTP_PORTS' defined :  [ 80:81 311 383 591 593 901 1220 1414 1741 1830 2301 2381 2809 3037 3128 3702 4343 4848 5250 6988 7000:7001 7144:7145 7510 7777 7779 8000 8008 8014 8028 8080 8085 8088 8090 8118 8123 8180:8181 8243 8280 8300 8800 8888 8899 9000 9060 9080 9090:9091 9443 9999 11371 34443:34444 41080 50002 55555 ]
PortVar 'SHELLCODE_PORTS' defined :  [ 0:79 81:65535 ]
PortVar 'ORACLE_PORTS' defined :  [ 1024:65535 ]
PortVar 'SSH_PORTS' defined :  [ 22 ]
PortVar 'FTP_PORTS' defined :  [ 21 2100 3535 ]
PortVar 'SIP_PORTS' defined :  [ 5060:5061 5600 ]
PortVar 'FILE_DATA_PORTS' defined :  [ 80:81 110 143 311 383 591 593 901 1220 1414 1741 1830 2301 2381 2809 3037 3128 3702 4343 4848 5250 6988 7000:7001 7144:7145 7510 7777 7779 8000 8008 8014 8028 8080 8085 8088 8090 8118 8123 8180:8181 8243 8280 8300 8800 8888 8899 9000 9060 9080 9090:9091 9443 9999 11371 34443:34444 41080 50002 55555 ]
PortVar 'GTP_PORTS' defined :  [ 2123 2152 3386 ]
Detection:
   Search-Method = AC-Full-Q
    Split Any/Any group = enabled
    Search-Method-Optimizations = enabled
    Maximum pattern length = 20
Tagged Packet Limit: 256
Loading dynamic engine /usr/lib/snort_dynamicengine/libsf_engine.so... done
Loading all dynamic detection libs from /usr/lib/snort_dynamicrules...
WARNING: No dynamic libraries found in directory /usr/lib/snort_dynamicrules.
  Finished Loading all dynamic detection libs from /usr/lib/snort_dynamicrules
Loading all dynamic preprocessor libs from /usr/lib/snort_dynamicpreprocessor/...
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_ssl_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_sip_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_imap_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_smtp_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_reputation_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_ftptelnet_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_dce2_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_sdf_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_modbus_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_gtp_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_dns_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_dnp3_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_ssh_preproc.so... done
  Loading dynamic preprocessor library /usr/lib/snort_dynamicpreprocessor//libsf_pop_preproc.so... done
  Finished Loading all dynamic preprocessor libs from /usr/lib/snort_dynamicpreprocessor/
Log directory = /var/log/snort
WARNING: ip4 normalizations disabled because not inline.
WARNING: tcp normalizations disabled because not inline.
WARNING: icmp4 normalizations disabled because not inline.
WARNING: ip6 normalizations disabled because not inline.
WARNING: icmp6 normalizations disabled because not inline.
Frag3 global config:
    Max frags: 65536
    Fragment memory cap: 4194304 bytes
Frag3 engine config:
    Bound Address: default
    Target-based policy: WINDOWS
    Fragment timeout: 180 seconds
    Fragment min_ttl:   1
    Fragment Anomalies: Alert
    Overlap Limit:     10
    Min fragment Length:     100
      Max Expected Streams: 768
Stream global config:
    Track TCP sessions: ACTIVE
    Max TCP sessions: 262144
    TCP cache pruning timeout: 30 seconds
    TCP cache nominal timeout: 3600 seconds
    Memcap (for reassembly packet storage): 8388608
    Track UDP sessions: ACTIVE
    Max UDP sessions: 131072
    UDP cache pruning timeout: 30 seconds
    UDP cache nominal timeout: 180 seconds
    Track ICMP sessions: INACTIVE
    Track IP sessions: INACTIVE
    Log info if session memory consumption exceeds 1048576
    Send up to 2 active responses
    Wait at least 5 seconds between responses
    Protocol Aware Flushing: ACTIVE
        Maximum Flush Point: 16000
Stream TCP Policy config:
    Bound Address: default
    Reassembly Policy: WINDOWS
    Timeout: 180 seconds
    Limit on TCP Overlaps: 10
    Maximum number of bytes to queue per session: 1048576
    Maximum number of segs to queue per session: 2621
    Options:
        Require 3-Way Handshake: YES
        3-Way Handshake Timeout: 180
        Detect Anomalies: YES
    Reassembly Ports:
      21 client (Footprint) 
      22 client (Footprint) 
      23 client (Footprint) 
      25 client (Footprint) 
      42 client (Footprint) 
      53 client (Footprint) 
      79 client (Footprint) 
      80 client (Footprint) server (Footprint)
      81 client (Footprint) server (Footprint)
      109 client (Footprint) 
      110 client (Footprint) 
      111 client (Footprint) 
      113 client (Footprint) 
      119 client (Footprint) 
      135 client (Footprint) 
      136 client (Footprint) 
      137 client (Footprint) 
      139 client (Footprint) 
      143 client (Footprint) 
      161 client (Footprint) 
      additional ports configured but not printed.
Stream UDP Policy config:
    Timeout: 180 seconds
HttpInspect Config:
    GLOBAL CONFIG
      Detect Proxy Usage:       NO
      IIS Unicode Map Filename: /etc/snort/unicode.map
      IIS Unicode Map Codepage: 1252
      Memcap used for logging URI and Hostname: 150994944
      Max Gzip Memory: 104857600
      Max Gzip Sessions: 201649
      Gzip Compress Depth: 65535
      Gzip Decompress Depth: 65535
    DEFAULT SERVER CONFIG:
      Server profile: All
      Ports (PAF): 80 81 311 383 591 593 901 1220 1414 1741 1830 2301 2381 2809 3037 3128 3702 4343 4848 5250 6988 7000 7001 7144 7145 7510 7777 7779 8000 8008 8014 8028 8080 8085 8088 8090 8118 8123 8180 8181 8243 8280 8300 8800 8888 8899 9000 9060 9080 9090 9091 9443 9999 11371 34443 34444 41080 50002 55555 
      Server Flow Depth: 0
      Client Flow Depth: 0
      Max Chunk Length: 500000
      Small Chunk Length Evasion: chunk size <= 10, threshold >= 5 times
      Max Header Field Length: 750
      Max Number Header Fields: 100
      Max Number of WhiteSpaces allowed with header folding: 200
      Inspect Pipeline Requests: YES
      URI Discovery Strict Mode: NO
      Allow Proxy Usage: NO
      Disable Alerting: NO
      Oversize Dir Length: 500
      Only inspect URI: NO
      Normalize HTTP Headers: NO
      Inspect HTTP Cookies: YES
      Inspect HTTP Responses: YES
      Extract Gzip from responses: YES
      Decompress response files:   
      Unlimited decompression of gzip data from responses: YES
      Normalize Javascripts in HTTP Responses: YES
      Max Number of WhiteSpaces allowed with Javascript Obfuscation in HTTP responses: 200
      Normalize HTTP Cookies: NO
      Enable XFF and True Client IP: NO
      Log HTTP URI data: NO
      Log HTTP Hostname data: NO
      Extended ASCII code support in URI: NO
      Ascii: YES alert: NO
      Double Decoding: YES alert: NO
      %U Encoding: YES alert: YES
      Bare Byte: YES alert: NO
      UTF 8: YES alert: NO
      IIS Unicode: YES alert: NO
      Multiple Slash: YES alert: NO
      IIS Backslash: YES alert: NO
      Directory Traversal: YES alert: NO
      Web Root Traversal: YES alert: NO
      Apache WhiteSpace: YES alert: NO
      IIS Delimiter: YES alert: NO
      IIS Unicode Map: GLOBAL IIS UNICODE MAP CONFIG
      Non-RFC Compliant Characters: 0x00 0x01 0x02 0x03 0x04 0x05 0x06 0x07 
      Whitespace Characters: 0x09 0x0b 0x0c 0x0d 
rpc_decode arguments:
    Ports to decode RPC on: 111 32770 32771 32772 32773 32774 32775 32776 32777 32778 32779 
    alert_fragments: INACTIVE
    alert_large_fragments: INACTIVE
    alert_incomplete: INACTIVE
    alert_multiple_requests: INACTIVE
FTPTelnet Config:
    GLOBAL CONFIG
      Inspection Type: stateful
      Check for Encrypted Traffic: YES alert: NO
      Continue to check encrypted data: YES
    TELNET CONFIG:
      Ports: 23 
      Are You There Threshold: 20
      Normalize: YES
      Detect Anomalies: YES
    FTP CONFIG:
      FTP Server: default
        Ports (PAF): 21 2100 3535 
        Check for Telnet Cmds: YES alert: YES
        Ignore Telnet Cmd Operations: YES alert: YES
        Ignore open data channels: NO
      FTP Client: default
        Check for Bounce Attacks: YES alert: YES
        Check for Telnet Cmds: YES alert: YES
        Ignore Telnet Cmd Operations: YES alert: YES
        Max Response Length: 256
SMTP Config:
    Ports: 25 465 587 691 
    Inspection Type: Stateful
    Normalize: ATRN AUTH BDAT DATA DEBUG EHLO EMAL ESAM ESND ESOM ETRN EVFY EXPN HELO HELP IDENT MAIL NOOP ONEX QUEU QUIT RCPT RSET SAML SEND STARTTLS SOML TICK TIME TURN TURNME VERB VRFY X-EXPS XADR XAUTH XCIR XEXCH50 XGEN XLICENSE X-LINK2STATE XQUE XSTA XTRN XUSR CHUNKING X-ADAT X-DRCP X-ERCP X-EXCH50 
    Ignore Data: No
    Ignore TLS Data: No
    Ignore SMTP Alerts: No
    Max Command Line Length: 512
    Max Specific Command Line Length: 
       ATRN:255 AUTH:246 BDAT:255 DATA:246 DEBUG:255 
       EHLO:500 EMAL:255 ESAM:255 ESND:255 ESOM:255 
       ETRN:246 EVFY:255 EXPN:255 HELO:500 HELP:500 
       IDENT:255 MAIL:260 NOOP:255 ONEX:246 QUEU:246 
       QUIT:246 RCPT:300 RSET:246 SAML:246 SEND:246 
       SIZE:255 STARTTLS:246 SOML:246 TICK:246 TIME:246 
       TURN:246 TURNME:246 VERB:246 VRFY:255 X-EXPS:246 
       XADR:246 XAUTH:246 XCIR:246 XEXCH50:246 XGEN:246 
       XLICENSE:246 X-LINK2STATE:246 XQUE:246 XSTA:246 XTRN:246 
       XUSR:246 
    Max Header Line Length: 1000
    Max Response Line Length: 512
    X-Link2State Alert: Yes
    Drop on X-Link2State Alert: No
    Alert on commands: None
    Alert on unknown commands: No
    SMTP Memcap: 838860
    MIME Max Mem: 838860
    Base64 Decoding: Enabled
    Base64 Decoding Depth: Unlimited
    Quoted-Printable Decoding: Enabled
    Quoted-Printable Decoding Depth: Unlimited
    Unix-to-Unix Decoding: Enabled
    Unix-to-Unix Decoding Depth: Unlimited
    Non-Encoded MIME attachment Extraction: Enabled
    Non-Encoded MIME attachment Extraction Depth: Unlimited
    Log Attachment filename: Enabled
    Log MAIL FROM Address: Enabled
    Log RCPT TO Addresses: Enabled
    Log Email Headers: Enabled
    Email Hdrs Log Depth: 1464
SSH config: 
    Autodetection: ENABLED
    Challenge-Response Overflow Alert: ENABLED
    SSH1 CRC32 Alert: ENABLED
    Server Version String Overflow Alert: ENABLED
    Protocol Mismatch Alert: ENABLED
    Bad Message Direction Alert: DISABLED
    Bad Payload Size Alert: DISABLED
    Unrecognized Version Alert: DISABLED
    Max Encrypted Packets: 20  
    Max Server Version String Length: 100  
    MaxClientBytes: 19600 (Default) 
    Ports:
	22
DCE/RPC 2 Preprocessor Configuration
  Global Configuration
    DCE/RPC Defragmentation: Enabled
    Memcap: 102400 KB
    Events: co 
    SMB Fingerprint policy: Disabled
  Server Default Configuration
    Policy: WinXP
    Detect ports (PAF)
      SMB: 139 445 
      TCP: 135 
      UDP: 135 
      RPC over HTTP server: 593 
      RPC over HTTP proxy: None
    Autodetect ports (PAF)
      SMB: None
      TCP: 1025-65535 
      UDP: 1025-65535 
      RPC over HTTP server: 1025-65535 
      RPC over HTTP proxy: None
    Invalid SMB shares: C$ D$ ADMIN$ 
    Maximum SMB command chaining: 3 commands
    SMB file inspection: Disabled
DNS config: 
    DNS Client rdata txt Overflow Alert: ACTIVE
    Obsolete DNS RR Types Alert: INACTIVE
    Experimental DNS RR Types Alert: INACTIVE
    Ports: 53
SSLPP config:
    Encrypted packets: not inspected
    Ports:
      443      465      563      636      989
      992      993      994      995     7801
     7802     7900     7901     7902     7903
     7904     7905     7906     7907     7908
     7909     7910     7911     7912     7913
     7914     7915     7916     7917     7918
     7919     7920
    Server side data is trusted
    Maximum SSL Heartbeat length: 0
Sensitive Data preprocessor config: 
    Global Alert Threshold: 25
    Masked Output: DISABLED
SIP config: 
    Max number of sessions: 40000  
    Max number of dialogs in a session: 4 (Default) 
    Status: ENABLED
    Ignore media channel: DISABLED
    Max URI length: 512  
    Max Call ID length: 80  
    Max Request name length: 20 (Default) 
    Max From length: 256 (Default) 
    Max To length: 256 (Default) 
    Max Via length: 1024 (Default) 
    Max Contact length: 512  
    Max Content length: 2048  
    Ports:
	5060	5061	5600
    Methods:
	  invite cancel ack bye register options refer subscribe update join info message notify benotify do qauth sprack publish service unsubscribe prack
IMAP Config:
    Ports: 143 
    IMAP Memcap: 838860
    MIME Max Mem: 838860
    Base64 Decoding: Enabled
    Base64 Decoding Depth: Unlimited
    Quoted-Printable Decoding: Enabled
    Quoted-Printable Decoding Depth: Unlimited
    Unix-to-Unix Decoding: Enabled
    Unix-to-Unix Decoding Depth: Unlimited
    Non-Encoded MIME attachment Extraction: Enabled
    Non-Encoded MIME attachment Extraction Depth: Unlimited
POP Config:
    Ports: 110 
    POP Memcap: 838860
    MIME Max Mem: 838860
    Base64 Decoding: Enabled
    Base64 Decoding Depth: Unlimited
    Quoted-Printable Decoding: Enabled
    Quoted-Printable Decoding Depth: Unlimited
    Unix-to-Unix Decoding: Enabled
    Unix-to-Unix Decoding Depth: Unlimited
    Non-Encoded MIME attachment Extraction: Enabled
    Non-Encoded MIME attachment Extraction Depth: Unlimited
Modbus config: 
    Ports:
	502
DNP3 config: 
    Memcap: 262144
    Check Link-Layer CRCs: ENABLED
    Ports:
	20000

+++++++++++++++++++++++++++++++++++++++++++++++++++
Initializing rule chains...
1 Snort rules read
    1 detection rules
    0 decoder rules
    0 preprocessor rules
1 Option Chains linked into 1 Chain Headers
0 Dynamic rules
+++++++++++++++++++++++++++++++++++++++++++++++++++

+-------------------[Rule Port Counts]---------------------------------------
|             tcp     udp    icmp      ip
|     src       0       0       0       0
|     dst       0       0       0       0
|     any       0       0       1       0
|      nc       0       0       1       0
|     s+d       0       0       0       0
+----------------------------------------------------------------------------

+-----------------------[detection-filter-config]------------------------------
| memory-cap : 1048576 bytes
+-----------------------[detection-filter-rules]-------------------------------
| none
-------------------------------------------------------------------------------

+-----------------------[rate-filter-config]-----------------------------------
| memory-cap : 1048576 bytes
+-----------------------[rate-filter-rules]------------------------------------
| none
-------------------------------------------------------------------------------

+-----------------------[event-filter-config]----------------------------------
| memory-cap : 1048576 bytes
+-----------------------[event-filter-global]----------------------------------
+-----------------------[event-filter-local]-----------------------------------
| none
+-----------------------[suppression]------------------------------------------
| none
-------------------------------------------------------------------------------
Rule application order: activation->dynamic->pass->drop->sdrop->reject->alert->log
Verifying Preprocessor Configurations!

[ Port Based Pattern Matching Memory ]
[ Number of patterns truncated to 20 bytes: 0 ]
ERROR: Active response: can't open ip!
Fatal Error, Quitting..

```

### Operation Mode 1: Sniffer Mode

![image](https://user-images.githubusercontent.com/94720207/167327315-6094c97b-8608-4458-93e3-0a751904257f.png)

- **Let's run Snort in Sniffer Mode**

- Like `tcpdump`, `Snort` has various flags capable of viewing various data about the packet it is ingesting.

    - `Sniffer mode **parameters**` are explained in the table below:

| **Parameter** | **Description **                              |
|---------------|------------------------------------------------------------------|
| **-v**        | Verbose. Display the TCP/IP output in the console.                               |
| **-d**        | Display the packet data (payload).      |
| **-e**        | Display the link-layer (TCP/IP/UDP/ICMP) headers.      |
| **-X**        | Display the full packet details in HEX.    |
| **-i**        | This parameter helps to define a specific network interface to listen/sniff. Once you have multiple interfaces, you can choose a specific interface to sniff.  |

- Let's start using each parameter and see the difference between them. 
- Snort needs active traffic on your interface, so we need to generate traffic to see Snort in action.

    - **To do this, use the traffic-generator script**

### Sniffing with parameter `-i`

- Start the Snort instance in verbose mode `-v` and use the interface `-i` `eth0`:
    
    - `sudo snort -v-i eth0` 

- In case you have only one interface, Snort uses it by default. 
- The above example demonstrates to sniff on the interface named "eth0". Once you simulate the parameter -v, you will notice it will automatically use the "eth0" interface and prompt it.

```
ubuntu@ip-10-10-39-43:~/Desktop/Task-Exercises$ sudo snort -v -i eth0
Running in packet dump mode

        --== Initializing Snort ==--
Initializing Output Plugins!
pcap DAQ configured to passive.
Acquiring network traffic from "eth0".
Decoding Ethernet

        --== Initialization Complete ==--

   ,,_     -*> Snort! <*-
  o"  )~   Version 2.9.7.0 GRE (Build 149) 
   ''''    By Martin Roesch & The Snort Team: http://www.snort.org/contact#team
           Copyright (C) 2014 Cisco and/or its affiliates. All rights reserved.
           Copyright (C) 1998-2013 Sourcefire, Inc., et al.
           Using libpcap version 1.9.1 (with TPACKET_V3)
           Using PCRE version: 8.39 2016-06-14
           Using ZLIB version: 1.2.11

Commencing packet processing (pid=2013)
05/09-02:12:54.021378 10.10.39.43:80 -> 10.100.1.202:60266
TCP TTL:64 TOS:0x0 ID:48838 IpLen:20 DgmLen:52 DF
***A**** Seq: 0x54CF68E  Ack: 0xD2E232FF  Win: 0x1BA  TcpLen: 32
TCP Options (3) => NOP NOP TS: 980332753 2814672190 
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

WARNING: No preprocessors configured for policy 0.
05/09-02:12:54.042983 10.100.1.202:60266 -> 10.10.39.43:80
TCP TTL:64 TOS:0x0 ID:57493 IpLen:20 DgmLen:84 DF
***AP*** Seq: 0xD2E232FF  Ack: 0x54CF68E  Win: 0x232D  TcpLen: 32
TCP Options (3) => NOP NOP TS: 2814672254 980332753 
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

.
.
.
.
.
.

WARNING: No preprocessors configured for policy 0.
05/09-02:12:54.915745 10.100.1.202:60266 -> 10.10.39.43:80
TCP TTL:64 TOS:0x0 ID:57506 IpLen:20 DgmLen:52 DF
***A**** Seq: 0xD2E233BF  Ack: 0x54DF2F0  Win: 0x232D  TcpLen: 32
TCP Options (3) => NOP NOP TS: 2814673127 980333647 
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

^C*** Caught Int-Signal
(snort_decoder) WARNING: IP dgm len > captured len
WARNING: No preprocessors configured for policy 0.
===============================================================================
Run time for packet processing was 2.39734 seconds
Snort processed 27 packets.
Snort ran for 0 days 0 hours 0 minutes 2 seconds
   Pkts/sec:           13
===============================================================================
Memory usage summary:
  Total non-mmapped bytes (arena):       786432
  Bytes in mapped regions (hblkhd):      12906496
  Total allocated space (uordblks):      679312
  Total free space (fordblks):           107120
  Topmost releasable block (keepcost):   105344
===============================================================================
Packet I/O Totals:
   Received:           80
   Analyzed:           27 ( 33.750%)
    Dropped:            0 (  0.000%)
   Filtered:            0 (  0.000%)
Outstanding:           53 ( 66.250%)
   Injected:            0
===============================================================================
Breakdown by protocol (includes rebuilt packets):
        Eth:           27 (100.000%)
       VLAN:            0 (  0.000%)
        IP4:           27 (100.000%)
       Frag:            0 (  0.000%)
       ICMP:            0 (  0.000%)
        UDP:            0 (  0.000%)
        TCP:           22 ( 81.481%)
        IP6:            0 (  0.000%)
    IP6 Ext:            0 (  0.000%)
   IP6 Opts:            0 (  0.000%)
      Frag6:            0 (  0.000%)
      ICMP6:            0 (  0.000%)
       UDP6:            0 (  0.000%)
       TCP6:            0 (  0.000%)
     Teredo:            0 (  0.000%)
    ICMP-IP:            0 (  0.000%)
    IP4/IP4:            0 (  0.000%)
    IP4/IP6:            0 (  0.000%)
    IP6/IP4:            0 (  0.000%)
    IP6/IP6:            0 (  0.000%)
        GRE:            0 (  0.000%)
    GRE Eth:            0 (  0.000%)
   GRE VLAN:            0 (  0.000%)
    GRE IP4:            0 (  0.000%)
    GRE IP6:            0 (  0.000%)
GRE IP6 Ext:            0 (  0.000%)
   GRE PPTP:            0 (  0.000%)
    GRE ARP:            0 (  0.000%)
    GRE IPX:            0 (  0.000%)
   GRE Loop:            0 (  0.000%)
       MPLS:            0 (  0.000%)
        ARP:            0 (  0.000%)
        IPX:            0 (  0.000%)
   Eth Loop:            0 (  0.000%)
   Eth Disc:            0 (  0.000%)
   IP4 Disc:            5 ( 18.519%)
   IP6 Disc:            0 (  0.000%)
   TCP Disc:            0 (  0.000%)
   UDP Disc:            0 (  0.000%)
  ICMP Disc:            0 (  0.000%)
All Discard:            5 ( 18.519%)
      Other:            0 (  0.000%)
Bad Chk Sum:            8 ( 29.630%)
    Bad TTL:            0 (  0.000%)
     S5 G 1:            0 (  0.000%)
     S5 G 2:            0 (  0.000%)
      Total:           27
===============================================================================
Snort exiting
ubuntu@ip-10-10-39-43:~/Desktop/Task-Exercises$

```
---

### Sniffing with parameter `-v`

- Start the Snort instance in verbose mode `-v`: 

    - `sudo snort -v`

- Now run the traffic-generator script as sudo and start `ICMP/HTTP` traffic. 

- Once the traffic is generated, snort will start showing the  packets in verbosity mode as follows:

```
user@ubuntu$ sudo snort -v
                             
Running in packet dump mode

        --== Initializing Snort ==--
...
Commencing packet processing (pid=64)
12/01-20:10:13.846653 192.168.175.129:34316 -> 192.168.175.2:53
UDP TTL:64 TOS:0x0 ID:23826 IpLen:20 DgmLen:64 DF
Len: 36
=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+

12/01-20:10:13.846794 192.168.175.129:38655 -> 192.168.175.2:53
UDP TTL:64 TOS:0x0 ID:23827 IpLen:20 DgmLen:64 DF
Len: 36
===============================================================================
.
.
.
.
.
Snort exiting
```

- As you can see in the given output, verbosity mode provides tcpdump like output information. Once we interrupt the sniffing with CTRL+C, it stops and summarises the sniffed packets.

### Sniffing with parameter `-d`

- Start the Snort instance in dumping packet data mode `-d`

    - `sudo snort -d`

