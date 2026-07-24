"""
Convert an image from the TU Wien repository to vtk format.

The input images are from 
https://www.cg.tuwien.ac.at/research/vis/datasets/

First you have to download the images from the repository.
The images are in .dat format. Then use this program to convert
them to vtk format.

python dat2vtk.py christmastree512x499x512.dat tree.vtk
python dat2vtk.py present492x492x442.dat present.vtk
python dat2vtk.py stagbeetle832x832x494.dat beetle.vtk
"""

import sys
sys.path.append('../')
from image3D import Image3D
from vtkio3D import writeVTKcells as writeVTK

"""
Data description from 
https://www.cg.tuwien.ac.at/research/vis/datasets/

All data sets are stored in a simple binary format. 
It consits of a 6 byte header which contains the data set dimensions 
(one unsigned 2 byte value per dimension) followed by the voxel data 
(one unsigned 2 byte value per voxel) in sequential slice-by-slice order. 
The data range is [0,4095]. The format uses little-endian byte order. 
"""

# ========================================================================
# Decode two bytes from the file to one int value

def decode2bytes(file_content, index):
  """
  file_content is the entire binary content of the file,
  from it the index-th pair of bytes will be decoded
  into a single number.
  The byte order encoded in BYTE_ORDER is used.
  """
  BYTE_ORDER = "BA" # little endian
  a, b = file_content[2*index], file_content[2*index+1]
  if BYTE_ORDER=="AB": value = a*256+b
  else: value = b*256+a
  return value

# ========================================================================
# Decode an image

def conversionDatToImage(file_name):
  """
  Decode an image from a file in .dat format and return it as
  an object of class image3D.
  """
  F = open(file_name,"rb")
  content = F.read()
  F.close()
  #decode dimensions (on 2 bytes each)
  nx = decode2bytes(content, 0)
  ny = decode2bytes(content, 1)
  nz = decode2bytes(content, 2)
  print("Dimensions",nx,ny,nz)
  img = Image3D(nx,ny,nz)
  img.disable_range_checking()
  i = 0
  for z in range(nz):
    for y in range(ny):
      for x in range(nx):
        i += 1
        val = decode2bytes(content, i)
        img.put(x,y,z, val)
  print("Valori fino a ",img.get_maxval(),"e li riscalo")
  img.rescale_values([0,img.get_maxval()])
  return img

# ========================================================================
# Main

if __name__=="__main__":
  if len(sys.argv)==3:
    volume = conversionDatToImage(sys.argv[1])
    writeVTK(volume,sys.argv[2])
    print("Written to",sys.argv[2])
  else:
    print("Need names of input dat file and output vtk file")
