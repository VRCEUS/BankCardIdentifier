#!/usr/bin/env python
# -*- coding:utf-8 -*-
 
"""
    Author Alexantao By Charm
"""
 
import cv2
 
# 定义,都可根据应用进行调整
binary_threshold = 130
segmentation_spacing =  0.95 # 普通车牌值0.95,新能源车牌改为0.9即可
 

# 1、读取图片，并做灰度处理
img = cv2.imread('G:/Homework/text-detection-ctpn/main/Img/0012v_0.png')
img_gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow('gray',img_gray)

#cv2.waitKey(0)
 

 
# 2、将灰度图二值化，设定阀值为140
img_thre = img_gray

blur = cv2.GaussianBlur(img_gray,(5,5),0)

cv2.threshold(blur, binary_threshold, 255, cv2.THRESH_BINARY_INV, img_thre)
cv2.imshow('threshold', img_thre)

#cv2.waitKey(0)
 
# 3、保存黑白图片
cv2.imwrite('G:/Homework/text-detection-ctpn/main/Img/thre_res.png',img_thre)
 
# 4、分割字符
white = []  # 记录每一列的白色像素总和
black = []  # 记录每一列的黑色像素总和
height = img_thre.shape[0]
width = img_thre.shape[1]
print(width, height)
white_max = 0   # 仅保存每列，取列中白色最多的像素总数
black_max = 0   # 仅保存每列，取列中黑色最多的像素总数
 
# 循环计算每一列的黑白色像素总和
for i in range(width):
    w_count = 0     # 这一列白色总数
    b_count = 0     # 这一列黑色总数
    for j in range(height):
        if img_thre[j][i] == 255:
            w_count += 1
        else:
            b_count += 1
    white_max = max(white_max, w_count)
    black_max = max(black_max, b_count)
    white.append(w_count)
    black.append(b_count)
 
 
# False表示白底黑字；True表示黑底白字
arg = black_max > white_max
 
 
# 分割图像，给定参数为要分割字符的开始位
def find_end(start_):
    end_ = start_ + 1
    for m in range(start_+1, width - 1):
        if(black[m] if arg else white[m]) > (segmentation_spacing * black_max if arg else segmentation_spacing * white_max):
            end_ = m
            break
    return end_
 
print("Begin")

n = 1
start = 1
end = 2
while n < width - 1:
    n += 1
    if(white[n] if arg else black[n]) > ((1 - segmentation_spacing) * white_max if arg else (1 - segmentation_spacing) * black_max):
        # 上面这些判断用来辨别是白底黑字还是黑底白字
        start = n
        end = find_end(start)
        n = end
        if end - start > 5:
            print(start, end)
            cj = img_thre[1:height, start:end]
            cv2.imwrite('G:/Homework/text-detection-ctpn/main/Img/Cut/{0}.png'.format(n), cj)      #此句是输出每个字符，当时未输出直接看的时候因为刷新问题，解决好久，后来发现只是显示刷新的问题
            cv2.imshow('cutChar', cj)
            cv2.waitKey(0)
