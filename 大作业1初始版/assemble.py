from input import process_data
import numpy as np

ID_node,ID_element,Information_element,_ = process_data()

def assembly_k(ID_node,ID_element,Information_element):
# 创建全局刚度矩阵
    num_nodes = 23
    K_global = np.zeros((2 * num_nodes, 2 * num_nodes))
    # 循环装配局部刚度矩阵到全局刚度矩阵
    for i in range(43):
        c = Information_element[i,0]
        s = Information_element[i,1]
        k_local = ( ID_element[i,2]* ID_element[i,3] / Information_element[i,2]) * np.array([[c**2, c*s, -c**2, -c*s],
                                                                                             [c*s, s**2, -c*s, -s**2],
                                                                                             [-c**2, -c*s, c**2, c*s],
                                                                                             [-c*s, -s**2, c*s, s**2]])
        
        dofs = [2 * ID_element[i,0] -2, 2 * ID_element[i,0] - 1 , 2 * ID_element[i,1] -2, 2 * ID_element[i,1] - 1]
        #print(dofs)
        for j in range(4):
            for k in range(4):
                K_global[int(dofs[j]), int(dofs[k])] += k_local[j, k]
                #print(f"dofs[j]: {dofs[j]}, dofs[k]: {dofs[k]}")

    #print(K_global)
    return K_global
assembly_k(ID_node,ID_element,Information_element)