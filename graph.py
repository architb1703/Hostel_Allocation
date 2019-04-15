#Top Trading Cycle Algorithm

from random import randint

#Class to implement Top Trading Cycle Algorithm
#Input: vertices-list of student names; initial-dictionary{student name: initial room number allocated};
# pref-dictionary{student: list of preference order}
class Graph():
    def __init__(self, vertices, initial, pref):
        #self.graph is the active dictionary which stores the student name along with list of room 
        # number initially allocated as well as the room prefences currently available
        self.graph=dict((name,[0,0]) for name in vertices)
        self.final={}       #Stores final room allocation data
        self.initial=initial
        self.pref=pref
        for name in self.graph.keys():
            self.graph[name][0]=self.initial[name]
            self.graph[name][1]=self.pref[name][0]
        self.display_info(vertices)
        self.find_cycle()
        print()
        print("Final allocation of rooms:", self.final)

    #Function to display the initial data passed
    def display_info(self, names):
        print("Students participating in this allocation:", names)
        print("Initial allocation of rooms:", self.initial)
        print("Preference list of students:", self.pref)
        print()

    #This function picks a key from self.graph and calls find fucntion with the key as parameter.
    # Then it calls ttc function to resolve the cycle found. This continues until self.graph is empty.  
    def find_cycle(self):
        while len(self.graph.keys())!=0:
            self.recur=[]   #Stores the list of all vertex encountered in a particular traversal
            graph_keys=list(self.graph.keys())
            vertice=self.find(graph_keys[0],graph_keys[0])
            self.ttc(vertice)

    #find function is a recursive fucntion.
    # It accepts a vertex of the graph as input and starting from this vertex travels along
    # the directed graph until it encounters a cycle. It then returns the vertex of the cycle 
    # encountered first in the traversal.
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
    
    #This function accepts the vertex of the cycle encountered and resolves the cycle. It adds students
    # and their final room to self.final and updates the number of students left self.graph.
    # Also calls update_pref(). 
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

    #This function is for updating the cuurent preference of the students left in the process by
    # finding highest preference of the student which has not yet been fianlly allocated.
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

#Function to provide initial random allocation of rooms to list of students given as input.
#Returns a dictionary of students and allocated rooms in form required by the Graph class.
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
