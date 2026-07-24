from image3D import Image3D
from image3D import writeOccupiedVoxels

def writeVTKpoints(img, filename, comment=None):
  """
  Write the image (instance of class Image3D) on the VTK 
  file VTK named filename.
  """
  if filename.endswith(".txt"):
    filename = filename[:len(filename)-4]
  if not filename.endswith(".vtk"):
    filename = filename + ".vtk" 
  #print(filename)
  f = open(filename,"w")
  f.write("# vtk DataFile Version 2.0\n")
  if comment and type(comment)==str:
    f.write(comment+"\n")
  else: f.write("\n")
  f.write("ASCII\n")
  f.write("DATASET STRUCTURED_POINTS\n")
  f.write("DIMENSIONS ")
  f.write(str(img.dimX)+" "+str(img.dimY)+" "+str(img.dimZ)+"\n")
  f.write("ASPECT_RATIO 1 1 1\n")
  f.write("ORIGIN 0 0 0\n")
  f.write("POINT_DATA "+str(img.dimX*img.dimY*img.dimZ)+"\n")
  f.write("SCALARS volume_scalars unsigned_char 1\n")
  f.write("LOOKUP_TABLE default\n")
  for z in range(img.dimZ):
    #for x in range(img.dimX):
    #  for y in range(img.dimY):
    for y in range(img.dimY):
      for x in range(img.dimX):
        f.write(str(img.get(x,y,z))+" ")
      f.write("\n")
    f.write("\n")
  f.close()

def writeVTKcells(img, filename, comment=None):
  """
  Write the image (instance of class Image3D) on the VTK 
  file VTK named filename.
  """
  if filename.endswith(".txt"):
    filename = filename[:len(filename)-4]
  if not filename.endswith(".vtk"):
    filename = filename + ".vtk" 
  #print(filename)
  f = open(filename,"w")
  f.write("# vtk DataFile Version 2.0\n")
  if comment and type(comment)==str:
    f.write(comment+"\n")
  else: f.write("\n")
  f.write("ASCII\n")
  f.write("DATASET STRUCTURED_POINTS\n")
  f.write("DIMENSIONS ")
  f.write(str(img.dimX+1)+" "+str(img.dimY+1)+" "+str(img.dimZ+1)+"\n")
  f.write("ASPECT_RATIO 1 1 1\n")
  f.write("ORIGIN 0 0 0\n")
  f.write("CELL_DATA "+str(img.dimX*img.dimY*img.dimZ)+"\n")
  f.write("SCALARS volume_scalars unsigned_char 1\n")
  f.write("LOOKUP_TABLE default\n")
  for z in range(img.dimZ):
    #for x in range(img.dimX):
    #  for y in range(img.dimY):
    for y in range(img.dimY):
      for x in range(img.dimX):
        f.write(str(img.get(x,y,z))+" ")
      f.write("\n")
    f.write("\n")
  f.close()

def read_next_line(file):
  """
  Read the next non-empty line from the file and return it.
  """
  while True:
    lin = file.readline().strip()
    if len(lin)>0: return lin
    
def read_line_with(file, keyword):
  """
  Read lines from the file, until a line starting with the given
  keyword is found, and return such line.
  """
  while True:
    lin = file.readline().strip()
    if lin==None or lin.startswith(keyword): 
       return lin
    
def readVTKpoints(filename):
  """
  Read a 3D image (instance of class Image3D) from the VTK file
  named filename, and return the image.
  """
  assert filename.endswith(".vtk") or filename.endswith(".VTK")
  f = open(filename,"r")
  read_line_with(f, "# vtk DataFile")
  read_line_with(f,"ASCII")
  read_line_with(f,"DATASET STRUCTURED_POINTS")
  lin = read_line_with(f,"DIMENSIONS ")
  assert lin
  lin = lin.split()
  lin = lin[1:]
  xx, yy, zz = [int(p) for p in lin]
  IMG = Image3D(xx,yy,zz)
  lin = read_line_with(f,"ASPECT_RATIO") #ci sono tre numeri
  lin = read_line_with(f,"ORIGIN") #ci sono tre numeri
  lin = read_line_with(f,"POINT_DATA") #un numero
  lin = read_line_with(f,"SCALARS") # volume_scalars char 1\n")
  lin = read_line_with(f,"LOOKUP_TABLE") # default\n")
  """
  for z in range(zz):
    for x in range(xx):
      lin = read_next_line(f).split()
      assert len(lin)==yy
      for y in range(yy):
        val = int(lin[y])
        IMG.put(x,y,z, val)
  """
  data = f.read().split()
  assert len(data) == xx * yy * zz
  i = 0
  for z in range(zz):
    for y in range(yy):
      for x in range(xx):
        val = int(data[i])
        IMG.put(x,y,z, val)
        i += 1
  f.close()  
  return IMG


