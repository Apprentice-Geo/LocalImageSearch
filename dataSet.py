import cv2
import os
import numpy as np
from sklearn.decomposition import PCA
from PIL import Image
import torch
from torchvision import models, transforms
from torch.autograd import Variable

class feature:
    def __init__(self):
        self.pca=PCA(n_components=500)
        self.hog=None
        self.initHOG()
        self.ResTransform = None
        self.Resnet_50 = None
        self.initResnet50()

    def initHOG(self):
        winSize = (128, 128)
        blockSize = (64, 64)
        blockStride = (32, 32)
        cellSize = (32, 32)
        nbins = 16
        self.hog=cv2.HOGDescriptor(winSize, blockSize, blockStride, cellSize, nbins)

    def initResnet50(self):
        resnet50_feature_extractor = models.resnet50(weights=models.ResNet50_Weights.DEFAULT)
        resnet50_feature_extractor.fc = torch.nn.Identity()

        for param in resnet50_feature_extractor.parameters():
            param.requires_grad = False
        self.Resnet_50=resnet50_feature_extractor
        self.ResTransform = transforms.Compose([
            transforms.Resize(512),
            transforms.CenterCrop(512),
            transforms.ToTensor()]
        )
    def getPCA(self,PIC):
        return self.pca.fit_transform(PIC.garyImg)
        #pcaInfoRate = np.sum(self.pca.explained_variance_ratio_)
    def getHOG(self,PIC):
        winStride = (64, 64)
        padding = (64, 64)
        return self.hog.compute(PIC.img, winStride, padding)
    def getRes(self,PIC):
        return self.Resnet_50(Variable(torch.unsqueeze(self.ResTransform(PIC.Img), dim=0).float(), requires_grad=False)).data.numpy()
class pic:
    def __init__(self, path):
        self.picPath = path
        self.savePath = "picDatas/"
        self.img = cv2.imread(path)
        self.Img=Image.open(path)
        self.garyImg = cv2.imread(path, 0)
        self.img = cv2.resize(self.img, (1600, 900))  # 统一尺寸
        self.garyImg =cv2.resize( self.garyImg, (1600, 900))
        self.PCAData = None
        self.HOGData = None
        self.ResData=None

    def showOriginPic(self):
        cv2.imshow(self.picPath + ' Origin Image', self.img)
        cv2.waitKey(0)

    def showGaryPic(self):
        cv2.imshow(self.picPath + 'Gary image', self.garyImg)
        cv2.waitKey(0)

    def saveData(self, dataType):
        if dataType == "PCA":
            np.save(self.savePath + 'PCA_' + self.picPath.split('/')[-1].split('.')[0], self.PCAData)
        elif dataType == "HOG":
            np.save(self.savePath + 'HOG_' + self.picPath.split('/')[-1].split('.')[0], self.HOGData)
        elif dataType == "Resnet50":
            np.save(self.savePath + 'Resnet50_' + self.picPath.split('/')[-1].split('.')[0], self.ResData,allow_pickle=True)


class dataSet:
    def __init__(self, picPath, picDataPath):
        self.featureGet=feature()
        self.picNames = os.listdir(picPath)
        self.picDataNames = os.listdir(picDataPath)
        picDataNameSplit = [x.split('.')[0] for x in self.picDataNames]
        self.datas = []
        for i in range(len(self.picNames)):
            picData = {'imgName': self.picNames[i]}
            if 'PCA_' + self.picNames[i].split('.')[0] in picDataNameSplit:
                picData["PCA"] = np.load(picDataPath + '/' + 'PCA_' + self.picNames[i].split('.')[0] + ".npy")
            else:
                print("%s PCA data lack" % self.picNames[i])
                tmp = pic(picPath + '/' + self.picNames[i])
                tmp.PCAData= self.featureGet.getPCA(tmp)
                picData["PCA"] = tmp.PCAData
                tmp.saveData("PCA")
            if 'HOG_' + self.picNames[i].split('.')[0] in picDataNameSplit:
                picData["HOG"] = np.load(picDataPath + '/' + 'HOG_' + self.picNames[i].split('.')[0] + ".npy")
            else:
                print("%s HOG data lack" % self.picNames[i])
                tmp = pic(picPath + '/' + self.picNames[i])
                tmp.HOGData= self.featureGet.getHOG(tmp)
                picData["HOG"] = tmp.HOGData
                tmp.saveData("HOG")
            if 'Resnet50_' + self.picNames[i].split('.')[0] in picDataNameSplit:
                picData["Resnet50"] = np.load(picDataPath + '/' + 'Resnet50_' + self.picNames[i].split('.')[0] + ".npy",allow_pickle=True)
            else:
                print("%s Resnet50 data lack" % self.picNames[i])
                tmp = pic(picPath + '/' + self.picNames[i])
                tmp.ResData = self.featureGet.getRes(tmp)
                picData["Resnet50"] = tmp.ResData
                tmp.saveData("Resnet50")
            self.datas.append(picData)

        print('\033[1;31;46m' + "dataSet read end: %d Image datas" % len(self.datas) + '\033[0m')


if __name__ == "__main__":
    dataSet = dataSet("pics", "picDatas")

