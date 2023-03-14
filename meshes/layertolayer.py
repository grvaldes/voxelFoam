# LayerToLayer
from TexGen.Core import *

nx = 12  # number of x (warp & binder) yarns
ny = 12  # number of y (weft) yarns
sx = 0.5  # x (warp / binder) yarn spacing
sy = 1  # y (weft) yarn spacing
hx = 0.1  # x (warp / binder) yarn heights
hy = 0.1  # y ( weft) yarn heights

# number of layers
nweft = 16  # number of weft layers
nwarp = nweft - 1  # number of warp layers
nbl = nweft - 2  # number of binder layers

# yarn dimensions and shape
wy = 0.4  # width of yarns on y direction(weft)
wb = 0.4  # binder yarn width
hb = 0.08  # binder yarn heights

# create layer to layer textile
weave = CTextileLayerToLayer(nx, ny, sx, sy, 0.1, hy, nbl, True)

# setting ratio of warp to binder yarns
rwarp = 0  # warp ratio
rbind = 1  # binder yarn ratio

weave.SetWarpRatio(rwarp)
weave.SetBinderRatio(rbind)  # If the warp ratio is 0 then all yarns in the x direction will be binders

# setting up the layers
weave.SetupLayers(nwarp, nweft, nbl)

# set yarn dimensions: widths/heights
weave.SetYYarnWidths(wy)
# weave.SetWarpYarnWidths(0.4)
weave.SetBinderYarnWidths(wb)
weave.SetBinderYarnHeights(hb)

# assign the z-positions to the binder yarns
P = [[0, 2, 2, 2, 1, 3, 3, 3, 1, 2, 2, 2],[1, 1, 2, 0, 0, 0, 2, 1, 1, 1, 3, 1],[2, 2, 0, 2, 2, 2, 1, 3, 3, 3, 1, 2],[3, 1, 1, 1, 2, 0, 0, 0, 2, 1, 1, 1],[1, 2, 2, 2, 0, 2, 2, 2, 1, 3, 3, 3],[1, 1, 3, 1, 1, 1, 2, 0, 0, 0, 2, 1],[3, 3, 1, 2, 2, 2, 0, 2, 2, 2, 1, 3],[2, 1, 1, 1, 3, 1, 1, 1, 2, 0, 0, 0],[1, 3, 3, 3, 1, 2, 2, 2, 0, 2, 2, 2],[0, 0, 2, 1, 1, 1, 3, 1, 1, 1, 2, 0],[2, 2, 1, 3, 3, 3, 1, 2, 2, 2, 0, 2],[2, 0, 0, 0, 2, 1, 1, 1, 3, 1, 1, 1]]

for y in range(0, nx):
    offset = 0
    for x in range(0, ny):
        weave.SetBinderPosition(x, y, P[y][offset])
        offset = offset + 1
      
#NewYarn = weave.AddXYarn(1,1)

# Assign a domain using a min/max box
weave.AssignDomain(CDomainPlanes(XYZ(-0.5, 0, -0.5), XYZ(1.5, 21, 0.5)))

# add textile to database
AddTextile('Textile06', weave)

#create a voxel mesh with the default boundaries 'CPeriodicBoundaries'
VoxMesh = CRectangularVoxelMesh()
vx=50
vy=50
vz=50
VoxMesh.SaveVoxelMesh(weave, "textile_06.inp", vx, vy, vz, False, True,
MATERIAL_CONTINUUM, 0 )
