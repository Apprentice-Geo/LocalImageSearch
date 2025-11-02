import os
from search import SearchCore
from tkinter import filedialog
from PIL import Image, ImageTk
from tkinter import messagebox, IntVar
import ttkbootstrap as ttk


class UI:
    def __init__(self):
        self.core = SearchCore()
        self.searchImgPath = None
        self.searchImg = None
        self.MaxShowResult = 24
        self.searchResult = [0 for _ in range(self.MaxShowResult)]
        self.searchImgSaveCnt = 0
        self.similarityLabel=None
        self.featureLabel=None
        self.searchImgSavePath = 'searchPics'
        self.root = ttk.Window(themename="cosmo",title="Picture Search")
        self.root.geometry("2000x1200")
        self.rootFrm=ttk.Frame(self.root, padding=20)
        self.rootFrm.pack()
        self.chooseFrm = ttk.Labelframe(self.rootFrm,text="Search image", padding=20,style="info")
        self.searchFrm = ttk.Labelframe(self.rootFrm,text="Search options", padding=20,style="info")
        self.resultFrm = ttk.Labelframe(self.rootFrm,text="Search result", padding=20,style="success")
        self.controlFrm= ttk.Frame(self.rootFrm, padding=20)
        self.chooseFrm.grid(column=0, row=0,padx=10, pady=5)
        self.searchFrm.grid(column=0, row=1,padx=10, pady=5)
        self.controlFrm.grid(column=0, row=2,padx=10)
        self.resultFrm.grid(column=1, row=0,rowspan=10)
        ttk.Button(self.chooseFrm, style='Outline.TButton', text="Choose an image", command=self.chooseImg).grid(column=0, row=1,padx=10, pady=10)
        ttk.Button(self.searchFrm, style='Outline.TButton', text="Search", command=self.Search).grid(column=0, row=5 ,ipadx=20,padx=20, pady=10,columnspan =3 )
        ttk.Button(self.controlFrm, style='Outline.TButton', text="Quit", command=self.Quit).grid(column=0, row=0,ipadx=10,padx=10, pady=10,columnspan =2 )
        self.backboard()
        self.root.mainloop()

    def backboard(self):
        tmp = Image.open("resource/Noresult.png").resize((192, 108))
        tmp = ImageTk.PhotoImage(tmp)
        for i in range(self.MaxShowResult):
            self.searchResult[i]=tmp
            ttk.Label(self.resultFrm, image=self.searchResult[i]).grid(column=2 + i % 4, row=1 + i // 4, padx=5, pady=5)
    def chooseImg(self):
        self.searchImgPath = filedialog.askopenfilename()
        img = Image.open(self.searchImgPath)
        self.searchImgSaveCnt += 1
        Maxsize = 155000
        self.backboard()
        w, h = img.size
        h = int((Maxsize * (h / w)) ** 0.5)
        w = int(Maxsize / h)
        img.save(self.searchImgSavePath + "/" + "searchPic_" + str(self.searchImgSaveCnt) + '.jpg')
        self.searchImg = ImageTk.PhotoImage(img.resize((w, h)))
        ttk.Label(self.chooseFrm, image=self.searchImg).grid(column=0, row=2,padx=10, pady=10)
        self.SearchSet()

    def SearchSet(self):
        if self.similarityLabel is not None:
            self.similarityLabel.config(
                text='')
        if self.featureLabel is not None:
            self.featureLabel.config(
                text='')
        self.featureVar = IntVar()
        self.featureVar.set(0)
        self.featureLabel = ttk.Label(self.searchFrm, text="Feature: " + self.core.searchFeature[self.featureVar.get()])
        self.featureLabel.grid(column=1, row=0,padx=10, pady=10)
        for i in range(len(self.core.searchFeature)):
            ttk.Radiobutton(self.searchFrm, style='warning.Outline.Toolbutton', text=self.core.searchFeature[i], variable=self.featureVar, value=i,
                            width=25,
                            command=lambda: self.featureLabel.config(
                                text="Feature: " + self.core.searchFeature[self.featureVar.get()])).grid(column=1,
                                                                                                         row=i + 1,padx=10, pady=10)
        self.similarityVar = IntVar()
        self.similarityVar.set(0)
        self.similarityLabel = ttk.Label(self.searchFrm, text="Similarity: " + self.core.searchSimilarity[self.similarityVar.get()])
        self.similarityLabel.grid(column=2, row=0,padx=10, pady=10)
        for i in range(len(self.core.searchSimilarity)):
            ttk.Radiobutton(self.searchFrm, style='warning.Outline.Toolbutton', text=self.core.searchSimilarity[i], variable=self.similarityVar, value=i,
                            width=25,
                            command=lambda: self.similarityLabel.config(
                                text="Similarity: " + self.core.searchSimilarity[self.similarityVar.get()])).grid(column=2,
                                                                                                               row=i + 1,padx=10, pady=10)

    def Search(self):
        if self.searchImgPath is None:
            messagebox.showinfo("Error", "No image is choosed")
            return
        self.core.search(self.searchImgSavePath + "/" + "searchPic_" + str(self.searchImgSaveCnt) + '.jpg',
                         self.core.searchFeature[self.featureVar.get()],
                         self.core.searchSimilarity[self.similarityVar.get()])
        for i in range(len(self.core.searchResult)):
            if i >=self.MaxShowResult:
                break
            tmp = Image.open("pics" + "/" + self.core.searchResult[i][1]).resize((192, 108))
            tmp = ImageTk.PhotoImage(tmp)
            self.searchResult[i]=tmp
            ttk.Label(self.resultFrm, image=self.searchResult[i]).grid(column=2 + i % 4, row=1 + i // 4,padx=5, pady=5)

    def Quit(self):
        self.searchImg=None
        searchImgs = os.listdir(self.searchImgSavePath)
        for f in searchImgs:
            os.remove(self.searchImgSavePath + '/' + f)
        self.root.destroy()


if __name__ == "__main__":
    UI()
