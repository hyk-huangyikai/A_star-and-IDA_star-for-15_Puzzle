import sys
import math
import numpy as np
import copy
import time
import heapq

class PriorityQueue:
    #初始化
    def __init__(self):
        self.heap = []
        self.count = 0
    #入队，将结点插入队列，同时输入fn作为排序依据
    def push(self, item, priority):
        entry = (priority, self.count, item)
        heapq.heappush(self.heap, entry)
        self.count += 1
    #取出fn最小的结点
    def pop(self):
        (_, _, item) = heapq.heappop(self.heap)
        return item
    #判断是否为空
    def isEmpty(self):
        return len(self.heap) == 0
    #更新，将结点按fn进行堆排序
    def update(self, item, priority):

        for index, (p, c, i) in enumerate(self.heap):
            if i == item:
                if p <= priority:
                    break
                del self.heap[index]
                self.heap.append((priority, c, item))
                heapq.heapify(self.heap)
                break
        else:
            self.push(item, priority)

class Node():
    def __init__(self,state,parent,gn,hn,element = 0):
        self.state = state  #矩阵状态
        self.parent = parent #父结点
        self.gn = gn  #目前花费代价
        self.hn = hn #预估代价
        self.fn = gn + hn #估价值
        self.element = element #上次移动的元素

def A_star(start_node,dst_node,target,move):

    close_queue = [] #已访问的结点集合
    close_queue.append(start_node.state)

    open_queue = PriorityQueue() #优先队列初始化
    open_queue.push(start_node,0)  #插入根结点
    print(heuristic_manhadun(start_node.state,target))

    while open_queue:

        node = open_queue.pop() #出队，选fn最小的结点
        print(node.gn,node.fn)
        #如果是目标状态，返回当前结点
        if node.state == dst_node.state:
            return node

        for i in range(len(node.state)):
            for j in range(len(node.state[0])):
                if node.state[i][j] == 0:
                    move_x = i
                    move_y = j
                    break
        for movement in move:
            x = move_x + movement[0] #更新x
            y = move_y + movement[1] #更新y
            #越界探测
            if x >= 4 or x < 0 or y >= 4 or y < 0:
                continue
            #保证不走回头路
            if node.state[x][y] == node.element:
                continue
            new_state = copy.deepcopy(node.state) #深复制，避免影响上一个结点
            new_state[move_x][move_y] = new_state[x][y] #移动位置
            new_state[x][y] = 0 #更换0的位置
            element = new_state[move_x][move_y] #存储移动的元素数值
            gn = node.gn+1 #成本加1
            hn = heuristic_manhadun(new_state, target) #求估计代价
            new_node = Node(new_state,node,gn,hn,element) #创建新结点
            #如果新结点状态已经探测，则放弃该方向扩展
            if new_node.state in close_queue:
                continue
            #否则进行扩展，置为已经访问
            else:
                close_queue.append(node.state)
                open_queue.push(new_node,new_node.fn)

    return None

def heuristic_manhadun(state,target):
    current_array = state
    length_x = len(current_array)
    length_y = len(current_array[0])
    hn = 0
    for i in range(length_x):
        for j in range(length_y):
            if (current_array[i][j] != 0):
                end_x,end_y = target[current_array[i][j]]
                x_dis = abs(end_x - i)
                y_dis = abs(end_y - j)
                hn = hn + x_dis + y_dis

    return hn


def main() :
    start = time.clock()
    # file_name = "sample_input.txt"
    file_name = "input1.txt"
    with open (file_name,'r',encoding="utf-8") as file1:
        sample_list = file1.readlines()

    for i in range(len(sample_list)):
        tmp = sample_list[i].split()
        sample_list[i] = [int(x) for x in tmp]

    array_number = 1
    array_size = 4

    end_state = []
    number = 1
    for i in range(array_size):
        tmp = []
        for j in range(array_size):
            tmp.append(number)
            number += 1
        end_state.append(tmp)
    end_state[array_size-1][array_size-1] = 0
    # print(end_state)
    dst_node = Node(end_state,None,0,0)

    target = {}
    number = 1
    target[0] = (array_size-1,array_size-1)
    for i in range(array_size):
        for j in range(array_size):
            target[number] = (i,j)
            number += 1
    # print(target)

    move = [[1,0],[0,1],[-1,0],[0,-1]]

    for i in range(array_number):
        index = i*array_size
        digital_array = copy.deepcopy(sample_list[index:index+array_size])
        start_node = Node(digital_array,None,0,0)
        # print(digital_array)
        result = A_star(start_node,dst_node,target,move)
        if result != None:
            print("move step: ",result.gn)
            road = []
            while result:
                # array = np.array(result.state)
                # print(array)
                road.append(result.element)
                result = result.parent
            road = list(reversed(road))
            print(road)
    end = time.clock()
    print("run time : " ,str(end - start),' s')

if __name__ == "__main__":
    main()