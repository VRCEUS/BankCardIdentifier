# coding:utf-8
import time
from glob import glob

import numpy as np
from PIL import Image

import model
# ces


paths = glob('./test/*.*')

if __name__ == '__main__':

    #单张图片路径
    img_dir="./test/3.png"


    im = Image.open("./test/3.png")
    img = np.array(im.convert('RGB'))
    t = time.time()
    '''
    result,img分别对应-识别结果，图像的数组
    '''
    #result, img, angle = model.model(img, model='keras', adjust=True, detectAngle=True)

    result, img = model.model(img, img_dir, adjust=True, detectAngle=False)


    print("It takes time:{}s".format(time.time() - t))
    print("---------------------------------------")
    for key in result:
        print(result[key][1])
