from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import argparse
import sys


from xml.etree import ElementTree
import pprint





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
    print(url)
    #print(url[len(url)-1])
    if(url[len(url)-1].find("/"))==-1:
        temp = temp + ('f',)
    else:
        temp = temp + ('d',)

    return (temp[ : 0 ] + temp[1 : ])


def splitPaths(paths):
    print(paths)
    level = 0
    len_paths = len(paths)
    
    if len_paths>1:
        for path in paths:
            level = level +1
            if (level == len_paths-1):
                print(paths[len_paths-1].find("f"))
                if(paths[len_paths-1].find("f"))!=-1:
                    writeWordLevelFile(path,0)
                else:
                    writeWordLevelFile(path,level)
            elif (level != len_paths):
                writeWordLevelFile(path,level)
           



def writeWordLevelFile(path,level):
    file = open(str(level)+".txt","a+")
    file.write(path+"\n")

parser = argparse.ArgumentParser()
parser.add_argument("-url", help="urlFormat: http://example.com/l1/l2/l3/l4")
args = parser.parse_args()


paths = getPaths(args.url)
splitPaths(paths)


with open('path_to_your_xml.xml', 'rt') as f:
    tree = ElementTree.parse(f)

for node in tree.iter():
    if(node.find("url") is not None):
        paths = getPaths(node.find("url").text)
        splitPaths(paths)
    #print(node.text)






