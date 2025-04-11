#!/bin/bash

function run()
{
    eval "$*" | awk '{ print strftime("%D %T"),$0 }'
}


run date

run echo 'hello'


run cat /etc/os-release
