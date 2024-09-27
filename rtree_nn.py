'''
rtree_nn.py
Аргументы: -d <datasetFile>, -q <queryFile>, -b <Bvalue>
Реализация алгоритма для поиска ближайших соседей
'''

import time
import getopt
import sys

import rtree_builder as rtree_builder
import tree.rtree as Rtree
import scan_nn

# ближайшая дистанция
global distance
# ближайшие соседи
global results

# ближайшая дистанция от query точки до ноды
def nDis(node, query):
    dis = 0
    if query[0] < node.range[0]:
        dis += (node.range[0]-query[0])**2
    elif query[0] > node.range[1]:
        dis += (query[0]-node.range[1])**2
    if query[1] < node.range[2]:
        dis += (node.range[2]-query[1])**2
    elif query[1] > node.range[3]:
        dis += (query[1]-node.range[3])**2

    return dis

# нахождение всех нод в лифах, которые являются ближайшими к query точке
def getNN(leaf, query):
    global distance
    global results
    
    for point in leaf.childList:
        newDis = (point.x-query[0])**2 + (point.y-query[1])**2
        if newDis < distance:
            distance = newDis
            results.clear()
            results.append(point)
        elif newDis == distance:
            results.append(point)

# Использование "Best First" алгоритма
def bestFirst(tupleList, query):
    global distance

    if isinstance(tupleList[0][1], Rtree.Branch):
        node = tupleList[0][1]
        del tupleList[0]
        for child in node.childList:
            tupleList.append((nDis(child, query), child))
        tupleList = sorted(tupleList, key=lambda t:t[0])
    elif isinstance(tupleList[0][1], Rtree.Leaf):
        node = tupleList[0][1]
        del tupleList[0]
        getNN(node, query)
        
    if distance < tupleList[0][0]:
        return

    bestFirst(tupleList, query)

# реализация "Best First" алгоритма с данным r-tree
def answerNnQueries(root, queries):
    global distance
    global results
    
    resultFile = 'resultNN.txt'
    # the start time
    timeStart = time.time()
    f = open(resultFile, 'wt')
    for query in queries:
        
        distance = float('inf')
        results = []
        
        bestFirst([(0, root)], query)
        for result in results:
            f.write(str(result.ident) + ' ')
        f.write('\r\n')
    
    timeEnd = time.time()
    f.close()
    i = len(queries)
    print('NN Queries finished. Average time: ' + str((timeEnd-timeStart)/i))

def main():
    datasetFile = 'data/dataset.txt'
    queryFile = 'data/queries_nn.txt'
    Bvalue = None
    
    # парсинг аргументов
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
    # вычисление nn
    queries = scan_nn.readNn(queryFile)
    answerNnQueries(root, queries)
    
if __name__ == '__main__':
    main()
