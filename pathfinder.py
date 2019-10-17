from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import argparse
import sys
from xml.etree import ElementTree
import pprint
import glob

import os
import glob
import re



globalCount=0
numberOfLines=0


def getDomain(url):
    cleanURL = re.sub("^(http|https)://","",url)
    cleanURL = re.sub("^(www)\.","",cleanURL)

    print(cleanURL)

    domain = re.search("^.[^/?&]+", cleanURL)
    print(domain.group(0))
    return domain.group(0)



def listFiles(path):
    files = [f for f in glob.glob(path + "**/*_L*.txt", recursive=True)]
    return files



def deleteFiles(files):
    for file in files:
        print(file)
    if files:
        answer= input('These files will be removed. Are you sure? (y/n): ')
        if (answer=='y' or answer=='Y'):
            for file in files:
                os.remove(file)
        elif (answer=='n' or answer=='n'):
            sys.exit()


parser = argparse.ArgumentParser()
parser.add_argument("-url", help="urlFormat: http://example.com/l1/l2/l3/l4")
parser.add_argument("-b", help="burp xml file")
parser.add_argument("-f", help="read urlFormat: http://example.com/l1/l2/l3/l4 from file")
parser.add_argument("-l", help="choice the path level", type=int)
parser.add_argument("-c", help="consolidate L* files in a single out file")
parser.add_argument("-d", help="delete L* files", action='store_true')
parser.add_argument("-t", help="TLD")

#check if any arguments have been passed 
# if(len(sys.argv)==1):
#     parser.print_help()
#     sys.exit()




def getNumberOfLines(filePath):
    count = 0
    try:
        with open(filePath,"r") as file:
            for url in file:
                count = count+1
            file.close()
    except FileNotFoundError:
        return False
    return count




#get paths in Posix Path format
#return as a tuple removing the first (/) character
def getPaths(url):
    global globalCount

    globalCount = globalCount +1
    print(url,(globalCount/1)*100)

    temp = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts
    #print(url[len(url)-1])
    if(url[len(url)-1].find("/"))==-1:
        temp = temp + ('f',)
    else:
        temp = temp + ('d',)

    return (temp[ : 0 ] + temp[1 : ])


def splitPaths(url,paths):
    level = 0
    len_paths = len(paths)
    
    if len_paths>1:
        for path in paths:
            level = level +1
            if (level == len_paths-1):
                if(paths[len_paths-1].find("f"))!=-1:
                    #print(checkDuplicatePath(0,path))
                    if(not checkDuplicatePath(getDomain(url),0,path)):
                        #print(path)
                        writeWordLevelFile(getDomain(url),path,0)
                else:
                    if(not checkDuplicatePath(getDomain(url),level,path)):
                        #print(path)
                        writeWordLevelFile(getDomain(url),path,level)
            elif (level != len_paths):
                if(not checkDuplicatePath(getDomain(url),level,path)):
                    #print(path)

                    writeWordLevelFile(getDomain(url),path,level)
           

def checkDuplicatePath(domain,level,path_check):
    try:
        with open(domain+"_"+"L"+str(level)+".txt","r") as file:
            for path in file:
                if path.find(path_check) >=0:
                    return True
                    #print(path)
            
            file.close()
    except FileNotFoundError:
        return False
    return False



def writeWordLevelFile(domain,path,level):
    if path != '':
        file = open(domain+"_"+"L"+str(level)+".txt","a+")
        path = path.replace("\n","")
        file.write(path+"\n")
        file.close


def getPathsFromBurpFile():
    with open(args.burp, 'rt') as f:
        tree = ElementTree.parse(f)

    for node in tree.iter():
        if(node.find("url") is not None):
            paths = getPaths(node.find("url").text)
            splitPaths(paths)
        #print(node.text)

def consolodateFiles(domain):
    #print(sorted(glob.glob(domain+"_L*.txt")))
    L_files = sorted(glob.glob(domain+"_L*.txt"))
    consolidatePathsFile=[]
    consolidatePathsGeneral=[]

    

    size_L_files = len(L_files)
    

    for i in range(size_L_files):
        #descartar size = 1 se L0.txt existir

        with open(L_files[i],'r') as paths:
            for path in paths:
                consolidatePathsFile.append(path)
                #print(path)
        consolidatePathsGeneral.append(consolidatePathsFile)
        consolidatePathsFile=[]

    if(L_files.__getitem__(0).__contains__('L0.txt')==True):
        temp = consolidatePathsGeneral[0]
        consolidatePathsGeneral[0]=consolidatePathsGeneral[len(consolidatePathsGeneral)-1]
        consolidatePathsGeneral[len(consolidatePathsGeneral)-1]=temp


    #print(consolidatePathsGeneral)

    r=[[]]
    for x in consolidatePathsGeneral:
        t = []
        for y in x:
            for i in r:
                t.append(i+[y])
        r = t
    #print(r)
    path = ""

    for i in range(0,len(r)):
        for j in range(0,len(r[i])):
            path = path+'/'+''.join(r[i][j].replace("\n",""))
        print (path)
        path = ""






    # for k in range(0,len(consolidatePathsGeneral)):
    #     for w in range(0,len(consolidatePathsGeneral[k])):
    #         str = ''.join(consolidatePathsGeneral[k][w])
    #         print(str)
    #         for i in range(w+1,len(consolidatePathsGeneral)):
    #             str = ''.join(consolidatePathsGeneral[i][w])
    #             print(str)
    #             for j in range(0,len(consolidatePathsGeneral[k])):
    #                 str = ''.join(consolidatePathsGeneral[i][w])
    #                 print(str)
    # return 1


def getPathsFromTxtFile(filePath):
    try:
        with open(filePath,"r") as file:
            for url in file:
                paths = getPaths(url)
                splitPaths(url,paths)
            file.close()
    except FileNotFoundError:
        return False
    return False

args = parser.parse_args()

if args.url:
    paths = getPaths(args.url)
    splitPaths(getDomain(args.url),paths)
elif args.b:
    getPathsFromBurpFile()
elif args.c:
    consolodateFiles(args.c)
elif args.f:
    numberOfLines = getNumberOfLines(args.f)
    getPathsFromTxtFile(args.f)
elif args.d:
    deleteFiles(listFiles(os.getcwd()))
elif args.t:
    getDomain(args.t)






