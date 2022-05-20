
---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169432767-1e87baf5-db18-4c5e-9b8c-a4d0acf1c83e.png)

- ![image](https://user-images.githubusercontent.com/94720207/169433751-06697c6d-d27a-451f-8afb-1b7fba777dac.png)

---

### Accesing Files

1. First I will check that `FTP` port accesing with `anonymous` login and download the `chatserver.exe` and the `essfunc.dll` from it
    
    - ![image](https://user-images.githubusercontent.com/94720207/169436929-93cad986-8310-402d-aa84-c4f39d72d45c.png)
    
2. As this is a buffer overflow Lab, it seems we got out `.exe` and `.dll` to exploit, so, nothing much more to do here...
    
    - Note: It's a little bit obvious that this room is based on the "Vuln Server" exploit, using default port 9999 and `essfunc.dll`...
        
    - [**Click here to read the full write up I did of `Vuln Server`**](/Cyber-Security-&-Hacking/Buffer-Overflow/buffer-overflow.md)
    
        - I will use the same setup for `Vuln Server`:
        
            - Using Windows 10 Pro on a bare metal CPU
            - Using Kali Linux in a VMware Pro VM
        
        - So I will transfer the files to a folder to the Windows 10 and use from there `Immunity Debugger` and also run the `chatserver.exe` binary.
        
            - ![image](https://user-images.githubusercontent.com/94720207/169447433-211b2e85-534b-4bd5-9f2f-ff799b1472d1.png)
          
        - Easy! 

---

### Buffer Overflow

- I will use the same steps used in `Vuln Server` lab... this steps work with allmost all the buffer overflow procedures:

- **Steps to conduct a buffer overflow:**

    1. Spiking - Method to find vuln part of the program
    2. Fuzzing - Send a bunch of characters and see if we can break it
    3. Finding the Offset - At what point did we break it
    4. Overwriting the EIP - Overwriting the Poiting Address and control it
    5. Finding Bad Characters - ...
    6. Finding the Right Module - ...
    7. Generating Shellcode - Once we know the bad characters and right module we can generate a shellcode
    8. Root!

---

### Spiking

- First of all, I will run `chatserver.exe` as administrator and then start `Immunity Debugger` and attach the program. 
    
    - ![image](https://user-images.githubusercontent.com/94720207/169447906-08c9b9a4-ae4a-4634-801f-260fe36a3f63.png) 

    - ![image](https://user-images.githubusercontent.com/94720207/169447827-45f81402-77c1-4a3e-af73-bae1465a264d.png)

- Then, I will run the Immunity Debugger with "play".

    - ![image](https://user-images.githubusercontent.com/94720207/169448256-98b7a075-5faf-466c-a79b-0845450d1362.png)

        - Running and ready to go!

- On Kali Linux:

    1. Connect to ChatServer:
        
        - Using the IP Address of the Windows Machine **192.168.10.100** + VulnServer Port **9999** (Default)
            
        - ![image](https://user-images.githubusercontent.com/94720207/169188519-02fab4e5-91e4-4272-a788-9239ad878c4a.png)
           
        - On Kali: `nc -nv 192.168.1.100 9999`
            
        - ![image](https://user-images.githubusercontent.com/94720207/169448471-a117bef5-2d59-40e8-9a37-19f0aeb3b263.png)
 

---

### References

- https://www.youtube.com/watch?v=T1-Sds8ZHBU
