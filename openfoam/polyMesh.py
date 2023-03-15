import numpy as np
from .common import *

class polyMesh:

    def __init__(self, mesh, fileType):
        # self.owner WILL NOT INCLUDE BOUNDARIES, THEY WILL ONLY BE WRITTEN

        self.origin = fileType
        self.points = mesh.points
        self.cells = self.getCellsFromMeshio(mesh, 3)
        self.pointZones = self.getZonesFromMeshio(mesh, 1)
        self.cellZones = self.getZonesFromMeshio(mesh, 3)

        self.cleanPoints()
        self.generateFaceZones()
        self.createAllFaces()


        # self.faceCenter = {}
        # self.cellCenter = {}

        # self.getFacesCenter()
        # self.getCellsCenter()

        # self.faceArea = {}
        # self.cellVolume = {}

        # self.getFacesArea()
        # self.getCellsVolume()


    
    def getCellsFromMeshio(self, mesh, ndim):
        cells = []

        for cellI in mesh.cells:
            if ndim == topological_dimension[cellI.type]:
                dict = {
                    "type": cellI.type,
                    "nPts": cellI.data.shape[-1],
                    "points": cellI.data
                }
                cells.append(dict) 

        return cells

    
    def getZonesFromMeshio(self, mesh, ndim):
        zones = {}

        if ndim == 1:
            for key, zoneI in mesh.point_sets.items():
                if "All" not in key:
                    zones[key] = zoneI

        elif ndim == 3:
            for key, value in mesh.cell_sets.items():
                if "All" not in key:
                        zones[key] = value

        return zones
        

    def getFacesCenter(self):
        if self.faceCenter == {}:
            for listI in self.boundFaces:
                x = np.mean(self.points[listI["points"],0], 1)
                y = np.mean(self.points[listI["points"],1], 1)
                z = np.mean(self.points[listI["points"],2], 1)

                self.faceCenter[listI["type"]] = np.array(np.vstack((x, y, z))).T

        try:
            for listI in self.innerFaces:
                x = np.mean(self.points[listI["points"],0], 1)
                y = np.mean(self.points[listI["points"],1], 1)
                z = np.mean(self.points[listI["points"],2], 1)

                self.faceCenter[listI["type"]] = np.array(np.vstack((x, y, z))).T
        except:
            print("Inner faces not defined yet.")


    def getCellsCenter(self):
        self.cellCenter = {}

        for listI in self.cells:
            x = np.mean(self.points[listI["points"],0], 1)
            y = np.mean(self.points[listI["points"],1], 1)
            z = np.mean(self.points[listI["points"],2], 1)

            self.cellCenter[listI["type"]] = np.array(np.vstack((x, y, z))).T


    def cleanPoints(self):
        nodes = np.ones(len(self.points), dtype=bool)

        for k, v in self.pointZones.items():
            if "Constraints" in k:
                nodes[v[0]] = False

        self.pointZones = {k: v for k, v in self.pointZones.items() if "Constraints" not in k}
        self.points = self.points[nodes,:]



    def createAllFaces(self):
        cellFaces = self.assignCellFaces()
        self.boundary = {}
        bnd_grp = {}

        count = 0

        face_ind = np.zeros(shape=(len(cellFaces["hexahedron"])*topological_faces["hexahedron"]), dtype="int32")
        face_arr = -np.ones(shape=(len(cellFaces["hexahedron"])*topological_faces["hexahedron"], nodes_per_face["hexahedron"]), dtype="int32")
        owner = np.zeros(shape=(len(cellFaces["hexahedron"])*topological_faces["hexahedron"]), dtype="int32")
        neigh = np.zeros(shape=(len(cellFaces["hexahedron"])*topological_faces["hexahedron"]), dtype="int32")
        
        for ind, faces in cellFaces["hexahedron"].items():
            for _, points in faces.items():
                face_ind[count] = int(ind)
                face_arr[count,:len(points)] = points
                count += 1

        mask = np.zeros(shape=(face_ind.size), dtype="int32")
        node = np.arange(face_ind.size, dtype="int32")
        _, ind, inv, cnt = np.unique(np.sort(face_arr, axis=1), axis=0, return_index=True, return_inverse=True, return_counts=True)
        
        for index in range(len(inv)):
            pair = np.nonzero(inv == inv[index])
            owner[index] = face_ind[pair[0][0]]
            
            if pair[0].size == 2:
                neigh[index] = face_ind[pair[0][1]]

        mask[ind] = cnt
        bound = node[np.nonzero(mask == 1)]            # index of faces we will take as boundaries (no repeated)
        inner = node[np.nonzero(mask == 2)]            # index of faces we will take as inner (no repeated)
        bowner = owner[node[np.nonzero(mask == 1)]]    # owner of inner faces
        owner = owner[node[np.nonzero(mask == 2)]]     # owner of inner faces
        neigh = neigh[node[np.nonzero(mask == 2)]]     # neighbour of each inner face

        self.innerFaces = face_arr[inner,:]

        for key in self.faceZones.keys():
            bnd_grp[key] = np.array([], dtype="int32")  
            self.boundary[key] = []  

        for j in range(bound.size):
            nod = bound[j]
            curr_face = face_arr[nod,:]

            for key in self.faceZones.keys():
                check = np.intersect1d(curr_face, self.faceZones[key])

                if check.size == curr_face.size:
                    bnd_grp[key] = np.hstack((bnd_grp[key], bowner[j]))
                    self.boundary[key].append(face_arr[nod,:])

        for key in self.boundary.keys():
            self.boundary[key] = np.vstack(tuple(self.boundary[key]))
            owner = np.hstack((owner, bnd_grp[key]))

        self.neighbour = neigh
        self.owner = owner

    
    def assignCellFaces(self):
        cellFace = {}
        ind = 0

        for elType in self.cells:
            elFace = {}

            for elem in elType["points"]:
                elFace[ind] = {}
            
                for k, v in of_hex.items():
                    elFace[ind][k] = elem[v]

                ind += 1

            cellFace[elType["type"]] = elFace

        return cellFace


    def generateFaceZones(self):
        self.faceZones = {}

        texgen_to_openfoam = {
            "outlet": ["FaceA","Edge2","Edge3","Edge6","Edge7","MasterNode2","MasterNode6","MasterNode7","MasterNode3"],
            "inlet": ["FaceB","Edge1","Edge4","Edge5","Edge8","MasterNode1","MasterNode4","MasterNode8","MasterNode5"],
            "front": ["FaceC","Edge3","Edge4","Edge10","Edge11","MasterNode4","MasterNode3","MasterNode7","MasterNode8"],
            "back": ["FaceD","Edge1","Edge2","Edge9","Edge12","MasterNode1","MasterNode5","MasterNode6","MasterNode2"],
            "top": ["FaceE","Edge7","Edge8","Edge11","Edge12","MasterNode5","MasterNode8","MasterNode7","MasterNode6"],
            "bottom": ["FaceF","Edge5","Edge6","Edge9","Edge10","MasterNode1","MasterNode2","MasterNode3","MasterNode4"],
        }

        for k, v in texgen_to_openfoam.items():
            self.faceZones[k] = np.array([], dtype="int32")
            
            for key in v:
                self.faceZones[k] = np.hstack((self.faceZones[k], self.pointZones[key]))


    def checkFaceOrientations(self):
        pass

    def getFacesArea(self):
        pass

    def getCellsVolume(self):
        pass