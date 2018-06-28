 
import numpy as np  
import matplotlib.pyplot as plt


def graph_linear(raw_range=(0,1023),constants=(1,0)):
    '''obtinee la grafica de una ecuacion lineal con los datos de entrada y sus constantes:
    Linear: Ax+B
    '''
    
    equation ='x*{constA}+{constB}'.format(constA=str(constants[0]),
                                           constB=str(constants[1]))
    x = np.array(range(raw_range[0],raw_range[1]))
    y = eval(equation)
    
    return x,y
    
