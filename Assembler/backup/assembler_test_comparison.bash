#!/usr/bin/env bash
# 11 August, 2016, DJR
# Quick and dirty test script for JackCC
# The two last test cases don't work, because they don't link to the right directories
#  (and that's okay!).

pushd ../Compiler/tests/test_code0/Extras_\(Non_Project\)/
for d in */; do
    ../../../../jackcc.py -o a.comparison "$d"
    echo -e "\n"
done

echo 'Comparisons: '
for f in */; do
    # echo "$f/a.hack $f/a.comparison"
    cmp $f/a.hack $f/a.comparison
done
popd
