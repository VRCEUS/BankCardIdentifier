# coding:utf-8
import time
from glob import glob

import numpy as np
from PIL import Image

import model

from ctpn.text_detect import text_detect
# ces

paths = glob('./test/*.*')

if __name__ == '__main__':
    im = Image.open("./test/3.png")
    img = np.array(im.convert('RGB'))
    t = time.time()
    '''
    result,img,angel分别对应-识别结果，图像的数组，文字旋转角度
    '''
    #result, img, angle = model.model(img, model='keras', adjust=True, detectAngle=True)

    result, img, angle = modeltest(img, model='keras', adjust=True, detectAngle=False)


    print("It takes time:{}s".format(time.time() - t))
    print("---------------------------------------")
    for key in result:
        print(result[key][1])


#定义测试方法
def modeltest(img, model='keras', adjust=False, detectAngle=False):
    """
    @@param:img,
    @@param:model,选择的ocr模型，支持keras\pytorch版本
    @@param:adjust 调整文字识别结果
    @@param:detectAngle,是否检测文字朝向
    
    """
    angle = 0

    # 进行图像中的文字区域的识别
    text_recs, tmp, img=text_detect(img)
    # 识别区域排列
    text_recs = model.sort_box(text_recs)
    # 
    result = model.crnnRec(img, text_recs, model, adjust=adjust)
    return result, tmp, angle