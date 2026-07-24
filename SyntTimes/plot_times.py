"""
Create the plots comparing the running times for extracting
the edge surfaces with Sobel filter and EK filter from the
synthetic images.

The file containing the running times have been obtained by running
the script ../make_synt_times
"""

# ========================================================================
# Read the running time for a given function from one file

def takeTimeFromOneFile(file_in, function_name, division=True):
  """
  The file contains lines of this format:
        NC    T1    T1_1    T2    T2_1  file.py:row(function)
  Find the line where function==function_name
  and take the time T2/NC (or T2 if division==False)
  """
  FI = open(file_in,"r")
  inform = FI.readline()
  while inform.find(function_name)==-1:
    inform = FI.readline()
  #print(inform)
  inform = inform.split()
  T2 = float(inform[3])
  FI.close()
  if division and NC>1:
    NC = int(inform[0])
    return T2/NC
  else:
    return T2

# ========================================================================
# Read the running time for a given function from all the files
# (taking the minimum among the files)

def takeTimes(file_prefix, ind1, ind2, function_name, ONLY_NUMBERS = True):
  """
  Arguments:
  the prefix name of the files to be examined
  the first and second endpoint of the intervals 
  the name of the function whose running time is to be extracted
  Example:
  time_Sobel_axis_
  1 10
  edge_detection
  It will examine the files 
  "time_Sobel_axis_1.txt" ... "time_Sobel_axis_8.txt"
  extracting the running time of function "extract_edges" from each
  of them and take the minimum.
  Each file contains lines of this format:
        NC    T1    T1_1    T2    T2_1  file.py:row(function_name)
  Take the time T2/NC from each file and the minumn over all the file.
  """
  assert ind1<=ind2
  file_suffix = ".txt"
  minimum = None
  for i in range(ind1, ind2+1):
     name = file_prefix+str(i)+file_suffix
     current = takeTimeFromOneFile(name, function_name, division=False)
     if minimum==None or current<minimum:
         minimum = current
  #if ONLY_NUMBERS:
  #    print(file_prefix[5:len(file_prefix)-1],"=",minimum)
  #else:
  #    print(file_prefix,"Min",function,minimum)
  return minimum

# ========================================================================
# Read the running time for the function for all the input images,
# both with Sobel and Ek filters
  
def get_function_times(function_name):
  #Sobel times
  Sobel_noisyplaneXYZ_016 = takeTimes("time_Sobel_noisy_slanted_016_", 1,10,function_name)
  Sobel_noisyplaneXYZ_032 = takeTimes("time_Sobel_noisy_slanted_032_", 1,10,function_name)
  Sobel_noisyplaneXYZ_064 = takeTimes("time_Sobel_noisy_slanted_064_", 1,10,function_name)
  Sobel_noisyplaneZ_016 = takeTimes("time_Sobel_noisy_axis_016_", 1,10,function_name)
  Sobel_noisyplaneZ_032 = takeTimes("time_Sobel_noisy_axis_032_", 1,10,function_name)
  Sobel_noisyplaneZ_064 = takeTimes("time_Sobel_noisy_axis_064_", 1,10,function_name)
  Sobel_noisysphereZ_016 = takeTimes("time_Sobel_noisy_sphere_016_", 1,10,function_name)
  Sobel_noisysphereZ_032 = takeTimes("time_Sobel_noisy_sphere_032_", 1,10,function_name)
  Sobel_noisysphereZ_064 = takeTimes("time_Sobel_noisy_sphere_064_", 1,10,function_name)
  Sobel_planeXYZ = takeTimes("time_Sobel_slanted_",1,10,function_name)
  Sobel_planeZ = takeTimes("time_Sobel_axis_",1,10,function_name)
  Sobel_sphere = takeTimes("time_Sobel_sphere_",1,10,function_name)
   
  Sobel0=[Sobel_planeZ,Sobel_planeXYZ,Sobel_sphere]
  Sobel1=[Sobel_noisyplaneZ_016,Sobel_noisyplaneZ_032,Sobel_noisyplaneZ_064]
  Sobel2=[Sobel_noisyplaneXYZ_016,Sobel_noisyplaneXYZ_032,Sobel_noisyplaneXYZ_064]
  Sobel3=[Sobel_noisysphereZ_016,Sobel_noisysphereZ_032,Sobel_noisysphereZ_064]
   
  #EK times
  EK_noisyplaneXYZ_016 = takeTimes("time_EK_noisy_slanted_016_", 1,10,function_name)
  EK_noisyplaneXYZ_032 = takeTimes("time_EK_noisy_slanted_032_", 1,10,function_name)
  EK_noisyplaneXYZ_064 = takeTimes("time_EK_noisy_slanted_064_", 1,10,function_name)
  EK_noisyplaneZ_016 = takeTimes("time_EK_noisy_axis_016_", 1,10,function_name)
  EK_noisyplaneZ_032 = takeTimes("time_EK_noisy_axis_032_", 1,10,function_name)
  EK_noisyplaneZ_064 = takeTimes("time_EK_noisy_axis_064_", 1,10,function_name)
  EK_noisysphereZ_016 = takeTimes("time_EK_noisy_sphere_016_", 1,10,function_name)
  EK_noisysphereZ_032 = takeTimes("time_EK_noisy_sphere_032_", 1,10,function_name)
  EK_noisysphereZ_064 = takeTimes("time_EK_noisy_sphere_064_", 1,10,function_name)
  EK_planeXYZ = takeTimes("time_EK_slanted_",1,10,function_name)
  EK_planeZ = takeTimes("time_EK_axis_",1,10,function_name)
  EK_sphere = takeTimes("time_EK_sphere_",1,10,function_name)
   
  EK0=[EK_planeZ,EK_planeXYZ,EK_sphere]
  EK1=[EK_noisyplaneZ_016,EK_noisyplaneZ_032,EK_noisyplaneZ_064]
  EK2=[EK_noisyplaneXYZ_016,EK_noisyplaneXYZ_032,EK_noisyplaneXYZ_064]
  EK3=[EK_noisysphereZ_016,EK_noisysphereZ_032,EK_noisysphereZ_064]
   
  all_Sobel = (Sobel0,Sobel1,Sobel2,Sobel3)
  all_EK = (EK0,EK1,EK2,EK3)
  return all_Sobel, all_EK


