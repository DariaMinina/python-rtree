'''
scan_range.py
Аргументы: -d <datasetFile>, -q <queryFile>
'''

import sys
import time
import getopt


def getPoint(nextLine):
    content = nextLine.strip('\n').split(' ')
    while content.count('') != 0:
        content.remove('')
    ident = int(content[0])
    x = float(content[1])
    y = float(content[2])
    
    return [ident, x, y]

def readPoints(datasetFile):
    fileHandle = open(datasetFile, 'rt')
    points = []
    nextLine = fileHandle.readline()
    nextLine = fileHandle.readline()
    
    while nextLine != '':
        points.append(getPoint(nextLine))
        nextLine = fileHandle.readline()
    
    fileHandle.close()
    return points

def getQuery(nextLine):
    content = nextLine.strip('\n').split(' ')
    while content.count('') != 0:
        content.remove('')
    result = []
    for s in content:
        result.append(float(s))
    
    return result


def sortQuery(result):
    if result[0]>result[1]:
        temp = result[0]
        result[0] = result[1]
        result[1] = temp
    if result[2]>result[3]:
        temp = result[2]
        result[2] = result[3]
        result[3] = temp
    return result


def readRanges(queryFile):
    fileHandle = open(queryFile, 'rt')
    queries = []
    nextLine = fileHandle.readline()
    
    while nextLine != '':
        query = getQuery(nextLine)
        queries.append(sortQuery(query))
        nextLine = fileHandle.readline()
    
    fileHandle.close()
    return queries


def isIntersect(point, query):

    x = point[1]
    y = point[2]

    left = query[0]
    right = query[1]
    top = query[2]
    bottom = query[3]
    
    if((x-left)*(x-right) <= 0 and (y-top)*(y-bottom) <= 0):
        return True
    else:
        return False


def scanRangeQueries(points, queries):

    resultFile = 'resultRange-scan.txt'
    fResult = open(resultFile, 'wt')

    timeStart = time.time()

    for query in queries:
        times = 0

        for point in points:
            if isIntersect(point, query):
                times += 1
                
        fResult.write(str(times) + '\r\n')
    
    fResult.close()

    timeEnd = time.time()
    i = len(queries)
    print('Scan range queries finished. Average time: ' + str((timeEnd-timeStart)/i))

def main():
    datasetFile = 'data/dataset.txt'
    queryFile = 'data/queries_range.txt'
    
    # Парсинг аргументов
    options,args = getopt.getopt(sys.argv[1:],"d:q:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
    
    # Сканирование датасета
    queries = readRanges(queryFile)
    points = readPoints(datasetFile)
    scanRangeQueries(points, queries)

if __name__ == '__main__':
    main()
