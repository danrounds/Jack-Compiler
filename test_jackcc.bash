#!/usr/bin/env bash
# 11 August, 2016, DJR

docstring="
QUICK AND DIRTY TEST SCRIPT FOR JACKCC
--------------------------------------------------------------------------
Takes us through a class full of Jack projects, full compilation.

TicJackToe will not work, because it doesn't link to the right directory (and
that's okay!--it was not coded to spec, anyway)

Warnings are absolutely to be expected. If anything, they let us know everything
is working as it should.

The only cause for alarm would be if the tests didn't compile, start to finish.
"

echo "$docstring"

read -n1 -r -p 'Press ENTER to proceed with tests' key
if [$key = '']; then
    echo
    pushd Compiler/tests/test_code0/Extras_\(Non_Project\)/
    for d in */; do
        ../../../../jackcc.py "$d"
        echo -e "\n"
    done
    popd
fi
