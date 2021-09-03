import sys
from os import walk
import os
import csv
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

from .Helper import HelperFunctions as hp

class TestBuilder:
    def BuildTest(directory,saveDirectory,imageSize):
        # Data Chunk Generator
        os.chdir(saveDirectory)
        try:
            os.mkdir(saveDirectory+'set')
        except:
            pass
        gfc=0
        filenames = next(walk(directory), (None, None, []))[2]  
        for i in filenames:
            print (i)
            gfc=hp.generateDataChunks(hp.ftl(directory+i),gfc)
        # Image Generation
        os.chdir(saveDirectory+"set/")
        gfc=0
        filenames = next(walk(saveDirectory+'set/'), (None, None, []))[2] 
        csvData=[]
        try:
            os.mkdir(saveDirectory+"set/images")
        except:
            pass   
        for i in filenames:
            try:
                print (round(100.0*float(gfc)/(len(filenames)), 3),'%')
                csvData.append(hp.generateImages(hp.ftl(i),gfc,saveDirectory,imageSize))
                os.remove(saveDirectory+'set/'+i)
            except:
                pass
            gfc+=1
        f=open(saveDirectory+"set/classifications.csv","w+")
        f.write("Names, ID \n")
        for x in csvData:
            f.write(str(x[0])+','+str(x[1])+'\n')
