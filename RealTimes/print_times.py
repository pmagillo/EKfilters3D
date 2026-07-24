"""
Create the plots comparing the running times for extracting
the edge surfaces with Sobel filter and EK filter from the
TU Wien images.

The file containing the running times have been obtained by running
the script ../make_real_times
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
  
def print_function_times(function_name):
  #Sobel times
  Sobel_beetle = takeTimes("time_Sobel_beetle_", 1,10,function_name)
  Sobel_tree = takeTimes("time_Sobel_tree_", 1,10,function_name)
  Sobel_present = takeTimes("time_Sobel_present_", 1,10,function_name)
  Sobel_CThead = takeTimes("time_Sobel_ctheadZ_", 1,10,function_name)
  Sobel_MRbrain = takeTimes("time_Sobel_mrbrainZ_", 1,10,function_name)
   
  #EK times
  EK_beetle = takeTimes("time_EK_beetle_", 1,10,function_name)
  EK_tree = takeTimes("time_EK_tree_", 1,10,function_name)
  EK_present = takeTimes("time_EK_present_", 1,10,function_name)
  EK_CThead = takeTimes("time_EK_ctheadZ_", 1,10,function_name)
  EK_MRbrain = takeTimes("time_EK_mrbrainZ_", 1,10,function_name)
  
  print("Stanford CT     ","\tSobel=",Sobel_CThead,"\tEK=",EK_CThead)
  print("Stanford MR     ","\tSobel=",Sobel_MRbrain,"\tEK=",EK_MRbrain)
  print("TU Wien: Present","\tSobel=",Sobel_present,"\tEK=",EK_present)
  print("TU Wien: Beetle ","\tSobel=",Sobel_beetle, "\tEK=",EK_beetle)
  print("TU Wien: Tree   ","\tSobel=",Sobel_tree,   "\tEK=",EK_tree)


# ========================================================================
# Main

if __name__=="__main__":
  print("Running times for the whole edge detection process")
  print_function_times("edge_detection")
  print()
  print("Running times for filter application (cumulative)")
  print_function_times("new_with_coeff")
