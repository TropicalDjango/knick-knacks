echo "Time since last reboot"
last reboot | head -2 | awk '{print $5,$6,$7,$8,$9,$10,$11}' | sed -n '2p'
uptime -p


