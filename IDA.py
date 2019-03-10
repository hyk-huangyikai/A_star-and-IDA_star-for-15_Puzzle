import sys
import math
import numpy as np
import copy
import time
import heapq


class Node():
    def __init__(self,state,parent,gn,hn,element = 0):
        self.state = state
        self.parent = parent
        self.gn = gn
        self.hn = hn
        self.fn = gn*1+ hn
        self.element = element


def choose_successor(node,target,move):
    for i in range(len(node.state)):
        for j in range(len(node.state[0])):
            if node.state[i][j] == 0:
                move_x = i
                move_y = j
                break
    success_list = []
    for movement in move:
        x = move_x + movement[0] #更新x
        y = move_y + movement[1] #更新y
        #判断是否越界
        if x >= 4 or x < 0 or y >= 4 or y < 0:
            continue
        #判断是否走回头路
        if node.state[x][y] == node.element:
            continue
        new_state = copy.deepcopy(node.state) #深复制
        new_state[move_x][move_y] = new_state[x][y] #移动元素
        new_state[x][y] = 0 #移动空格
        element = new_state[move_x][move_y] #记录移动的元素
        gn = node.gn+1 #改变实际代价
        hn = heuristic_manhadun(new_state, target) #求估计代价
        # hn = heuristic_chebyshev_distance(new_state,target)
        new_node = Node(new_state,node,gn,hn,element) #创建新结点
        success_list.append(new_node) #加入队列
    #对扩展的3个方向进行选择，按照fn从小到大
    return sorted(success_list,key = lambda x : x.fn)

def A_DFS(open_queue,g,bound,close_queue,target,move,dst_node):

    node = open_queue[-1] #取最后入队的一个结点进行扩展
    print(node.gn,node.fn)
    if node.state == dst_node.state: #如果到达目标状态，返回
        return -2

    min_limit = 10000 #找出最小的估价函数值
    #按照fn从小到达选择要扩展的方向
    for succ in choose_successor(node,target,move):
        new_node = succ
        isvisit = 0
        #判断结点是否在开启队列中
        for node1 in open_queue:
            if new_node.state == node1.state:
                isvisit = 1
                break
        if isvisit == 1:
            continue
        else:
            #判断结点是否在关闭队列中
            if new_node.state in close_queue:
                continue
            #如果新结点的fn大于阈值，停止扩展，返回
            if new_node.fn > bound:
                return new_node.fn
            #添加结点到关闭队列
            close_queue.append(new_node.state)
            #添加结点到开启队列
            open_queue.append(new_node)
            #递归调用A_DFS函数
            result = A_DFS(open_queue,g+1,bound,close_queue,target,move,dst_node)
            #如果找到结果，直接返回-2
            if result == -2:
                return result
            #否则比较当前的估价函数值，得出最小的更新到min_limit
            elif result < min_limit:
                min_limit = result
            open_queue.pop(-1) #出队，恢复
            close_queue.pop(-1) #出队，恢复

    return min_limit #返回最小的估价函数值

def IDA(start_node,dst_node,target,move):
    bound = heuristic_manhadun(start_node.state,target) #以初始点到终点的估价函数值为阈值
    open_queue = [] #开启列表
    open_queue.append(start_node) #初始点入队
    while True:
        print(bound)
        close_queue = [] #关闭列表
        close_queue.append(start_node.state) #初始点置为已经访问
        #将阈值作为探索的深度，调用以DFS为基础的A*算法函数
        result = A_DFS(open_queue,0,bound,close_queue,target,move,dst_node)
        #结果等于-2，则找到正确结果
        if result == -2:
            return open_queue
        #超过一定深度，不再探索
        if result > 100:
            return None
        #将返回的估计函数最小值作为下一次迭代的阈值
        bound = result
    return None

#计算曼哈顿距离
def heuristic_manhadun(state,target):
    current_array = state  #矩阵状态
    length_x = len(current_array)
    length_y = len(current_array[0]) #计算矩阵的size
    hn = 0
    for i in range(length_x):
        for j in range(length_y):
            if (current_array[i][j] != 0): #排除0的影响，保证可采纳性
                end_x,end_y = target[current_array[i][j]]
                x_dis = abs(end_x - i)
                y_dis = abs(end_y - j)
                hn = hn + x_dis + y_dis  #加上横坐标和纵坐标差的绝对值
                # print(x_dis+y_dis,current_array[i][j],target[current_array[i][j]],i,j)
    return hn

#计算切比雪夫距离
def heuristic_chebyshev_distance(state,target):
    current_array = state
    length_x = len(current_array) #计算矩阵大小的size
    length_y = len(current_array[0])
    hn = 0
    for i in range(length_x):  #遍历计算每个元素
        for j in range(length_y):
            end_x, end_y = target[current_array[i][j]]  #寻找元素目标位置
            x_dis = abs(end_x - i) #横坐标差绝对值
            y_dis = abs(end_y - j) #纵坐标差绝对值
            hn = hn + max(x_dis, y_dis) #取横、纵坐标差绝对值的最大值相加

    return hn  #评估值

#计算元素正确位置个数
def heuristic_element_num(state,target):
    current_array = state  #当前十五数码状态
    length_x = len(current_array) #矩阵的size
    length_y = len(current_array[0])
    hn = 0
    for i in range(length_x): #遍历每个元素，统计
        for j in range(length_y):
            end_x, end_y = target[current_array[i][j]] #得到元素的目标坐标
            if end_x != i or end_y != j: #判断元素是否到达目标位置，如果不是，加1
                hn += 1

    return hn #返回元素正确到达位置个数


def main() :
    start = time.clock()
    # file_name = "sample_input.txt"
    file_name = "input6.txt"
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

    for i in range(array_size):
        for j in range(array_size):
            target[number] = (i,j)
            number += 1
    target[0] = (array_size - 1, array_size - 1)
    # print(target)

    move = [[1,0],[0,1],[-1,0],[0,-1]]

    for i in range(array_number):
        index = i*array_size
        digital_array = copy.deepcopy(sample_list[index:index+array_size])
        start_node = Node(digital_array,None,0,0)
        # print(digital_array)
        result = IDA(start_node,dst_node,target,move)
        if result != None:
            print("move step: ",result[-1].gn)
            road = []
            for node in result:
                # array = np.array(node.state)
                # print(array)
                # print(node.gn)
                road.append(node.element)

            print(road)
            # print(len(road))


    end = time.clock()
    print("run time : " ,str(end - start),' s')

if __name__ == "__main__":
    main()