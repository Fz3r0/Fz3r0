

---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169636811-a9a34ab5-9d7f-42ec-a883-627f1ad94948.png))

- ![image](https://user-images.githubusercontent.com/94720207/169636037-e216bbad-391c-496c-b461-0e2d65dc1b94.png)

- ![image](https://user-images.githubusercontent.com/94720207/169636850-2f3d5382-d440-4761-9dc2-d9acc64dc4d2.png)

- ![image](https://user-images.githubusercontent.com/94720207/169636867-93df1b45-60a1-45d5-85ce-7dd9eb2aac5c.png)


---

### Services Enumeration

- `smbclient -N -L \\\\$ip_target\\`

- ![image](https://user-images.githubusercontent.com/94720207/169636978-f9fc5e1c-08a2-4e13-a051-7b259bcf8ff4.png)

    - **"Users" share is available for login without password, let's sniff inside.**

- `smbclient -N -L \\\\$ip_target\\Users`

    - I've found the executable `gatekeeper.exe` I will download it and prepare the `Buffer Overflow Lab` in my own bare metal Windows 10. 

- ![image](https://user-images.githubusercontent.com/94720207/169637348-142c6a3f-de24-4c58-8bee-b1c7c6046552.png)

---

### Lab Setup:

- I will use the same setup for `Vuln Server`:
        
    - Using Windows 10 Pro on a bare metal CPU
        - `gatekeeper.exe` running here
        - `Immunity Debugger` + `mona` running here
                
    - Using Kali Linux in a VMware Pro VM
        - `python` scripts and tricky tricks running here
            
    - Both machines connected on the same Network 192.168.1.0/24 (My local Network)
            
    - Once I've exploited the program `vulnserver.exe` in my own machine, then I can exploit "the real" server with the final script:
            
        - `TryHackMe - Gatekeeper` Network, UK.    
        
    - So I will transfer the files from the TryHackMe Machine-FTP to a folder to my Windows 10 and use from there `Immunity Debugger` and also run the `chatserver.exe` binary.
        
        - ![image](https://user-images.githubusercontent.com/94720207/169637748-1ae93fc6-73a3-4e21-88ae-14f3e833c142.png)
          
    - Easy! Let's do it! 

---

### Buffer Overflow

- I will use the same steps used in `Vuln Server` lab... this steps work with allmost all the buffer overflow procedures:

- **Steps to conduct a buffer overflow:**

    1. _Spiking - Method to find vuln part of the program_ Not necessary in this Lab
    2. Fuzzing - Send a bunch of characters and see if we can break it
    4. Finding the Offset - At what point did we break it
    5. Overwriting the EIP - Overwriting the Poiting Address and control it
    6. Finding Bad Characters - ...
    7. Finding the Right Module - ...
    8. Generating Shellcode - Once we know the bad characters and right module we can generate a shellcode
    9. Root!

---








---

### References

https://github.com/hamza07-w/gatekeeper-tryHackme-writeup
