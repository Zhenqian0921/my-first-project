from input import process_data
from assemble import assembly_k
import numpy as np
import openpyxl


ID_node, ID_element, Information_element, BCs = process_data()
Stiffness_matrix = assembly_k(ID_node, ID_element, Information_element) 
Num_node = 23
    
def Solve_problem(Stiffness_matrix, ID_node, ID_element, Information_element, BCs, Num_node):
    # 记录非固定节点以及方向
    Record = []  # 记录非固定的节点
    for i in range(Num_node):
        if BCs[i,2] == 0:
            Record.append(2 * i)
        if BCs[i,3] == 0:
            Record.append(2 * i + 1)

    # 外载组成列向量
    External_load_sum = np.zeros(2 * Num_node)  # 外载矩阵组合成一起
    for i in range(2 * Num_node):
        if i % 2 == 0:
            External_load_sum[i] = BCs[i // 2,0]
        else:
            External_load_sum[i] = BCs[i // 2,1]

    # 筛选出非固定节点的对应刚度矩阵
    Free_External_load = np.zeros(len(Record))  # 筛选外载为零的列向量
    Free_stiffness = np.zeros((len(Record), len(Record)))  # 筛选出外载为零对应的刚度矩阵
    for i in range(len(Record)):
        Free_External_load[i] = External_load_sum[Record[i]]
        for j in range(len(Record)):
            Free_stiffness[i][j] = Stiffness_matrix[Record[i]][Record[j]]#

    # 求解出节点位移以及支反力
    Free_Displacement = np.linalg.solve(Free_stiffness, Free_External_load)  # 求解得出自由位移
    Displacement = np.zeros(2 * Num_node)  # 创建整体位移的列向量
    for i in range(len(Record)):  # 重新组装为整体
        Displacement[Record[i]] = Free_Displacement[i]
    Force = np.dot(Stiffness_matrix, Displacement)  # 得到各个节点所得到的支反力
    #print(Displacement, Force)
    return Displacement, Force
Displacement, Force = Solve_problem(Stiffness_matrix, ID_node, ID_element, Information_element, BCs, Num_node)#调用Solve_problem函数得到全局的位移和节点力（包括固定节点）
#Solve_problem(Stiffness_matrix, ID_node, ID_element, Information_element, BCs, Num_node)    
