#!/bin/sh

read -p "Enter some text:" a

b=${a:-'default'}
echo "Stdout: $b"

>&2 echo "Error: some error"
exit 1

