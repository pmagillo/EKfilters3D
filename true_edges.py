from image3D import Image3D
from vtkio3D import readVTKcells as readVTK
from vtkio3D import writeVTKcells as writeVTK
from vtkio3D import writeNonBlackVTK, writeCubesVTK

def check_pair(val, img, x,y,z, separation=128):
  """
  Return true if and only if 
  val<separation and img is < separation at (x,y,z)
  or vice versa.
  """
  if x<0 or y<0 or z<0: return False
  if x>=img.dimX or y>=img.dimY or z>=img.dimX: return False  
  other_val = img.get(x,y,z)
  if val<separation and other_val>separation: return True
  if val>separation and other_val<separation: return True
  return False

def boundary_voxel(img, x,y,z, separation=128):
   val = img.get(x,y,z)
   on_boundary = False
   on_boundary = on_boundary or check_pair(val, img,x+1,y,z, separation)
   on_boundary = on_boundary or check_pair(val, img,x-1,y,z, separation)
   on_boundary = on_boundary or check_pair(val, img,x,y-1,z, separation)
   on_boundary = on_boundary or check_pair(val, img,x,y+1,z, separation)
   on_boundary = on_boundary or check_pair(val, img,x,y,z-1, separation)
   on_boundary = on_boundary or check_pair(val, img,x,y,z+1, separation)
   return on_boundary

# ========================================================================

def get_boundary_image(img, separation=128):
  """
  Generate the ideal edge surface for the image img.
  """
  bnd = Image3D(img.dimX,img.dimY,img.dimZ)
  for x in range(img.dimX):
    for y in range(img.dimY):
      for z in range(img.dimZ):
         if boundary_voxel(img, x,y,z, separation):
            bnd.put(x,y,z, 255)
  return bnd     

# ========================================================================
# Instructions

def print_instructions():
  print("Generate the ground truth edge surfaces for a given synthetic image.")
  print("Need the following command-line arguments:")
  print("1) image file name, it must be in vtk format")
  print("2) optionally, output file name, it must end by .vtk or .VTK")

# ========================================================================
# Main

if __name__=="__main__":
  import sys
  try:
    assert len(sys.argv) in [2,3]
    assert sys.argv[1].endswith(".vtk") or sys.argv[1].endswith(".VTK")
    if len(sys.argv)>2:   output_name = sys.argv[2]
    else:   output_name = "image_boundary.vtk"
    assert output_name.endswith(".vtk") or output_name.endswith(".VTK")    
    img = readVTK(sys.argv[1])
    boundary_img = get_boundary_image(img)
    writeVTK(boundary_img, output_name, comment="Ideal boundaries for "+sys.argv[1])
    print("Written", output_name)
  except:
    print_instructions()
