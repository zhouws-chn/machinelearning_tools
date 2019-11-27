# coding:utf-8
import matplotlib.pyplot as plt
import time
import numpy as np
from math import *

# 根据已知的x,y坐标点来画图,出现绘制的图形后,程序会暂停在plt.show()函数中,关闭绘制的图像,程序将继续执行.
def plot2D():
    x1 = [1,2,3,4,5,6,7]
    y1 = [2.6,3.6,8.3,56,12.7,5.3,8.9]
    plt.plot(x1,y1,color='green',label='cab_1',linewidth=2) #画连线图 color:点的颜色 label:标签 linewidth:线宽
    #plt.scatter(x1,y1,color='green',label='cab_1') #画散点 color:点的颜色
    x2 = [1, 2, 3, 4, 5, 6, 7]
    y2 = [8.9,2.6, 3.6, 8.3, 56, 12.7, 5.3]
    plt.scatter(x2, y2, color='red', label='cab_2')  # 画散点 color:点的颜色 label:标签
    plt.legend() # 显示label标签
    plt.show()

# 动态显示数据,历史数据会被存储到列表中
def plot2d_dynamic():
    plt.ion()
    plt.figure(1)
    t=[0]
    t_now = 0
    m = [sin(t_now)]

    for i in range(2000):
        plt.clf() # 清空画布上的所有内容
        t_now = i*0.1
        t.append(t_now)
        m.append(sin(t_now))
        plt.plot(t,m,'-r')
        plt.pause(0.01)

# 动态显示数据,历史数据不会被存储
def plot2d_dynamic_nosave():
    plt.ion() #开启 interactive mode
    plt.figure(1)
    t=[0]
    t_now = 0
    m = [sin(t_now)]

    for i in range(2000):
        #plt.clf() # 清空画布上的所有内容
        t_now = i*0.1
        # 如果需要画线的话,需要把上次的点保存下来,然后传入两个点进行画线操作.
        #plt.plot(t_now,sin(t_now),'.',color='red')
        plt.scatter(t_now, sin(t_now), '.', color='red')
        plt.pause(0.1)

# 动态显示数据,历史数据不会被存储
def plot2d_dynamic_nosave2():
    plt.ion() #开启 interactive mode
    plt.figure(1)
    t = np.linspace(0,20,100)

    for i in range(2000):
        #plt.clf() # 清空画布上的所有内容
        y = np.sin(t*i/10.0)
        # 如果需要画线的话,需要把上次的点保存下来,然后传入两个点进行画线操作.
        plt.plot(t,y)
        #plt.scatter(t_now, sin(t_now), '.', color='red')
        plt.pause(1)



if __name__ == '__main__':
    print('draw before.')
    plot2d_dynamic_nosave()
    print('draw after.')