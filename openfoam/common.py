import numpy as np

MM_TO_METERS = 0.001

topological_dimension = {
    "line": 1,
    "polygon": 2,
    "triangle": 2,
    "quad": 2,
    "tetra": 3,
    "hexahedron": 3,
    "wedge": 3,
    "pyramid": 3,
    "line3": 1,
    "triangle6": 2,
    "quad9": 2,
    "tetra10": 3,
    "hexahedron27": 3,
    "wedge18": 3,
    "pyramid14": 3,
    "vertex": 0,
    "quad8": 2,
    "hexahedron20": 3,
    "triangle10": 2,
    "triangle15": 2,
    "triangle21": 2,
    "line4": 1,
    "line5": 1,
    "line6": 1,
    "tetra20": 3,
    "tetra35": 3,
    "tetra56": 3,
    "quad16": 2,
    "quad25": 2,
    "quad36": 2,
    "triangle28": 2,
    "triangle36": 2,
    "triangle45": 2,
    "triangle55": 2,
    "triangle66": 2,
    "quad49": 2,
    "quad64": 2,
    "quad81": 2,
    "quad100": 2,
    "quad121": 2,
    "line7": 1,
    "line8": 1,
    "line9": 1,
    "line10": 1,
    "line11": 1,
    "tetra84": 3,
    "tetra120": 3,
    "tetra165": 3,
    "tetra220": 3,
    "tetra286": 3,
    "wedge40": 3,
    "wedge75": 3,
    "hexahedron64": 3,
    "hexahedron125": 3,
    "hexahedron216": 3,
    "hexahedron343": 3,
    "hexahedron512": 3,
    "hexahedron729": 3,
    "hexahedron1000": 3,
    "wedge126": 3,
    "wedge196": 3,
    "wedge288": 3,
    "wedge405": 3,
    "wedge550": 3,
    "VTK_LAGRANGE_CURVE": 1,
    "VTK_LAGRANGE_TRIANGLE": 2,
    "VTK_LAGRANGE_QUADRILATERAL": 2,
    "VTK_LAGRANGE_TETRAHEDRON": 3,
    "VTK_LAGRANGE_HEXAHEDRON": 3,
    "VTK_LAGRANGE_WEDGE": 3,
    "VTK_LAGRANGE_PYRAMID": 3,
}

topological_faces = {
    "line": 0,
    "polygon": 1,
    "triangle": 1,
    "quad": 1,
    "tetra": 4,
    "hexahedron": 6,
    "wedge": 5,
    "pyramid": 5,
    "line3": 0,
    "triangle6": 1,
    "quad9": 1,
    "tetra10": 4,
    "hexahedron27": 6,
    "wedge18": 5,
    "pyramid14": 5,
    "vertex": 0,
    "quad8": 1,
    "hexahedron20": 6,
    "triangle10": 1,
    "triangle15": 1,
    "triangle21": 1,
    "line4": 0,
    "line5": 0,
    "line6": 0,
    "tetra20": 4,
    "tetra35": 4,
    "tetra56": 4,
    "quad16": 1,
    "quad25": 1,
    "quad36": 1,
    "triangle28": 1,
    "triangle36": 1,
    "triangle45": 1,
    "triangle55": 1,
    "triangle66": 1,
    "quad49": 1,
    "quad64": 1,
    "quad81": 1,
    "quad100": 1,
    "quad121": 1,
    "line7": 0,
    "line8": 0,
    "line9": 0,
    "line10": 0,
    "line11": 0,
    "tetra84": 4,
    "tetra120": 4,
    "tetra165": 4,
    "tetra220": 4,
    "tetra286": 4,
    "wedge40": 5,
    "wedge75": 5,
    "hexahedron64": 6,
    "hexahedron125": 6,
    "hexahedron216": 6,
    "hexahedron343": 6,
    "hexahedron512": 6,
    "hexahedron729": 6,
    "hexahedron1000": 6,
    "wedge126": 5,
    "wedge196": 5,
    "wedge288": 5,
    "wedge405": 5,
    "wedge550": 5,
    "VTK_LAGRANGE_CURVE": 0,
    "VTK_LAGRANGE_TRIANGLE": 1,
    "VTK_LAGRANGE_QUADRILATERAL": 1,
    "VTK_LAGRANGE_TETRAHEDRON": 4,
    "VTK_LAGRANGE_HEXAHEDRON": 6,
    "VTK_LAGRANGE_WEDGE": 5,
    "VTK_LAGRANGE_PYRAMID": 5,
}

