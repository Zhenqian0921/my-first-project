import numpy as np
import matplotlib.pyplot as plt
from displacement import Solve_problem
from input import process_data
from assemble import assembly_k

ID_node, ID_element, Information_element, BCs = process_data()
Stiffness_matrix = assembly_k(ID_node,ID_element,Information_element)
Num_node = 23
Displacement, _ = Solve_problem(Stiffness_matrix, ID_node, ID_element, Information_element, BCs, Num_node)
def output(Displacement,ID_node,ID_element):
# 计算变形后的节点坐标
    #deformed_data = ID_node + Displacement  # 直接相加，只包括 x 和 y 方向上的位移
    deformed_data = ID_node + Displacement.reshape(ID_node.shape)
    #print(deformed_data)
    # 绘制初始时的桁架图案（蓝色）
    plt.figure(figsize=(8, 4))
    plt.scatter(ID_node[:, 0], ID_node[:, 1], marker='o', color='blue', label='初始节点')
    for i in range(len(ID_node)):
        plt.text(ID_node[i, 0], ID_node[i, 1], f'节点 {i}', fontsize=12, ha='right', va='bottom')

    # 绘制桁架连接线
    for i in range(len(ID_element) ):
        node1 = (ID_element[i,0]) - 1
        node2 = (ID_element[i,1]) - 1
        #print(node1,node2)
        plt.plot([ID_node[int(node1), 0], ID_node[int(node2), 0]],
                 [ID_node[int(node1), 1], ID_node[int(node2), 1]], 'b-')
    plt.title('初始时的桁架图案')
    plt.xlabel('X坐标')
    plt.ylabel('Y坐标')
    plt.grid(True)

    # 绘制变形后的桁架图案（红色）
    plt.figure(figsize=(8, 4))
    plt.scatter(deformed_data[:, 0], deformed_data[:, 1], marker='x', color='red', label='变形节点')
    for i in range(len(deformed_data)):
        plt.text(deformed_data[i, 0], deformed_data[i, 1], f'节点 {i}', fontsize=14, ha='right', va='bottom')

    # 绘制桁架连接线
    for i in range(len(ID_element) ):
        deformed_node1 = (ID_element[i,0]) - 1
        deformed_node2 = (ID_element[i,1]) - 1
        #print(deformed_node1,deformed_node2)
        plt.plot([deformed_data[int(deformed_node1), 0], deformed_data[int(deformed_node2), 0]],
                 [deformed_data[int(deformed_node1), 1], deformed_data[int(deformed_node2), 1]], 'r-')
    plt.title('变形后的桁架图案')
    plt.xlabel('X坐标')
    plt.ylabel('Y坐标')
    plt.grid(True)

    plt.show()
output(Displacement,ID_node,ID_element)