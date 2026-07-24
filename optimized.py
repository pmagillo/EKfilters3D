from image3D import Image3D
from image3D import writeOccupiedVoxels
from vtkio3D import readVTKcells as readVTK
from vtkio3D import writeVTKcells as writeVTK
from vtkio3D import writeNonBlackVTK

# ========================================================================
# Generate the optimized filters for Sobel and EK
"""
Each filter is a dictionary with key = the coordinates of a neighbor voxel
and value = the coefficient to apply to such neighbor.
The coordinates are in relative indexes wrt to the voxel on which the
filter will be placed (i.e., from -1 to 1).
"""

def ottimSobel1():
  coord = [(-1,-1,-1), (-1,-1,0), (-1,-1,1), (-1,0,-1), (-1,0,0), (-1,0,1), (-1,1,-1), (-1,1,0), (-1,1,1), (1,-1,-1), (1,-1,0), (1,-1,1), (1,0,-1), (1,0,0), (1,0,1), (1,1,-1), (1,1,0), (1,1,1)]
  coeff = [1,2,1,2,4,2,1,2,1,-1,-2,-1,-2,-4,-2,-1,-2,-1] 
  return [(c[0],c[1],c[2],t) for c,t in zip(coord, coeff)]

def ottimSobel2():
  coord = [(-1,-1,-1), (-1,-1,1), (-1,0,-1), (-1,0,1), (-1,1,-1), (-1,1,1), (0,-1,-1), (0,-1,1), (0,0,-1), (0,0,1), (0,1,-1), (0,1,1), (1,-1,-1), (1,-1,1), (1,0,-1), (1,0,1), (1,1,-1), (1,1,1)]
  coeff = [1,-1,2,-2,1,-1,2,-2,4,-4,2,-2,1,-1,2,-2,1,-1]
  return [(c[0],c[1],c[2],t) for c,t in zip(coord, coeff)]

def ottimSobel3():
  coord = [(-1,-1,-1), (-1,-1,0), (-1,-1,1), (-1,1,-1), (-1,1,0), (-1,1,1), (0,-1,-1), (0,-1,0), (0,-1,1), (0,1,-1), (0,1,0), (0,1,1), (1,-1,-1), (1,-1,0), (1,-1,1), (1,1,-1), (1,1,0), (1,1,1)]
  coeff = [1,2,1,-1,-2,-1,2,4,2,-2,-4,-2,1,2,1,-1,-2,-1] 
  return [(c[0],c[1],c[2],t) for c,t in zip(coord, coeff)]

def ottimEK1():
  coord = [(-1,-1,-1), (-1,0,0), (0,-1,0), (0,0,-1), (0,0,1), (0,1,0), (1,0,0), (1, 1, 1)]
  coeff = [-2,-1,-1,-1,1,1,1,2]
  return [(c[0],c[1],c[2],t) for c,t in zip(coord, coeff)]

def ottimEK2():
  coord = [(-1,0,0), (-1,1,-1), (0,-1,0), (0,0,-1), (0,0,1), (0,1,0), (1,-1,1), (1,0,0)]
  coeff = [-1,-2,1,-1,1,-1,2,1]
  return [(c[0],c[1],c[2],t) for c,t in zip(coord, coeff)]
 
def ottimEK3():
  coord = [(-1,-1,1), (-1,0,0), (0,-1,0), (0,0,-1), (0,0,1), (0,1,0), (1,0,0), (1,1,-1)] 
  coeff = [-2,-1,-1,1,-1,1,1,2]
  return [(c[0],c[1],c[2],t) for c,t in zip(coord, coeff)]
  
def ottimEK4():
  coord = [(-1,0,0), (-1,1,1), (0,-1,0), (0,0,-1), (0,0,1), (0,1,0), (1,-1,-1), (1,0,0)]
  coeff = [-1,-2,1,1,-1,-1,2,1]
  return [(c[0],c[1],c[2],t) for c,t in zip(coord, coeff)]

# ========================================================================
# Compute edge value at a voxel

def new_with_coeff(img, x,y,z, ccc):
  """
  img is an image, (x,y,z) are the coordinates of one of its voxels.
  ccc is a dictionary generated with one of the above functions, and 
  represents a directional edge filter.
  Apply the filter to the voxel and return the absolute value of the
  resulting edge value.
  """
  S = 0
  for i,j,k,c in ccc:
    S += ( img.loose_get(x+i,y+j,z+k)*c )
  if S<0: S = -S
  return S

# ========================================================================
# Perform edge detection

def edge_detection(img, coords_coeffs, rescaling=True):
  """
  img is an image. coords_coeffs are the 3 (for Sobel) or 4 (for EK)
  directional filters.
  Filter the image with all the directional filters and combine
  the results by using the square root of the squares of each
  directional value.
  """
  temp = [0]*len(coords_coeffs)
  newimg = Image3D(img.dimX, img.dimY, img.dimZ)
  newimg.disable_range_checking()
  for x in range(img.dimX):
    for y in range(img.dimY):
      for z in range(img.dimZ):
        for t in range(len(coords_coeffs)):
           temp[t] = new_with_coeff(img, x,y,z, coords_coeffs[t])
        val = sum(v*v for v in temp) # val>=0
        newimg.put(x,y,z, int(val**0.5))
  if not rescaling: newimg.truncate_values()
  else: newimg.rescale_values((0,newimg.get_maxval()))
  return newimg

# ========================================================================
# Apply one of the two edge detection filters to the image

def apply_edge_detect(img, method):
  print("Apply "+method+" -----------------------");
  if method=="Sobel":
    masks = (ottimSobel1(),ottimSobel2(),ottimSobel3())
  elif method=="EK":
    masks = (ottimEK1(),ottimEK2(),ottimEK3(),ottimEK4())
  else:
    raise ValueError

  return edge_detection(img, masks)

# ========================================================================
# Auxiliary function to shorten the main

def main(input_name, method_name, writing=True):
  print("Apply "+method_name+" filter to 3D image in "+input_name)
  img = readVTK(input_name)
  dir_prefix = input_name.rfind("/")
  if dir_prefix>=0: input_name = input_name[dir_prefix+1:]
  print("Image name=",input_name)
  edges = apply_edge_detect(img, method_name)  
  output_name = method_name + "_" + input_name
  if writing: 
    writeVTK(edges, output_name)
    print("Generated file: "+output_name)

# ========================================================================
# Instructions

def print_instructions():
  print("Need the following command-line arguments:")
  print("1) image file name, it must be in vtk format")
  print("2) edge filte, it must be one of Sobel or EK")
  print("3) optionally, NOOUT --> the output is not generated")

# ========================================================================
# Main

if __name__=="__main__":
  import sys
  args = sys.argv[:]
  try:
    if "NOOUT" in args: args.remove("NOOUT")
    assert len(args)==3
    assert args[2] in ["Sobel","EK"]
    assert args[1].endswith(".vtk") or args[1].endswith(".VTK")
    print("Optimized Edge extraction with "+args[2]+" filters")
    if "NOOUT" in sys.argv: main(args[1], args[2], writing=False)
    else: main(args[1], args[2], writing=True)
  except AssertionError:
    print_instructions()
  except FileNotFoundError as err:
    print("Input file not found", e.getMessage())
  except:
    raise
