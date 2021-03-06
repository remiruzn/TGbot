from torchvision import models
from PIL import Image
import matplotlib.pyplot as plt
import torch
import numpy as np
import torchvision.transforms as T
import cv2



fcn = models.segmentation.fcn_resnet101(pretrained=True).eval()

dlab = models.segmentation.deeplabv3_resnet101(pretrained=1).eval()


# Define the helper function
def decode_segmap(image, nc=21):
    label_colors = np.array([(0, 0, 0),  # 0=background
                             # 1=aeroplane, 2=bicycle, 3=bird, 4=boat, 5=bottle
                             (128, 0, 0), (0, 128, 0), (128, 128, 0), (0, 0, 128), (128, 0, 128),
                             # 6=bus, 7=car, 8=cat, 9=chair, 10=cow
                             (0, 128, 128), (255, 255, 255), (64, 0, 0), (192, 0, 0), (64, 128, 0),
                             # 11=dining table, 12=dog, 13=horse, 14=motorbike, 15=person
                             (192, 128, 0), (64, 0, 128), (192, 0, 128), (64, 128, 128), (192, 128, 128),
                             # 16=potted plant, 17=sheep, 18=sofa, 19=train, 20=tv/monitor
                             (0, 64, 0), (128, 64, 0), (0, 192, 0), (128, 192, 0), (0, 64, 128)])

    r = np.zeros_like(image).astype(np.uint8)
    g = np.zeros_like(image).astype(np.uint8)
    b = np.zeros_like(image).astype(np.uint8)

    for l in range(0, nc):
        idx = image == l
        r[idx] = label_colors[l, 0]
        g[idx] = label_colors[l, 1]
        b[idx] = label_colors[l, 2]

    rgb = np.stack([r, g, b], axis=2)
    return rgb


# Функция получает путь изображения и возвращает обрезанное авто
def segment(path):
  net = dlab
  img_opencv = cv2.imread(path)
  img = Image.open(path)
  if img.size[0] > img.size[1]:
      smaller_size = img.size[1]
  else: smaller_size = img.size[0]
  # Comment the Resize and CenterCrop for better inference results
  trf = T.Compose([T.Resize(512),
                   T.ToTensor(),
                   T.Normalize(mean = [0.485, 0.456, 0.406],
                               std = [0.229, 0.224, 0.225])])
  inp = trf(img).unsqueeze(0)
  out = net(inp)['out']
  om = torch.argmax(out.squeeze(), dim=0).detach().cpu().numpy()
  rgb = decode_segmap(om)

  renova = cv2.resize(rgb.copy(), (img.size[0], img.size[1]))

  renova_bin = cv2.cvtColor(renova, cv2.COLOR_BGR2GRAY)

  kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
  renova_dil = cv2.dilate(renova_bin, kernel, iterations=3)


  masked = cv2.bitwise_and(img_opencv, img_opencv, mask=renova_dil)



  return renova_bin
