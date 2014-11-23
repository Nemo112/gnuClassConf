#!/bin/bash
# Needitujte nikdy tento soubor!
# DOM
iptables -F INPUT;
iptables -F OUTPUT;
iptables -F FORWARD;

# ===
# NET

iptables -A OUTPUT -j ACCEPT;
iptables -A INPUT -j ACCEPT;
iptables -D INPUT -i lo -j ACCEPT
iptables -D OUTPUT -o lo -j ACCEPT
iptables -D OUTPUT -j DROP;
iptables -D INPUT -j DROP;
# ===




