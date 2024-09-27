'''
scan_nn.py
Аргументы: -d <datasetFile>, -q <queryFile>
'''

import sys
import time
import getopt

import scan_range


def readNn(queryFile):
    fileHandle = open(queryFile, 'rt')
    queries = []
    nextLine = fileHandle.readline()
    
    while nextLine != '':
        queries.append(scan_range.getQuery(nextLine))
        nextLine = fileHandle.readline()
    
    fileHandle.close()
    return queries

# расстояние между точкой и query
def getDis(point, query):
    return (point[1]-query[0])**2 + (point[2]-query[1])**2

# нахождение всех queries с помощью метода сканирования
def scanNNQueries(points, queries):
    
    resultFile = 'resultNN-scan.txt'
    f = open(resultFile, 'wt')
    
    timeStart = time.time()
    
    for query in queries:
        distance = getDis(points[0], query)
        results = [points[0]]
        
        for j in range(1, len(points)):
            newDis = getDis(points[j], query)
            if newDis < distance:
                results.clear()
                results.append(points[j])
                distance = newDis
            elif newDis == distance:
                results.append(points[j])
        
        for result in results:
            f.write(str(result[0]) + ' ')
            
        f.write('\r\n')
    
    f.close()
    
    timeEnd = time.time()
    i = len(queries)
    print('Scan NN queries finished. Average time: ' + str((timeEnd-timeStart)/i))

def main():
    datasetFile = 'data/dataset.txt'
    queryFile = 'data/queries_nn.txt'
    
    # Парсинг аргументов
    options,args = getopt.getopt(sys.argv[1:],"d:q:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
    
    # сканирование датасета
    points = scan_range.readPoints(datasetFile)
    queries = readNn(queryFile)
    scanNNQueries(points, queries)

if __name__ == '__main__':
    main()
