import torch
from torch.autograd import Variable
import utils
import dataset
from PIL import Image

import models.crnn as crnn
from collections import OrderedDict


model_path = './expr/netCRNN_48_21.pth'
img_path = './train/data/images/8_26f_0.png'
alphabet = '0123456789'

nclass = len(alphabet) + 1

model = crnn.CRNN(32, 1, nclass, 256)
if torch.cuda.is_available():
    print("gpu")
    model = model.cuda()
print('loading pretrained model from %s' % model_path)

trainWeights = torch.load(model_path)
modelWeights = OrderedDict()
for k, v in trainWeights.items():
    name = k.replace('module.', '')  # 去掉model才能在单gpu上跑
    modelWeights[name] = v

model.load_state_dict(modelWeights)

converter = utils.strLabelConverter(alphabet)

transformer = dataset.resizeNormalize((100, 32))
image = Image.open(img_path).convert('L')
image = transformer(image)
if torch.cuda.is_available():
    image = image.cuda()
image = image.view(1, *image.size())
image = Variable(image)

model.eval()
preds = model(image)

_, preds = preds.max(2)
preds = preds.transpose(1, 0).contiguous().view(-1)

preds_size = Variable(torch.IntTensor([preds.size(0)]))
raw_pred = converter.decode(preds.data, preds_size.data, raw=True)
sim_pred = converter.decode(preds.data, preds_size.data, raw=False)
print('%-20s => %-20s' % (raw_pred, sim_pred))
