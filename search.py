import dataSet as DS
import numpy as np


class SearchCore:
    def __init__(self):
        self.featureGet=DS.feature()
        self.dataset = DS.dataSet("pics", "picDatas")
        self.searchResult = None
        self.searchImg = None
        self.searchFeature = {0: "PCA", 1: "HOG",2:"Resnet50",3:"All"}
        self.searchSimilarity = {0: "Euler", 1: "Cosine"}

    def search(self, picPath, Feature, similarity):
        self.searchImg = DS.pic(picPath)
        picFeature=[]
        otherFeature=[]
        if Feature == "PCA":
            self.searchImg.PCAData= self.featureGet.getPCA(self.searchImg)
            picFeature.append(self.searchImg.PCAData)
            otherFeature.append("PCA")
        elif Feature == "HOG":
            self.searchImg.HOGData= self.featureGet.getHOG(self.searchImg)
            picFeature.append(self.searchImg.HOGData)
            otherFeature.append("HOG")
        elif Feature == "Resnet50":
            self.searchImg.ResData = self.featureGet.getRes(self.searchImg)
            picFeature.append(self.searchImg.ResData)
            otherFeature.append("Resnet50")
        elif Feature == "All":
            self.searchImg.PCAData = self.featureGet.getPCA(self.searchImg)
            picFeature.append(self.searchImg.PCAData)
            otherFeature.append("PCA")
            self.searchImg.HOGData = self.featureGet.getHOG(self.searchImg)
            picFeature.append(self.searchImg.HOGData)
            otherFeature.append("HOG")
            self.searchImg.ResData = self.featureGet.getRes(self.searchImg)
            picFeature.append(self.searchImg.ResData)
            otherFeature.append("Resnet50")
        self.searchResult = []
        for i in range(len(self.dataset.datas)):
            # print("cal dis%d" % i)
            tmp=0
            for j in range(len(picFeature)):
                if similarity == "Euler":
                    tmp+=self.calEuler(picFeature[j], self.dataset.datas[i][otherFeature[j]])
                elif similarity == "Cosine":
                    tmp += self.calCosine(picFeature[j], self.dataset.datas[i][otherFeature[j]])
            self.searchResult.append(
                (tmp, self.dataset.datas[i]['imgName']))
        self.searchResult.sort(key=lambda x: x[0])

    def calEuler(self, selfFeature, otherFeature):
        return np.linalg.norm(selfFeature - otherFeature)  # 使用numpy运算速度大大加快

    def calCosine(self, selfFeature, otherFeature):
        return -(np.sum(selfFeature * otherFeature) / (np.linalg.norm(selfFeature) * (np.linalg.norm(otherFeature))))

    def showResult(self):
        if self.searchResult is None:
            print('\033[1;38;41m' + "no result" + '\033[0m')
            return
        print("The number of the searchResult: %d" % len(self.searchResult))
        print("searchResult:", end=' ')
        print(self.searchResult)
        for i in range(len(self.searchResult)):
            if i > 15:
                break
            tmp = DS.pic("pics" + "/" + self.searchResult[i][1])
            tmp.showOriginPic()


if __name__ == "__main__":
    core = SearchCore()
    core.search("pics/coin_9.jpg", "Resnet50", "Cosine")
    core.showResult()
