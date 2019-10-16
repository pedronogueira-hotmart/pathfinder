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
    domain = re.search("^.[^/?&]+", url)
    print(domain.group(0))
    return domain.group(0)



def listFiles(path):
    files = [f for f in glob.glob(path + "**/L*.txt", recursive=True)]
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


def splitPaths(paths):
    level = 0
    len_paths = len(paths)
    
    if len_paths>1:
        for path in paths:
            level = level +1
            if (level == len_paths-1):
                if(paths[len_paths-1].find("f"))!=-1:
                    #print(checkDuplicatePath(0,path))
                    if(not checkDuplicatePath(0,path)):
                        #print(path)
                        writeWordLevelFile(path,0)
                else:
                    if(not checkDuplicatePath(level,path)):
                        #print(path)
                        writeWordLevelFile(path,level)
            elif (level != len_paths):
                if(not checkDuplicatePath(level,path)):
                    #print(path)

                    writeWordLevelFile(path,level)
           

def checkDuplicatePath(level,path_check):
    try:
        with open("L"+str(level)+".txt","r") as file:
            for path in file:
                if path.find(path_check) >=0:
                    return True
                    #print(path)
            
            file.close()
    except FileNotFoundError:
        return False
    return False



def writeWordLevelFile(path,level):
    file = open(getDomain(path)+"_"+"L"+str(level)+".txt","a+")
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

def consolodateFiles(path_L_files):
    print(path_L_files+"L*.txt")
    print(sorted(glob.glob(path_L_files+"L*.txt")))
    L_files = sorted(glob.glob(path_L_files+"L*.txt"))

    size_L_files = len(L_files)

    for i in range(size_L_files):
        #descartar size = 1 se L0.txt existir

        with open(l_file,'r') as paths:
            for path in paths:
                print(path)

    


        print(L_files[i])


    for l_file in sorted(glob.glob(path_L_files+"L*.txt")):
        with open(l_file,'r') as paths:
            for path in paths:
                print(path)
    

    return 1


def getPathsFromTxtFile(filePath):
    try:
        with open(filePath,"r") as file:
            for url in file:
                paths = getPaths(url)
                splitPaths(paths)
            file.close()
    except FileNotFoundError:
        return False
    return False

args = parser.parse_args()

if args.url:
    paths = getPaths(args.url)
    splitPaths(paths)
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






