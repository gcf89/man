#!/bin/bash

function _trap_DEBUG() {
    echo "# $BASH_COMMAND";
    while read -r -e -p "debug> " _command; do
        if [ -n "$_command" ]; then
            eval "$_command";
        else
            break;
        fi;
    done
}


trap '_trap_DEBUG' DEBUG

