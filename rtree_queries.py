'''
rtree_queries.py
Аргументы: -d <datasetFile>, -r <rangeQueryFile>, -n <nnQueryFile>, -b <Bvalue>
'''

import time
import sys
import getopt

import rtree_builder
import rtree_range
import rtree_nn
import scan_range
import scan_nn

# сканирование данные последовательно 
def scanDataSet(datasetFile):
    points = []
    start = time.time()
    f = open(datasetFile, 'rt')
    nextLine = f.readline() 
    nextLine = f.readline()
    while nextLine != '':
        points.append(scan_range.getPoint(nextLine))
        nextLine = f.readline()
        
    f.close()
    end = time.time()
    print('Scanning time:', str(end-start))
    return points

def main():
    datasetFile = 'data/dataset.txt'
    rangeFile = 'data/queries_range.txt'
    nnFile = 'data/queries_nn.txt'
    Bvalue = None
    scanFlag = 'n'
    
    # парсинг аргументов
    options,args = getopt.getopt(sys.argv[1:],"d:r:n:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-r':
            rangeFile = para
        if opt == '-n':
            nnFile = para
        if opt == '-b':
            Bvalue = int(para)
        
    # сканирование датасета
    points = scanDataSet(datasetFile)
    
    # построение r-tree
    try:
        root = rtree_builder.buildRtree(datasetFile, Bvalue)
        rtree_builder.checkRtree(root)
    except Exception:
        print('Memory overflow')
    
    # вывод range queries
    queries = scan_range.readRanges(rangeFile)
    scan_range.scanRangeQueries(points, queries)
    rtree_range.answerRangeQueries(root, queries)
    
    # вывод nn queries
    queries = scan_nn.readNn(nnFile)
    scan_nn.scanNNQueries(points, queries)
    rtree_nn.answerNnQueries(root, queries)

if __name__ == '__main__':
    main()
