"""
This program is STAGE 1 in processing the two images 
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

Instructions to perform stage 1:

First download the files and unzip them. Then run:

python3 decode.py head
python3 decode.py brain

these two commands will generate the files
cthead.vtk
mrbrain.vtk
"""

import sys
sys.path.append('../')
from image3D import Image3D
from vtkio3D import writeVTKcells as writeVTK
from PIL import Image
import numpy
from math import sqrt

# ========================================================================
# byte order

#BYTE_ORDER = "BA" # little endian
BYTE_ORDER = "AB" # big endian

# ========================================================================
# Not used

def decodeBinaryOne(name):
  """
  Read the Stanford binary format of one image
  and return numpy array.
  """
  assert type(name) is str
  F = open(name,"br")
  content = F.read()
  F.close()
  print("Quanti byte",len(content))
  assert len(content) % 2 == 0
  N = sqrt(len(content)//2)
  assert N == int(N)
  N = int(N)
  output = numpy.zeros((N,N), dtype=numpy.uint8)
  Mini, Maxi = None, None
  for x in range(N):
    for y in range(N):
      index = x*N+y
      # a,b are the two bytes composing an integer number
      a, b = content[2*index], content[2*index+1]
      if BYTE_ORDER=="AB": value = a*256+b
      else: value = b*256+a
      # value is from 0 to 65536-1
      value //= 256
      assert value>=0 and value<256
      output[x][y] = value
      if Mini==None or value<Mini: Mini=value
      if Maxi==None or value>Maxi: Maxi=value
  print("Values from",Mini,"to",Maxi)
  return output

# ========================================================================
# Used function: decode one slice of the 3D image

def decodeOneOfMany(file_content, volume_image, slice_num):
  """
  Take file_content, which must be the bits read from one file,
  and the already created volume_image, add the bits of the
  2D image encoded in the file_content to the volume_image
  (i.e., fill one slice).
  """
  N = sqrt(len(file_content)//2) # each 2 bytes are one pixel
  assert N == int(N)
  N = int(N)
  print("Decoding slice",slice_num)
  for x in range(N):
    for y in range(N):
      index = x*N+y
      # a,b are the two bytes composing an integer number
      a, b = file_content[2*index], file_content[2*index+1]
      if BYTE_ORDER=="AB": value = a*256+b
      else: value = b*256+a
      # value is from 0 to 65536-1
      volume_image.put(x,y, slice_num, value)

# ========================================================================
# Used function: decode all the slices and create the 3D image 

def decodeBinaryMany(basename, nx,ny,nz):
  """
  Read the Stanford binary format of number images named
  basename.N for N=1...number and return a 3D image.
  """
  img = Image3D(nx,ny,nz)
  img.disable_range_checking()
  for iz in range(nz):
     name = basename + '.' + str(iz+1)
     F = open(name,"br")
     content = F.read()
     F.close()
     decodeOneOfMany(content, img, iz)
  print("Image values are up to ",img.get_maxval())
  print("and I am rescaling them to range 0..255")
  img.rescale_values([0,img.get_maxval()])
  return img
  
# ========================================================================
# Not used main function

"""
sys.path.append('../IMG_PY')
from imageutil import saveImageArray

def main3D_trial(): # trial: one image of the series
  assert len(sys.argv)==3
  IMAGE = leggiBinario(sys.argv[1])
  print(type(IMAGE))
  saveImageArray(IMAGE, sys.argv[2])
"""

# ========================================================================
# Used main function

def main3D():
  """
  The first argument on command-line must be one of: head brain
  Decode the corresponding image.
  """
  if len(sys.argv)!=2:
    print("Need argument head or brain")
  elif sys.argv[1]=="head":
    volume = decodeBinaryMany("CThead", 256, 256, 113)
    writeVTK(volume, "cthead.vtk")
  elif sys.argv[1]=="brain":
    volume = decodeBinaryMany("MRbrain", 256, 256, 109)
    writeVTK(volume, "mrbrain.vtk")
  else:
    print("Wrong dataset name")

# ========================================================================
# MAIN 
if __name__=="__main__":
  main()