def readVTKcells(filename):
  """
  Read a 3D image (instance of class Image3D) from the VTK file
  named filename, and return the image.
  """
  assert filename.endswith(".vtk") or filename.endswith(".VTK")
  f = open(filename,"r")
  read_line_with(f, "# vtk DataFile")
  read_line_with(f,"ASCII")
  read_line_with(f,"DATASET STRUCTURED_POINTS")
  lin = read_line_with(f,"DIMENSIONS ")
  assert lin
  lin = lin.split()
  lin = lin[1:]
  xx, yy, zz = [int(p)-1 for p in lin] #assuming cell-centered colors
  IMG = Image3D(xx,yy,zz)
  lin = read_line_with(f,"ASPECT_RATIO") #ci sono tre numeri
  lin = read_line_with(f,"ORIGIN") #ci sono tre numeri
  lin = read_line_with(f,"CELL_DATA") #un numero
  lin = read_line_with(f,"SCALARS") # volume_scalars char 1\n")
  lin = read_line_with(f,"LOOKUP_TABLE") # default\n")
  """
  for z in range(zz):
    for x in range(xx):
      lin = read_next_line(f).split()
      assert len(lin)==yy
      for y in range(yy):
        val = int(lin[y])
        IMG.put(x,y,z, val)
  """
  data = f.read().split()
  assert len(data) == xx * yy * zz
  i = 0
  for z in range(zz):
    for y in range(yy):
      for x in range(xx):
        val = int(data[i])
        IMG.put(x,y,z, val)
        i += 1
  f.close()  
  return IMG


def writeCubesVTK(cubes, filename, comment=None, shift=0, values=None):
  N = len(cubes)
  if filename.endswith(".txt"):
    filename = filename[:len(filename)-4]
  if not filename.endswith(".vtk"):
    filename = filename + ".vtk" 
  #print(filename)
  f = open(filename,"w")
  f.write("# vtk DataFile Version 2.0\n")
  if comment and type(comment)==str:
    f.write(comment+"\n")
  else: f.write("\n")
  f.write("ASCII\n")
  f.write("DATASET UNSTRUCTURED_GRIDS\n\n")
  f.write("POINTS "+str(8*N)+" float\n")
  for x,y,z in cubes:
    for xx in (x-0.5,x+0.5):
      for yy in (y-0.5,y+0.5):
        for zz in (z-0.5,z+0.5):
           f.write(str(xx+shift)+" "+str(yy+shift)+" "+str(zz+shift)+"\n")
  f.write("CELLS "+str(N)+" "+str(9*N)+"\n")
  for i in range(N):
    f.write("8")
    for j in range(8): f.write(" "+str(8*i+j))
    f.write("\n")
  f.write("CELL_TYPES "+str(N)+"\n")
  for i in range(N):
    f.write(" 11")
  f.write("\n")
  if values:
    assert len(values)==N
    f.write("CELL_DATA "+str(N)+"\n")
    if type(values[0]) is int:
      f.write("SCALARS cell_scalars int 1\n")
    elif type(values[0]) is float:
      f.write("SCALARS cell_scalars float 1\n")
    else:
      raise ValueError
    f.write("LOOKUP_TABLE default\n")
    for i in range(N):
      f.write(" "+str(values[i]))
    f.write("\n")
  f.close()

def writeNonBlackVTK(img, filename, comment=None):
  voxels = img.non_black_voxels()
  writeCubesVTK(voxels, filename, comment)
  
if __name__=="__main__":
  readVTK = readVTKpoints
  import sys
  #print("Leggo immagine 3D come matrice e scrivo solo i voxel non vuoti")
  img = readVTK(sys.argv[1])
  writeOccupiedVoxels(img)
  writeNonBlackVTK(img,"nonneri.vtk")

