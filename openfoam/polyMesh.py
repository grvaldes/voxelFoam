import numpy as np
from .common import *

class polyMesh:

    def __init__(self, mesh, fileType):
        self.origin = fileType
        self.points = self.getPoints(mesh)
        self.cells = self.getCellsFromMeshio(mesh, 3)
        self.pointZones = self.getZonesFromMeshio(mesh, 1)
        self.cellZones = self.getZonesFromMeshio(mesh, 3)

        self.cleanPoints()
        self.generateFaceZones()
        self.createAllFaces()


        # self.faceCenter = {}
        # self.cellCenter = {}

        # self.getFacesCenter()"
        # self.getCellsCenter()

        # self.faceArea = {}
        # self.cellVolume = {}

        # self.getFacesArea()
        # self.getCellsVolume()


    def getPoints(self, mesh):
        pts = mesh.points
        zon = mesh.point_sets

        self.boundBox = np.vstack((np.min(pts,0),np.max(pts,0))).T
        self.discretization = np.array([zon["Edge9"].size, zon["Edge5"].size, zon["Edge1"].size], dtype="int32") + 1

        return pts

    
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

        dx, dy, dz = self.discretization

        bound = {
            "left" : np.hstack(tuple(np.arange(0, dx*dy, dx) + k*dx*dy for k in range(dz))),
            "right" : np.hstack(tuple(np.arange(dx-1, dx*dy+1, dx) + k*dx*dy for k in range(dz))),
            "front" : np.hstack(tuple(np.arange(dx) + k*dx*dy for k in range(dz))),
            "back" : np.hstack(tuple(np.arange(dx*(dy-1), dx*dy) + k*dx*dy for k in range(dz))),
            "top" : np.arange(dx*dy*(dz-1), dx*dy*dz),
            "bottom" : np.arange(dx*dy),
        }

        self.boundary["left"] = np.array([cellFaces[int(k)]["face4"] for k in bound["left"]], dtype="int32")
        self.boundary["right"] = np.array([cellFaces[int(k)]["face3"] for k in bound["right"]], dtype="int32")
        self.boundary["front"] = np.array([cellFaces[int(k)]["face1"] for k in bound["front"]], dtype="int32")
        self.boundary["back"] = np.array([cellFaces[int(k)]["face2"] for k in bound["back"]], dtype="int32")
        self.boundary["top"] = np.array([cellFaces[int(k)]["face6"] for k in bound["top"]], dtype="int32")
        self.boundary["bottom"] = np.array([cellFaces[int(k)]["face5"] for k in bound["bottom"]], dtype="int32")

        bound_owner = np.hstack(tuple(bound[key] for key in bound.keys()))

        count = 0

        cell_ind_of_face = np.tile(np.arange(len(cellFaces), dtype="int32"), (topological_faces["hexahedron"],1)).T
        face_array_nodes = -np.ones(shape=(len(cellFaces)*topological_faces["hexahedron"], nodes_per_face["hexahedron"]), dtype="int32")

        for faces in cellFaces.values():
            for nodes in faces.values():
                face_array_nodes[count,:] = nodes
                count += 1
        
        owner = np.ones(shape=(cell_ind_of_face.shape), dtype=bool)
        neigh = np.zeros(shape=(cell_ind_of_face.shape), dtype="int32")

        owner[:,[0,3,4]] = 0          # Deleting all left, bottom and front faces from ownership
        owner[bound["back"],1] = 0    # Deleting boundaries from ownership
        owner[bound["right"],2] = 0
        owner[bound["top"],5] = 0

        neigh[:,0] = -dx
        neigh[:,1] = dx
        neigh[:,2] = 1
        neigh[:,3] = -1
        neigh[:,4] = -dx*dy
        neigh[:,5] = dx*dy

        inner_owner = cell_ind_of_face[owner].reshape(-1)
        self.neighbour = (cell_ind_of_face + neigh).reshape(-1)
        self.owner = np.hstack((inner_owner, bound_owner))

        self.innerFaces = face_array_nodes[inner_owner.reshape(-1),:]
    

    def assignCellFaces(self):
        cellFace = {}
        ind = 0

        # for k, v in of_hex.items():
        #     cellFace[k] = []

        #     for elem in self.cells[0]["points"]:
        #         pass

        for elem in self.cells[0]["points"]:
            cellFace[ind] = {}
        
            for k, v in of_hex.items():
                cellFace[ind][k] = elem[v]

            ind += 1

        return cellFace


    def generateFaceZones(self):
        self.faceZones = {}

        texgen_to_openfoam = {
            "right": ["FaceA","Edge2","Edge3","Edge6","Edge7","MasterNode2","MasterNode6","MasterNode7","MasterNode3"],
            "left": ["FaceB","Edge1","Edge4","Edge5","Edge8","MasterNode1","MasterNode4","MasterNode8","MasterNode5"],
            "back": ["FaceC","Edge3","Edge4","Edge10","Edge11","MasterNode4","MasterNode3","MasterNode7","MasterNode8"],
            "front": ["FaceD","Edge1","Edge2","Edge9","Edge12","MasterNode1","MasterNode5","MasterNode6","MasterNode2"],
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