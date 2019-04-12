from random import randint

class Graph():
    def __init__(self, vertices, initial, pref):
        self.graph=dict((name,[0,0]) for name in vertices)
        self.final={}
        self.initial=initial
        self.pref=pref
        for name in self.graph.keys():
            self.graph[name][0]=self.initial[name]
            self.graph[name][1]=self.pref[name][0]
        self.display_info(vertices)
        self.find_cycle()
        print()
        print("Final allocation of rooms:", self.final)

    def display_info(self, names):
        print("Students participating in this allocation:", names)
        print("Initial allocation of rooms:", self.initial)
        print("Preference list of students:", self.pref)
        print()

    def find_cycle(self):
        self.recur=[]
        while len(self.recur)!=len(self.graph.keys()):
            graph_keys=list(self.graph.keys())
            for i in graph_keys:
                if i not in self.final.keys():
                    vertice=self.find(i,i)
                    self.ttc(vertice)
                    break

    def find(self, vertex, start, flag=1):
        if (vertex in self.recur):
            return vertex
        else:
            print(vertex, "has room", self.graph[vertex][0], "wants room", self.graph[vertex][1])
            self.recur.append(vertex)
            for v in self.graph.keys():
                if self.graph[vertex][1]==self.graph[v][0]:
                    point=self.find(v, start)
                    if(point):
                        return point
    
    def ttc(self, start):
        num=self.recur.index(start)
        temp=self.graph[start][0]
        for i in range(num,len(self.recur)-1):
            self.final[self.recur[i]]=self.graph[self.recur[i+1]][0]
            print(self.recur[i], "gets room", self.final[self.recur[i]])
            self.graph.pop(self.recur[i])
        self.final[self.recur[-1]]=temp
        print(self.recur[-1], "gets room", self.final[self.recur[-1]])
        self.graph.pop(self.recur[-1])
        self.recur=[]
        self.update_pref()
        self.find_cycle()

    def update_pref(self):
        val_list=[]
        for k in self.graph.values():   
            val_list.append(k[0])
        for i in self.graph.keys():
            for j in self.pref[i]:
                if j in val_list:
                    self.graph[i][1]=j
                    break
        print("Preferences updated")

def randomroom(vertices):
    rooms=[1,1,1,1,1,1,1,2,2]
    initial={}
    for i in vertices:
        while True:
            roomnum=randint(1,9)
            if rooms[roomnum-1]!=0:
                initial[i]=roomnum
                rooms[roomnum-1]-=1
                break
    return initial