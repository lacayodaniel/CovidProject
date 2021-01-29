class City:
    def __init__(self, cid, cname, cstate, pop, cases, left=None, right=None):
        self.cid = cid               # city id
        self.cname = cname           # city name
        self.cstate = cstate         # state name relating to city
        self.pop = pop               # population of city
        self.cases = cases           # array that contains the numbers of confirmed covid cases
        self.leftChild = left        # used for the AVL BST to point to a city with a smaller cid
        self.rightChild = right      # used for the AVL BST to point to a city with a larger cid
        self.height = 1              # represents how many "levels" are beneath itself
                                     # (including itself; top is root, bottom is last added)
        self.key = cid

    def __str__(self):
        # print out the city id, name, state, population, and latest number of confirmed cases
        return "cid: {}; cname: {}; cstate: {}; cases:{}".format(self.cid, self.cname, self.cstate, self.cases[-1])
