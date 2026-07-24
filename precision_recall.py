from image3D import Image3D
from vtkio3D import readVTKcells as readVTK

# ========================================================================
"""
Compute precision and recall (needed for F-measure) for the edge surfaces
computed from the synthetic images.
If run without argument, instructions are printed.
"""

HUMAN_READABLE = False # How to print the output

# ========================================================================
# Auxiliary functions

def ordered_neighbors(max_dist):
  """
  Take all the voxels at distance <= max_dist from (0,0,0),
  sort them in distance order and return the list of
  pairs (distance, point).
  """
  dist_range = range(-max_dist,max_dist+1)
  L = []
  for i in dist_range:
     for j in dist_range:
       for k in dist_range:
          D = (i*i + j*j + k*k)**0.5 
          if D<max_dist:
            L.append((D, i,j,k))
  L.sort()
  return L
  
def min_dist_within(x,y,z, neighbors, condition):
  """
  The content of neighbors is a list of (distance, position)
  sorted by increasing distance.
  Find the min distance of voxel P=(x,y,z) from a voxel of
  the neighbors, which satisfies the condition.
  """
  DD = None
  for dist, i,j,k in neighbors:
    # voxels (i,j,k) are in increasing distance order
    if x+i<0 or x+i>63: continue
    if y+j<0 or y+j>63: continue
    if z+k<0 or z+k>63: continue
    if condition(x+i,y+j,z+k):
          DD = dist
          break 
  return DD
    
# ========================================================================
# Print the computed measures

def print_results(total_true, detected, detected_true, detected_false, missing_true, prefix="", additional_precision=0, additional_recall=0):
  if HUMAN_READABLE:
    print(prefix,"True edges:", total_true)
    print(prefix,"Detected edges:", detected)
    print(prefix,"Detected true edges (correctly classified):", detected_true)
    print(prefix,"Detected false edges (wrongly classified):", detected_false)
    print(prefix,"Missing true edges (wrongly classified):", missing_true)
    ###SUBMITTEDprint(prefix,"Precision (detected true edges/detected edges):", detected_true/detected)
    print(prefix,"Precision (detected true edges/detected edges):", (detected_true+additional_precision)/detected)
    #print(prefix,"Recall (detected true edges/true edges):", detected_true/total_true)
    #the above one is wrong when considering voxels within distance...
    #the one below is equivalent without considering distances and correct in all cases
    ###SUBMITTEDprint(prefix,"Recall (detected true edges/(detected true+missing true):", detected_true/(detected_true+missing_true))
    print(prefix,"Recall (detected true edges/total true):", (detected_true+additional_recall)/total_true)
  else:
    ###SUBMITTEDprint(prefix,"Precision:", detected_true/detected)
    print(prefix,"Precision:", (detected_true+additional_precision)/detected)
    ###SUBMITTEDprint(prefix,"Recall:", detected_true/(detected_true+missing_true)) 
    print(prefix,"Recall:", detected_true/total_true)

# ========================================================================
# Compute precision and recall,
# both exact and within the given tolerated distance

