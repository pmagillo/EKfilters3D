class Image3D:
  """
  Class for a 3D greyscale image.
  Grey levels are in range 0..255 unless range checking is disabled
  (function disable_range_checking).
  For reducing the values to range 0.255 two methods are possible:
  truncated larger values, or rescale them so that the maximum value
  becomes 255 (functions truncate_values are rescale_values).
  Function get checks that the indexes are inside the image,
  function loose_get returns the value of the nearest image voxel,
  if the indexes are outside.
  """

  def __init__(self, a,b,c):
    """
    Create a 3D image with dimensions a,b,c on the three sides.
    The created image contains only zero values.
    """
    self.create(a,b,c)
  
  def create(self, dimX, dimY, dimZ):
      """
      Create a 3D image with dimX, dimY, dimZ voxels
      on the three sides, where all voxels are zero (black).
      """
      assert dimX>0 and dimY>0 and dimZ>0
      self.dimX = dimX
      self.dimY = dimY
      self.dimZ = dimZ
      self.voxels = [0 for i in range(dimX)]
      for x in range(dimX):
        self.voxels[x] = [0 for i in range(dimY)]
        for y in range(dimY):
          self.voxels[x][y] = [0 for i in range(dimZ)]
      self.__range_checking = True
      
  def put(self, x,y,z, col):
    """
    Put the given color col (an integer between 0 and 255)
    into voxel of coordinates x,y,z.
    """
    if self.__range_checking:
      assert type(col) is int
      assert col>=0 and col<=255
    assert x>=0 and x<self.dimX
    assert y>=0 and y<self.dimY
    assert z>=0 and z<self.dimZ
    self.voxels[x][y][z] = col

  def get(self, x,y,z):
    """
    Get and return the color of the voxel of coordinates x,y,z.
    """
    assert x>=0 and x<self.dimX
    assert y>=0 and y<self.dimY
    assert z>=0 and z<self.dimZ
    return self.voxels[x][y][z]

  def loose_get(self, x,y,z):
    """
    Get and return the color of the voxel of coordinates x,y,z.
    If (x,y,z) is ouside the image, return the color of the
    nearest image voxel to (x,y,z).
    """
    if x<0: x = 0
    elif x>=self.dimX: x = self.dimX-1
    if y<0: y = 0
    elif y>=self.dimY: y = self.dimY-1
    if z<0: z = 0
    elif z>=self.dimZ: z = self.dimZ-1
    return self.voxels[x][y][z]

  def non_black_voxels(self):
    """
    Return the non-black voxels of the image
    as a list of triplets (x,y,z).
    """
    L = []
    for z in range(self.dimZ):  
      for x in range(self.dimX):
        for y in range(self.dimY):
           val = self.get(x,y,z)
           if val:
             L.append( (x,y,z) )
    return L

  def disable_range_checking(self):
      self.__range_checking = False
      
  def rescale_values(self, interval):
    if self.__range_checking: return
    for v in interval: assert type(v)==int
    v0, v1 = interval
    diff = v1-v0
    assert diff>=1

    for z in range(self.dimZ):  
      for x in range(self.dimX):
        for y in range(self.dimY):
           val = self.get(x,y,z)
           val = int(255*(val-v0)/diff)
           if val<0: val = 0
           elif val>255: val = 255
           self.put(x,y,z, val)
    self.__range_checking = True

  def truncate_values(self):
    if self.__range_checking: return
    for z in range(self.dimZ):  
      for x in range(self.dimX):
        for y in range(self.dimY):
           val = self.get(x,y,z)
           self.put(x,y,z, min(255,max(0,val)))
    self.__range_checking = True

  def get_maxval(self):
    return max([max([max([self.voxels[x][y][z] for z in range(self.dimZ)]) for y in range(self.dimY)]) for x in range(self.dimX)])

def readTXT(filename):
  """
  Load the image from the text file named filename.
  This is feasible only for very small test images.
  """
  f = open(filename,"r")
  # first line has dimX dimY dimZ
  s = f.readline().split()
  assert len(s) == 3
  img = Image3D(int(s[0]), int(s[1]), int(s[2]))
  # next lines have the colors
  for z in range(img.dimZ):
    for x in range(img.dimX):
      s = []
      while len(s)==0: s = f.readline().split()
      assert len(s) == img.dimY
      for y in range(img.dimY):
        img.put(x,y,z, int(s[y]))
  return img

def writeTXT(img, filename):
  """
  Write the given image to the text file named filename.
  This is feasible only for very small test images.
  """
  f = open(filename,"w")
  f.write(str(img.dimX)+" "+str(img.dimY)+" "+str(img.dimZ)+"\n")
  for z in range(img.dimZ):
    for x in range(img.dimX):
      for y in range(img.dimY):
        f.write(str(img.get(x,y,z))+" ")
      f.write("\n")
    f.write("\n")
  f.close()

def writeOccupiedVoxels(img, filename=None):
  """
  Write only the non-black voxels of the given image
  onto the text file named filename.
  This is feasible only for very small test images.
  If no filename is given, print them to the terminal.
  The x y z coordinates of the voxels are written.
  """
  if filename: F = open(filename,"w")
  else: F = None
  for x,y,z in img.non_black_voxels():
     s = str(x)+" "+str(y)+" "+str(z)
     if F:  F.write(s+"\n")
     else:  print(s)
  if F: F.close()
