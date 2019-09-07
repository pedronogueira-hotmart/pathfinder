from urllib.parse import unquote, urlparse
from pathlib import PurePosixPath
import argparse

#get paths in Posix Path format
#return as a tuple removing the last (/) character
def getPaths(url):
    temp = PurePosixPath(
        unquote(
            urlparse(
                url
            ).path
        )
    ).parts
    return (temp[ : 0 ] + temp[1 : ])


def splitPaths(paths):
    level = 0
    if paths:
        for path in paths:
            level = level +1
            writeWordLevelFile(path,level)


def writeWordLevelFile(path,level):
    file = open(str(level)+".txt","a+")
    file.write(path+"\n")

parser = argparse.ArgumentParser()
parser.add_argument("-url", help="urlFormat: http://example.com/l1/l2/l3/l4")
args = parser.parse_args()


paths = getPaths(args.url)
splitPaths(paths)



