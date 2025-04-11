#!/bin/bash

target_ver="1.9.72"

deb="windows-data-migration"

# get cur ver
if ! cur_ver=$(dpkg -s $deb | awk '$1 == "Version:" {print $2;}'); then
    echo "$deb is not installed. Exit"
    exit 1
fi

# get last repo ver
if ! apt update &>/dev/null; then
    echo "apt udpate failed"
    exit 1
fi

if ! apt_show=$(apt show -a $deb); then
    echo "apt show failed"
    exit 1
fi

while read line; do
    if [[ "$line" =~ Version:.* ]]; then
        version=$(echo "$line" | awk '{print $2;}')
        #echo version=$version   
    elif [[ "$line" =~ APT-Sources: ]]; then
        apt_source=$(echo "$line" | awk '{print $2;}')
        #echo apt_source=$apt_source
    elif [[ -z "$line" ]]; then
        if [[ "$apt_source" =~ .*repo.* ]]; then
            #echo "do job cause good source"
            versions="$versions $version"
        fi
    fi
done <<< "$apt_show"

echo versions=$versions

last_ver=$(echo "$versions" | tr "[:space:]" "\n" | sort -V | tail -n1)
if [[ -z "$last_ver" ]]; then
    echo "No available debs"
    exit 1
fi

echo cur_ver=$cur_ver last_ver=$last_ver

# Взять отсюда: https://stackoverflow.com/questions/4023830/how-to-compare-two-strings-in-dot-separated-version-format-in-bash
vercomp() {

    if [[ "$1" == "$2" ]]; then
        return 0
    fi

    local IFS=.
    local i ver1=($1) ver2=($2)
    # fill empty fields in ver1 with zeros
    for ((i=${#ver1[@]}; i<${#ver2[@]}; i++)); do
        ver1[i]=0
    done

    for ((i=0; i<${#ver1[@]}; i++)); do
        if ((10#${ver1[i]:=0} > 10#${ver2[i]:=0})); then
            return 1
        fi

        if ((10#${ver1[i]} < 10#${ver2[i]})); then
            return 2
        fi
    done

    return 0
}

# делаем что хотим с этими знаниями
