from input import process_data
from assemble import assembly_k
from displacement import Solve_problem
import numpy as np
import openpyxl

ID_node, ID_element,  Information_element, BCs = process_data()
Stiffness_matrix = assembly_k(ID_node,ID_element,Information_element)
Num_node = 23
Displacement, _ = Solve_problem(Stiffness_matrix, ID_node, ID_element, Information_element, BCs, Num_node)

#ID_element 单元的节点连接关系
#Information_element 两个方向余弦，长度和弹性模量
def Post_treatment(Displacement, ID_element, Information_element):
    Num_element = ID_element.shape[0]
    Strain = []  # 初始化单元局部应变
    Stress = np.zeros(Num_element)  # 初始化单元应力

    for i in range(Num_element):
        u = np.dot( # 矩阵乘法
            np.array([[Information_element[i, 0], Information_element[i, 1], 0, 0],
                      [0, 0, Information_element[i, 0], Information_element[i, 1]]]), # 转换矩阵
            np.array([Displacement[int(2 * ID_element[i, 0] - 2)], Displacement[int(2 * ID_element[i, 0] - 1)],
                      Displacement[int(2 * ID_element[i, 1] - 2)], Displacement[int(2 * ID_element[i, 1] - 1)]])) # 全局位移转为局部位移
        '''print(Displacement[int(2 * ID_element[i, 0] - 2)], Displacement[int(2 * ID_element[i, 0] - 1)],
                      Displacement[int(2 * ID_element[i, 1] - 2)], Displacement[int(2 * ID_element[i, 1] - 1)])'''
        u = u.flatten()

        local_strain = (u[1] - u[0]) / Information_element[i, 2]
        Strain.append(local_strain)

        Stress[i] = ID_element[i, 2] * local_strain

    return Stress, Strain
    #print(Strain,Stress)
#Stress,Strain = Post_treatment(Displacement, ID_element, Information_element)
#Post_treatment(Displacement, ID_element, Information_element)
