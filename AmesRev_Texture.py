import math
import numpy as np
import cv2
import random
#import os
#os.getcwd()
#os.chdir('D:\\WorkingDirectory')

file_rect_img = "ChessImage.png"
type_face = "B" # "F", "B", "D", "U"

if False: # Original (Ittelson, 1952, pp.183-189, No.1)
    thetaF_deg = 33.7
    xL = 21.33
    xR = 21.33
    yD = 21.33
    yU = 21.33
    zB = 0
    zF = 42.66
else: # Revised (Figure 1c in Myrov et al., 2023)
    thetaF_deg = 33.7
    xL = 42.66 * 1.0/3.0 # 14.22
    xR = 42.66 * 2.0/3.0 # 28.44
    yD = 42.66 * 1.0/4.0 # 10.66
    yU = 42.66 * 3.0/4.0 # 32.00
    zB = 42.66 * 3.0/5.0 # 25.60
    zF = 42.66 * 2.0/5.0 # 17.06

w_rect = xL+xR
h_rect = yD+yU
d_rect = zF+zB

cosF = np.cos(thetaF_deg/180.0*np.pi)
sinF = np.sin(thetaF_deg/180.0*np.pi)
tanF = np.tan(thetaF_deg/180.0*np.pi)

kl = zF/(zF-xL*tanF)
kr = zF/(zF+xR*tanF)
kMax = np.max([kl,kr])



# Loading src image
img_src = cv2.imread(file_rect_img)
height_src, width_src, channel_src = img_src.shape
dpi = width_src/w_rect
#cv2.imshow('Input', img_src); cv2.waitKey(0); cv2.destroyAllWindows()


if type_face=="F":
    arr_x_src = np.linspace(-xL +0.5/dpi,
                            +xR -0.5/dpi, num= width_src)
    arr_y_src = np.linspace(+yU -0.5/dpi,
                            -yD +0.5/dpi, num=height_src)

    w_ames = (xL*kl+xR*kr)/cosF
    h_ames = h_rect*kMax
    width_tran  = int(dpi*w_ames)
    height_tran = int(dpi*h_ames)
    
    arr_x2_tran = np.linspace(-xL*kl/cosF +0.5/dpi,
                              +xR*kr/cosF -0.5/dpi, num=width_tran) 
    arr_y2_tran = np.linspace(+yU*kMax -0.5/dpi,
                              -yD*kMax +0.5/dpi, num=height_tran)
    mat_x2_tran, mat_y2_tran = np.meshgrid(arr_x2_tran, arr_y2_tran)

    mat_tran_inv = np.zeros((height_tran, width_tran, 3))
    mat_tran_inv = mat_tran_inv.astype('float32')
    mat_tran_inv[:,:,0] = mat_x2_tran*zF*cosF
    mat_tran_inv[:,:,1] = mat_y2_tran*zF
    mat_tran_inv[:,:,2] = -mat_x2_tran*sinF + zF

    mat_tran_inv_x2 = mat_tran_inv[:,:,0]/mat_tran_inv[:,:,2]
    mat_tran_inv_y2 = mat_tran_inv[:,:,1]/mat_tran_inv[:,:,2]
    mat_tran_inv_x2 -= arr_x_src[0]
    mat_tran_inv_y2 -= arr_y_src[height_src-1]
    mat_tran_inv_x2 *= dpi
    mat_tran_inv_y2 *= dpi
    mat_tran_inv_y2 = (height_src-1)-mat_tran_inv_y2

elif type_face=="B":
    arr_x_src = np.linspace(-xR +0.5/dpi,
                            +xL -0.5/dpi, num= width_src)
    arr_y_src = np.linspace(+yU -0.5/dpi,
                            -yD +0.5/dpi, num=height_src)

    tanB= (zB/zF)*tanF 
    cosB= np.cos(np.arctan(tanB))
    sinB= np.sin(np.arctan(tanB))

    w_ames = (xL*kl+xR*kr)/cosB
    h_ames = h_rect*kMax
    width_tran  = int(dpi*w_ames)
    height_tran = int(dpi*h_ames)
    
    arr_x2_tran = np.linspace(-xR*kr/cosB +0.5/dpi,
                              +xL*kl/cosB -0.5/dpi, num=width_tran) 
    arr_y2_tran = np.linspace(+yU*kMax -0.5/dpi,
                              -yD*kMax +0.5/dpi, num=height_tran)
    mat_x2_tran, mat_y2_tran = np.meshgrid(arr_x2_tran, arr_y2_tran)

    mat_tran_inv = np.zeros((height_tran, width_tran, 3))
    mat_tran_inv = mat_tran_inv.astype('float32')
    mat_tran_inv[:,:,0] = mat_x2_tran*zB*cosB
    mat_tran_inv[:,:,1] = mat_y2_tran*zB
    mat_tran_inv[:,:,2] = mat_x2_tran*sinB + zB

    mat_tran_inv_x2 = mat_tran_inv[:,:,0]/mat_tran_inv[:,:,2]
    mat_tran_inv_y2 = mat_tran_inv[:,:,1]/mat_tran_inv[:,:,2]
    mat_tran_inv_x2 -= arr_x_src[0]
    mat_tran_inv_y2 -= arr_y_src[height_src-1]
    mat_tran_inv_x2 *= dpi
    mat_tran_inv_y2 *= dpi
    mat_tran_inv_y2 = (height_src-1)-mat_tran_inv_y2

