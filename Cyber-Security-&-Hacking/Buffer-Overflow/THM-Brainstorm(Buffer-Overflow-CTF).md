
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
 
 - **It looks that this program `Chat Server` take commands based on what you type AKA `strings` to generate a `username`**
 
 - **The username request a `max of 20 characters`**
 
     - This means, maybe the buffer overflow and/or the pointer of `EIP` that we need to exploit is located after those 20 characters...maybe 21...maybe 2739?, 666?!, who knows?!
     
     - So, **we will do our `spiking` process to know how many bytes do we need to crash the program `chatserver.exe`**
     
- As difference with `Vuln Server` Lab, here we are NOT using commands, just a user `string`

- So, instead of using **`generic_send_tcp`**, I will write a simple python script doing the following:

```python
#!/usr/bin/python

print "A" * 5000
```

- Or just using a python command:

    - `python -c 'print "A" * 5000'` 

- With this simple script we will generate 5000 bytes of "A's" at once:

    - ![image](https://user-images.githubusercontent.com/94720207/169452006-9a56b1a1-57e0-4207-bebd-3ab5640cb374.png)

- And we will copy and paste it to the program, it's just like a "manual fuzzing":

    - ![image](https://user-images.githubusercontent.com/94720207/169452204-f1194a76-9fce-4845-8ed0-0b7618825ffb.png)
 

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
| **SKIPSTR**            | ()0                        |

---

### Spike Script

- We will generate a file called "stats.spk"

```
s_readline();              <<<-----| 1. We will read the line
s_string("AAAAAAAAAAAAAAAAAAAA");        <<<-----| 2. We will take the string ("AAAAAAAAAAAAAAAAAAAA" [A*20] in this case)
s_string_variable("0");    <<<-----| 3. We will send a variable to the "AAAAAAAAAAAAAAAAAAAA" string
```

- The trick for the spike is this:  

---

### References

- https://tryhackme.com/room/brainstorm
- https://github.com/Fz3r0/Fz3r0/blob/main/Cyber-Security-&-Hacking/Buffer-Overflow/buffer-overflow.md
- https://www.youtube.com/watch?v=T1-Sds8ZHBU
