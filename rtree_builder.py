'''
rtree_builder.py
Аргументы: -d <datasetFile>, -b <Bvalue>
Построение r-tree из созданного датасета
'''

import getopt
import sys

import tree.rtree as Rtree
import scan_range

global root
global Bvalue

def handleOverFlow(node):
    global root
    global Bvalue
    
    # сплит ноды на две новые ноды
    nodes = node.split()
    # если root нода переполнена, строится новый root 
    if node.paren == None:
        root = Rtree.Branch(Bvalue, node.level + 1, nodes[0])
        root.addChild(nodes[0])
        root.addChild(nodes[1])
        root.childList[0].paren = root
        root.childList[1].paren = root
    else:
        # обновление родительной ноды
        parent = node.paren
        parent.childList.remove(node)
        parent.childList += nodes

        if parent.isOverFlow():
            handleOverFlow(parent)

# добавление точки в ноду
def insert(node, point):    
    # если нода является листком
    if  isinstance(node, Rtree.Leaf):
        node.addChild(point)
        if node.isOverFlow():
            handleOverFlow(node)

    # если нода является бранчем
    elif isinstance(node, Rtree.Branch):
        node.update(point)
        childNode = node.chooseChild(point)
        insert(childNode, point)

    else:
        pass

def buildRtree(dataSetName, *B):
    global root
    global Bvalue
    
    Bvalue = 25
    if len(B) == 1 and B[0] != None:
        Bvalue = B[0]
        
    f = open(dataSetName, 'rt')
    nextLine = f.readline()
    # размер датасета
    size = int(nextLine.strip('\n'))
    
    nextLine = f.readline()
    point = Rtree.Point(scan_range.getPoint(nextLine))
    root = Rtree.Leaf(Bvalue, 1, point)
    root.addChild(point)
    
    nextLine = f.readline()
    while nextLine != '':
        point = Rtree.Point(scan_range.getPoint(nextLine))
        insert(root, point)
        nextLine = f.readline()

    f.close()
    print('R-tree has been built. B is:', Bvalue,'Highest level is:',root.level)
    return root

def checkRtree(rtree):    
    checkBranch(rtree)
    print('Finished checking R-tree')

def checkLeaf(leaf):    
    def insideLeaf(x, y, parent):
        if x<parent[0] or x>parent[1] or y<parent[2] or y>parent[3]:
            return False
        else:
            return True
    
    checkNode(leaf)
    for point in leaf.childList:
        if not insideLeaf(point.x, point.y, leaf.range):
            print('point(', point.x, point.y, 'is not in leaf range:', leaf.range)

def checkBranch(branch):    
    def insideBranch(child, parent):
        if child[0]<parent[0] or child[1]>parent[1] or child[2]<parent[2] or child[3]>parent[3]:
            return False
        else:
            return True
    
    checkNode(branch)
    for child in branch.childList:
        if not insideBranch(child.range, branch.range):
            print('child range:', child.range, 'is not in node range:', branch.range)

        if isinstance(child, Rtree.Branch):
            checkBranch(child)
        elif isinstance(child, Rtree.Leaf):
            checkLeaf(child)

def checkNode(node):
    global Bvalue
    
    length = len(node.childList)
    if length == 0:
        print('empty node. node level:', node.level, 'node range:', node.range)
    if length > Bvalue:
        print('overflow. node level:', node.level, 'node range:', node.range)
        
    r = node.range
    if (r[0]+r[1])/2 != node.centre[0] or (r[2]+r[3])/2 != node.centre[1]:
        print('wrong centre. node level:', node.level, 'node range:', node.range)
    if r[0]>r[1] or r[2]>r[3]:
        print('wrong range. node level:', node.level, 'node range:', node.range)

def main():
    global root

    datasetFile = 'data/dataset.txt'
    Bvalue = None
    
    # парсинг аргументов
    options,args = getopt.getopt(sys.argv[1:],"d:b:")
    for opt, para in options:
        if opt == '-d':
            datasetFile = para
        if opt == '-b':
            Bvalue = int(para)
    
    # построение r-tree из датасета
    buildRtree(datasetFile, Bvalue)
    # проверка корректности r-tree
    checkRtree(root)

if __name__ == "__main__":
    main()
