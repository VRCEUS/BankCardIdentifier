import sys
import os
import tensorflow as tf
import time
from glob import glob

import numpy as np
from PIL import Image
from CRNN import model

from text_detection_ctpn.text_detect import right_ctpn

sys.path.append(os.getcwd())

if __name__ == '__main__':
    imdir = "./text_detection_ctpn/data/demo/2.jpeg"
    im = Image.open(imdir)

    img = np.array(im.convert('RGB'))
    t = time.time()

    # CTPN检测
    scores, boxes, r_img, cardimg = right_ctpn(imdir)

    cardimg=cardimg.convert('L')
    cardimg.show()

    #CRNN识别
    model.crnn_get(cardimg)


def Begin(imdir):
    #imdir = "./text_detection_ctpn/data/demo/2.jpeg"
    im = Image.open(imdir)

    img = np.array(im.convert('RGB'))
    t = time.time()

    # CTPN检测
    scores, boxes, r_img, pcardimg = right_ctpn(imdir)

    cardimg=pcardimg.convert('L')
    #cardimg.show()

    #CRNN识别
    cardnumber = model.crnn_get(cardimg)

    return cardnumber, pcardimg