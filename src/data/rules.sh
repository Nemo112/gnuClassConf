#!/bin/bash
# Needitujte nikdy tento soubor!
# DOM
iptables -F INPUT;
iptables -F OUTPUT;

# ===
# NET

iptables -A OUTPUT -j ACCEPT;
iptables -A INPUT -j ACCEPT;
iptables -D OUTPUT -j DROP;
iptables -D INPUT -j DROP;
# ===