nodes_per_face = {
    "triangle": 3,
    "quad": 4,
    "tetra": 3,
    "hexahedron": 4,
    "wedge": 4,
    "pyramid": 4,
    "triangle6": 6,
    "quad9": 9,
    "tetra10": 6,
    "hexahedron27": 9,
    "wedge18": 9,
    "pyramid14": 9,
    "quad8": 8,
    "hexahedron20": 8,
    "triangle10": 10,
    "triangle15": 15,
    "triangle21": 21,
    "tetra20": 10,
    "tetra35": 15,
    "tetra56": 21,
    "quad16": 16,
    "quad25": 25,
    "quad36": 36,
    "triangle28": 28,
    "triangle36": 36,
    "triangle45": 45,
    "triangle55": 55,
    "triangle66": 66,
    "quad49": 49,
    "quad64": 64,
    "quad81": 81,
    "quad100": 100,
    "quad121": 121,
    # "tetra84": 4,
    # "tetra120": 4,
    # "tetra165": 4,
    # "tetra220": 4,
    # "tetra286": 4,
    # "wedge40": 5,
    # "wedge75": 5,
    # "hexahedron64": 6,
    # "hexahedron125": 6,
    # "hexahedron216": 6,
    # "hexahedron343": 6,
    # "hexahedron512": 6,
    # "hexahedron729": 6,
    # "hexahedron1000": 6,
    # "wedge126": 5,
    # "wedge196": 5,
    # "wedge288": 5,
    # "wedge405": 5,
    # "wedge550": 5,
    "VTK_LAGRANGE_TRIANGLE": 3,
    "VTK_LAGRANGE_QUADRILATERAL": 4,
    "VTK_LAGRANGE_TETRAHEDRON": 3,
    "VTK_LAGRANGE_HEXAHEDRON": 4,
    "VTK_LAGRANGE_WEDGE": 4,
    "VTK_LAGRANGE_PYRAMID": 4,
}

abaqus_tet = {
    "face1": np.array([0, 1, 2]),
    "face2": np.array([0, 3, 1]),
    "face3": np.array([1, 3, 2]),
    "face4": np.array([2, 3, 0])
}
abaqus_hex = {
    "face1": np.array([0, 1, 2, 3]),
    "face2": np.array([4, 7, 6, 5]),
    "face3": np.array([0, 4, 5, 1]),
    "face4": np.array([1, 5, 6, 2]),
    "face5": np.array([2, 6, 7, 3]),
    "face6": np.array([3, 7, 4, 0])
}
abaqus_psm = {
    "face1": np.array([0, 1, 2]),
    "face2": np.array([3, 5, 4]),
    "face3": np.array([0, 3, 4, 1]),
    "face4": np.array([1, 4, 5, 2]),
    "face5": np.array([2, 5, 4, 1])
}

of_tet = {
    "face1": np.array([1, 2, 3]),
    "face2": np.array([2, 0, 3]),
    "face3": np.array([0, 1, 3]),
    "face4": np.array([1, 0, 2])
}
of_hex = {
    "face1": np.array([0, 4, 7, 3]),
    "face2": np.array([1, 2, 6, 5]),
    "face3": np.array([0, 1, 5, 4]),
    "face4": np.array([2, 3, 7, 6]),
    "face5": np.array([0, 3, 2, 1]),
    "face6": np.array([4 ,5 ,6 ,7])
}
of_psm = {
    "face1": np.array([0, 2, 1]),
    "face2": np.array([3 ,4, 5]),
    "face3": np.array([0, 3, 5, 2]),
    "face4": np.array([1, 2, 5 ,4]),
    "face5": np.array([0, 1, 4, 3])
}
of_pyr = {
    "face1": np.array([0, 3, 2, 1]),
    "face2": np.array([0, 4, 3]),
    "face3": np.array([2, 3, 4]),
    "face4": np.array([1, 2, 4]),
    "face5": np.array([0, 1, 4])
}
of_wdg = {
    "face1": np.array([0, 2, 1]),
    "face2": np.array([3, 4, 5, 6]),
    "face3": np.array([0, 3, 6]),
    "face4": np.array([1, 2, 5, 4]),
    "face5": np.array([0, 1, 4, 3]),
    "face6": np.array([0, 6, 5, 2])
}
of_twg = {
    "face1": np.array([0, 2, 1]),
    "face2": np.array([0, 1, 3]),
    "face3": np.array([0, 3, 4, 2]),
    "face4": np.array([1, 3, 4, 3])
}

texgen_to_openfoam = {
    "right": ["FaceA","Edge2","Edge3","Edge6","Edge7","MasterNode2","MasterNode6","MasterNode7","MasterNode3"],
    "left": ["FaceB","Edge1","Edge4","Edge5","Edge8","MasterNode1","MasterNode4","MasterNode8","MasterNode5"],
    "back": ["FaceC","Edge3","Edge4","Edge10","Edge11","MasterNode4","MasterNode3","MasterNode7","MasterNode8"],
    "front": ["FaceD","Edge1","Edge2","Edge9","Edge12","MasterNode1","MasterNode5","MasterNode6","MasterNode2"],
    "top": ["FaceE","Edge7","Edge8","Edge11","Edge12","MasterNode5","MasterNode8","MasterNode7","MasterNode6"],
    "bottom": ["FaceF","Edge5","Edge6","Edge9","Edge10","MasterNode1","MasterNode2","MasterNode3","MasterNode4"],
}