#!/bin/sh
# Persistent Linux host configuration for the DREAMLTE CDC-ECM gadget.
set -eu
name=DREAMLTE-XNU-USB
if [ "${1:-}" = --help ]; then
    echo "Usage: sudo $0"
    echo 'Install a MAC-bound NetworkManager profile that reconnects after phone reboot.'
    exit 0
fi
if ! nmcli -g connection.id connection show "$name" >/dev/null 2>&1; then
    nmcli connection add type ethernet con-name "$name" ifname '*' 802-3-ethernet.mac-address 02:00:5e:77:ee:01
fi
nmcli connection modify "$name" connection.interface-name '' connection.autoconnect yes connection.autoconnect-priority 100 802-3-ethernet.mac-address 02:00:5e:77:ee:01 ipv4.method manual ipv4.addresses 192.168.7.1/24 ipv4.gateway '' ipv4.never-default yes ipv4.ignore-auto-dns yes ipv6.method disabled
for net in /sys/class/net/*; do
    [ "$(cat "$net/address")" = 02:00:5e:77:ee:01 ] || continue
    iface=${net##*/}
    nmcli device set "$iface" managed yes
    nmcli connection up "$name" ifname "$iface"
done
