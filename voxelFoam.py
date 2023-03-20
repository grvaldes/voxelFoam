import meshiofoam as meshio
import openfoam as of
import writers as w


def voxelFoam(argv):
    # Reading arguments
    file_in = argv[1]
    file_out = argv[2]

    # Reading the mesh
    mesh = meshio.read(file_in)

    # Adjusting mesh object according to mesh origin
    poly = of.polyMesh(mesh, file_in.split(".")[-1])

    poly = of.cellRepetition(poly, 5, 5, 3)

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
