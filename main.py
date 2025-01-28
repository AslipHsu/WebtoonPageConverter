import cv2
import os
from converter import PageConverter

# needleImage="./pic/1.jpg"
# needleImage2="./pic/2.jpg"
# https://m.ac.qq.com/comic/index/id/655106 (webtoon)
# https://tw.manhuagui.com/comic/51466/ (book)

# # 800x2500
# # 938x1331
# nimg = cv2.imread(needleImage)

# # 縮小 50%
# scale_factor = 0.5
# original_height, original_width = nimg.shape[:2]
# print("n shape:",original_height,"x", original_width)
# new_width = int(original_width * scale_factor)
# new_height = int(original_height * scale_factor)
# new_size = (new_width, new_height)
# resized_image = cv2.resize(nimg, new_size, interpolation=cv2.INTER_AREA)#INTER_AREA插值
# resized_height, resized_width = resized_image.shape[:2]
# # 裁切
# crop_factor = int(0.5*resized_height)
# print("a:",crop_factor,"b:", len(resized_image[0]))
# crop_image_1=resized_image[0:crop_factor,:]
# crop_image_2=resized_image[crop_factor:,:]  

# # 合併00
# resized_image_2=cv2.hconcat([crop_image_1, crop_image_2])


# _, binaryBlack = cv2.threshold(next_area, 25, 255, cv2.THRESH_TOZERO)# <25 轉成0(全黑)
# _, binary = cv2.threshold(binaryBlack, 200, 255, cv2.THRESH_TOZERO_INV)#>200轉成0(全黑)
# cv2.imshow("s2",resized_image_2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


folder_path="./testPic"
a=PageConverter()
pic=a.LoadAndConcate(folder_path)
panels=a.CropPic(pic)
for i,panel in enumerate(panels):
    cv2.imwrite("./result/"+str(i+1)+".jpg", panel)
