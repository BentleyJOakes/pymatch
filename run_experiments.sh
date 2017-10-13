#!/bin/bash

for ((i=0;i<4000;i+=16))
do
    #echo $i $((i + 16))
    python3 main.py $i $((i + 16))
done
