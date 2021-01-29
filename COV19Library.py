from City import *

class COV19Library:
    def __init__(self):
        self.cityArray = []        # array of City objects
        self.size = 0              # len for self.cities
        self.isSorted = False      # a flag to show if self.cities is sorted or not
        self.root = None           # root for BST
        self.timeLine = []         # used for graphing

    def LoadData(self, filename):
        # store the data of cities from filename into the library
        raw_data = open(filename, "r")
        list_data = raw_data.readlines()
        raw_data.close()
        # save the part of the first row with the dates to use for graphing later
        self.timeLine = list_data[0].split(',')[3:]
        del self.timeLine[0]
        # delete the first row of data (headers & labels) to avoid initializing it into a city
        del list_data[0]
        # parse list_data, create city objects, add cities to self.cityArray
        for line in list_data:
            dataArray = line.split(',')
            cid = dataArray[0]
            # this cell has the city and state so it needs to be split further
            city_state = dataArray[1].split()
            cname = " ".join(city_state[:-1]) if len(city_state) > 1 else city_state[0] # if the cell only has a cname
            cstate = city_state[-1] if len(city_state) > 1 else ""                      # cstate is left blank
            pop = dataArray[2]
            # change cases to int for plotting later
            cases = list(map(int, dataArray[3:]))
            # cases[0] is not a case figure
            del cases[0]
            new_city = City(cid, cname, cstate, pop, cases)
            self.cityArray.append(new_city)
        self.size = len(self.cityArray)

    def linearSearch(self, city, attribute):
        # search self.cityArray element by element for city based on the attribute; return city or "City not found"
        if attribute == "name":
            for c in self.cityArray:
                if c.cname == city:
                    return c
        elif attribute == "id":
            for c in self.cityArray:
                if c.cid == city:
                    return c
        return "City not found"

    def quickSort(self):
        # sort the city library based on the city name
        self.quickSortHelper(0, self.size - 1)
        self.isSorted = True

    def quickSortHelper(self, first, last):
        # if there is something to sort
        if first < last:
            splitpoint = self.partition(first, last)
            # perform the sort again with the new partitioned indices
            self.quickSortHelper(first, splitpoint - 1)
            self.quickSortHelper(splitpoint + 1, last)

    def partition(self, first, last):
        # pivot will be in the correct position of the sorted array; elements to the left are smaller, right are bigger
        pivotvalue = self.cityArray[first]
        leftmark = first + 1
        rightmark = last
        done = False
        while not done:
            # move leftmark to where cityArray[leftmark] > pivotvalue
            while self.cityArray[leftmark].cname <= pivotvalue.cname and leftmark <= rightmark:
                leftmark += 1
            # move rightmark to where cityArray[rightmark] < pivotvalue
            while self.cityArray[rightmark].cname >= pivotvalue.cname and rightmark >= leftmark:
                rightmark -= 1
            # no more sorting to left
            if rightmark < leftmark:
                done = True
            else:
                # swap cityArray[leftmark] with cityArray[rightmark]
                self.cityArray[leftmark], self.cityArray[rightmark] = self.cityArray[rightmark], self.cityArray[leftmark]
        # swap pivotvalue with cityArray[rightmark] (values left of pivot < pivot < values right of pivot)
        self.cityArray[first], self.cityArray[rightmark] = self.cityArray[rightmark], self.cityArray[first]
        # indicate where to split the list to do it again
        return rightmark

    def buildBST(self):
        # build a balanced BST of cities based on the city id
        for city in self.cityArray:
            # update the root after each call to account for balancing
            self.root = self.insert(self.root, city.cid, city)

    def insert(self, root, key, city):
        # place node in the correct place
        # if the root is None or the child is None
        if not root:
            return city
        # search for where to put the node/city
        elif key < root.cid:
            root.leftChild = self.insert(root.leftChild, key, city)
        else:
            root.rightChild = self.insert(root.rightChild, key, city)
        # calculate height and balance for previous node
        root.height = self.calculateHeight(root)
        balance = self.getBalance(root)
        # if the node is unbalanced, then see which case we have
        if balance > 1:
            # Left Right
            if key > root.leftChild.cid:
                root.leftChild = self.leftRotate(root.leftChild)
            # Right
            return self.rightRotate(root) # becomes root for next pass
        if balance < -1:
            # Right Left
            if key < root.rightChild.cid:
                root.rightChild = self.rightRotate(root.rightChild)
            # Left
            return self.leftRotate(root) # becomes root for next pass
        # no balancing needed
        return root

    def leftRotate(self, rotRoot):
        # rotate nodes
        newRoot = rotRoot.rightChild
        newRoot.leftChild, rotRoot.rightChild = rotRoot, newRoot.leftChild
        # calculate heights
        rotRoot.height = self.calculateHeight(rotRoot)
        newRoot.height = self.calculateHeight(newRoot)
        return newRoot # return to insert

    def rightRotate(self, rotRoot):
        # rotate
        newRoot = rotRoot.leftChild
        newRoot.rightChild, rotRoot.leftChild = rotRoot, newRoot.rightChild
        # calculate heights
        rotRoot.height = self.calculateHeight(rotRoot)
        newRoot.height = self.calculateHeight(newRoot)
        return newRoot # return to insert

    def getHeight(self, node):
        # remember; not None => True; not <some_class> => False; None => False
        if node:
            return node.height
        return 0 # node was None

    def getBalance(self, node):
        # remember; not None => True; not <some_class> => False; None => False
        if node:
            return self.getHeight(node.leftChild) - self.getHeight(node.rightChild)
        return 0 # node was None

    def calculateHeight(self, node):
        # use max to find the unbalanced height
        return 1 + max(self.getHeight(node.leftChild), self.getHeight(node.rightChild))

    def searchBST(self, cid):
        # search the BST based on a city id
        city = self._searchBST(cid, self.root)
        # if the city is not None then the city was found
        if city:
            return city
        return "City not found"

    def _searchBST(self, key, currentNode):
        if not currentNode:
            return None # city not found
        elif currentNode.key == key:
            return currentNode
        # move currentNode to the next node in the direction of the key node
        elif key < currentNode.key:
            return self._searchBST(key, currentNode.leftChild)
        else:
            return self._searchBST(key, currentNode.rightChild)
