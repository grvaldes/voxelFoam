import numpy as np
from .common import *

class polyMesh:

    def __init__(self, mesh, fileType):
        # self.owner WILL NOT INCLUDE BOUNDARIES, THEY WILL ONLY BE WRITTEN

        self.origin = fileType
        self.points = mesh.points
        self.boundFaces = self.getCellsFromMeshio(mesh, 2)
        self.cells = self.getCellsFromMeshio(mesh, 3)
        self.pointZones = self.getZonesFromMeshio(mesh, 1)
        self.faceZones = self.getZonesFromMeshio(mesh, 2)
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
            if mesh.point_data == {}:
                for key, zoneI in mesh.point_sets.items():
                    zones[key] = zoneI
            elif mesh.point_sets == {}:
                for key, zoneI in mesh.point_data.items():
                    zones[key] = zoneI
            else:
                Warning("No point sets in the mesh.")
        
        elif ndim > 1:
            if self.origin == "msh":
                if ndim == 2:
                    zones_array = mesh.cell_data["gmsh:physical"][0]
                elif ndim == 3:
                    zones_array = mesh.cell_data["gmsh:physical"][1]

                for key, value in mesh.field_data.items():
                    if ndim == value[-1]:
                        zones[key] = np.nonzero(zones_array == value[0])[0]

            elif self.origin == "inp":
                for key, value in mesh.cell_sets_dict.items():
                    if key != "All":
                        for inKey, inValue in value.items():
                            if ndim == topological_dimension[inKey]:
                                zones[key + "_" + inKey] = inValue

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
        self.innerFaces = {}
        self.boundary = {}
        bnd_grp = {}

        face_ind = []
        face_arr = []
        bound = []
        inner = []
        neigh = []
        owner = []
        bowner = []

        shcount = 0
        count = 0

        for geom, elems in cellFaces.items():
            face_ind.append(np.zeros(shape=(len(elems)*topological_faces[geom]), dtype="int32"))
            face_arr.append(-np.ones(shape=(len(elems)*topological_faces[geom], nodes_per_face[geom]), dtype="int32"))
            bound.append(np.zeros(shape=(len(elems)*topological_faces[geom]), dtype="int32"))
            inner.append(np.zeros(shape=(len(elems)*topological_faces[geom]), dtype="int32"))
            neigh.append(np.zeros(shape=(len(elems)*topological_faces[geom]), dtype="int32"))
            owner.append(np.zeros(shape=(len(elems)*topological_faces[geom]), dtype="int32"))
            bowner.append(np.zeros(shape=(len(elems)*topological_faces[geom]), dtype="int32"))

            for ind, faces in elems.items():
                for _, points in faces.items():
                    face_ind[shcount][count] = int(ind)
                    face_arr[shcount][count,:len(points)] = points
                    count += 1

            shcount += 1

        tot_cl = 0
        tot_in = 0

        for i in range(len(face_arr)):
            mask = np.zeros(shape=(face_ind[i].size), dtype="int32")
            node = np.arange(face_ind[i].size, dtype="int32")
            _, ind, inv, cnt = np.unique(np.sort(face_arr[i], axis=1), axis=0, return_index=True, return_inverse=True, return_counts=True)
            
            for index in range(len(inv)):
                pair = np.nonzero(inv == inv[index])
                owner[i][index] = face_ind[i][pair[0][0]]
                
                if pair[0].size == 2:
                    neigh[i][index] = face_ind[i][pair[0][1]]

            mask[ind] = cnt
            bound[i] = node[np.nonzero(mask == 1)]                     # index of faces we will take as boundaries (no repeated)
            inner[i] = node[np.nonzero(mask == 2)] + tot_in            # index of faces we will take as inner (no repeated)
            bowner[i] = owner[i][node[np.nonzero(mask == 1)]] + tot_cl # owner of inner faces
            owner[i] = owner[i][node[np.nonzero(mask == 2)]] + tot_cl  # owner of inner faces
            neigh[i] = neigh[i][node[np.nonzero(mask == 2)]] + tot_cl  # neighbour of each inner face

            self.innerFaces[face_arr[i].shape[1]] = face_arr[i][inner[i],:]

            tot_cl += np.max(face_ind[i]) + 1
            tot_in += inner[i].size

            for k in self.faceZones.keys():
                key = k + "_" + str(face_arr[i].shape[1])
                bnd_grp[key] = np.array([], dtype="int32")  
                self.boundary[key] = []  

            for j in range(bound[i].size):
                nod = bound[i][j]
                curr_face = face_arr[i][nod,:]

                for k in self.faceZones.keys():
                    key = k + "_" + str(face_arr[i].shape[1])
                    check = np.intersect1d(curr_face, self.faceZones[k])

                    if check.size == curr_face.size:
                        bnd_grp[key] = np.hstack((bnd_grp[key], bowner[i][j]))
                        self.boundary[key].append(face_arr[i][nod,:])

        for k in sorted(self.boundary.keys()):
            self.boundary[k] = np.vstack(tuple(self.boundary[k]))
            owner.append(bnd_grp[k])

        self.neighbour = np.hstack(tuple(neigh))
        self.owner = np.hstack(tuple(owner))

    
    def assignCellFaces(self):
        cellFace = {}
        ind = 0

        for elType in self.cells:
            if elType["type"] == "hexahedron":
                of_elem = of_hex
            elif elType["type"] == "tetra":
                of_elem = of_tet
            elif elType["type"] == "wedge":
                of_elem = of_psm
            elif elType["type"] == "pyramid":
                of_elem = of_pyr

            elFace = {}

            for elem in elType["points"]:
                elFace[ind] = {}
            
                for k, v in of_elem.items():
                    elFace[ind][k] = elem[v]

                ind += 1

            cellFace[elType["type"]] = elFace

        return cellFace


    def generateFaceZones(self):
        # FOR NOW THIS IS ONLY VALID FOR THE TEXGEN INP FILES.
        # I NEED TO MAKE IT GENERIC.

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