#!/usr/bin/python3

#Import some useful libraries
from math import sqrt #Import of the sqrt function
import time
import sys
import queue as q
import resource


class State:
    def __init__(self, board, parent="", depth=0):
        self.board=board
        self.parent=parent
        self.depth=depth

    def len_board(self):
        return len(self.board)

    def size_board(self):
        return int(sqrt(self.len_board()))

    def pos_0(self):
        return self.board.index(0)

    def up(self):
        return self.pos_0()-self.size_board()

    def down(self):
        return self.pos_0()+self.size_board()

    def left(self):
        return self.pos_0()-1

    def right(self):
        return self.pos_0()+1

    def childs(self,reverse=0):
        a,b,c,d=None,None,None,None
        #Up
        if self.pos_0() >= self.size_board():
            board_l = list(self.board)
            board_l[self.pos_0()], board_l[self.up()] = board_l[self.up()], board_l[self.pos_0()]
            a=State(tuple(board_l), self, self.depth+1)
        #Down
        if self.pos_0()< self.len_board() - self.size_board():
            board_l=list(self.board)
            board_l[self.pos_0()], board_l[self.down()] = board_l[self.down()], board_l[self.pos_0()]
            b=State(tuple(board_l),self,self.depth+1)   
        #Left
        if self.pos_0() % self.size_board() != 0:
            board_l=list(self.board)
            board_l[self.pos_0()], board_l[self.left()] = board_l[self.left()], board_l[self.pos_0()]
            c=State(tuple(board_l),self,self.depth+1)     
        #Right
        if self.pos_0() % self.size_board() != self.size_board()-1:
            board_l=list(self.board)
            board_l[self.pos_0()], board_l[self.right()] = board_l[self.right()], board_l[self.pos_0()]
            d=State(tuple(board_l),self,self.depth+1)
        if reverse==0:
            return tuple(i for i in (a,b,c,d) if i!=None)
        else:
            return tuple(i for i in (d,c,b,a) if i!=None)