elif type_face=="D":
    arr_x_src = np.linspace(-xL +0.5/dpi,
                            +xR -0.5/dpi, num= width_src)
    arr_y_src = np.linspace(+zF -0.5/dpi,
                            -zB +0.5/dpi, num=height_src)

    tanD= -(yD*kr-yD*kl)/(xL*kl+xR*kr)
    cosD= np.cos(np.arctan(tanD))
    sinD= np.sin(np.arctan(tanD))

    w_ames = (xL*kl+xR*kr)/cosD
    h_ames = d_rect*kMax
    width_tran  = int(dpi*w_ames)
    height_tran = int(dpi*h_ames)
    
    arr_x2_tran = np.linspace(-xL*kl/cosD +0.5/dpi,
                              +xR*kr/cosD -0.5/dpi, num=width_tran) 
    arr_y2_tran = np.linspace(+zF*kMax -0.5/dpi,
                              -zB*kMax +0.5/dpi, num=height_tran)
    mat_x2_tran, mat_y2_tran = np.meshgrid(arr_x2_tran, arr_y2_tran)

    mat_tran_inv = np.zeros((height_tran, width_tran, 3))
    mat_tran_inv = mat_tran_inv.astype('float32')
    mat_tran_inv[:,:,0] = -mat_x2_tran*yD*cosD
    mat_tran_inv[:,:,1] = -mat_y2_tran*yD
    mat_tran_inv[:,:,2] =  mat_x2_tran*sinD - yD

    mat_tran_inv_x2 = mat_tran_inv[:,:,0]/mat_tran_inv[:,:,2]
    mat_tran_inv_y2 = mat_tran_inv[:,:,1]/mat_tran_inv[:,:,2]
    mat_tran_inv_x2 -= arr_x_src[0]
    mat_tran_inv_y2 -= arr_y_src[height_src-1]
    mat_tran_inv_x2 *= dpi
    mat_tran_inv_y2 *= dpi
    mat_tran_inv_y2 = (height_src-1)-mat_tran_inv_y2

elif type_face=="U":
    arr_x_src = np.linspace(-xL +0.5/dpi,
                            +xR -0.5/dpi, num= width_src)
    arr_y_src = np.linspace(-zB +0.5/dpi,
                            +zF -0.5/dpi, num=height_src)

    tanU= (yU*kr-yU*kl)/(xL*kl+xR*kr)
    cosU= np.cos(np.arctan(tanU))
    sinU= np.sin(np.arctan(tanU))

    w_ames = (xL*kl+xR*kr)/cosU
    h_ames = d_rect*kMax
    width_tran  = int(dpi*w_ames)
    height_tran = int(dpi*h_ames)
    
    arr_x2_tran = np.linspace(-xL*kl/cosU +0.5/dpi,
                              +xR*kr/cosU -0.5/dpi, num=width_tran) 
    arr_y2_tran = np.linspace(-zB*kMax +0.5/dpi,
                              +zF*kMax -0.5/dpi, num=height_tran)
    mat_x2_tran, mat_y2_tran = np.meshgrid(arr_x2_tran, arr_y2_tran)

    mat_tran_inv = np.zeros((height_tran, width_tran, 3))
    mat_tran_inv = mat_tran_inv.astype('float32')
    mat_tran_inv[:,:,0] = mat_x2_tran*yU*cosU
    mat_tran_inv[:,:,1] = mat_y2_tran*yU
    mat_tran_inv[:,:,2] = mat_x2_tran*sinU + yU

    mat_tran_inv_x2 = mat_tran_inv[:,:,0]/mat_tran_inv[:,:,2]
    mat_tran_inv_y2 = mat_tran_inv[:,:,1]/mat_tran_inv[:,:,2]
    mat_tran_inv_x2 -= arr_x_src[0]
    mat_tran_inv_y2 -= arr_y_src[0]
    mat_tran_inv_x2 *= dpi
    mat_tran_inv_y2 *= dpi


mat_tran_inv_x2[mat_tran_inv_x2 > (width_src -1)] = width_src -1
mat_tran_inv_y2[mat_tran_inv_y2 > (height_src-1)] = height_src-1
mat_tran_inv_x2[mat_tran_inv_x2 < 0] = 0
mat_tran_inv_y2[mat_tran_inv_y2 < 0] = 0

img_tran= cv2.remap(img_src, mat_tran_inv_x2, mat_tran_inv_y2, cv2.INTER_LINEAR)

img_tran = img_tran.astype('uint8')
cv2.imshow(type_face, img_tran); cv2.waitKey(0); cv2.destroyAllWindows()
#cv2.imwrite('./Texture'+type_face+'.png', img_tran)




