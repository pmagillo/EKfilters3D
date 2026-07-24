from vtkio3D import readVTKcells as readVTK
from matplotlib import pyplot as plt
import sys

"""
Plot which compares the classification of the voxels
given by 2 edge detectors.
The first one will go on x axis, the other one(s) on the y axis.

If three images are given:
first one is the ideal edge surface,
the other two are the two edge surfaces to compare.
The ideal edge surface is used to color the blobs
differently if they correspond to detected true edge or not.

If two images are given:
they are two are the two edge surfaces to compare.
"""

# ========Main parameters==============================================
#Default
WITH_TEXT = False  # The blobs are annotated with text
WITH_CUT = False   # The lines x=... and y=... are shown
CUT = 64           # Value for the lines x=... and y=...
SAVING = False     # The image is saved

# =====================================================================
# Auxiliary functions

def linearize(img):
  """
  Generate a list with all the pairs (greylevel, voxel)
  from all voxels of the image.
  """
  values = []
  for x in range(img.dimX):
    for y in range(img.dimY):  
      for z in range(img.dimZ):
        pair = (img.get(x,y,z), (x,y,z))
        values.append(pair)
  return values


def linearize_zero_edge(img, ideal):
  """
  Generate two lists with pairs (greylevel, voxel)
  from voxels of the image:
  one with the voxels having zero value in the ideal image,
  and the other one with all the other voxels.
  """
  zeros, edges = [], []
  for x in range(img.dimX):
    for y in range(img.dimY):  
      for z in range(img.dimZ):
        pair = (img.get(x,y,z), (x,y,z))
        if ideal.get(x,y,z)==0:
          zeros.append(pair)
        else:
          edges.append(pair)
  return zeros, edges

# ========================================================================
# Function to generate the plot with two edge surfaces to compare

def plot_values_xy(img0, img1, title="", color=None):
  """
  The values of img0 go on the x-axis and those of img1 on the y-axis.
  The size of the blobs is proportional to the number of voxels
  having that x and that y value.
  The global variables WITH_CUT and WITH_TEXT are used to decide
  further decorations of the plot.
  """
  if color==None: color='magenta'
  Y0 = linearize(img0)
  top0 = max([v for v,w in Y0])
  Y1 = linearize(img1)
  top1 = max([v for v,w in Y1])
  if top0>250 or top1>250:
     top = top0 = top1 = 256
  elif top0>150 or top1>150:
     top = top0 = top1 = 224
  else:
     top = top0 = top1 = 128
  # start of plotting
  fig, ax = plt.subplots(layout="constrained")
  ax.set_title(title, fontsize=18) 
  if WITH_CUT:
    ax.plot([CUT,CUT],[0,top1],color='black',linewidth=0.5)
    ax.plot([0,top0],[CUT,CUT],color='black',linewidth=0.5)
  X = [v for v,p in Y0]
  Y = [v for v,p in Y1] 
  D = dict()
  for v1,v2 in zip(X,Y):
    if (v1,v2) in D: D[(v1,v2)] += 1
    else: D[(v1,v2)] = 1
  SX = [v1 for v1, v2 in D]
  SY = [v2 for v1, v2 in D]
  SS = [D[v] for v in D]
  ax.scatter(SX, SY, s=[0.01*v for v in SS], c=color)
  ax.plot([0,top],[0,top],color='black',linewidth=0.5)
  if WITH_TEXT:
     for x,y,s in zip(SX,SY,SS):
        ax.text(x+0.01*255,y-0.01*top,str(s), fontsize=12)
  ax.set_box_aspect(1)
  return fig,ax

# ========================================================================
# Function to generate the plot with ideal edge surface
# and two edge surfaces to compare

