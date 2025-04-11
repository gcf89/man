#
# Server
#

sudo apt update
sudo apt upgrade

sudo apt install openvpn easy-rsa net-tools

wget https://raw.githubusercontent.com/angristan/openvpn-install/master/openvpn-install.sh

chmod +x openvpn-install.sh
./openvpn-install.sh

: choose defaults
: run again to create client config


#
# Android
#

install openvpn client
add .ovpn file

