# Fz3r0 OPs NetSec - FortiDoomsGate

## Eva II - Backup & Restore

### Backup & Restore por UI

- Dashboard Inicial > Parte superior derecha (cerca de usuiario) > click!

1. Configuration > Backup:

    - Local PC / USB Disk (local usb port)

2. Configuration > Restore:    

    - (En VM aveces se puede crashear y no hacer, para arreglarlo)

        - Ir a consola:

        - `config system global`

        - `get | grep http` (revisar el http connection timeout, default: 2)

        - `set admin-http-connection-receive-timeout 60`

        - `end`

        - `y`

- **Importante:** Los archivos de backup se pueden abrir con edites de texto. 

    - **Ching...Fortideras:** Para cambiar el nombre por ejemplo de una VPN_Sec se tendría que creare un backup, cambiar nombres a manita y después cargar el backup. Son Fortideras! 

- **Consultar cambios:**

- `get system global | grep http `

- _Si está en 60 de timout todo salió bien (15 días de prueba)_

### Revisions

- _Funciona para guardar una revisión local en Forti_

    - **Muy útil para casos de nuevas configs y roll backs**    

- Dashboard Inicial > Parte superior derecha (cerca de usuiario) > click!

- Configuration > Revision:

- click: `save changes` > agregar info y ver detalles

    - _En los detalles del revisions puedes ver el valor anterior y actual_

- **Revert / Rollback**

    - Click derecho en la revisión, backup

- **OJO!!!** Esto no sustituye el backup!!! siempre es mejor un backup fuera.        

### Restore Backup por TFTP

- Para laboratorio en Windows usar servidor TFTP:

    - Usar: `tftpd32`
    - http://tftpd32.jounin.net/tftpd32_download.html

- [Tutorial](https://www.youtube.com/watch?v=fuMBd8rXtC0)     

### Restore Backup por CLI

- Se necesitan los backups (Archivos de texto después de todo).

- Se edita lo siguiente:

1. Quitar primeras 4 lineas:

```
#config-version=FGVMK6-6.2.0-FW-build0866-190328:opmode=0:vdom=0:user=admin
#conf_file_ver=184619169261541
#buildno=0866
#global_vdom=1
.
.
.
```

2. Buscar keyword `set uuid`    

    - Replace por: `  `  (_nada, jeje lo demás marcará error de sintaxis pero da =_)

3. Buscar keyword `partition`

    - **Eliminar** toda la sección donde se encuentre por ejemplo:
    
```
config system storage
    edit "Virtual-Disk"
        set status enable
        set media-status enable
        set order 1
        set partition "LOGUSEDXA9B43DC5" <-------------- Aqui está Wally!!!
        set device "/dev/vdb1"
        set size 8062
        set usage log
    next
end
```        

- **Ahora ya se puede acceder por SSH o como quieras y copiar y pegar la configuración en el shell.**

- Importante - reiniciar!!! `execute reboot`  
