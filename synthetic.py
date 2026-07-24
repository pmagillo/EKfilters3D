from image3D import Image3D
from vtkio3D import writeVTKcells as writeVTK
import numpy
from math import pi, sin

# ========================================================================
# Generate Gaussian noise with given mean and variance,
# and add it to the given image, clipping the result to 255

def add_gaussian_noise(img, sigma2):
  for x in range(64):
    for y in range(64):
      for z in range(64):
         val = img.get(x,y,z) + int(numpy.random.normal(0.0, sigma2))
         if val>255: val = 255
         elif val<0: val = 0
         img.put(x,y,z, val)
  return img

# ========================================================================
# Condition defining the boundary between the two values in the images

def planeZ(x,y,z):
  return z < 31.5

def sphere(x,y,z):
  x,y,z = x-1, y-1, z-1
  return (x*x+y*y+z*z) < (60.81)**2

def planeXYZ(x,y,z):
  return (x+y+z) > 94

def sinusZ(x,y,z):
  X = pi*(x+0.25)/32
  S = 30*sin(X)+31.5
  return S>z

# ========================================================================
# Generate an image with two values, where the condition defines
# whether a given voxel has one value or the other value

def imageTwoValues(val1, val2, condition):
  """
  Generate an image of side = 64 with two grey values v1 and v2.
  The voxels satisfying the condition will be set to v1,
  the other voxels to v2.
  """
  img = Image3D(64,64,64)
  N1 = N2 = 0
  for x in range(64):
    for y in range(64):
      for z in range(64):
        if condition(x,y,z):
          v = val1
          N1 += 1
        else:
          v = val2
          N2 += 1
        img.put(x,y,z, v)
  return img, N1, N2

# ========================================================================
# Auxiliary function to shorten the main

def generate_save_image(title, name, v1, v2, condition, noise_level=0):
  IMG, N1, N2 = imageTwoValues(v1,v2, condition)
  if noise_level==0:
    # clean image
    name = name + ".vtk"  
    writeVTK(IMG, name, title)
    print("Written " + name)
    print("Voxels with "+str(v1)+"\t"+str(N1))
    print("Voxels with "+str(v2)+"\t"+str(N2))
  else:
    # noisy image with variance = noise_level
    s = str(noise_level)
    if len(s)<3: s = '0'+s
    title = title + " with Gaussian noise, variance= "+str(noise_level)
    noisy_name = "noisy_" + name + "_" + s + ".vtk" 
    noisy_IMG = add_gaussian_noise(IMG, noise_level)
    writeVTK(noisy_IMG, noisy_name, title)
    print("Written " + noisy_name)

# ========================================================================
# Instructions

def print_instructions():
  print("Need the following command-line arguments:")
  print("1) shape name, one of: axis, slanted, sphere, sinus")
  print("2) noise level, one of: 0, 16, 32, 64")

# ========================================================================
# Main
  
if __name__=="__main__":
  import sys
  try:
    # get parameters
    assert len(sys.argv)==3
    shape = sys.argv[1]
    assert shape in ["axis", "slanted", "sphere", "sinus"]
    noise = int(sys.argv[2])
    assert noise in [0,16,32,64]
    # gray levels
    v1, v2 = 64, 192
    ns = " and values "+str(v1)+" and "+str(v2)
    if shape=="axis":
      title = "Image with orthogonal edge surface" + ns
      generate_save_image(title, shape, v1, v2, planeZ, noise)
    if shape=="slanted":
      title = "Image with slanted edge surface" + ns
      generate_save_image(title, shape, v1, v2, planeXYZ, noise)
    if shape=="sphere":
      title = "Image with spheric edge surface" + ns
      generate_save_image(title, shape, v1, v2, sphere, noise)
    if shape=="sinus":
      title = "Image with sinusoidal edge surface" + ns
      generate_save_image(title, shape, v1, v2, sinusZ, noise)
  except:
    print_instructions()
