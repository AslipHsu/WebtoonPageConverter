import cv2
from pathlib import Path
from PIL.Image import Image as ImageType
import numpy as np
import re



#根據空白區域切分panel
def split_webtoon_image_by_cut_space(image: ImageType)-> list[ImageType]:
    width, _ = image.size
    img = np.array(image)[:, :, ::-1]#轉換顏色通道順序
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    print(gray.shape[0])

    filter_length=100
    panels: list[ImageType] = []
    filter_pointer=0
    is_cropping=False

    i=0
    while(i<gray.shape[0]):

        #判斷區域內是否全黑or全白 
        area_top,area_down=i,min(i + filter_length, gray.shape[0])
        next_area=gray[area_top:area_down]
        _, binaryBlack = cv2.threshold(next_area, 40, 255, cv2.THRESH_TOZERO)# 小於25轉成0(全黑),其他不變
        _, binaryWhite = cv2.threshold(next_area, 200, 255, cv2.THRESH_BINARY)#>200轉成255(全白),其他全轉0
        countBlack = np.sum(binaryBlack == 0)
        countWhite = np.sum(binaryWhite == 255)
        allBlackOrAllWhite=(countBlack>=np.size(next_area)*0.99 or countWhite>=np.size(next_area)*0.99)

        if (allBlackOrAllWhite or area_down==gray.shape[0]) and is_cropping:
            #下一區塊為全黑or全白時完成裁切
            # cropped_img=image[ffilter_pointer:i]
            box = (0, filter_pointer, width, i)
            cropped_image = image.crop(box)
            panels.append(cropped_image)
            is_cropping=False
            # print("end scropping")
        elif not allBlackOrAllWhite and not is_cropping:
            # 下一區塊有圖時開始裁切
            filter_pointer=i
            is_cropping=True
            # print("start scropping")
        i+=filter_length

    # print(panels[0])
    # cv2.imshow("s2",panels[0])
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return panels
