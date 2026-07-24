"""
Given the edge images computed through Sobel filter and EK filter,
and a threshold value (voxels with greylevel>=threshold are considered
as edge voxels), create a VTK file where:
- cubes that are edges both in Sobel and EK   have value 100
- cubes that are edges in Sobel and not in EK have value 50
- cubes that are edges in EK and not in Sobel have value 150
- cubes that are non-edges in both have value zero
"""

from vtkio3D import readVTKcells as readVTK
from vtkio3D import writeVTKcells as writeVTK
from image3D import Image3D
import sys

# ========================================================================
# Auxiliary function

from vtkio3D import read_next_line

def read_another(current_line, f):
  """
  The parameter current_line contains the last line read from vtk file f,
  already split into a list and each element of the list converted to int.
  Read another element (int) from the line.
  If line is finisced, read another line. Otherwise take the
  element from this line and eliminate the element.
  """
  if len(current_line)==0:
    #line was empty
    current_line = read_next_line(f)
    current_line = [int(v) for v in current_line.split()]
  value = current_line[0]
  return (value, current_line[1:])

# ========================================================================
# Scan the two input images in parallel and create the output image

def read_two_create_one(T, sobel_input, ek_input, output):
    """
    read the two edge images sobel_input and ek_input,
    generate the output image while reading
    """
    f1 = open(sobel_input,"r")
    f2 = open(ek_input,"r")
    outf = open(output,"w")
    data = False
    while (not data):
      line1 = f1.readline()
      line2 = f2.readline()
      if line1.startswith("DIMENSIONS"):
        p1, p2 = line1.split(), line2.split()
        for i in range(1,4): assert p1[i]==p2[i]
        dx, dy, dz = int(p1[1]), int(p1[2]), int(p1[3])
      outf.write(line1)
      if line1.startswith("LOOKUP_TABLE"): data = True
    total_num = (dx-1)*(dy-1)*(dz-1)
    line1, line2 = [], []
    i = 0
    while (i<total_num):
          #print("Read element",i,"of",total_num)
          sobel, line1 = read_another(line1, f1)
          ek, line2 = read_another(line2, f2)
          if sobel<T and ek<T: classif = 0
          if sobel>=T and ek>=T: classif = 100
          if sobel>=T and ek<T: classif = 50
          if sobel<T and ek>=T: classif = 150
          outf.write(str(classif)+" ")
          i += 1
    f1.close()
    f2.close()
    outf.close()

# ========================================================================
# Main function

def main(args):
    N = len(args)
    #for i in range(N): print("Arg",i,args[i])
    assert N>3 and N<6
    T = int(args[1])
    assert T>0 and T<=255
    assert args[2].find("Sobel")>=0
    assert args[3].find("EK")>=0
    for i in (2,3): assert args[i].endswith(".vtk") or args[i].endswith(".VTK")
    if N==5:
       assert args[4].endswith(".vtk") or args[4].endswith(".VTK")
       output_name = args[4]
    else:
       output_name = "output.vtk"
    print("Input images:",args[2],args[3])
    print("Output image:",output_name)
    read_two_create_one(T, args[2], args[3], output_name)

# ========================================================================
# Instructions

def print_instructions():
     print("Need the following parameters on the command-line:")
     print("1) a threshold value, it must be in range 1...255")
     print("2) a 3D images in VTK format (edge image from Sobel)")
     print("3) another 3D images in VTK format (edge image from EK)")
     print("and the two images must have equal sizes.")
     print("4) optionally, the name of the output file,")
     print("   if not given, it will be output.vtk")

# ========================================================================
# Main

if __name__=="__main__":
  try:
    main(sys.argv)
  except Exception as e:
    print_instructions()
    print(type(e))
    print(e)
    raise
  