import pandas as pd
import matplotlib.pyplot as plt
import os
from os import walk
import shutil

# Functions used across multiple files
class HelperFunctions():
    def CreateImageFolders(path):
        try:
            os.mkdir(path+'/buy')
            os.mkdir(path+'/sell')
            os.mkdir(path+'/nothing')
            status=0
        except:
            pass

    def SetupDirectories(currentPath):
        status=1
        try:
            os.mkdir(currentPath+'/data')
            os.mkdir(currentPath+'/generatedData')
            os.mkdir(currentPath+'/generatedModels')
            os.mkdir(currentPath+'/tests')
            os.mkdir(currentPath+'/logs')
            status=0
        except:
            pass
        try:
            f = open(currentPath+'/logs/logs.txt', 'a')
            f.close()
            f = open(currentPath+'/logs/holdings.txt', 'a')
            f.close()
        except:
            print ("Failed to create Log Files.")
            pass     
        return status

    def ListToJPEG(data,filename):
        newData=[]
        for i in range(len(data)):
            if (i>=(len(data)-101)):
                newData.append(data[i])
        df = pd.DataFrame(newData, columns=['data'])
        df.data.plot()
        plt.savefig(filename,dpi=30)
        plt.clf()

    def D2listToCSV(data,directory):
        f=open(directory,"w+")
        f.write("Names, ID \n")
        for x in data:
            f.write(str(x[0])+','+str(x[1])+'\n')  
        f.close()

    def CSVBuilderClassification(directory):
        data=[]
        counter=0
        directoryList=[directory+'/nothing/',directory+'/buy/',directory+'/sell/']
        for x in directoryList:
            sd=next(walk(x),(None, None, []))[2]
            for i in sd:
                tmp=[]
                tmp.append(i)
                tmp.append(str(counter))
                data.append(tmp)
            counter+=1
        HelperFunctions.D2listToCSV(data,directory+"/classifications.csv")

    def SplitImagesFromFolders(directory):
        directoryList=[directory+'/nothing/',directory+'/buy/',directory+'/sell/']
        for x in directoryList:
            sd=next(walk(x),(None, None, []))[2]
            for i in sd:
                pass
                # Line Broken
                # shutil.move(x + i, directory+'/images/'+i)

    def sortDifferentNames(directory,identifier):
        data=[]
        counter=0
        sd=next(walk(directory),(None, None, []))[2]
        HelperFunctions.CreateImageFolders(directory)
        for x in sd:
            if (x[0]=='n'):
                shutil.move(directory +'/'+ x, directory+'/nothing/'+identifier+x)
            elif (x[0]=='b'):
                shutil.move(directory +'/'+ x, directory+'/buy/'+identifier+x)
            elif (x[0]=='s'):
                shutil.move(directory +'/'+ x, directory+'/sell/'+identifier+x)
        HelperFunctions.CSVBuilderClassification(directory)

    def ftl(filename1):
        f=open(filename1,'r')
        lines = f.readlines()
        data=[]
        for line in lines:
            data.append(float(line.replace("\n", "")))
        return data
    
    def holdingCheck(filename):
        f=open(filename,'r')
        lines = f.readlines()
        data=[]
        for line in lines:
            data.append(line.replace("\n", ""))
        return data

    def dtf(filename,data):
        f=open(filename,'w+')
        f.write(str(data)+'\n')
        f.close()

    def ltf(filename,data):
        f=open(filename,'w+')
        for x in data:
            f.write(str(x)+'\n')
        f.close()
    
    def appendLineToFile(filename,data):
        f=open(filename,'a')
        f.write(str(data)+'\n')
        f.close()

    def generateDataChunks(data,gfc):
        for x in range(len(data)):
            if (x<len(data)-101):
                test=[]
                for i in range(100):
                    test.append(data[x+i])
                HelperFunctions.ltf('set/'+str(gfc),test)
                gfc+=1 
        return (gfc)

    def generateImages(data,gfc,saveDirectory,size):
        temp=[]
        df = pd.DataFrame(data, columns=['data'])
        df['min'] = df.data[(df.data.shift(1) > df.data) & (df.data.shift(-1) > df.data)]
        min= df['min'].values.tolist()
        temp.append(str(gfc)+'.jpeg')
        if (len(min)>3):
            if (min[len(min)-2]>=1): 
                HelperFunctions.imgGen(saveDirectory+'set/images/'+str(gfc)+'.jpeg',df,size)
                temp.append(1)
            else:
                HelperFunctions.imgGen(saveDirectory+'set/images/'+str(gfc)+'.jpeg',df,size)
                temp.append(0)
        else:
            HelperFunctions.imgGen(saveDirectory+'set/images/'+str(gfc)+'.jpeg',df,size)
            temp.append(0)
        return temp

    def imgGen(filename,df,size):
        df.data.plot()
        if (size=="full"):
            plt.savefig(filename)
        elif (size=="30"):
            plt.savefig(filename,dpi=30)   
        plt.clf()