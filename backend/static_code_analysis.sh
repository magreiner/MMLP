#!/bin/bash

cd mmlp
mkdir -p code_stats

echo "Number of classes:  $(rgrep 'class ' . | grep -v '#' | wc -l)" &> code_stats/generic.txt
echo "Number of functions:  $(rgrep 'def ' . | grep -v '#' | wc -l)" &>> code_stats/generic.txt
echo "Number of python files: $(find . -name '*.py' | wc -l)" &>> code_stats/generic.txt

radon cc . -sa &> code_stats/radon_cc.txt
radon raw . -s &> code_stats/radon_raw.txt
radon mi . -s &> code_stats/radon_mi.txt
radon hal . &> code_stats/radon_hal.txt
