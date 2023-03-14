from pathlib import Path

def createFolderStructure(filename):
    
    Path(filename).mkdir(exist_ok=True)

    Path(filename + "/0").mkdir(exist_ok=True)
    Path(filename + "/constant").mkdir(exist_ok=True)
    Path(filename + "/system").mkdir(exist_ok=True)

    Path(filename + "/constant/polyMesh").mkdir(exist_ok=True)
    Path(filename + "/constant/polyMesh/sets").mkdir(exist_ok=True)


def cleanFolderStructure(filename):

    path = Path(filename + "/constant/polyMesh/sets")

    if not any(path.iterdir()):
        path.rmdir()