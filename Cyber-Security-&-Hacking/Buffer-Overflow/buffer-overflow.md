
### Intro

- Anatomy of the Memory
- Anatomy of the Stack
- Buffer Overflow Walkthrought

### Anatomy of Memory

![image](https://user-images.githubusercontent.com/94720207/169180891-ba8923c4-2493-4ec7-b1b9-00f7d41c9e7c.png)

- We will be focusing on the stack

### Anatomy of the Stack

![image](https://user-images.githubusercontent.com/94720207/169181017-6f10103d-2a74-4fc3-8019-c58f75f6c460.png)

- Buffer characters

![image](https://user-images.githubusercontent.com/94720207/169181180-421ba203-1f62-43f9-b4f8-a3e3f447bcd5.png)

- Buffer Overflow

    - Reaching the EBP & EIP:
      
![image](https://user-images.githubusercontent.com/94720207/169181279-72b722a1-fb3f-4e3b-af8f-e06b649d71d2.png)

### Steps to conduct a buffer overflow

1. Spiking - Method to find vuln part of the program
2. Fuzzing - Send a bunch of characters and see if we can break it
3. Finding the Offset - At what point did we break it
4. Overwriting the EIP - Overwriting the Poiting Address and control it
5. Finding Bad Characters - ...
6. Finding the Right Module - ...
7. Generating Shellcode - Once we know the bad characters and right module we can generate a shellcode
8. Root!

### Tools for the Buffer Overflow Lab

1. Victim Machine: Windows 10 Pro
2. Vulnerable Software: [Vulnserver](https://github.com/stephenbradshaw/vulnserver) Direct Download: [.zip fz3r0 Sp3ci4l :D DOWNLOAD!](https://github.com/Fz3r0/Fz3r0/files/8721984/vulnserver.zip)
3. Attacker Machine: Kali Linux
4. Debugger: [Immunity Debugger](https://debugger.immunityinc.com/ID_register.py) Direct Download: [.zip fz3r0 Sp3ci4l :3 DOWNLOAD!](https://github.com/Fz3r0/Fz3r0/files/8722812/immunity.debugger.zip)

- **Setup**
    
    - Run Windows 10 as Base OS (TURN OFF WINDOWS DEFENDER)
    - VMware Pro Running Kali Linux

---

### Spiking

1. Run vulnserver.exe as Administrator
2. Run Immunity Debugger as Administrator

    - On Immunitu Debugger:

        1. File > Attach > Vuln Server 
            - ![image](https://user-images.githubusercontent.com/94720207/169189657-1fc8ab40-54e7-4323-81af-f6dbb9897d29.png)

            - ![image](https://user-images.githubusercontent.com/94720207/169189603-5ebfccbf-18e9-4439-86d4-aa79ebd7cbc4.png)
        2. Press Play!
        3. Running and ready to go! _(Bottom Right Corner)_
       
            - ![image](https://user-images.githubusercontent.com/94720207/169189986-6b8b761f-a087-4c14-90c2-e9d21eff2a81.png)

3. Run Kali Linux

    - On Kali Linux:

        1. Connect to VulnServer:
        
            - Using the IP Address of the Windows Machine **192.168.10.100** + VulnServer Port **9999** (Default)
            
            - ![image](https://user-images.githubusercontent.com/94720207/169188519-02fab4e5-91e4-4272-a788-9239ad878c4a.png)
           
            - On Kali: `nc -nv 192.168.1.100 9999`
            
            - ![image](https://user-images.githubusercontent.com/94720207/169188968-e1437e10-af9f-4077-a6a7-8356bfe557e4.png)

- **It looks that this program `Vuln Server` take `commands` based on what you type AKA `strings`**

- **Spoiler Alert: TRUN command is vulnerable, but how to know it?!**

    - **To find the vulnerability we do something called `spinking`**
    
    - For example:
    
        - Let's take a command like `STATS` (first on the list)
        - I want to try to send a bunch of characters (like "A") and try to overflow it. 
        - **If we can overflow the command, then the program will `crash`** 
        - **If the program crash, then it's mean it's vulnerable!**
        - _If the command is not vulnerable then we move to the next one..._
    
    - To compare how a vulnerable command looks like VS a non vulnerable command we will compare `STATS`(not vuln) VS `TRUN` vuln, that's the way we will learn how to identify the difference. 

- For spiking we will use a tool called:

    - **`generic_send_tcp`** 

        - Usage:
        
            - `**./generic_send_tcp host port spike_script SKIPVAR SKIPSTR**`
            
| **Instruction**        | **Result**                 |
|------------------------|----------------------------|
| **./generic_send_tcp** | Command                    |
| **host**               | (Target) 192.168.1.100     |
| **port**               | (Target) 9999              |
| **spike_script**       | (Spike File) something.spk |
| **SKIPVAR**            | ()0                        |

### Spike Script

- We will generate a file called "stats.spk"

```
s_readline();              <<<-----| 1. We will read the line
s_string("STATS ");        <<<-----| 2. We will take the string (STATS in this case)
s_string_variable("0");    <<<-----| 3. We will send a variable to the "STATS" string

```

- The trick for the spike is this:
    
    - **We will send variables in all different forms and itterations, for example 1000 at a time, 10K at a time, 100K at a time, etc...** 
    - We do this because we are looking for something to break the program! "Buscando la aguja en el pajar"
    
        - **Spike is sending all kind of different characters randomly to try to break this part of the program**

- Essentialy we can do that exact same process for all the commands, but instead `s_string("STATS ");` it will use another different command like "TRUN": `s_string("TRUN ");` 

- 
 










### References

- https://www.youtube.com/watch?v=qSnPayW6F7U&list=PLLKT__MCUeix3O0DPbmuaRuR_4Hxo4m3G
