#!/bin/sh

/usr/local/bin/gpio write 3 1

/usr/local/bin/gpio mode 3 output

echo "GPIO ports setup"
