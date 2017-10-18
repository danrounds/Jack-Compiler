#!/usr/bin/env bash

base_dir="./tests/test_code0"

echo "projects/10/ArrayTest/MainT.xml and MainT_.xml"
diff -w $base_dir/ArrayTest/MainT.xml $base_dir/ArrayTest/MainT_.xml
# pause

echo "projects/10/ExpressionlessSquare/MainT.xml and MainT_.xml"
diff -w $base_dir/ExpressionlessSquare/MainT.xml $base_dir/ExpressionlessSquare/MainT_.xml

echo "projects/10/ExpressionlessSquare/SquareGameT.xml and SquareGameT_.xml"
diff -w $base_dir/ExpressionlessSquare/SquareGameT.xml $base_dir/ExpressionlessSquare/SquareGameT_.xml

echo "projects/10/ExpressionlessSquare/SquareT.xml and SquareT_.xml"
diff -w $base_dir/ExpressionlessSquare/SquareT.xml $base_dir/ExpressionlessSquare/SquareT_.xml

echo "projects/10/Square/MainT.xml and MainT_.xml"
diff -w $base_dir/Square/MainT.xml $base_dir/Square/MainT_.xml

echo "projects/10/Square/SquareGameT.xml and SquareGameT_.xml"
diff -w $base_dir/Square/SquareGameT.xml $base_dir/Square/SquareGameT_.xml

echo "projects/10/Square/SquareT.xml and SquareT_.xml"
diff -w $base_dir/Square/SquareT.xml $base_dir/Square/SquareT_.xml