def precision_recall(ideal_img, given_img, cut_limit=0, tolerated_dist=None):
  """
  ideal_img contains the ideal edge surface.
  given_img contains the computed edge surface.
  If tolerated_dist!=None, it may be a number or a list of numbers.

  Precision:
  Count the number of voxels that are non-zero in given_img
  (detected edge voxels),
  and check how many of them are non-zero in ideal_img
  (true edge voxels).
  If a voxel in given_img has value <= cut_limit, then it
  is considered as zero.

  Recall:
  Count the number of voxels that are non-zero in ideal_img
  (true edge voxels), and are non-zero in given_img as well
  (detected true edge voxels).

  Precision with tolerated distance:
  For each non-zero voxel P in given_img, that is zero in ideal_img 
  (detected edge voxel that is not a true edge voxel),
  we search for a non-zero voxel in ideal_img, that is distant from P
  <= tolerated_dist 

  Recall with tolerated distance:
  For each zero voxel P in given_img, that is non-zero in ideal_img 
  (missing true edge),
  we search for a non-zero voxel in given_img, that is zero in ideal_img
  and distant from P  <= tolerated_dist
  """

  # the two images must have equal size
  assert ideal_img.dimX==given_img.dimX
  assert ideal_img.dimY==given_img.dimY
  assert ideal_img.dimZ==given_img.dimZ

  # EXACT precision and recall
  detected_n = 0 # non-zero in given_img
  true_n = 0     # non-zero in ideal_img
  detected_true_n = 0    # non-zero in both
  detected_false_n = 0   # non-zero in given_img, zero in ideal_img
  missing_true_n = 0     # zero in given_img, non-zero in ideal_img
  for x in range(ideal_img.dimX):
    for y in range(ideal_img.dimY):
      for z in range(ideal_img.dimZ):
         detected_e = given_img.get(x,y,z)>cut_limit
         true_e = ideal_img.get(x,y,z)>0
         if detected_e:
            detected_n += 1
            if true_e: detected_true_n += 1
            else: detected_false_n += 1
         if true_e:
            true_n += 1
            if not detected_e: missing_true_n += 1
  print_results(true_n, detected_n, detected_true_n, detected_false_n, missing_true_n,"EXACT")
  if HUMAN_READABLE: print()

  # WITH DISTANCE
  # Consider possible matching within tolerated_dist
  if not tolerated_dist: return
  # tolerated distance may be a list of values
  if type(tolerated_dist)==int or type(tolerated_dist)==float:
    tolerated_dist = [tolerated_dist]
  tolerated_dist.sort()
  max_tolerated_dist = int(tolerated_dist[-1]+0.5)
  #dist_range = range(-max_tolerated_dist,max_tolerated_dist+1)
  range_neighbors = ordered_neighbors(max_tolerated_dist)
  false_within_distance = [0]*len(tolerated_dist)
  true_within_distance = [0]*len(tolerated_dist)
  for x in range(ideal_img.dimX):
    for y in range(ideal_img.dimY):
      for z in range(ideal_img.dimZ):
         detected_e = given_img.get(x,y,z)>cut_limit
         true_e = ideal_img.get(x,y,z)>0
         if detected_e and not true_e:
            #detected false edge, find the nearest true edge
            requirement = lambda i, j, k : ideal_img.get(i,j,k)>0
            dist = min_dist_within(x,y,z, range_neighbors, requirement)
            if dist!=None:
              for t in range(len(tolerated_dist)):
                 if dist <= t:     false_within_distance[t] += 1
            
         elif true_e and not detected_e:
            #missing true edge, find the nearest detected edge
            requirement = lambda i, j, k : given_img.get(i,j,k)>cut_limit and ideal_img.get(i,j,k)==0
            dist = min_dist_within(x,y,z, range_neighbors, requirement)
            if dist!=None:
              for t in range(len(tolerated_dist)):
                 if dist <= t:     true_within_distance[t] += 1

  for d,fn,tn in zip(tolerated_dist, false_within_distance, true_within_distance):
    if fn>0 or tn>0:
      if HUMAN_READABLE:
        print("Detected false edge voxels within distance",d,"from a true edge:",fn)
        print("True edge voxels within distance",d,"from a detected edge voxel:",tn)
      print_results(true_n, detected_n, detected_true_n, detected_false_n, missing_true_n,"D"+str(d),fn,tn)
    else:
      if HUMAN_READABLE:
        print("D"+str(d),"Distance",d,"causes no variation")
        print()

# ========================================================================
# Instructions

def print_instructions():
  print("Compare the ideal edge surface with the computed edge surface.")
  print("The parameters on the command-line must be:")
  print("1) the image file with the ideal edge surface")
  print("   (this image has values 0 and 255 only).")
  print("2) the image file with the computed values")
  print("   (this image may have all the range of values 0..255)")
  print("3) opzionally, a threshold, or a list of thresholds,")
  print("   to be applied to the computed values")
  print("   (voxels with value<threshold are considered as 0),")
  print("   each threshold must be a natural number.")
  print("   if no threshold is present, 0 is used")
  print("All images must be 64 x 64 x 64 voxels and in vtk format.")
  print()
  print("Precision and recall are computed:")
  print(" EXACT = according to definition")
  print(" D2    = within distance 2")
  print(" D3    = within distance 3")

# ========================================================================
# Function to simplify the main:
# compute precision and recall with a given tolerance

def measure(name1, name2, img1, img2, threshold, distances):
  print("============ F measure ============")
  print("Ideal image ", name1)
  if threshold>0:
    print("Computed image", name2, "(values<=", threshold, "considered as 0)")
  else:
    print("Computed image", name2)
  precision_recall(img1, img2, cut_limit=threshold, tolerated_dist=distances)

# ========================================================================
# Main

if __name__=="__main__":
  import sys
  try:
    assert len(sys.argv)>=3
    name1 = sys.argv[1]
    name2 = sys.argv[2]
    for n in [name1,name2]:
       assert n.endswith(".vtk") or n.endswith(".VTK")
    limits = [0]
    if len(sys.argv)>3:
      limits = [int(v) for v in sys.argv[3:]]
      limits = sorted(set(limits))
      for v in limits: assert v>=0

    IMG1 = readVTK(name1)
    IMG2 = readVTK(name2)
    distances = [1, 2, 3] 
    for t in limits:
      measure(name1, name2, IMG1, IMG2, t, distances)

  except AssertionError:
    print_instructions()
  except Exception as err:
    print(err)
    print_instructions()

    