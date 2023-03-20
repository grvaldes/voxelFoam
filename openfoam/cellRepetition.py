from .common import texgen_to_openfoam
import numpy as np

def cellRepetition(poly, dx = 1, dy = 1, dz = 1):
    mask = np.ones(shape=(3,poly.points.shape[0]), dtype=bool)
    pbounds = {
        "left": np.hstack(tuple((poly.pointZones[k] for k in texgen_to_openfoam["left"]))),
        "front": np.hstack(tuple((poly.pointZones[k] for k in texgen_to_openfoam["front"]))),
        "bottom": np.hstack(tuple((poly.pointZones[k] for k in texgen_to_openfoam["bottom"]))),
    }

    mask[0,pbounds["left"]] = 0
    mask[1,pbounds["front"]] = 0
    mask[2,pbounds["bottom"]] = 0

    rep = []

    wd = poly.boundBox[:,1] - poly.boundBox[:,0]

    for z in range(dz):
        for y in range(dy):
            for x in range(dx):
                np.vstack((poly.points, poly.points[mask[0,:], :] + x*wd))
                newElems = poly.cells[0]["points"]
                
    
    return poly