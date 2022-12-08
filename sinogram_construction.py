import numpy as np
import tifffile as tiff
import matplotlib.pylab as plt

# with tiff.imread() you can read multiple files and the output is a 3d array, the array's format is (L,N,M) 
# where L is the projection, and N and M are the rows and columns of each projection

# tiff.imread() can read multiple files if they are in a list type array
data_info= np.genfromtxt('Battery_27s_info.csv', dtype='str', delimiter=';') #reading projection info from data

temp1= data_info[2:,1] #selecting the file names from the projection info

temp2= np.zeros(temp1.shape,dtype='U16') #loading array to add the correct file extension to all file names
for n in np.arange(temp1.shape[0]):
    temp2[n]=".tif"
    
temp3= np.zeros(temp1.shape,dtype='U16') #name change of files, thanks klaas
for n in np.arange(temp1.shape[0]):
    temp3[n]="norm_"
    
data_names= np.char.chararray.tolist(np.char.add(temp3,np.char.add(temp1,temp2))) #list of names of projections

proj = np.array(tiff.imread(data_names[0:36])) #reading projection data into 3d array



#data range to select from projections
row_sel= [1000,1050] 
col_sel= [1000,1100]

proj = proj[:,row_sel[0]:row_sel[1],col_sel[0]:col_sel[1]] #projections array to construct sinograms from



# with the projections array, the sinogram can be constructed by selecting the same row from each projection
# and stacking them one after another in a separate array, the sinograms array
N= row_sel[1]-row_sel[0]    # N sinograms
L= proj.shape[0]            # L projections per sinogram
M= col_sel[1]-col_sel[0]    # M samples per sinogram row

sinogram_stack= np.zeros((N,L,M)) # N sinograms, each of L projections of M samples

for n in np.arange(N):
    for l in np.arange(L):
        sinogram_stack[n,l,:]= proj[l,n,:]
    
# the sinogram stack is of dimensions(N,L,M) where N is the rows from the projections L that get stacked on
# top of each other