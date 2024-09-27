'''
Rtree.py
Класс с реализацией r-tree
'''
import math

# точка в r-tree
class Point:
    def __init__(self, pointInfo):
        self.ident = pointInfo[0]
        self.x = pointInfo[1]
        self.y = pointInfo[2]

    # получение координаты
    def position(self, index):
        if index == 1:
            return self.x
        elif index == 2:
            return self.y

# r-tree нода
class Node:
    def __init__(self, Bvalue, level):
        self.childList = []
        self.range = []
        self.centre = []
        self.Bvalue = Bvalue
        self.paren = None
        self.level = level

    # добавление нового потомка к существующей ноде
    def addChild(self, child):
        self.childList.append(child)
        self.update(child)

    # обновление диапазона покрытия узла при добавлении новой точки или узла
    def update(self, child):
        # обновление x и y
        if isinstance(child, Point):
            self.updateRange([child.x, child.x, child.y, child.y])
                
        elif isinstance(child, Node):
            self.updateRange(child.range)

        # обновление координат центра
        self.centre[0] = sum(self.range[0:2])/2
        self.centre[1] = sum(self.range[2:4])/2

    # впомогательная функция для "update" функции
    def updateRange(self, newRange):
        # сравнение и обновление ранга
        if newRange[0] < self.range[0]:
            self.range[0] = newRange[0]

        if newRange[1] > self.range[1]:
            self.range[1] = newRange[1]

        if newRange[2] < self.range[2]:
            self.range[2] = newRange[2]

        if newRange[3] > self.range[3]:
            self.range[3] = newRange[3]
        
    def isOverFlow(self):
        if len(self.childList) > self.Bvalue:
            return True
        else:
            return False

    # расстояние между точкой и центром ноды
    def disToCentre(self, point):
        return ((self.centre[0]-point.x)**2+(self.centre[1]-point.y)**2)**0.5

    def getIncrease(self, point):
        result = 0
        
        if point.x > self.range[1]:
            result += point.x-self.range[1]
        elif point.x < self.range[0]:
            result += self.range[0] - point.x
        if point.y > self.range[3]:
            result += point.y - self.range[3]
        elif point.y < self.range[2]:
            result += self.range[2] - point.y
        
        return result

    # периметр текущей ноды
    def getPerimeter(self):
        return self.range[1]-self.range[0]+self.range[3]-self.range[2]
    
    # сплит ноды, a node, перепись Leaf and Branch
    def split(self):
        return None

# leaf нода, которая содержит в себе только точки
class Leaf(Node):
    def __init__(self, Bvalue, level, point):
        super().__init__(Bvalue, level)
        self.range = [point.x, point.x, point.y, point.y]
        self.centre = [point.x, point.y]

    def split(self):
        # сортировка по x координате
        self.sortChildren(1)
        nodes = self.getBestSplit()
        periSum = nodes[0].getPerimeter() + nodes[1].getPerimeter()
        # сортировка по y координате
        self.sortChildren(2)
        newNodes = self.getBestSplit()
        newSum = newNodes[0].getPerimeter() + newNodes[1].getPerimeter()
        # возвращает лучший сплит
        if newSum < periSum:
            return newNodes
        else:
            return nodes

    # сортировка потомка по x или y координате
    def sortChildren(self, index):
        length = len(self.childList)
        for i in range(0, length):
            for j in range(i+1, length):
                if self.childList[i].position(index) > self.childList[j].position(index):
                    temp = self.childList[i]
                    self.childList[i] = self.childList[j]
                    self.childList[j] = temp

    # выдача лучшего сплита по сортировке потомка
    def getBestSplit(self):
        # переменная для хранения минимального периметра
        periSum = float('inf')
        # переменная для хранения лучшего сплита
        nodes = []
        b = math.floor(0.4 * self.Bvalue)
        for i in range(b, len(self.childList) - b + 1):
            
            node1 = Leaf(self.Bvalue, 1, self.childList[0])
            node1.paren = self.paren
            # MBR первого множества
            for j in range(0, i):
                node1.addChild(self.childList[j])
            
            node2 = Leaf(self.Bvalue, 1, self.childList[i])
            node2.paren = self.paren
            # MBR второго множества
            for j in range(i, len(self.childList)):
                node2.addChild(self.childList[j])

            # проверка на лучший сплит
            newSum = node1.getPerimeter() + node2.getPerimeter()
            if newSum < periSum:
                periSum = newSum
                nodes = [node1,node2]

        # возращение лучшего сплита
        return nodes
                

# хранит только ноды
class Branch(Node):
    def __init__(self, Bvalue, level, node):
        super().__init__(Bvalue, level)
        self.range = node.range[:]
        self.centre = node.centre[:]

    
    def chooseChild(self, point):
        result = None
        increase = None
        for child in self.childList:
            newIncrease = child.disToCentre(point)
            
            if increase == None:
                increase = newIncrease
                result = child
            elif increase != 0 and newIncrease/increase > 0.93 and newIncrease/increase < 1.07:
                if len(result.childList)/len(child.childList)>2:
                    increase = newIncrease
                    result = child
            elif newIncrease < increase:
                increase = newIncrease
                result = child
            
        return result

    def split(self):
        
        self.sortChildren(0)
        nodes = self.getBestSplit()
        periSum = nodes[0].getPerimeter() + nodes[1].getPerimeter()
        
        for i in range(1,4):
            self.sortChildren(i)
            newNodes = self.getBestSplit()
            newSum = newNodes[0].getPerimeter() + newNodes[1].getPerimeter()
            
            if newSum < periSum:
                periSum = newSum
                nodes = newNodes

        for node in nodes[0].childList:
            node.paren = nodes[0]
        for node in nodes[1].childList:
            node.paren = nodes[1]
        return nodes

    def sortChildren(self, index):
        length = len(self.childList)
        for i in range(0, length):
            for j in range(i+1, length):
                if self.childList[i].range[index] > self.childList[j].range[index]:
                    temp = self.childList[i]
                    self.childList[i] = self.childList[j]
                    self.childList[j] = temp

    def getBestSplit(self):
        periSum = float('inf')
        nodes = []
        b = math.floor(0.4 * self.Bvalue)
        for i in range(b, len(self.childList) - b + 1):
            node1 = Branch(self.Bvalue, self.level, self.childList[0])
            node1.paren = self.paren
            # MBR первого множества
            for j in range(0, i):
                node1.addChild(self.childList[j])
            node2 = Branch(self.Bvalue, self.level, self.childList[i])
            node2.paren = self.paren
            # MBR второго множества
            for j in range(i, len(self.childList)):
                node2.addChild(self.childList[j])
            # проверка на лучший сплит
            newSum = node1.getPerimeter() + node2.getPerimeter()
            if newSum < periSum:
                periSum = newSum
                nodes = [node1,node2]
        # возвращение лучшего сплита
        return nodes
