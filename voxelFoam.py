import sys

import meshiofoam as meshio
import openfoam as of
import writers as w


# Reading arguments
file_in = sys.argv[1]
file_out = sys.argv[2]

# Reading the mesh
mesh = meshio.read(file_in)

# Adjusting mesh object according to mesh origin
poly = of.polyMesh(mesh, file_in.split(".")[-1])

# Creating folder structure
of.createFolderStructure(file_out)

# Writing files
w.writePointsFile(poly, file_out)
# writeCellsFile(poly, file_out)
w.writeFacesFile(poly, file_out)
w.writeOwnerFile(poly, file_out)
w.writeNeighbourFile(poly, file_out)
w.writeBoundaryFile(poly, file_out)
w.writeSets(poly, file_out)
# w.writePointZones(poly, file_out)
# w.writeFaceZones(poly, file_out)
w.writeCellZones(poly, file_out)
w.createFoamFile(file_out)
