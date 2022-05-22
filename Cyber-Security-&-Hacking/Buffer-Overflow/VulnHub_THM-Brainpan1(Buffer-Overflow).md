
---

### Intro

- Reverse engineer a Windows executable, find a buffer overflow and exploit it on a Linux machine.

- Brainpan is perfect for OSCP practice and has been highly recommended to complete before the exam. 

- Exploit a buffer overflow vulnerability by analyzing a Windows executable on a Linux machine. 

    - Try Hack Me Lab Link: https://tryhackme.com/room/brainpan
    
    - VulnHub Lab Link: https://www.vulnhub.com/entry/brainpan-1,51/ 

---

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
 
