#!/bin/bash

#sudo npm install -g complexity-report

cd src
mkdir -p code_stats

echo "Number of js functions:  $(find . -name '*.js' | xargs grep 'function' . | grep -v '//' | wc -l)" &> code_stats/generic.txt
echo "Number of vue functions:  $(find . -name '*.vue' | xargs grep ') {' . | grep -v '//' | wc -l)" &>> code_stats/generic.txt
echo "Number of vue files: $(find . -name '*.vue' | wc -l)" &>> code_stats/generic.txt
echo "Number of js files: $(find . -name '*.js' | wc -l)" &>> code_stats/generic.txt
echo "Lines of code vue: $(find . -name '*.vue' | xargs wc -l | grep 'total')" &>> code_stats/generic.txt
echo "Lines of code js: $(find . -name '*.js' | xargs wc -l | grep 'total')" &>> code_stats/generic.txt