def manhat(board):
    max_man=0
    size=int(sqrt(len(board)))
    for i in board:
        if i!=0:
            max_man+=abs(board.index(i)%size-i%size)+abs(board.index(i)//size-i//size)
    return max_man

def miniboard(x):
    return x.board

def bfs(*board):
    start_time=time.time()
    goal_board=tuple(sorted(list(board)))   #Initialization of the goal board
    max_frontier=0
    max_depth=0
    frontier=[State(board)]
    explored_state=set()
    explored=set()
    explored.add(board)

    while frontier!=[]:
        #------------------------------
        #1.Remove a node from the fringe
        #------------------------------
        dequeue=frontier[0]
        frontier.remove(dequeue)
        explored_state.add(dequeue)

        #------------------------------
        #2.Check Goal reached
        #------------------------------
        if dequeue.board==goal_board:
            break

        #------------------------------
        #3.Adding elements to the fringe
        #------------------------------
        for i in dequeue.childs():
            if i.board not in explored:
                frontier.append(i)
                explored.add(i.board)

        #------------------------------
        #4.Update of maxs
        #------------------------------
        max_frontier=max(max_frontier,len(frontier))
        if frontier !=[]:
            max_depth=max(max_depth,frontier[-1].depth)
                
    #------------------------------
    #5.Writing in a txt file
    #------------------------------ 

    #Pathfinding
    path=[]
    c_st=dequeue
    while c_st.depth != 0:
        if c_st.pos_0() == c_st.parent.up():
            path.append('Up')
        elif c_st.pos_0() == c_st.parent.down():
            path.append('Down')
        elif c_st.pos_0() == c_st.parent.left():
            path.append('Left')
        else :
            path.append('Right')
        c_st=c_st.parent
    path=path[::-1]
        
    file(path, dequeue.depth, len(explored)-len(frontier)-1, len(frontier), max_frontier, max_depth, time.time()-start_time, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000)
    return


def dfs(*board):
    start_time=time.time()
    goal_board=tuple(sorted(list(board)))   #Initialization of the goal board
    max_frontier=0
    max_depth=0
    frontier=[State(board, depth=0)]
    explored_state=set()
    explored=set()
    explored.add(board)

    while frontier!=[]:
        #------------------------------
        #1.Remove a node from the fringe
        #------------------------------
        dequeue=frontier.pop()
        explored_state.add(dequeue)

        #------------------------------
        #2.Check Goal reached
        #------------------------------
        if dequeue.board==goal_board:
            break

        #------------------------------
        #3.Adding elements to the fringe
        #------------------------------
        for i in dequeue.childs(1):
            if i.board not in explored:
                frontier.append(i)
                explored.add(i.board)

        #------------------------------
        #4.Update of maxs
        #------------------------------
        max_frontier=max(max_frontier,len(frontier))
        if frontier !=[]:
            max_depth=max(max_depth,frontier[-1].depth)

    #------------------------------
    #5.Writing in a txt file
    #------------------------------ 

    #Pathfinding
    path=[]
    c_st=dequeue
    while c_st.depth != 0:
        if c_st.pos_0() == c_st.parent.up():
            path.append('Up')
        elif c_st.pos_0() == c_st.parent.down():
            path.append('Down')
        elif c_st.pos_0() == c_st.parent.left():
            path.append('Left')
        else :
            path.append('Right')
        c_st=c_st.parent
    path=path[::-1]

    file(path, dequeue.depth, len(explored)-len(frontier)-1, len(frontier), max_frontier, max_depth, time.time()-start_time, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000)
    return


def ast(*board):
    start_time=time.time()
    goal_board=tuple(sorted(list(board)))   #Initialization of the goal board
    max_frontier=0
    max_depth=0
    frontier=q.PriorityQueue()
    init_state=State(board, depth=0)
    prior=0
    frontier.put((manhat(board),prior,init_state))
    explored_state=set()
    explored=set()
    explored.add(board)
    

    while frontier.qsize()!=0:
        #------------------------------
        #1.Remove a node from the fringe
        #------------------------------
        a=frontier.get()
        current=a[2]
        explored_state.add(current)

        #------------------------------
        #2.Check Goal reached
        #------------------------------
        if current.board==goal_board:
            break

        #------------------------------
        #3.Adding elements to the fringe
        #------------------------------
        for i in current.childs():
            if i.board not in explored:
                prior+=1
                frontier.put((i.depth+manhat(i.board),prior,i))
                explored.add(i.board)
                max_depth=max(max_depth,i.depth)
        #------------------------------
        #4.Update of maxs
        #------------------------------
        max_frontier=max(max_frontier,frontier.qsize())

    #------------------------------
    #5.Writing in a txt file
    #------------------------------ 

    #Pathfinding
    path=[]
    c_st=current
    while c_st.depth != 0:
        if c_st.pos_0() == c_st.parent.up():
            path.append('Up')
        elif c_st.pos_0() == c_st.parent.down():
            path.append('Down')
        elif c_st.pos_0() == c_st.parent.left():
            path.append('Left')
        else :
            path.append('Right')
        c_st=c_st.parent
    path=path[::-1]

    file(path, current.depth, len(explored)-frontier.qsize()-1, frontier.qsize(), max_frontier, max_depth, time.time()-start_time, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000)
    return

def ida(*board):
    start_time=time.time()
    goal_board=tuple(sorted(list(board)))   #Initialization of the goal board
    max_frontier=0
    max_depth=0
    it_limit=manhat(board)
    nodes_explored=0

    while 1:
        frontier=q.PriorityQueue()
        init_state=State(board, depth=0)
        prior=0
        frontier.put((manhat(board),prior,init_state))
        explored_state=set()
        explored=set()
        explored.add(board)

        while frontier.qsize()!=0:
            #------------------------------
            #1.Remove a node from the fringe
            #------------------------------
            a=frontier.get()
            current=a[2]
            explored_state.add(current)
            mini=10**9

            #------------------------------
            #2.Check Goal reached
            #------------------------------
            if current.board==goal_board:
                break

            #------------------------------
            #3.Adding elements to the fringe
            #------------------------------
            for i in current.childs(1):
                if i.board not in explored:
                    func=i.depth+manhat(i.board)
                    if func <=it_limit:
                        prior+=1
                        frontier.put((func,prior,i))
                        explored.add(i.board)
                        max_depth=max(max_depth,i.depth)
                    else:
                        mini=min(func,mini)

            #------------------------------
            #4.Update of maxs
            #------------------------------
            max_frontier=max(max_frontier,frontier.qsize())
        nodes_explored+=len(explored)-frontier.qsize()-1
        if current.board==goal_board:
            break
        it_limit=mini
        

    #------------------------------
    #5.Writing in a txt file
    #------------------------------ 

    #Pathfinding
    path=[]
    c_st=current
    while c_st.depth != 0:
        if c_st.pos_0() == c_st.parent.up():
            path.append('Up')
        elif c_st.pos_0() == c_st.parent.down():
            path.append('Down')
        elif c_st.pos_0() == c_st.parent.left():
            path.append('Left')
        else :
            path.append('Right')
        c_st=c_st.parent
    path=path[::-1]
        
    file(path, current.depth, nodes_explored, frontier.qsize(), max_frontier, max_depth, time.time()-start_time, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000)
    return

def file(path_f ,depth_f ,nodes_f ,fringe_f ,m_fringe_f, m_depth_f, time_f, ram_f):
    F=open("output.txt","w")
    F.write("path_to_goal: {}\n".format(path_f))
    F.write("cost_of_path: {}\n".format(depth_f))
    F.write("nodes_expanded: {}\n".format(nodes_f))
    F.write("fringe_size: {}\n".format(fringe_f))
    F.write("max_fringe_size: {}\n".format(m_fringe_f))
    F.write("search_depth: {}\n".format(depth_f))
    F.write("max_search_depth: {}\n".format(m_depth_f))
    F.write("running_time: %.8f\n" %time_f)
    F.write("max_ram_usage: {}\n".format(ram_f))
    F.close()

#script encoding
if __name__ == '__main__':
    if sys.argv[1]=='bfs':
        bfs(*eval(sys.argv[2]))
    if sys.argv[1]=='dfs':
        dfs(*eval(sys.argv[2]))
    if sys.argv[1]=='ast':
        ast(*eval(sys.argv[2]))
    if sys.argv[1]=='ida':
        ida(*eval(sys.argv[2]))

