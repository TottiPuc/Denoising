#!/bin/bash

pastaCorrompidos='/home/christianlab/python/white/10dB/'

find $pastaCorrompidos -name "*.wav" | while read line
do
echo "processing file $line..."

python wavelet.py $line

mv a.wav $line
done 


