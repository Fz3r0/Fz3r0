


---

### Before anything else!!!

- This room will cover the Printnightmare vulnerability from a offensive and defensive perspective.

    - Per Microsoft: 
    
        - **A remote code execution vulnerability exists when the Windows Print Spooler service improperly performs privileged file operations.** 
    
        - **An attacker who successfully exploited this vulnerability could run arbitrary code with SYSTEM privileges.** 
    
        - **An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights.**

    - Learning Objectives: 
        
        - In this room, you will learn what PrintNightmare vulnerability is, how to exploit and mitigate it. 
        
        - You will also learn the detection mechanisms using Windows Event Logs and Wireshark. 

    - Outcome: 
    
        - As a result, you will be ready to defend your organization against any potential PrintNightmare attacks. 

- _Learning Pre-requisites: You should be familiar with Wireshark, Windows Event Logs, Linux Fundamentals, and Meterpreter prior to joining this room._

---

### Windows Print Spooler Service

- Microsoft defines the [Print spooler service](https://docs.microsoft.com/en-us/openspecs/windows_protocols/ms-prsod/7262f540-dd18-46a3-b645-8ea9b59753dc) as a service that runs on each computer system. 

- As you can guess from the name, the Print spooler service manages the printing processes. 

- The Print spooler's responsibilities are managing the print jobs, receiving files to be printed, queueing them, and scheduling.

- You are able to Start/Stop/Pause/Resume the Print Spooler Service by simply navigating to Services on your Windows system:

    - Services:
     
        -  ![image](https://user-images.githubusercontent.com/94720207/167273156-8fce5430-c619-4c64-8d8b-b6b5057c5fa0.png)
     
     - Print Spooler Properties (Services):
     
         - ![image](https://user-images.githubusercontent.com/94720207/167273189-9eacc8ba-8414-4266-8c82-d1cefbb1a2af.png)

- The Print spooler service allows the systems to act as print clients, administrative clients, or print servers. 

- It is also important to note that the Print spooler service is enabled by default in all Windows clients and servers. 

- It's necessary to have a Print spooler service on the computer to connect to a printer. 

- There are third-party software and drivers provided by the printer manufacturers that would not require you to have the Print spooler service enabled. Still, most companies prefer to utilize Print spooler services. 

- Domain Controllers mainly use Print spooler service for printer pruning (the process of removing the printers that are not in use anymore on the network and have been added as objects to Active Directory).

--- 

### Remote Code Execution Vulnerability

- There has been some confusion if the CVE-2021-1675 and CVE-2021-34527 are related to each other. 

- They go under the same name: Windows Print Spooler Remote Code Execution Vulnerability and are both related to the Print Spooler.

- As Microsoft states in the FAQ, the PrintNightmare (CVE-2021-34527) vulnerability _is similar but distinct from the vulnerability that is assigned CVE-2021-1675. The attack vector is different as well."_

- Per Microsoft's definition, PrintNightmare vulnerability is: 
    <ote code execution vulnerability exists when the Windows Print Spooler service improperly performs privileged file operations. An attacker who successfully exploited this vulnerability could run arbitrary code with SYSTEM privileges. An attacker could then install programs; view, change, or delete data; or create new accounts with full user rights.".
