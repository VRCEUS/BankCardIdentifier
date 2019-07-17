import sys
import os
import cv2

import tensorflow as tf
from PIL import Image


base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))

sys.path.append(os.getcwd())

#print(base_path)
print(os.path.dirname(__file__))
#print(os.getcwd())

from text_detection_ctpn.main.ctpnboxes import get_ctpn_info

# from ..lib.networks.factory import get_network
# from ..lib.fast_rcnn.config import cfg
# from..lib.fast_rcnn.test import test_ctpn
'''
load network
输入的名称为'Net_model'
'VGGnet_test'--test
'VGGnet_train'-train
'''

# init model
#sess, saver, net = load_tf_model()


# 进行文本识别

def right_ctpn(img_dir):
    """
    text box detect
    """
    # 对图像进行resize，输出的图像长宽
    #r_img, f = resize_im(img, scale=scale, max_scale=max_scale)
    scores, boxes, img, cardposdir = get_ctpn_info(img_dir)
    print(cardposdir)
    cardpos = getcardpos(cardposdir)
    #cardpos = [ int(x) for x in cardpos ]

    #原始图片
    im = Image.open(img_dir)
    #格式转换
    image = Image.fromarray(cv2.cvtColor(img,cv2.COLOR_BGR2RGB))

    #图片切割
    #误差补充
    supply = (int(cardpos[2]) - int(cardpos[0]))/20
    region = image.crop((int(cardpos[0]) - supply, int(cardpos[1]), int(cardpos[2]) + supply, int(cardpos[5])))
    region.save("./text_detection_ctpn/data/cut/1.jpeg")
    print("save")
    return scores, boxes, image, region



def getcardpos(cardposdir):
    maxlen = 0
    f = open(cardposdir, 'r')
    for i in f:
        strlist = i.split(',')	# 用逗号分割str字符串，并保存到列表
        #print(strlist)
        if len(strlist) > 1:
            if (int(strlist[2]) - int(strlist[0])) > maxlen :
                maxlen = int(strlist[2]) - int(strlist[0])
                #print(maxlen)
                cardpos = strlist[:]
                #print(cardpos)
        #print(cardpos)
        strlist.clear()

    print(cardpos)
    return cardpos