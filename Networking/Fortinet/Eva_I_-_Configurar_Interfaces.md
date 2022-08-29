
# Fz3r0 OPs NetSec - FortiDoomsGate

## Eva I - Configurar Interfaces:

### Configurar Interfaces por UI

- **Obtener Info de interface (IP, netbios)**

    - `get system interface`

    - Nota: _sa IP es la que se usa en Web para abrir UI ;)_

    - Pro:

    - `get system interface | grep port1`

- **Configurar IPs (UI)**


- Network > Interfaces

    - Click en `Port 1` (es la que estoy usando en el lab para conectar la red de Internet)

    - Click: `Edit Interface` (lápiz)      

- Optional: Revisar y seleccionar el `Administrative Access Deseado`

-  **Address** - _Aquí vienen todas las opciones, actualmente está en DHCP_

    - NOTA: Dentro de cada interface se configura un mundo de sorpresas. 

- Optional: **DHCP Server** - En caso que se requiera se puede habilitar un DHCP server (Incluyendo la Pool)

    - En este ejemplo podría usar una pool de `10.0.1.1` a `10.0.1.253`
    - Netmask: 255.255.255.0    
    - Default Gateway: Se puede especificar a mano o usar el mismo de la Interface
    - DNS Server: Se puede especificar a mano o usar el mismo de la Interface     
- Network Devices

    - **Device Detection** - Se aconseja siempre tenerlo encendido. 

- Tags

    - Role (Depende del rol se puede agregar descripciones como `estimated bandwith`)

- **Finalizar:** Hacer click en `OK`     

### Configurar por CLI

- Entrar al modo config interface:

    - `config system interface`

- Editar puertos:

    - `edit port4`

- Agregar IP:

    - `set ip 10.0.2.254/24`

- AllowAccess:

    - Ping: `set allowaccess ping`    
    - HTTP & HTTPs: `set allowaccess http https`  
    - **unset:** `unset allowacces`

- OK!!! < (END)

    - `end`

- Ejemplo completo:

```
FortiGate-VM64-KVM # config system interface

FortiGate-VM64-KVM (interface) # edit port4

FortiGate-VM64-KVM (port3) # set ip 10.0.2.254/24

FortiGate-VM64-KVM (port3) # set allowaccess ping

FortiGate-VM64-KVM (port3) # end

.
.
.

FortiGate-VM64-KVM # config system interface

FortiGate-VM64-KVM (interface) # edit port4

FortiGate-VM64-KVM (port3) # unset allowaccess
```    

---

### Tips, tips y más tips:

- Tip: usar `show` para ver sus configs **SOLO OPCIONES PROGRAMADAS**    

```
FortiGate-VM64-KVM # config system interface

FortiGate-VM64-KVM (interface) # show
config system interface
    edit "port1"
        set vdom "root"
        set mode dhcp
        set allowaccess ping https ssh http fgfm
        set type physical
        set snmp-index 1
    next
    edit "port2"
        set vdom "root"
        set type physical
        set snmp-index 2
    next
.
.
.

end      

FortiGate-VM64-KVM (interface) # 
```

- Tip: usar `get` para ver sus configs **(TODAS LAS OPCIONES)** 

```
FortiGate-VM64-KVM (interface) # get
== [ port1 ]
name: port1   mode: dhcp    ip: 192.168.42.134 255.255.255.0   status: up    netbios-forward: disable    type: physical   netflow-sampler: disable    sflow-sampler: disable    src-check: enable    explicit-web-proxy: disable    explicit-ftp-proxy: disable    proxy-captive-portal: disable    mtu-override: disable    wccp: disable    drop-overlapped-fragment: disable    drop-fragment: disable
.
.
.
```

---

#### Common Passwords Used:

- Default Forti login:

    - admin (blank password)

- Labs Passwords:    

    - `Pa$$w0rd2`
    - `Pa$$w0rd`
	- `C1sco.12345`