# ========================================================================
# Create plot

from matplotlib import pyplot as plt

def plot_times(function_name):
  # get data
  Sobel, EK = get_function_times(function_name)
  if function_name=="edge_detection":
    title = "edge detection"
    sx, dx = 9.05, 9.3
    sy, dy = 6.15, 6.4 
    loc1, loc2 = (9.1,6.2), (9.1,6.3)
  elif function_name=="new_with_coeff":
    title = "filter application (cumulative)"
    sx, dx = 7.65, 7.85
    sy, dy = 4.65, 4.85
    loc1, loc2 = (7.7,4.676), (7.7,4.776)
  fig, ax = plt.subplots()

  # compute ratios
  ratio = []
  for i in range(len(Sobel)):
     ratio.append([ek/sob for ek,sob in zip(EK[i],Sobel[i])])

  # unpack data
  Sobel0,Sobel1,Sobel2,Sobel3 = Sobel
  EK0,EK1,EK2,EK3 = EK
  ratio0,ratio1,ratio2,ratio3 = ratio
  ax.set_title(title, fontsize=18) 

  # ratio min max
  mi = min(ratio0+ratio1+ratio2+ratio3)
  co1 = str(mi)[:5]
  ma = max(ratio0+ratio1+ratio2+ratio3)
  co2 = str(ma)[:5]
  print("Min Max Ratio",mi,ma)

  # lines for min and max ratio
  ax.plot([sx,dx],[sx*mi,dx*mi],"0.1", label="y="+co1+"x")
  ax.plot([sx,dx],[sx*ma,dx*ma],"0.6", label="y="+co2+"x")
  #ax.text(loc1[0],loc1[1],"y="+co1+"x") #min
  #ax.text(loc2[0],loc2[1],"y="+co2+"x") #max

  # colors for times
  col0,col1,col2,col3,col4 = '#08AAAA','red','blue','green','magenta'
  names = ["normal_plane","slanted_plane","sphere","sinusoid"]
  for n,c in zip(names,[col1,col2,col3,col4]):
    print(n,c)

  # plot times
  ax.plot(Sobel0[0],EK0[0],color=col1, marker="D",markersize=4, label="axis")
  ax.plot(Sobel0[1],EK0[1],color=col2, marker="D",markersize=4, label="slanted")
  ax.plot(Sobel0[2],EK0[2],color=col3, marker="D",markersize=4, label="sphere")
  ax.plot(Sobel1, EK1, color=col1, marker="o",markersize=4,linewidth=0)
  ax.plot(Sobel2, EK2, color=col2, marker="o",markersize=4,linewidth=0)
  ax.plot(Sobel3, EK3, color=col3, marker="o",markersize=4,linewidth=0)

  # end
  ax.legend(loc='lower right', fontsize=12)
  ax.set_box_aspect(0.95)
  ax.grid(True)
  ax.set_xticks([sx+0.05*d for d in range(0,1+int(20*(dx-sx)+0.5),1)])
  ax.set_yticks([sy+0.05*d for d in range(0,1+int(20*(dy-sy)+0.5),1)])
  ax.set_xlabel("execution time with Sobel filters", fontsize=14)
  ax.set_ylabel("execution times with EK filters", fontsize=14)
  return fig, ax

# ========================================================================
# Main

if __name__=="__main__":
  fig1,ax1 = plot_times("edge_detection")
  fig3,ax3 = plot_times("new_with_coeff")
  plt.show()
  name1 = "plot_edge_detection.png"
  name3 = "plot_filter_cumul.png"
  for f,n in zip([fig1,fig3],[name1,name3]):
    f.savefig(n)
    print("Saved figure ",n)
