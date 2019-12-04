import cv2
import utils
from runsingleimage import init 
from crop import run

import sys
import show3d


# fondo = utils.cap_image("fondo")
# imagen1 = utils.cap_image("imagen1")
# imagen2 = utils.cap_image("imagen2")

imagen1 = cv2.imread("test/1.png")

mask_imagen1  = cv2.imread("test/1_m.png")
# mask_imagen1 = utils.get_mask(fondo,imagen1)

normal_c_1 , mask_c_1 = run(imagen1,mask_imagen1) ##crop


cv2.imwrite("normal_c_1.jpg",normal_c_1)

xyzs = init(normal_c_1,mask_c_1,res="demo")
cv2.namedWindow('show3d')
cv2.moveWindow('show3d',0,0)
cv2.setMouseCallback('show3d',show3d.onmouse)
while True:
    cmd = show3d.showpoints(xyzs,waittime=1)
    if cmd == ord('q'):
        break
cv2.imwrite("mask_c_1.jpg",mask_c_1)









# cv2.destroyAllWindows()



# xyzs = init(normal_c_1,mask_c_1,res="demo")
# cv2.namedWindow('show3d')
# cv2.moveWindow('show3d',0,0)
# cv2.setMouseCallback('show3d',show3d.onmouse)
# while True:
#     cmd = show3d.showpoints(xyzs,waittime=1)
#     if cmd == ord('q'):
#         break

# # xyzs = init(normal_c_2,mask_c_2,res="demo2")
# # cv2.namedWindow('show3d')
# # cv2.moveWindow('show3d',0,0)
# # cv2.setMouseCallback('show3d',show3d.onmouse)
# # while True:
# #     cmd = show3d.showpoints(xyzs,waittime=1)
# #     if cmd == ord('q'):
# #         break