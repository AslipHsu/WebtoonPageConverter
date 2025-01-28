
import cv2
from pathlib import Path
import numpy as np
import re

class PageConverter():
    def __init__(self):
        return 
    def extract_number(self,file_name):
        match = re.search(r'\d+', file_name)
        return int(match.group()) if match else 0
    
    def LoadAndConcate(self,folder_path:str):
        #TODO 考慮讀取大量圖片,分批?多執行緒?
        path = Path(folder_path)
        files = [f for f in path.iterdir() if f.is_file()]
        files.sort(key=lambda f: self.extract_number(f.name))#按數字排序
        images = []
        for file in files:
            #TODO 檢查file格式
            print(file.name)
            nimg = cv2.imread(folder_path+"/"+file.name)
            images.append(nimg)


        resized_image_2=cv2.vconcat(images)    
        # cv2.imshow("s2",resized_image_2)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # print(type(resized_image_2))
        # print(resized_image_2[0].shape)
        return resized_image_2
    
    # 將大圖片處理成單格圖片
    # panel:漫畫中的單一格
    def CropPic(self,img:np.ndarray):

        # 二值化處理：黑色區域變為白色
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        print(gray.shape[0])

        fliter_length=50
        panels=[]
        fliter_pointer=0
        is_cropping=False

        i=0
        while(i<gray.shape[0]):
            if i+fliter_length>gray.shape[0]:
                #TODO 溢出部分先不處理
                break

            #判斷區域內是否全黑or全白 
            next_area=gray[i:i+fliter_length]
            _, binaryBlack = cv2.threshold(next_area, 25, 255, cv2.THRESH_TOZERO)# 小於25轉成0(全黑),其他不變
            _, binaryWhite = cv2.threshold(next_area, 200, 255, cv2.THRESH_BINARY)#>200轉成255(全白),其他全轉0
            countBlack = np.sum(binaryBlack == 0)
            countWhite = np.sum(binaryWhite == 255)
            allBlackOrAllWhite=(countBlack>=np.size(next_area)*0.99 or countWhite>=np.size(next_area)*0.99)
            if allBlackOrAllWhite and is_cropping:
                    #下一區塊為全黑or全白時完成裁切
                    cropped_img=img[fliter_pointer:i]
                    panels.append(cropped_img)
                    is_cropping=False
                    # print("end scropping")
            elif not allBlackOrAllWhite and not is_cropping:
                # 下一區塊有圖時開始裁切
                fliter_pointer=i
                is_cropping=True
                # print("start scropping")
            i+=fliter_length

        # print(panels[0])
        # cv2.imshow("s2",panels[0])
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        return panels


#========Note========
# 1.合併
# 2.切掉全黑or全白的row=>分出單格圖片
# 3.單格合併成一張



#偵測圖片分類? 風景,人,表情,動作等 判斷擺放位置
#根據不同類型漫畫 有不同排版and偵測方式?