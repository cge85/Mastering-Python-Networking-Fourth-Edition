#!/usr/bin/env python3
from scapy.all import IP, ICMP, TCP, UDP, sr

def icmp_ping(destination):
    ans, unans = sr(IP(dst=destination)/ICMP(), timeout=2, verbose=0)
    return ans

def tcp_ping(destination, dport):
    ans, unans = sr(IP(dst=destination)/TCP(dport=dport, flags="S"), timeout=2, verbose=0)
    return ans

def udp_ping(destination):
    ans, unans = sr(IP(dst=destination)/UDP(dport=0), timeout=2, verbose=0)
    return ans

def answer_summary(ans):
    for send, recv in ans:
        print(recv.sprintf("%IP.src% is alive"))

def main():
    print("** ICMP Ping **")
    answer_summary(icmp_ping("192.168.0.41"))

    print("** TCP Ping **")
    answer_summary(tcp_ping("192.168.0.40", 22))

    print("** UDP Ping **")
    answer_summary(udp_ping("192.168.0.40"))

if __name__ == "__main__":
    main()