import math
from collections import defaultdict

class DataPoint:
    def __init__(self, numattributes):
        self.attributes = [0] * numattributes

class TreeNode:
    def __init__(self):
        self.entropy = 0.0
        self.data = []
        self.decompositionAttribute = -1
        self.decompositionValue = -1
        self.children = []
        self.parent = None

class ID3:
    def __init__(self):
        self.numAttributes = 0
        self.attributeNames = []
        self.domains = []

    def getSymbolValue(self, attribute, symbol):
        if symbol not in self.domains[attribute]:
            self.domains[attribute].append(symbol)
        return self.domains[attribute].index(symbol)

    def getAllValues(self, data, attribute):
        values = []
        for point in data:
            symbol = self.domains[attribute][point.attributes[attribute]]
            if symbol not in values:
                values.append(symbol)
        return [self.domains[attribute].index(symbol) for symbol in values]

    def getSubset(self, data, attribute, value):
        subset = [point for point in data if point.attributes[attribute] == value]
        return subset

    def calculateEntropy(self, data):
        numdata = len(data)
        if numdata == 0:
            return 0
        attribute = self.numAttributes - 1
        value_counts = defaultdict(int)

        for point in data:
            value_counts[point.attributes[attribute]] += 1

        sum_entropy = 0
        for count in value_counts.values():
            probability = count / numdata
            if probability > 0:
                sum_entropy += -probability * math.log(probability, 2)

        return sum_entropy

    def alreadyUsedToDecompose(self, node, attribute):
        if node.children:
            if node.decompositionAttribute == attribute:
                return True
        if node.parent is None:
            return False
        return self.alreadyUsedToDecompose(node.parent, attribute)

    def decomposeNode(self, node):
        numdata = len(node.data)
        numinputattributes = self.numAttributes - 1
        node.entropy = self.calculateEntropy(node.data)

        if node.entropy == 0:
            return

        selected = False
        selectedAttribute = -1
        bestEntropy = 0

        for i in range(numinputattributes):
            if self.alreadyUsedToDecompose(node, i):
                continue

            averageentropy = 0
            numvalues = len(self.domains[i])

            for j in range(numvalues):
                subset = self.getSubset(node.data, i, j)
                if len(subset) == 0:
                    continue
                subentropy = self.calculateEntropy(subset)
                averageentropy += subentropy * len(subset)

            averageentropy /= numdata

            if not selected or averageentropy < bestEntropy:
                selected = True
                bestEntropy = averageentropy
                selectedAttribute = i

        if not selected:
            return

        node.decompositionAttribute = selectedAttribute
        numvalues = len(self.domains[selectedAttribute])
        node.children = [TreeNode() for _ in range(numvalues)]

        for j in range(numvalues):
            node.children[j].parent = node
            node.children[j].data = self.getSubset(node.data, selectedAttribute, j)
            node.children[j].decompositionValue = j

        for j in range(numvalues):
            self.decomposeNode(node.children[j])

        node.data = None

    def readData(self, filename):
        try:
            with open(filename, 'r') as file:
                lines = file.readlines()
        except Exception as e:
            print(f"Unable to open data file: {filename}\n{e}")
            return 0

        lines = [line.strip() for line in lines if line.strip() and not line.startswith("//")]

        if len(lines) == 0:
            print(f"No data found in the data file: {filename}\n")
            return 0

        self.attributeNames = lines[0].split()
        self.numAttributes = len(self.attributeNames)

        if self.numAttributes <= 1:
            print(f"Read line: {lines[0]}")
            print(f"Could not obtain the names of attributes in the line")
            print(f"Expecting at least one input attribute and one output attribute")
            return 0

        self.domains = [[] for _ in range(self.numAttributes)]
        root = TreeNode()

        for line in lines[1:]:
            tokens = line.split()
            if len(tokens) != self.numAttributes:
                print(f"Read {len(root.data)} data")
                print(f"Last line read: {line}")
                print(f"Expecting {self.numAttributes} attributes")
                return 0

            point = DataPoint(self.numAttributes)
            for i in range(self.numAttributes):
                point.attributes[i] = self.getSymbolValue(i, tokens[i])

            root.data.append(point)

        self.root = root
        return 1

    def printTree(self, node, tab=""):
        outputattr = self.numAttributes - 1
        if node.children == []:
            values = self.getAllValues(node.data, outputattr)
            if len(values) == 1:
                print(f"{tab}\t{self.attributeNames[outputattr]} = \"{self.domains[outputattr][values[0]]}\";")
                return

            print(f"{tab}\t{self.attributeNames[outputattr]} = {{", end="")
            print(", ".join(f"\"{self.domains[outputattr][value]}\"" for value in values), end="")
            print(" };")
            return

        numvalues = len(node.children)
        for i in range(numvalues):
            print(f"{tab}if( {self.attributeNames[node.decompositionAttribute]} == \"{self.domains[node.decompositionAttribute][i]}\" ) {{")
            self.printTree(node.children[i], tab + "\t")
            if i != numvalues - 1:
                print(f"{tab}}} else ", end="")
            else:
                print(f"{tab}}}")

    def createDecisionTree(self):
        self.decomposeNode(self.root)
        self.printTree(self.root, "")

if __name__ == "__main__":
    me = ID3()
    status = me.readData("input.txt")


    if status > 0:
        me.createDecisionTree()
