import os

import cv2
import lmdb  # install lmdb by "pip install lmdb"
import numpy as np


# from genLineText import GenTextImage

def checkImageIsValid(imageBin):
    if imageBin is None:
        return False
    imageBuf = np.fromstring(imageBin, dtype=np.uint8)
    img = cv2.imdecode(imageBuf, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return False
    imgH, imgW = img.shape[0], img.shape[1]
    if imgH * imgW == 0:
        return False
    return True


def writeCache(env, cache):
    with env.begin(write=True) as txn:
        for k, v in cache.items():
            txn.put(k.encode(), v)


def createDataset(outputPath, imagePathList, labelList, lexiconList=None, checkValid=True):
    """
    Create LMDB dataset for CRNN training.

    ARGS:
        outputPath    : LMDB output path
        imagePathList : list of image path
        labelList     : list of corresponding groundtruth texts
        lexiconList   : (optional) list of lexicon lists
        checkValid    : if true, check the validity of every image
    """
    # print (len(imagePathList) , len(labelList))
    assert (len(imagePathList) == len(labelList))
    nSamples = len(imagePathList)
    print('...................')
    env = lmdb.open(outputPath, map_size=1099511627776)

    cache = {}
    cnt = 1
    for i in range(nSamples):
        imagePath = imagePathList[i]
        label = labelList[i]
        if not os.path.exists(imagePath):
            print('%s does not exist' % imagePath)
            continue
        with open(imagePath, 'rb') as f:
            imageBin = f.read()
        if checkValid:
            if not checkImageIsValid(imageBin):
                print('%s is not a valid image' % imagePath)
                continue

        imageKey = 'image-%09d' % cnt
        labelKey = 'label-%09d' % cnt
        cache[imageKey] = imageBin
        cache[labelKey] = label.encode()
        if lexiconList:
            lexiconKey = 'lexicon-%09d' % cnt
            cache[lexiconKey] = ' '.join(lexiconList[i]).encode()
        if cnt % 1000 == 0:
            writeCache(env, cache)
            cache = {}
            print('Written %d / %d' % (cnt, nSamples))
        cnt += 1
    nSamples = cnt - 1
    cache['num-samples'] = str(nSamples).encode()
    writeCache(env, cache)
    print('Created dataset with %d samples' % nSamples)


def read_text(path):
    with open(path) as f:
        text = f.read()
    text = text.strip()

    return text

#正则获取图片正确标签
def getrightword(path):
    text = path.split("/")[-1]
    #pattern = re.compile(r"\d|_{4}")

    text1 = re.match(r'(\d|.){4}',text).group()
    text2 = re.match(r'\d{3,}',text1).group()

    print (text2)

    return text2


import re
import urllib.request


import glob

if __name__ == '__main__':

    ##lmdb 输出目录
    #outputPath = 'lmdb/train_lmdb'
    outputPath = 'lmdb/val_lmdb'

    #图片路径
    #path = "train/data/train/*.png"
    path = "train/data/valtrain/*.png"
    #path1 = "train/data/train/*.jpg"
    path1 = "train/data/valtrain/*.jpg"

    imagePathList = glob.glob(path)
    imagePathList += glob.glob(path1)

    print('------------', len(imagePathList), '------------')
    imgLabelLists = []

    for p in imagePathList:
        try:
            print(p)
            #imgLabelLists.append((p, read_text(p.replace('.png', '.txt'))))
            imgLabelLists.append((p, getrightword(p)))

        except:
            continue

    # imgLabelList = [ (p,read_text(p.replace('.jpg','.txt'))) for p in imagePathList]
    ##sort by lebelList 

    imgLabelList = sorted(imgLabelLists, key=lambda x: len(x[1]))
    imgPaths = [p[0] for p in imgLabelList]
    txtLists = [p[1] for p in imgLabelList]
    print(imgPaths)
    print(txtLists)

    createDataset(outputPath, imgPaths, txtLists, lexiconList=None, checkValid=True)
