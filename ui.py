import tkinter as tk
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import cv2
from demo import Begin
import numpy


def loadimg():
    '''
    文件路径   selecfile
    图片文件   src
    :return:
    '''
    selectFile = tk.filedialog.askopenfilename(title='选择文件')  # askopenfilename 1次上传1个；askopenfilenames1次上传多个
    text_adress.delete('1.0','end')
    text_adress.insert('end', selectFile)
    #load = Image.open(selectFile)
    src = cv2.imread(selectFile)
    resizepic = src
    #cv2.imshow(selectFile)


    imgsize = src.shape
    imgwidth = imgsize[1]
    imghight = imgsize[0]

    print(imgsize, imghight, imgwidth)
    if imgsize[1] > 495:
        imgwidth = 495
        #resize = cv2.resize(src, (imgwidth, imgsize[0]), 0, 0, cv2.INTER_LINEAR)

    if imgsize[0] > 300:
        imghight = 300

    resizepic = cv2.resize(src, (imgwidth, imghight), 0, 0, cv2.INTER_LINEAR)

    b,g,r = cv2.split(resizepic) 
    resizepic = cv2.merge([r,g,b]) 

    load = Image.fromarray(resizepic)

    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render, cursor='crosshair')
    img.image = render
    img.place(x=50, y=100)


def startorc():
    '''
    :return:
    '''
    srctext = text_adress.get('0.0', 'end')
    #srctext=srctext.replace('\n', '').replace('\n', '')
    srctext=srctext[:-1]
    print(srctext)
    cardnumber, cardimg = Begin(srctext)

    #src = cv2.imread(srctext)
    img = cv2.cvtColor(numpy.asarray(cardimg),cv2.COLOR_RGB2BGR)  
    resize = cv2.resize(img,(300,30),0,0,cv2.INTER_LINEAR)

    b,g,r = cv2.split(resize) 
    resize = cv2.merge([r,g,b]) 

    load = Image.fromarray(resize)
    render = ImageTk.PhotoImage(load)
    img = tk.Label(image=render, cursor='crosshair')
    img.image = render
    img.place(x=50, y=425)

    text_out.delete('1.0','end')

    text_out.insert('end', cardnumber)

def call_back(event):
    # 按哪个键，在console中打印
    print("现在的位置是", event.x_root, event.y_root)


root = tk.Tk()
root.title('bankcardOCR')
root.geometry('800x570')

#text_img = tk.Text(root, height=24, width=70)
#text_img.place(x=50, y=100, anchor='nw')
text_adress = tk.Text(root, height=2, width=70)
text_adress.place(x=50, y=50, anchor='nw')
text_out = tk.Text(root, height=2, width=70)
text_out.place(x=50, y=500, anchor='nw')
button_load = tk.Button(root, text='上传文件', height=3, width=20, background='SlateGray', borderwidth=0, cursor='hand2', command=loadimg)
button_load.place(x=600, y=100, anchor='nw')
button_orc = tk.Button(root, text='开始识别', height=3, width=20, background='SlateGray', borderwidth=0, cursor='hand2', command=startorc)
button_orc.place(x=600, y=200, anchor='nw')
label_out = tk.Label(root,text = '识别结果')
label_out.place(x=50, y=460, anchor='nw')
label_adress = tk.Label(root,text = '图片地址')
label_adress.place(x=50, y=25, anchor='nw')
label_cut = tk.Label(root,text = '区域识别')
label_cut.place(x=50, y=400, anchor='nw')

frame = Frame(root,
                  width=495, height=300,
                  background='LightSlateGray')

frame.bind("<Motion>", call_back)
frame.place(x=50, y=100, anchor='nw')

root.mainloop()


