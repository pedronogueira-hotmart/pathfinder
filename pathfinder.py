from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import argparse
import sys
from xml.etree import ElementTree
import pprint


parser = argparse.ArgumentParser()
parser.add_argument("-url", help="urlFormat: http://example.com/l1/l2/l3/l4")
parser.add_argument("-b", help="burp xml file")
parser.add_argument("-f", help="read urlFormat: http://example.com/l1/l2/l3/l4 from file")



#get paths in Posix Path format
#return as a tuple removing the first (/) character
def getPaths(url):
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
                    print(checkDuplicatePath(0,path))
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
    file = open("L"+str(level)+".txt","a+")
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
elif args.f:
    getPathsFromTxtFile(args.f)








