#!/usr/bin/env bash

pushd tests/test_code0/Extras_\(Non_Project\)/Maze3d

cmp Cam3D.vm Cam3D_COMPARE.vm
cmp Display.vm Display_COMPARE.vm
cmp Float.vm Float_COMPARE.vm
cmp Grid.vm Grid_COMPARE.vm
cmp LineBuffer.vm LineBuffer_COMPARE.vm
cmp M4D.vm M4D_COMPARE.vm
cmp Main.vm Main_COMPARE.vm
cmp Point.vm Point_COMPARE.vm
cmp Tile.vm Tile_COMPARE.vm
cmp V2D.vm V2D_COMPARE.vm
cmp V3D.vm V3D_COMPARE.vm

popd
