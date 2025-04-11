#!/bin/bash

# Shell style: echo ${1^^}

echo $1 | tr '[:lower:]' '[:upper:]'

