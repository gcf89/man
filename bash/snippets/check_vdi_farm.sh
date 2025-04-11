#!/bin/bash


CITRIX_LINK="citrix_addr"
HORIZON_LINK="vmwareHorizonAddressAlpha"

SETTINGS="/etc/settings.txt"
[[ -e $SETTINGS ]] && vdi=$(awk -F= '/^vdi/ {print $2}' $SETTINGS) || vdi="none"

while true; do
    # get list of ifaces
    ifaces=$(ip -br addr show | awk '!/lo/ {print $1}')

    # check if at least one of them is UP and has IP
    for iface in $ifaces; do
        state=$(ip -br addr show | awk "/$iface/ {print \$2}")
        if [[ "$state" == "UP" ]]; then
            addr=$(ip -br addr show | awk "/$iface/ {print \$3}")
            # remove CIDR
            ip=$(echo $addr | sed -E 's+/.*$++g')

            if [[ "$ip" =~ ^(([1-9]?[0-9]|1[0-9][0-9]|2([0-4][0-9]|5[0-5]))\.){3}([1-9]?[0-9]|1[0-9][0-9]|2([0-4][0-9]|5[0-5]))$ ]]; then
                # Are thin clients could really work in SIGMA?
                # TODO: check if we are in alpha/sigma (settings.txt: alphaCheckAddress/sigmaCheckAddress)

                # check if farm is available via telnet by port
                if [[ -e "$(which telnet)" ]]; then
                    case "$vdi" in
                        "citrix")
                            #citrix_addr=https://sf3xcod.omega.sbrf.ru/Citrix/VARM-BusinessCritical/discovery
                            target_addr=$(awk -F= "/^$CITRIX_LINK/ {print \$2}" $SETTINGS | sed -E -e 's+"++g')
                            ;;
                        "vmware")
                            #vmwareHorizonAddressAlpha="a-horizon.omega.sbrf.ru"
                            target_addr=$(awk -F= "/^$HORIZON_LINK/ {print \$2}" $SETTINGS | sed -E -e 's+"++g')
                            ;;
                        *)
                            # No VDI, assume success
                            exit 0
                            ;;
                    esac

                    host=$(echo $target_addr | sed -E -e 's+https?://++' -e 's+[:/].*++')

                    prot=$(echo $target_addr | awk -F: '{print $1}')

                    # handle case when prot is not set
                    if [[ $(echo $target_addr | grep -cE '^http') -ne 0 ]]; then
                        port=$(echo $target_addr | awk -F: '{print $3}' | sed -E 's+/.*++g')
                    else
                        port=$(echo $target_addr | awk -F: '{print $2}' | sed -E 's+/.*++g')
                    fi

                    if [[ -z "$port" ]]; then
                        case "$prot" in
                            https)
                                port=443
                                ;;
                            http)
                                port=80
                                ;;
                            *)
                                # default
                                port=443
                                ;;
                        esac
                    fi

                    # Check connection to port. Exit if it's ok
                    echo 'exit' | timeout 3s telnet $host $port | grep 'Connected'
                    [[ "$?" -eq 0 ]] && exit 0
                else
                    # Assume succsess, cause we have UP and running iface with IP, but can't check farm port
                    exit 0
                fi
            fi
        fi
    done

    notify-send --urgency=low -i info -t 100 "Жду подключения к сети"
    sleep 3
done

