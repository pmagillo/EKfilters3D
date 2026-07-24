"""
This program is STAGE 2 in processing the two images 
CT Head
MR Brain
from the repository of the Stanford University:
https://graphics.stanford.edu/data/voldata/

STAGE 1: 
The 3D image is given as a sequence of 2D images
(with greylevel on 2 bytes).
Make a unique file in vtk format (with greylevel
on 1 byte, by rescaling the values).

STAGE 2:
In the given image the sampling distance along z-direction
is double wrt the distances along x- and y-directions.
Add a layer of voxels between any two slices, with
interpolated greylevel value.

Instructions to perform stage 2:

From stage1 you have the files
cthead.vtk
mrbrain.vtk

python3 addsliceZ.py cthead.vtk ctheadZ.vtk
python3 addsliceZ.py mrbrain.vtk mrbrainZ.vtk
"""

import sys
sys.path.append('../')
from image3D import Image3D
from vtkio3D import writeVTKcells as writeVTK
from vtkio3D import readVTKcells as readVTK

# ========================================================================
# Function adding a slice between any two slices

def add_slice_z(name_in, name_out):
  IMG = readVTK(name_in)
  dx,dy,dz = IMG.dimX, IMG.dimY, IMG.dimZ
  NEWIMG = Image3D(dx,dy,2*dz-1)
  for z in range(dz):
    for x in range(dx):
      for y in range(dy):
         v1 = IMG.get(x,y,z)
         NEWIMG.put(x,y,2*z, v1)
         if z>0:
           v2 = IMG.get(x,y,z-1)
           NEWIMG.put(x,y, 2*z-1, (v1+v2)//2)
  writeVTK(NEWIMG, name_out)

# ========================================================================
# Main function

def main():
  if len(sys.argv)!=3:
    print("Need input and output file name")
  else:
    print("Reading",sys.argv[1],"and writing",sys.argv[2])
    add_slice_z(sys.argv[1], sys.argv[2])

if __name__=="__main__":
  main()
