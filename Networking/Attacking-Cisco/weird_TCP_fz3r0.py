##############################################################################
#
#    https://www.youtube.com/watch?v=CIWD9fYmDig
#
#
#
#
#
#
#
#
#
#
#
#
##############################################################################

'''
- Importaré TODA la librería de Scapy: 

      from scapy.all import *

- crearé las siguientes variables
  utilizando esas librerías de Scapy:

    * Ether
    * IP
    * IPv6

---

- *Ether = Ethernet Frame Header @ Scapy
- La variable Layer2 será entonces el Ethernet Header

- *show = muestra en consola la variable(header) `Layer2` 

---

- *IP = IPv4 Packet Header @ Scapy
- La variable Layer3 será entonces el IPv4 Header

- *show = muestra en consola la variable(header) `Layer3`

---

- *IPv6 = IPv6 Packet Header @ Scapy
- La variable MyIPv6 será entonces el IPv6 Header (host)

- *show = muestra en consola la variable(header) `IPv6`

---

'''

from scapy.all import *

Layer2 = Ether()
#Layer2.show()
Layer3 = IP() 
#Layer3.show()
MyIPv6 = IPv6()
#IPv6.show()

'''

- Ya que tengo Scapy listo, puedo empezar por modificar cualquiera de los flags o variables de los headers

=-=-=-=-=-=-=-=-=-=-=-=-=-= LHOST MAC Spoofer =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

- Layer2 = MAC Address (Generar un frame con la Source-MAC / LHOST spoofed por mi):

- *Ether = Ethernet Frame Header @ Scapy

    - *Ether contiene la variable `src`, que es la "Ethernet Source" (ó Source MAC/LHOST)
    
- Entonces, Ether será igual al MAC-Source que yo quiera:

'''

Layer2=Ether(src="01:02:03:04:05:06")
#Layer2.show()

'''

- Ya que tengo Scapy listo, puedo empezar por modificar cualquiera de los flags o variables de los headers

=-=-=-=-=-=-=-=-=-=-=-=-=-= LHOST IPv4 Spoofer =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-

- También puedo cambiar el source y destination del IPv4 Address:

'''

Layer3=IP(dst="192.168.1.90")
#Layer3.show()

'''

- Enviar tráfico hacia la Network:

send=sendp(Layer2)                      <<< Envía el paquete generado (variable Layer2)

send=sendp(Layer2/Layer3)               <<< Apila Layer 3 en el paquete con "/"

send=sendp(Layer2/Layer3/Layer3)        <<< Apila x2 Layer 3 + x1 Layer2 en el paquete con "/"
                                           Es decir, rompe la regla OSI/TCP, adiós CCNA :P

send=sendp(Layer2/Layer3/Layer3/Layer3) <<< Este bad boy rompe la teoría OSI y TCP pero!

    - Apila x1 Layer2 + x3 Layer3 (algo que "no" pasaría en "la vida real")
    - Aunque de hecho..."si pasaría" ya que "es la regla"... de poderse apilar:

    - Es decir, la regla se puede romper generando paquetes extraños y viajarán por la red mal formados...

    - Ya que... ¿Por qué no podrían?, son raros, llegan con errores, pero son generados como cualquier paquete de protocolo de red

                                          

'''

#send=sendp(Layer2/)

#send=sendp(Layer2/Layer3)

send=sendp(Layer2/Layer3/Layer3)
