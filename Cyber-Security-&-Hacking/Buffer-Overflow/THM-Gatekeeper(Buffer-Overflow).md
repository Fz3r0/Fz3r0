

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

- I will use the same setup for `Vuln Server` Lab:
        
    - Using Windows 10 Pro on a bare metal CPU
        - `gatekeeper.exe` running here
        - `Immunity Debugger` + `mona` running here
                
    - Using Kali Linux in a VMware Pro VM
        - `python` scripts and tricky tricks running here
            
    - Both machines connected on the same Network 192.168.1.0/24 (My local Network)
            
    - Once I've exploited the program `gatekeeper.exe` in my own machine, then I can exploit "the real" server with the final script:
            
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

### Fuzzing

- First of all, I will run `gatekeeper.exe` as administrator and then start `Immunity Debugger` and attach the program. 
    
    - ![image](https://user-images.githubusercontent.com/94720207/169637970-252158e3-9967-41e1-a6ac-587a548bde3f.png)

    - ![image](https://user-images.githubusercontent.com/94720207/169637996-c25fa35e-bcd9-4026-b12b-110bc8870e04.png)

- Then, I will run the Immunity Debugger with "play".

    - ![image](https://user-images.githubusercontent.com/94720207/169638036-2ab7bd99-0fea-484a-af2f-7c2e09a96df6.png)

        - Running and ready to go!

- On Kali Linux:

    1. Connect to `gatekeeper.exe`:
        
        - Using the IP Address of the Windows Machine **192.168.10.100** + gatekeeper.exe Port **31337** (We've seen that port on `nmap` typing "help, help, help")
            
        - ![image](https://user-images.githubusercontent.com/94720207/169188519-02fab4e5-91e4-4272-a788-9239ad878c4a.png)
           
        - On Kali: `nc -nv 192.168.1.100 9999`
            
        - ![image](https://user-images.githubusercontent.com/94720207/169638159-af1130de-075d-47b0-b6ab-a43b1ca45838.png)
 
 - **It looks that this program `Gatekeeper` take commands based on what you type AKA `strings` to generate an `answer` with the instruction `Hello ("%variable%")!!!`**
  
     - This means, maybe the buffer overflow and/or the pointer of `EIP` that we need to exploit is located there, maybe I need to send 100 bytes of characters, maybe 3000...who knows!?
     
     - So, **we will do our `fuzzing` process to know how many bytes (characters) do we need to crash the program `gatekeeper.exe`**
     
- **As difference with `Vuln Server` Lab, here we are NOT using commands, just a string to make the `gatekeeper server` respond with a `string`**

    - **So, instead of using **`generic_send_tcp`** technique and spiking the strings, I will write a simple python script doing the following large strings and "jump" the spiking process, I really don't care very much being so precise with the breaking point at this moment, so I will only spam thousands of bytes and see what happen.**
    
```python
#!/usr/bin/python

print "A" * 5000
```

- Or just using a python command:

    - `python -c 'print "A" * 5000'` 

- With this simple script we will generate 5000 bytes of "A's" at once:

    - ![image](https://user-images.githubusercontent.com/94720207/169638415-43d37e2b-079b-4bd0-a8e2-e96c3a00c6dd.png)

- And we will copy and paste it to the program, it's just like a basic "manual fuzzing" and then press `enter`:

    - ![image](https://user-images.githubusercontent.com/94720207/169638479-071a4226-18aa-4c60-8247-eeef445f0750.png)

- BOOM!!! We did it!!! The `chatserver.exe` have just crashed, it means the `buffer space` of "message" is not sanitized and we can exploit it. 

    - ![image](https://user-images.githubusercontent.com/94720207/169638574-63ddd521-886b-4327-a82b-c0bfdff6feb1.png)

- Bota fixa papai!

    - If we look at `EBP` we can see `41414141`: THAT'S THE HEX CODE FOR: `AAAA`
    
        - ![image](https://user-images.githubusercontent.com/94720207/169456928-65563691-936f-441c-9ade-edf2f7c31752.png) 

    - Also, we went over `ESP` with a bunch of "A"

    - Finally, we get into `EIP` too with `41414141`: THA'TS THE HEX CODE FOR: `AAAA`

- Remember: **The `EIP` is the important factor!**

    - If we control `EIP` we can point somethin malicious! But for that, we need to locate "where's `EIP` now?"

- NOTE: The program has crashed, so we will need to restart the `Chat Server` and attach it again to the `Immunity Debugger`

    - **It's better to close everything and start from 0 to avoid errors** 

- We already know that the program `Chat Server` can crash somewhere if we send a string overflow of 5000 bytes (A's)

- **As difference with `vuln server` we did this process a lot quickier, that's because in this scenario we did not needed `spiking`.**

    - **Instead, with just a bunch of "A's" we did realize that the string can crash the program, that means now we need to `find the offset`
    
- we just need to know aprox where we crashed the program, and we know is somewhere around **less than 5000 bytes**

    - Now, that we know that the crash is somewhere less 5000 bytes, we need to know: **where's the `EIP` value at?**

    - Remember, controlling the `EIP` is the puprose of all of this attack. 

---  

### Finding the Offset







---

### References

https://github.com/hamza07-w/gatekeeper-tryHackme-writeup
