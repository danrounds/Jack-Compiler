#!/usr/bin/env bash

pushd tests/test_code0/Extras_\(Non_Project\)/Maze3d

cmp Cam3D.vm COMPARE/Cam3D_COMPARE.vm
cmp Display.vm COMPARE/Display_COMPARE.vm
cmp Float.vm COMPARE/Float_COMPARE.vm
cmp Grid.vm COMPARE/Grid_COMPARE.vm
cmp LineBuffer.vm COMPARE/LineBuffer_COMPARE.vm
cmp M4D.vm COMPARE/M4D_COMPARE.vm
cmp Main.vm COMPARE/Main_COMPARE.vm
cmp Point.vm COMPARE/Point_COMPARE.vm
cmp Tile.vm COMPARE/Tile_COMPARE.vm
cmp V2D.vm COMPARE/V2D_COMPARE.vm
cmp V3D.vm COMPARE/V3D_COMPARE.vm

popd
