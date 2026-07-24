from image3D import Image3D
from vtkio3D import readVTKcells as readVTK
from vtkio3D import writeVTKcells as writeVTK

# ========================================================================
# Average value at a voxel

def avg_value(img, x,y,z, ind1, ind2):
  """
  Replace the value of voxel (x,y,z) with the average of its
  neighborhod from ind1 to ind2
  """
  n = 0 #number of considered neighbors
  total = 0
  for i in range(ind1,ind2):
    for j in range(ind1,ind2):
      for k in range(ind1,ind2):
         xx,yy,zz = x+i, y+j, z+k
         if xx>=0 and xx<img.dimX and yy>=0 and yy<img.dimY and zz>=0 and zz<img.dimZ:
           n += 1
           total += img.get(xx,yy,zz)
  return total//n
 
# ========================================================================
# Smooth the image by averaging the values of the voxels

def average(img, dim):
  """
  Modify the image by averaging each voxel with its dim^3 neighbors,
  for example dim=3 or dim=5.
  """
  ind2 = dim//2
  ind1 = -ind2
  ind2 += 1
  # examples: dim=3, ind1=-1,ind2=2 or dim=5, ind1=-2, ind2=3
  #print(dim,ind1,ind2)
  newimg = Image3D(img.dimX, img.dimY, img.dimZ)
  for x in range(img.dimX):
    for y in range(img.dimY):
      for z in range(img.dimZ):
         val = avg_value(img, x,y,z, ind1,ind2)
         if val<0: val=0
         elif val>255: val=255
         newimg.put(x,y,z, val)
  return newimg

# ========================================================================
# Smoothing an image, including i/o

def main(input_name, dimension):
  img = readVTK(input_name)
  dir_prefix = input_name.rfind("/")
  if dir_prefix>=0: input_name = input_name[dir_prefix+1:]
  print("Input image name=",input_name)
  averaged_img = average(img, dimension) 
  output_name = "avg_" + str(dimension) + "_" + input_name
  writeVTK(averaged_img, output_name)
  print("Generated file: "+output_name)

# ========================================================================
# Instructions

def print_instructions():
  print("Need the following command-line arguments:")
  print("1) image file name, a file in vtk format")
  print("2) neigborhood size, an odd integer >=3")

# ========================================================================
# Main

if __name__=="__main__":
  import sys
  try:
    assert len(sys.argv)==3
    assert sys.argv[1].endswith(".vtk") or sys.argv[1].endswith(".VTK")
    dim = int(sys.argv[2])
    if dim<3: raise ValueError
    if dim%2==0: raise ValueError
    print("Smooth image by averaging",dim,"x",dim,"x",dim,"voxels")
    main(sys.argv[1], dim)
  except:
    print_instructions()
