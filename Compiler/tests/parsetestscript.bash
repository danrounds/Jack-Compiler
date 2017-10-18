#!/usr/bin/env bash

base_dir="./tests/test_code0"

echo "projects/10, Compiler I -- Syntax Analysis/ArrayTest/Main.xml and Main_.xml"
diff -w $base_dir/ArrayTest/Main.xml $base_dir/ArrayTest/Main_.xml

echo projects/10, Compiler I -- Syntax Analysis/ExpressionlessSquare/Main.xml and Main_.xml
diff -w $base_dir/ExpressionlessSquare/Main.xml $base_dir/ExpressionlessSquare/Main_.xml

echo projects/10, Compiler I -- Syntax Analysis/ExpressionlessSquare/SquareGame.xml and SquareGame_.xml
diff -w $base_dir/ExpressionlessSquare/SquareGame.xml $base_dir/ExpressionlessSquare/SquareGame_.xml

echo projects/10, Compiler I -- Syntax Analysis/ExpressionlessSquare/Square.xml and Square_.xml
diff -w $base_dir/ExpressionlessSquare/Square.xml $base_dir/ExpressionlessSquare/Square_.xml

echo projects/10, Compiler I -- Syntax Analysis/Square/Main.xml and Main_.xml
diff -w $base_dir/Square/Main.xml $base_dir/Square/Main_.xml

echo projects/10, Compiler I -- Syntax Analysis/Square/SquareGame.xml and SquareGame_.xml
diff -w $base_dir/Square/SquareGame.xml $base_dir/Square/SquareGame_.xml

echo projects/10, Compiler I -- Syntax Analysis/Square/Square.xml and Square_.xml
diff -w $base_dir/Square/Square.xml $base_dir/Square/Square_.xml