def plot_values_ixy(ideal, img0, img1, title="", colors=None):
  """
  The values of img0 go on the x-axis and those of img1 on the y-axis.
  The size of the blobs is proportional to the number of voxels
  having that x and that y value.
  The color of the blob depends on whether such voxels are true edges
  or not (as coded in the ideal image).
  The global variables WITH_CUT and WITH_TEXT are used to decide
  further decorations of the plot.
  """
  if colors==None:
    colors = ('red','blue')
  Y0zero, Y0edge = linearize_zero_edge(img0, ideal)
  top0 = max([v for v,w in Y0zero+Y0edge])
  Y1zero, Y1edge = linearize_zero_edge(img1, ideal)
  top1 = max([v for v,w in Y1zero+Y1edge])
  if top0>250 or top1>250:
     maximum = 256
     top = top0 = top1 = 256
  elif top0>150 or top1>150:
     maximum = 256
     top = top0 = top1 = 224
  else:
     maximum = 140
     top = top0 = top1 = 128
  # start of plotting
  fig, ax = plt.subplots(layout="constrained")
  ax.set_title(title, fontsize=18)
  #print(top,maximum)
  ax.set_xticks(range(0,maximum+1,32))
  ax.set_yticks(range(0,maximum+1,32))
  #ax.grid(True)
  if WITH_CUT:
    ax.plot([CUT,CUT],[0,top1],color='0.5',linestyle="--",linewidth=0.6)
    ax.plot([0,top0],[CUT,CUT],color='0.5',linestyle="--",linewidth=0.6)
    ax.text(0,CUT+2, "y="+str(CUT),color='black', fontsize=12)
    ax.text(CUT+1,0, "x="+str(CUT), rotation=90, color='black', fontsize=12)
  ax.plot([0,top],[0,top],color='black',linewidth=0.6)
  ax.text( (1.08*top)//2, (0.98*top)//2, "y=x", color='black', rotation=45, fontsize=12)
  X = [v for v,p in Y0zero]
  Y = [v for v,p in Y1zero] 
  Dzero = dict()
  for v1, v2 in zip(X,Y):
    if (v1,v2) in Dzero: Dzero[(v1,v2)] += 1
    else: Dzero[(v1,v2)] = 1
  SXzero = [v1 for v1, v2 in Dzero]
  SYzero = [v2 for v1, v2 in Dzero]
  SSzero = [Dzero[v] for v in Dzero]
  X = [v for v,p in Y0edge]
  Y = [v for v,p in Y1edge] 
  Dedge = dict()
  for v1, v2 in zip(X,Y):
    if (v1,v2) in Dedge: Dedge[(v1,v2)] += 1
    else: Dedge[(v1,v2)] = 1
  SXedge = [v1 for v1, v2 in Dedge]
  SYedge = [v2 for v1, v2 in Dedge]
  SSedge = [Dedge[v] for v in Dedge]
  ax.scatter(SXzero, SYzero, s=[0.015*v for v in SSzero], color=colors[0])
  ax.scatter(SXedge, SYedge, s=[0.015*v for v in SSedge], color=colors[1])
  if WITH_TEXT:
     for x,y,s in zip(SXzero,SYzero,SSzero):
         ax.text(x+0.01*255,y-0.01*top,str(s), fontsize=12)
     for x,y,s in zip(SXedge,SYedge,SSedge):
         ax.text(x+0.01*255,y-0.01*top,str(s), fontsize=12)
  ax.set_box_aspect(1)
  return fig,ax

# ========================================================================
# Functions defining colors and text for the various elements of the plot.

def titles_color_for(name1,name2):
  if name1.find("deal")>=0:
    if name2.find("obel")>=0: return 'Sobel','ideal','red';
    if name2.find("EK")>=0: return 'EK','ideal','cyan';
  elif name1.find("Sobel")>=0:
    if name2.find("EK")>=0: return 'EK','Sobel','magenta';
    if name2.find("deal")>=0: return 'Ideal','Sobel','red';
  elif name1.find("EK")>=0:
    if name2.find("obel")>=0: return 'Sobel','EK','magenta';
    if name2.find("deal")>=0: return 'Ideal','EK','cyan';
  return 'yellow'
  
def take_color(arglist,ind):
  if ind>=len(arglist) or not arglist[ind].startswith('['):
     return None
  color_descr = arglist[ind]
  assert color_descr.endswith(']')
  color_descr = "#"+color_descr[1:len(color_descr)-1]
  print("Take color ",color_descr)
  return color_descr

def image_name_from(name1,name2):
  i = name1.rfind("_")
  if i>=0: name1 = name1[i+1:]
  if name1.endswith(".vtk"): name1 = name1[:len(name1)-4]
  i = name2.rfind("_")
  if i>=0: name2 = name2[i+1:]
  if name2.endswith(".vtk"): name2 = name2[:len(name2)-4]
  assert name1==name2
  return name1

# ========================================================================  
# Main function if two images are given

def main_two(args):
  N = len(args)
  if N<2:
     print("Need at least two names of 3D images in VTK format")
     print("and optionally filename for saving figure")
     raise IndexError
  # read
  first_image = readVTK(args[0])
  second_image = readVTK(args[1])
  print("x-axis", args[0])
  print("y-asis", args[1])
    
  # generate figure
  titY, titX, aux_color = titles_color_for(args[0],args[1])
  title = titY+"(y-axis) compared to "+titX+"(x-axis)"
  fig, ax = plot_values_xy(first_image, second_image, title=title)
  plt.show()
  if SAVING:   # save figure
    output = "output"
    if N>2:  output = args[2]
    if not ( output.endswith(".png") or output.endswith(".PNG") ):
      output = output + ".png"
    fig.savefig(output)
    print("output figure",output)

# ========================================================================  
# Main function if two images are given (the first one is the ideal edge
# surface)

def main_three(args):
  N = len(args)
  if N<3:
     print("Need at least three names of 3D images in VTK format")
     print("and optionally filename for saving figure")
     print("The first image is the ideal one,")
     print("the other twio images are the ones to be compared")
     raise IndexError
  # read
  ideal_image = readVTK(args[0])
  first_image = readVTK(args[1])
  second_image = readVTK(args[2])
  print("x-axis", args[1])
  print("y-asis", args[2])
    
  # generate figure
  titY, titX, aux_color = titles_color_for(args[1],args[2])
  #title = titY+"(y-axis) compared to "+titX+"(x-axis)"
  title = image_name_from(args[1],args[2])
  colors = ('red', 'blue')
  fig, ax = plot_values_ixy(ideal_image, first_image, second_image, title=title, colors=colors)
  ax.set_xlabel(titX+" values", fontsize=14)
  ax.set_ylabel(titY+" values", fontsize=14)
  plt.show()
  if SAVING:   # save figure
    output = "output"
    if N>3:  output = args[3]
    if not ( output.endswith(".png") or output.endswith(".PNG") ):
      output = output + ".png"
    fig.savefig(output)
    print("output figure",output)

# ========================================================================  
# General main: get parameters and
# decide which one to call between main_three and main_two

if __name__=="__main__":
  try:
    if len(sys.argv)>=4 and [sys.argv[i].endswith(".vtk") for i in (1,2,3)]==[True,True,True]:
       WITH_CUT = True
       SAVING = True
       CUT = 128
       main_three(sys.argv[1:])
    elif [sys.argv[i].endswith(".vtk") for i in (1,2)]==[True,True]:
       SAVING = True
       main_two(sys.argv[1:])
    else:
       raise ValueError
  except Exception as e:
    print(type(e))
    print(e)
    raise
    