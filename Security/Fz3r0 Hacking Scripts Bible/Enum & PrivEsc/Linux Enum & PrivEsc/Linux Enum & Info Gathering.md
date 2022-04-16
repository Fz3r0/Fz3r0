---
### Fz3r0 Operations  [Cyber-Security & Hacking]

### Linux System Enumeration
---


##### Twitter  : [@fz3r0_OPs](https://twitter.com/Fz3r0_OPs) 
##### Github  : [Fz3r0](https://github.com/fz3r0) 

---

#### Keywords: `Linux` `enumeration` `bash` `find` `command` `PrivEsc`
---

### Best friends commands

`id`

`id User`
`id root`
`id John`

`hostname`

`uname -a`

`/proc/version`

`/etc/issue`

`ps`
`ps -A`
`ps axjf`

`env`

`sudo -l` 
`sudo -l -l`

`ls` 
`ls -la`
`ls -lAh`

`cat /etc/passwd`

`history`

`ifconfig`

`ip route`

`netstat`
`netstat -a`
`netstat -at`
`netstat -au`
`netstat -l`
`netstat -lt`
`netstat -s`
`netstat -tp`
`netstat -ano`

`find`
`locate`
`grep`
`cut`
`sort`

---

### Find Command

| Command                                         | Action                 |  
|-------------------------------------------------|------------------------|
|`find / -type f -name 'file.py'`                 |buscar ARCHIVO "file.py" en: /  |
|`find / -type d -name 'folder'`                  |buscar DIRECTORIO "folder" en: /|
|‎  |‎  |
|`find / -type f -name user.txt 2> /dev/null`     | buscar flag "user.txt" en: /|
|`find / -type f -name root.txt 2> /dev/null`     | buscar flag "root.txt" en: /|
|`find / -type f -name flag.txt 2> /dev/null`     | buscar flag "flag.txt" en: /|
|`find . -name f -name flag.txt 2> /dev/null`     | buscar flag "flag.txt" en: .|
|‎  |‎  |
|`find -type f -perm -u=s 2>/dev/null`              | buscar permisos suid        |
|`find / type -f -user root -perm -u=s 2> /dev/null`| buscar permisos suid        | 
|`find / -perm -u=s -type f 2>/dev/null`            | buscar permisos específicos |
|‎  |‎  |
|`find / -type f -perm 0777`     | find files with the 777 permissions (Executable by ALL users)|
|`find / -perm a=x`              | find executable files|
|`find /home -user frank`        | find all files for user “frank” under “/home”        |
|`find / -type f -perm 0777`     | find files with the 777 permissions (Executable by ALL users)|
|`find / -mtime 10`|             | find files that were modified in the last 10 days    |
|`find / -atime 10`|             | find files that were accessed in the last 10 day     |
|`find / -cmin -60`|             | find files changed within the last hour (60 minutes) |
|`find / -amin -60`|             | find files accesses within the last hour (60 minutes)|
|`find / -size 50M`|             | find files with a 50 MB size|

- This command can also be used with (+) and (-) signs to specify a file that is larger or smaller than the given size.

- Use the “find” command with “-type f 2>/dev/null” to redirect errors to “/dev/null” and have a cleaner output

| Command                      | Action                                     |  
|------------------------------|--------------------------------------------|
|find / -writable -type d 2>/dev/null |       Find world-writeable folders  |
|find / -perm -222 -type d 2>/dev/null|       Find world-writeable folders  |
|find / -perm -o w -type d 2>/dev/null|       Find world-writeable folders  |
|find / -perm -o x -type d 2>/dev/null|       Find world-executable folder  |


### Find development tools and supported languages:

| Command                      | Action                                     |  
|------------------------------|--------------------------------------------|
|`find / -name perl*`   |  Perl   |
|`find / -name python*` |  Python |
|`find / -name gcc*`    |  GNU    |

---
