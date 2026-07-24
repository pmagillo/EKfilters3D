# EKfilters3D
EK-filters to extract edge surfaces from a 3D greylevel image. They are an alternative to traditional 3D Sobel filters. They consider the 4 diagonal directions instead of the 3 Cartesian axis-parallel directions.

We consider the problem of detecting edge surfaces (composed of voxels with high gradient variation) from a greyscale 3D image.
This operation can be performed by a triplet of gradient filters in the three cardinal directions of space.
We propose an alternative approach considering the four directions of the four diagonals of the unit cube, 
motivated by thinking of the cubic grid as a deformed BCC grid.
We have four gradient filters instead of three, but the overall number of non-zero entries is smaller, 
therefore an optimized implementation performs edge detection in shorter time with respect to the classic Sobel filters,
with comparable effectiveness.

This repository contains the software associated with the paper

"Edge detection in 3D images using four gradient filters"
by Paola Magillo (University of Genova, Italy) and Lidija Comic (University of Novi Sad, Serbia)

accepted for publication at the 28th International Conference on Pattern Recognition (ICPR 2026)
https://icpr2026.org/program.html 
