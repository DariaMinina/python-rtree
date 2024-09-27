'''
rtree_range.py
Аргументы: -d <datasetFile>, -q <queryFile>, -b <Bvalue>
'''

import time
import getopt
import sys

import rtree_builder as rtree_builder
import tree.rtree as Rtree
import scan_range

# range-query алгоритма
def rangeQuery(node, queryRange):
    result = 0
    if isinstance(node, Rtree.Leaf):
        
        result = searchLeaf(node, queryRange)
    else:
        
        for child in node.childList:
            if isIntersect(child.range, queryRange):
                result += rangeQuery(child, queryRange)
    
    return result


def searchLeaf(leaf, ranges):
    result = 0
    for point in leaf.childList:
        if point.x<ranges[0] or point.x>ranges[1] or point.y<ranges[2] or point.y>ranges[3]:
            pass
        else:
            result += 1
        
    return result

def isIntersect(range1, range2):
    if range1[0]>range2[1] or range1[1]<range2[0] or range1[2]>range2[3] or range1[3]<range2[2]:
        return False
    else:
        return True

# запуск range-query алгоритма на данном r-tree 
def answerRangeQueries(root, queries):
    resultFile = 'resultRange.txt'
    # start time
    timeStart = time.time()
    f = open(resultFile, 'wt')
    for query in queries:
        result = rangeQuery(root, query)
        f.write(str(result) + '\r\n')
    # the end time
    timeEnd = time.time()
    f.close()
    i = len(queries)
    print('Range Queries finished. Average time: ' + str((timeEnd-timeStart)/i))


def main():
    datasetFile = 'dataset.txt'
    queryFile = 'queriesRange.txt'
    Bvalue = None
    
    # Парсинг аргументов
    options,args = getopt.getopt(sys.argv[1:],"d:q:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-q':
            queryFile = para
        if opt == '-b':
            Bvalue = int(para)
    
    # построение r-tree
    root = rtree_builder.buildRtree(datasetFile, Bvalue)
    rtree_builder.checkRtree(root)
    # ответ
    queries = scan_range.readRanges(queryFile)
    answerRangeQueries(root, queries)

if __name__ == '__main__':
    main()
