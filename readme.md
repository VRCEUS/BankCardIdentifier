

# BankCardIdentifier说明

功能为银行卡号端到端的检测与识别。

实现基础为基于CTPN的文本检测和基于CRNN的文本识别。

CTPN依赖于TensorFlow，CRNN依赖于Pytorch。

过程为在Linux上训练CRNN网络，可以在Linux或Windows上使用网络进行识别。

（本仓库没有上传训练的神经网络。CTPN的网络来自参考引用代码中的仓库，CRNN的网络须使用该仓库代码进行训练。）

#### 代码部署步骤介绍

 首先根据readme.md安装配置必须的环境

 CTPN部署：  

 需要对所有模型及图片的引用路径根据自己环境的不同进行修正。  

 执行```setup_new.py```文件  
 修改部分代码，大致步骤在项目文档中已经说明。  
最终对```BankCardIdentifier\text_detection_ctpn\utils\bbox ```中的**bbox.pyx**和**nms.pyx**文件进行编译。生成**bbox.cp36-win_amd64.pyd**和
**nms.cp36-win_amd64.pyd**文件(不同环境编译的文件名称可能不同)

 CRNN部署：  

 根据训练数据和目的的不同，修改**alphabat**中的参数，修改crnn模型的输入参数(如相同，可无需修改)

 训练时指定的模型路径，以及训练集，验证集路径。

 此项目流程是Ubuntu 16.04系统下GPU训练模型，转到Windows 10系统下使用单CPU加载改模型进行识别。

 数据集创建


#### 代码运行步骤介绍

启动ui.py   
上传图片，点击识别，即可输出结果


#### 代码说明

text_detection_ctpn文件夹包含所有的CTPN代码及配置文件

CRNN文件夹包含所有的CRNN识别运行代码及配置文件

crnn.pytorch文件夹包含所有的CRNN训练相关代码及配置文件

其中，crnn.pytorch运行环境为Ubuntu 16.04
text_detection_ctpn和CRNN运行环境为Windows10

根目录中，ui.py为图形界面代码，执行后可直接在图形界面选择图片进行识别

demo.py为程序执行入口，调用其中的Begin()方法进行识别。也可单独执行demo.py在控制台终端输出运行结果。

Begin()方法中，right_ctpn()方法返回参数路径指定图片检测到的文本定位信息，crnn_get()方法输出图片的识别结果

text_detection_ctpn\text_detect.py文件主要是对CTPN检测后输出的原始数据进行处理。包含getcardpos()和right_ctpn()两个方法。

CRNN\model.py文件主要是调用CRNN\crnn\crnn.py中核心的识别方法crnnOcr()。

训练开始前，需要先运行crnn.pytorch\train\create_dataset\create_dataset.py，指定训练集图片和验证集图片，从而创建训练集数据和验证集数据。输入输出路径需要自己指定。其中getrightword()方法作用是提取图片正确的标签。

通过执行crnn.pytorch\train.py文件，即可开始对crnn网络开始训练。但在训练之前，需要自己对其中的参数进行自定义工作。包括alphabet，trainRoot，valRoot，batchSize，saveInterval等。开始运行后，即可在终端查看训练过程中输出的信息。crnn.pytorch\train.py中val()作用是对神经网络进行验证，并输出验证结果，得分和准确率。trainBatch()方法返回训练的损失。


环境配置：

1. Ananconda for Windows
2. python3
3. tensorflow/tensorflow-gpu
4. keras，pytorch等
5. win10-64位系统
6. 本机GPU：NVIDIA DeForce GTX 1060
7. cuda
8. cuDNN

环境搭建(部分)：

1. Ananconda， 下载地址：https://www.anaconda.com

2. 打开安装程序，安装Anaconda，打开命令行，输入“conda -V”,判断是否安装成功。

3. 安装keras，pytorch，tensorflow(gpu)等

4. 安装匹配的cuda和cuDNN
下载cuda，下载地址：https://developer.nvidia.com/cuda-toolkit-archive
打开安装程序，安装cuda，打开命令行，输入“ncvv -V”，判断是否安装成功。
下载cuDNN，下载地址：https://developer.nvidia.com/rdp/cudnn-archive
注意cuda和cuDNN的版本要相匹配。

5. 参考与引用代码：
https://github.com/meijieru/crnn.pytorch 
https://github.com/xiaofengShi/CHINESE-OCR 
https://github.com/eragonruan/text-detection-ctpn 
https://github.com/bay1/card-crnn-ctpn (飞爷tql)


