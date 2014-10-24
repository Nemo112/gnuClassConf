#!/bin/bash
# Needitujte nikdy tento soubor!
# NET
iptables -F;
iptables -X;
iptables -A OUTPUT -j ACCEPT;
iptables -A INPUT -j ACCEPT;
# ===
# DOM

# ===
