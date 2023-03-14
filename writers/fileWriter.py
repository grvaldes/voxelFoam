import numpy as np

def writePointsFile(poly, filename):
    with open(filename + "/constant/polyMesh/points","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("vectorField","constant/polyMesh","points"))
        writer.write(writeBreak(1))
        writer.write("\n\n")

        writer.write(f"{poly.points.shape[0]}\n(\n")

        for line in poly.points:
            writer.write(f"({line[0]:5.4f}\t{line[1]:5.4f}\t{line[2]:5.4f})\n".expandtabs(4))

        writer.write(")\n")
        writer.write("\n\n")
        writer.write(writeBreak(2))


def writeCellsFile(poly, filename):
    with open(filename + "/constant/polyMesh/cells","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("cellList","constant/polyMesh","cells"))
        writer.write(writeBreak(1))
        writer.write("\n\n")

        nCells = 0

        for v in poly.cells:
            nCells += v["points"].shape[0]

        writer.write(f"{nCells}\n(\n")

        for v in poly.cells:
            for line in v["points"]:
                cellNods = v["nPts"]
                ar2str = " ".join(map(str, line))
                writer.write(f"{cellNods}({ar2str})\n")

        writer.write(")\n")
        writer.write("\n\n")
        writer.write(writeBreak(2))


def writeFacesFile(poly, filename):
    with open(filename + "/constant/polyMesh/faces","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("faceList","constant/polyMesh","faces"))
        writer.write(writeBreak(1))
        writer.write("\n\n")

        nFaces = 0

        for _, v in poly.innerFaces.items():
            nFaces += v.shape[0]

        for _, v in poly.boundary.items():
            nFaces += v.shape[0]

        writer.write(f"{nFaces}\n(\n")

        for k, v in poly.innerFaces.items():
            for line in v:
                ar2str = " ".join(map(str, line))
                writer.write(f"{k}({ar2str})\n")

        for k, v in sorted(poly.boundary.items()):
            pts = k.split("_")[-1]
            for line in v:
                ar2str = " ".join(map(str, line))
                writer.write(f"{pts}({ar2str})\n")

        writer.write(")\n")
        writer.write("\n\n")
        writer.write(writeBreak(2))


def writeOwnerFile(poly, filename):
    with open(filename + "/constant/polyMesh/owner","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("labelList","constant/polyMesh","owner"))
        writer.write(writeBreak(1))
        writer.write("\n\n")

        nFaces = 0

        for _, v in poly.innerFaces.items():
            nFaces += v.shape[0]

        for _, v in poly.boundary.items():
            nFaces += v.shape[0]

        writer.write(f"{nFaces}\n(\n")

        for line in poly.owner:
            writer.write(f"{line}\n")

        writer.write(")\n")
        writer.write("\n\n")
        writer.write(writeBreak(2))


def writeNeighbourFile(poly, filename):
    with open(filename + "/constant/polyMesh/neighbour","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("labelList","constant/polyMesh","neighbour"))
        writer.write(writeBreak(1))
        writer.write("\n\n")

        writer.write(f"{poly.neighbour.size}\n(\n")

        for line in poly.neighbour:
            writer.write(f"{line}\n")

        writer.write(")\n")
        writer.write("\n\n")
        writer.write(writeBreak(2))



def writeBoundaryFile(poly, filename):
    with open(filename + "/constant/polyMesh/boundary","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("polyBoundaryMesh","constant/polyMesh","boundary"))
        writer.write(writeBreak(1))
        writer.write("\n\n")

        bounds = []

        for key in sorted(poly.boundary.keys()):
            bounds.append(key.split("_")[0])

        bounds = np.unique(bounds)

        n_bound = len(bounds)
        n_start = len(poly.neighbour)

        writer.write(f"{n_bound}\n(\n")

        for patch in bounds:
            n_faces = 0

            writer.write(f"\t{patch}\n".expandtabs(4))
            writer.write("\t{\n".expandtabs(4))
            writer.write("\t\ttype\t\t\tpatch;\n".expandtabs(4))
            writer.write("\t\tphysicalType\tpatch;\n".expandtabs(4))

            for key, value in poly.boundary.items():
                if patch in key:
                    n_faces += value.shape[0]

            writer.write(f"\t\tnFaces\t\t\t{n_faces};\n".expandtabs(4))
            writer.write(f"\t\tstartFace\t\t{n_start};\n".expandtabs(4))
            writer.write("\t}\n".expandtabs(4))

            n_start += n_faces

        writer.write(")\n")
        writer.write("\n\n")
        writer.write(writeBreak(2))


def writeSets(poly, filename):
    sets = []

    for key in sorted(poly.cellZones.keys()):
        if "All" in key:
            continue

        sets.append(key.split("_")[0])

    sets = np.unique(sets)
    
    for set in sets:
        nElems = 0
        tElems = []

        with open(filename + "/constant/polyMesh/sets/" + set,"w") as writer:
            writer.write(writeBanner())
            writer.write(writeFoamFile("cellSet","constant/polyMesh",set))
            writer.write(writeBreak(1))
            writer.write("\n\n")

            for key, value in poly.cellZones.items():
                if set in key:
                    nElems += value.size
                    tElems.append(value)

            tElems = np.hstack(tuple(tElems))
            writer.write(f"{nElems}\n(\n")

            for line in tElems:
                writer.write(f"{line}\n")

            writer.write(")\n")
            writer.write("\n\n")
            writer.write(writeBreak(2))


def writePointZones(poly, filename):
    with open(filename + "/constant/polyMesh/pointZones","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("regIOobject","constant/polyMesh","pointZones"))
        writer.write(writeBreak(1))
        writer.write("\n\n")


def writeFaceZones(poly, filename):
    with open(filename + "/constant/polyMesh/faceZones","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("regIOobject","constant/polyMesh","faceZones"))
        writer.write(writeBreak(1))
        writer.write("\n\n")


def writeCellZones(poly, filename):
    sets = []

    for key in sorted(poly.cellZones.keys()):
        if "All" in key:
            continue

        sets.append(key.split("_")[0])

    sets = np.unique(sets)

    with open(filename + "/constant/polyMesh/cellZones","w") as writer:
        writer.write(writeBanner())
        writer.write(writeFoamFile("regIOobject","constant/polyMesh","cellZones"))
        writer.write(writeBreak(1))
        writer.write("\n\n")

        writer.write(f"{sets.size}\n(\n")

        for set in sets:
            nElems = 0
            tElems = []

            for key, value in poly.cellZones.items():
                if set in key:
                    nElems += value.size
                    tElems.append(value)

            tElems = np.hstack(tuple(tElems))

            writer.write(set + "\n{\n")
            writer.write("\ttype\t\tcellZone;\n".expandtabs(4))
            writer.write("\tcellLabels\tList<label>\n".expandtabs(4))
            writer.write(f"\t{nElems}\n\t(\n".expandtabs(4))
            
            for line in tElems:
                writer.write(f"\t\t{line}\n".expandtabs(4))

            writer.write("\t);\n}\n\n".expandtabs(4))

        writer.write(")\n")
        writer.write("\n\n")
        writer.write(writeBreak(2))


def createFoamFile(filename):
    with open(filename + "/case.foam","w") as _:
        pass


def writeBanner(OF_version = 8):
    banner = ("/*--------------------------------*- C++ -*----------------------------------*\ \n" + 
     "  =========                 | \n" +
     "  \\\\      /  F ield         | OpenFOAM: The Open Source CFD Toolbox \n" +
     "   \\\\    /   O peration     | Website:  https://openfoam.org \n" +
    f"    \\\\  /    A nd           | Version:  {OF_version} \n" +
     "     \\\\/     M anipulation  | Generated with meshioToFoam\n" +
     "\*---------------------------------------------------------------------------*/\n")

    return banner



def writeBreak(i):
    if i == 1:
        brk = "// * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * //\n"
    elif i == 2:
        brk = "// ************************************************************************* //"

    return brk



def writeFoamFile(foamClass, location, object, version = 2.0, format = "ascii"):
    foamFile = ("FoamFile\n" +
        "{\n" +
        f"\tversion\t\t{version};\n".expandtabs(4) +
        f"\tformat\t\t{format};\n".expandtabs(4) +
        f"\tclass\t\t{foamClass};\n".expandtabs(4) +
        f"\tlocation\t\"{location}\";\n".expandtabs(4) +
        f"\tobject\t\t{object};\n".expandtabs(4) +
        "}\n")

    return foamFile