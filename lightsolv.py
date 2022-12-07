#Light puzzle
import numpy as np
import copy

level = [[1,1,0,1],[1,1,1,1],[0,1,1,1],[1,1,1,1]]

class Node():
    def __init__(self,lvl,parent):
        self.lvl = lvl
        self.parent = parent

class Solver():
    def __init__(self,lvl):
        self.lvl = Node(np.array(lvl,dtype=np.uint8),None)
        self.actions = [(a,b) for a in [0,1,2,3] for b in [0,1,2,3]]

    def action(self,node,m,n):
        #m = row
        #n = col
        curr = np.copy(node.lvl)
        curr[m,:] = curr[m,:] ^ 1
        curr[:,n] = curr[:,n] ^ 1
        curr[m,n] = curr[m,n] ^ 1

        new = Node(curr,node)
        return new
        

    def goaltest(self,node):
        return node.lvl.all()

    def map2bin(self,node):
        x = node.lvl
        tmp = x.flatten()
        return (tmp.dot(1 << np.arange(tmp.shape[0] - 1, -1, -1)),node.parent)

    def bin2map(self,b):
        tmp = np.array([int(x) for x in "{0:016b}".format(b[0])])
        new = Node(np.reshape(np.copy(tmp),(4,4)),b[1])
        return new
        
        

    def bfs(self,mlevel):
        node = copy.deepcopy(self.lvl)
        clevel = 0
        if self.goaltest(node):
            return self.path
        frontier = [self.map2bin(node)]
        frontiern = [self.map2bin(node)[0]]
        explored = []
        exploredn = []
        while clevel < mlevel:
            if len(explored) % 100 == 0:
                print(len(explored))
            if len(frontier) == 0:
                return False
            n = self.bin2map(frontier.pop(0))
            explored.append(self.map2bin(copy.deepcopy(n)))
            exploredn.append(self.map2bin(copy.deepcopy(n))[0])
            for act in self.actions:
                child = self.map2bin(self.action(n,act[0],act[1]))
                if child[0] not in exploredn and child[0] not in frontiern:
                    if self.goaltest(self.bin2map(child)):
                        return self.bin2map(child)
                    frontier.append(child)
                    frontiern.append(child[0])

def path(n):
    p = n.parent
    print(n.lvl)
    while p != None:
        print(p.lvl)
        n = p
        p = n.parent
        

s = Solver(level)
path(s.bfs(1000))
