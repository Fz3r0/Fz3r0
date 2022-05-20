
---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169432767-1e87baf5-db18-4c5e-9b8c-a4d0acf1c83e.png)

- ![image](https://user-images.githubusercontent.com/94720207/169433751-06697c6d-d27a-451f-8afb-1b7fba777dac.png)

---

### Accesing Files

1. First I will check that `FTP` port and download the `chatserver.exe` and the `essfunc.dll` from it
    
    - ![image](https://user-images.githubusercontent.com/94720207/169436929-93cad986-8310-402d-aa84-c4f39d72d45c.png)
    
2. As this is a buffer overflow Lab, it seems we got out .exe and .dll to exploit, so, nothing much more to do here
    
    - Note: It's a little obvious right now that this room is based on the "Vuln Server" exploit, using default port 9999 and `essfunc.dll`.
        
    - [**Click here to read the full write up of `Vuln Server`**](/Cyber-Security-&-Hacking/Buffer-Overflow/buffer-overflow.md)
    
        - I will use the same setup for `Vuln Server`:
        
            - Using Windows 10 Pro on a bare metal CPU
            - Using Kali Linux in a VMware Pro VM
        
        - So I will transfer the files to a folder to the Windows 10 and use from there `Immunity Debugger` and also run the `chatserver.exe` binary. 

---
---

### References

https://www.youtube.com/watch?v=T1-Sds8ZHBU&t=1598s
