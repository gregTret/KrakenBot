import sys
from os import walk
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def BuildTest(directory,saveDirectory):
    def ftl(filename1):
        f=open(filename1,'r')
        lines = f.readlines()
        data=[]
        for line in lines:
            data.append(float(line.replace("\n", "")))
        return data
    def ltf(filename,data):
        f=open(filename,'w+')
        for x in data:
            f.write(str(x)+'\n')
        f.close()
    def generate(data,gfc):
        for x in range(len(data)):
            if (x<len(data)-101):
                test=[]
                for i in range(100):
                    test.append(data[x+i])
                ltf('set/'+str(gfc),test)
                gfc+=1 
        return (gfc)

    os.chdir(saveDirectory)
    try:
        os.mkdir(saveDirectory+'set')
    except:
        pass

    gfc=0
    filenames = next(walk(directory), (None, None, []))[2]  
    for i in filenames:
        print (i)
        gfc=generate(ftl(directory+i),gfc)

    
    #START OF IMAGE CREATION

    totalPass=0
    totalFail=0
    os.chdir(saveDirectory+"set/")
    gfc=0
    filenames = next(walk(saveDirectory+'set/'), (None, None, []))[2] 
    csvData=[]

    try:
        os.mkdir(saveDirectory+"set/images")
    except:
        pass

    def ftl(filename1):
        f=open(filename1,'r')
        lines = f.readlines()
        data=[]
        for line in lines:
            data.append(float(line.replace("\n", "")))
        return data

    def dtf(filename,data):
        f=open(filename,'w+')
        f.write(str(data)+'\n')
        f.close()

    def imgGen(filename,df):
        df.data.plot()
        plt.savefig(filename,dpi=20)
        # For Fullsize Images
        # plt.savefig(filename)
        plt.clf()

    def generate(data,gfc):
        temp=[]
        df = pd.DataFrame(data, columns=['data'])
        df['min'] = df.data[(df.data.shift(1) > df.data) & (df.data.shift(-1) > df.data)]
        min= df['min'].values.tolist()
        temp.append(str(gfc)+'.jpeg')
        if (len(min)>3):
            if (min[len(min)-2]>=1): 
                imgGen(saveDirectory+'set/images/'+str(gfc)+'.jpeg',df)
                temp.append(1)
            else:
                imgGen(saveDirectory+'set/images/'+str(gfc)+'.jpeg',df)
                temp.append(0)
        else:
            imgGen(saveDirectory+'set/images/'+str(gfc)+'.jpeg',df)
            temp.append(0)
        return temp
        
    for i in filenames:
        try:
            print (round(100.0*float(gfc)/(len(filenames)), 3),'%')
            csvData.append(generate(ftl(i),gfc))
            os.remove(saveDirectory+'set/'+i)
        except:
            pass
        gfc+=1

    f=open(saveDirectory+"set/classifications.csv","w+")
    f.write("Names, ID \n")
    for x in csvData:
        f.write(str(x[0])+','+str(x[1])+'\n')


