# 2DTextile.py
# Specify weave parameters
nwarp=4 #Number of weft yarns in the unit cell
nweft=4 #Number of warp yarns in the unit cell
s=1.2 #Spacing between the yarns
t=0.6 #Thickness of the fabric (sum of two yarn heights)
ref=True #Refine model (True/False)
# Create 2D textile
weave = CTextileWeave2D( nweft, nwarp, s, t, ref )
weave.SetGapSize(0)
weave.SetYarnWidths(0.8)
# Set the weave pattern
weave.SwapPosition(0, 1)
weave.SwapPosition(0, 3)
weave.SwapPosition(1, 0)
weave.SwapPosition(1, 2)
weave.SwapPosition(2, 1)
weave.SwapPosition(2, 3)
weave.SwapPosition(3, 0)
weave.SwapPosition(3, 2)
weave.SetXYarnWidths(0, 0.8)
weave.SetXYarnHeights(0, 0.4)
weave.SetXYarnWidths(1, 0.8)
weave.SetXYarnHeights(1, 0.4)
weave.SetXYarnWidths(2, 0.8)
weave.SetXYarnHeights(2, 0.4)
weave.SetXYarnWidths(3, 0.8) 
weave.SetXYarnHeights(3, 0.4)
weave.SetYYarnWidths(0, 0.57)
weave.SetYYarnHeights(0, 0.28)
weave.SetYYarnWidths(1, 0.57)
weave.SetYYarnHeights(1, 0.2)
weave.SetYYarnWidths(2, 0.57)
weave.SetYYarnHeights(2, 0.28)
weave.SetYYarnWidths(3, 0.57)
weave.SetYYarnHeights(3, 0.28)

weave.AssignDefaultDomain()

textilename = AddTextile(weave)

#Add to the textile database
AddTextile(weave)

section = CSectionPowerEllipse(0.4, 0.2, 1, 0)
yarnsection.AddSection(section)
yarnsection.AddSection(section)
yarnsection.AddSection(section)
yarnsection.AddSection(section)
yarnsection.AddSection(section)
textile = GetTextile('2DWeave(W:4,H:4)')
textile.GetYarn(4).AssignSection(yarnsection)
textile.GetYarn(5).AssignSection(yarnsection)
textile.GetYarn(6).AssignSection(yarnsection)
textile.GetYarn(7).AssignSection(yarnsection)




