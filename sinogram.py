import numpy as np
import matplotlib.pylab as plt
import scipy.fftpack as fft

# define image size
img = np.zeros((128, 128))
# define simple shapes
# square
img[30:60, 80:110] = img[30:60, 80:110] + 80
# rectangle
img[79:100, 20:80] = img[79:100, 20:80] + 120
# img[0:33 , 0:57] = img[0:33, 0:57] + 250
# cicle
xc = 40
yc = 40
r = 25


def distance(x, y):
    return ((x - xc) ** 2 + (y - yc) ** 2) ** 0.5


def check(x, y):
    if distance(x, y) > r:  # outside of cicle
        return 0
    else:  # inside circle
        return 1


for i in np.arange(128):
    for j in np.arange(128):
        if check(i, j):
            img[i, j] = img[i, j] + 50
plt.figure()
plt.imshow(img, interpolation='nearest')
plt.gray()
plt.show()
# coordinate transformation
# build xoy coordinates according to the centerpoint
cor_i = np.arange(128)
cor_j = np.arange(128)
cor_x = (cor_j - 128 / 2) + 0.5
cor_y = (cor_i - 128 / 2) + 0.5
# angles
number_of_projs = 360
angle_step = np.pi * 2 / number_of_projs
angles = np.arange(number_of_projs) * angle_step
# sinogram
sinogram = np.zeros((number_of_projs, int(np.sqrt(2) * 128) + 3))  # shape[sprt(2) * 128 + 1, 501] = shape[182,501]
# cor_j_sino = np.arange(184)
# cor_x_sino = (cor_j_sino - 184/2) + 0.5
#
for nn, aa in enumerate(angles):
    print(nn)
    pass
    img_n = np.zeros(img.shape)
    for j in cor_j:
        for i in cor_i:
            x_new = cor_x[j] * np.cos(aa) + cor_y[i] * np.sin(aa)  # rotation direction = counterclockwise
            y_new = cor_y[i] * np.cos(aa) - cor_x[j] * np.sin(aa)
            x_new_to_cor_j_img = int((x_new - 0.5) + 128 / 2)
            y_new_to_cor_i_img = int((y_new - 0.5) + 128 / 2)
            # if x_new_to_cor_j_img<128 and y_new_to_cor_i_img<128:
            #  img_n[y_new_to_cor_i_img, x_new_to_cor_j_img] = img[i, j]

            x_new_to_cor_j_sino = int((x_new - 0.5) + 184 / 2)  # convert x-cor to sinogram i-cor

            if img[i, j]:
                sinogram[nn, x_new_to_cor_j_sino] = sinogram[nn, x_new_to_cor_j_sino] + img[i, j]

    pass

# print(i[120,110])

plt.imshow(img_n, interpolation='nearest')
plt.gray()
# plt.show()


plt.imshow(sinogram, interpolation='nearest')
plt.gray()
plt.show()

sinogram_nomo = sinogram / sinogram.max() * 2 ** 16
# import scipy.misc
# scipy.misc.imsave('sinogram.tiff', sinogram)
# ar2 = scipy.misc.imread('sinogram.tiff')

# from libtiff import TIFF
# tiff = TIFF.open('sinogram.tiff', mode='w')
# tiff.write_image(sinogram)
# tiff.close()

# tiff_img = TIFF.open('img.tiff', mode='w')
# tiff_img.write_image(img)
# tiff_img.close()

# from PIL import Image
# im = Image.fromarray(sinogram, 'I;16')
# im.save("sinogram.tiff")
pass

###################################################################################3
# start of added code


fourunf = fft.rfft(sinogram, axis=1)
plt.imshow(fourunf, interpolation='nearest')
plt.gray()
plt.show()
ramp = np.floor(np.arange(0.5, fourunf.shape[1] // 2 + 0.1, 0.5))
fourfil = fourunf * ramp
plt.imshow(fourfil, interpolation='nearest')
plt.gray()
plt.show()

for i in np.arange(number_of_projs):
    for j in np.arange(184):
        if fourfil[i, j] > 100000 and j > 40 and (48 > i > 42 or 138 > i > 132 or 228 > i > 222 or 318 > i > 312):
            fourfil[i, j] = 1000
        if fourfil[i, j] < -100000 and j > 40 and (48 > i > 42 or 138 > i > 132 or 228 > i > 222 or 318 > i > 312):
            fourfil[i, j] = -1000

for i in np.arange(number_of_projs):
    for j in np.arange(184):
        if fourfil[i, j] > 0 and j > 130:
            fourfil[i, j] = 0
        if fourfil[i, j] < 0 and j > 130:
            fourfil[i, j] = 0

plt.imshow(fourfil, interpolation='nearest')
plt.gray()
plt.show()

newsino = fft.irfft(fourfil, axis=1)

img2 = np.zeros((128, 128))

for nn, aa in enumerate(angles):
    print(nn)
    for x in cor_x:
        for y in cor_y:
            x_sino = x * np.cos(aa) + y * np.sin(aa)
            i = int((y - 0.5) + 128 / 2)
            j = int((x - 0.5) + 128 / 2)
            img2[i, j] = img2[i, j] + newsino[nn, int((x_sino - 0.5) + 184 / 2)]
# for nn,aa in enumerate(angles):
# print(nn)
# for x in cor_x:
# for y in cor_y:
# i=int((y - 0.5) + 128/2)
# j=int((x - 0.5) + 128/2)
# if sinogram[nn, int((x_sino - 0.5) + 184/2)] < 10:
# img2[i,j]=0
plt.imshow(newsino, interpolation='nearest')
plt.gray()
plt.show()

maxvalue = 0

for i in np.arange(128):
    for j in np.arange(128):
        if img2[i, j] > maxvalue:
            maxvalue = img2[i, j]

print(maxvalue)

# for i in np.arange(128):
#  for j in np.arange(128):
# img2[i,j]=np.floor(img2[i,j]*4/maxvalue)
# if img2[i,j]<0:
# img2[i,j]=0


plt.imshow(img2, interpolation='nearest')
plt.gray()
plt.show()

# for i in np.arange(184):
#	print(sinogram[8,i])
