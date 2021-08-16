import os
def SetupDirectories(currentPath):
    status=1
    try:
        os.mkdir(currentPath+'/data')
        print("Directory "+currentPath+'/data Successfully Created')
        status=0
    except:
        print("Directory "+currentPath+'/data Already Exists')
        pass
    try:
        os.mkdir(currentPath+'/generatedData')
        print("Directory "+currentPath+'/generatedData Successfully Created')
        status=0
    except:
        print("Directory "+currentPath+'/generatedData Already Exists')
        pass
    try:
        os.mkdir(currentPath+'/generatedModels')
        print("Directory "+currentPath+'/generatedModels Successfully Created')
        status=0
    except:
        print("Directory "+currentPath+'/generatedModels Already Exists')
        pass
    try:
        os.mkdir(currentPath+'/tests')
        print("Directory "+currentPath+'/tests Successfully Created')
        status=0
    except:
        print("Directory "+currentPath+'/tests Already Exists')
        pass
    return status