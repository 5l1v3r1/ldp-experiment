import numpy as np
from scipy.linalg import hadamard
import hashlib
import hmac
import re
import pandas as pd
import matplotlib.pyplot as plt 
import matplotlib.mlab as mlab 
import sys
'''
import pymysql
db = pymysql.connect("localhost","root","","chatroom")
cursor = db.cursor()
'''
k=2048
m=256
def sha512x64(s):
    s=s.encode("utf-8")
    shaval=""
    for i in range(0,int((k/64)*(3/2))):
        shaval+=hmac.new(str(i).encode("utf-8"),s,hashlib.sha512).hexdigest()
    return shaval
def mysha512(s):
    s=s.encode("utf-8")
    #print(s)
    shaval = hashlib.sha512(s).hexdigest()
    return shaval
def f(d,M,k,m,n):
    h=re.findall("...",sha512x64(d))
    h=[int(i,16)%m for i in h]

    result=0
    temp=0
    for l in range(0,k):
        temp+=M[l,h[l]]
    result=( (m/(m-1)) * ( (1/k) * temp -n/m ) )
    return result

def mape(y_true,y_pred):
    n = len(y_true)
    mape = sum (np.abs((y_true-y_pred)/y_true))/n*100
    return mape
def main():
    if(len(sys.argv)<2):
        exit()
    dataset=pd.read_csv(sys.argv[1])
    dataset=np.array(dataset)
    #print(dataset)
    ws=np.array(dataset)[:,0]
    js=np.array(dataset)[:,1]
    ls=np.array(dataset)[:,2]
    #print(ws,js,ls)
    epsilon=2
    c_epsilon=(np.exp(epsilon)+1)/(np.exp(epsilon)-1)
    #print("c:",c_epsilon)
    #num of hash 16


    xs=np.zeros(len(dataset))
    
    for i in range(len(dataset)):
        x=k*c_epsilon*ws[i]
        #print(np.array(x))
        xs[i]=x
    M=np.zeros(shape=(k,m))
    #print(xs)
    for i in range(0,len(dataset)):
        M[int(js[i]),ls[i]]=M[int(js[i]),ls[i]]+xs[i]
    hM=hadamard(m)
    M=M@hM.T


    histx=[]
    for i in range(1,76):
        emo="[em_"+str(i)+"]"
        histx.append(f(emo,M,k,m,len(dataset)))
    histx=np.array(histx)
    print("pinshu",np.sum(histx))
    #histx=histx-min(histx)
    #print(histx)
    originaldis=np.array([125, 139, 153, 169, 188, 207, 230, 253, 281, 311, 343, 379, 419, 463, 512, 567, 626, 691, 764, 845, 934, 1032, 1141, 1261, 1394, 1540, 1703, 1882, 2079, 2299, 2540, 2808, 3103, 3430, 3791, 4189, 4630, 5158, 4630, 4189, 3791, 3430, 3103, 2808, 2540, 2299, 2079, 1882, 1703, 1540, 1394, 1261, 1141, 1032, 934, 845, 764, 691, 626, 567, 512, 463, 419, 379, 343, 311, 281, 253, 230, 207, 188, 169, 153, 139, 125])
    # 设置图形的显示风格
   # print("方差:",np.sum((histx-originaldis)**2)/75)
    wucha=mape(originaldis,histx)
    print("MAPE=",wucha)
    plt.style.use( 'ggplot')

    # 绘图：乘客年龄的频数直方图
    
    x=np.array(range(1,76))
    plt.bar(x,originaldis/sum(originaldis),width=0.5,alpha=0.9,edgecolor="white",lw=1)
    plt.bar(x+0.5,histx/np.sum(histx),width=0.5,alpha=0.9,edgecolor="white",lw=1)
    
    
    plt.tick_params(top= 'off', right= 'off')

    # 显示图例

    plt.legend()

    # 显示图形

    plt.show() 
    '''
    sql = "select * from chat"
    cursor.execute(sql)
    dataset= cursor.fetchall()
    epsilon=4
    c_epsilon=(np.exp(epsilon/2)+1)/(np.exp(epsilon/2)-1)
    print("c:",c_epsilon)
    #num of hash 16

    xs=np.zeros(shape=(len(dataset),m))
    
    for i in range(len(dataset)):
        x=k*((c_epsilon/2)*np.array(dataset[i][0].split(",")).astype(int) + 1/2*1)
        #print(np.array(x))
        xs[i]=x
    M=np.zeros(shape=(k,m))
    #print(xs)
    for i in range(0,len(dataset)):
        for l in range(0,m):
            M[int(dataset[i][1]),l]=M[int(dataset[i][1]),l]+xs[i][l]
    for i in range(1,76):
        emo="[em_"+str(i)+"]"
        print(emo,f(emo,M,k,m,len(dataset)))
    '''
if __name__ == "__main__":
    main()
