# voxelFoam

Python script for transforming voxelized ABAQUS meshes generated in TexGen into OpenFOAM folder structure.

## Usage

Call with command:

    python3 voxelFoam <mesh_file> <case_folder_name>
    
## Issues

Texgen has an issue where the file has the wrong encoding and the program can't read the .inp file. The solution for now is to retype the problematic line and save the file before running the script.
An easy way to find the problematic line is to run the program in debug mode and see in which line the code stops reading the file. Usually it's only one bad line per file, around the definition of NSets and Equations.
