import threading
import numpy as np
import math as m
import time
import matplotlib.pyplot as plt

class plant:
    def __init__(self):
        self.bias=0.01
        self.yaw=0
        self.vyaw=0
        self.time=0
        self.bias_mu=0
        self.bias_sig=0.003
        self.flag=1

    def update(self,dt):
        self.yaw=self.yaw+self.vyaw*dt
        #self.bias=self.bias+np.random.normal(self.bias_mu, self.bias_sig, 1)[0]# comment this line to make the bias be constant(remember to give it a value in __init__)
        self.time+=dt

    def get_rate(self):
        return [(self.vyaw+self.bias),self.time]

    def get_orient(self):
        return [self.yaw,self.time]

    def get_real(self):
        return np.array([self.yaw,self.bias,self.time])

    def set_vyaw(self,vyaw):
        self.vyaw=vyaw

    def routine(self,per):
        while(self.flag):
            #self.set_vyaw(0.5*m.cos(0.5*self.time+0.3))# comment this line to make vyaw constant
            self.set_vyaw(0.1)# uncomment this line to make vyaw constant
            self.update(per)
            time.sleep(0.00001)

    def stop(self):
        self.flag=0

class observer:
    def __init__(self,newL):
        self.x=np.zeros((2,1))
        
        self.A=np.eye(2)

        self.B=np.array([[0.],[0.]])
        self.C=np.array([[1.,0.]])
        self.L=newL

        self.lastT=0

    def update(self,yaw,vyaw,t):
        dt=t-self.lastT
        self.A[0,1]=-dt
        self.B[0,0]=dt
        self.x=self.A.dot(self.x)+self.B*vyaw
        self.x=self.x+self.L.dot(np.array([[yaw]])-self.C.dot(self.x))
        self.lastT=t

        result=np.zeros((3,1))
        result[0:2,:]=self.x
        result[2,:]=t
        return result

def run():
    boat=plant()
    L=np.array([[1.9],[-1.5]])
    sensor=observer(L)
    t = threading.Thread(target = boat.routine, args=(0.001,))
    t.start()

    n=500
    real_array=np.zeros((n,3))
    esti_array=np.zeros((n,3))
    lastT=0;
    i=0
    while(i<n):
        time=boat.get_orient()[1]
        if((time-lastT)>0.01):
            yaw=boat.get_orient()[0]
            vyaw=boat.get_rate()[0]
            real_array[i,:]=boat.get_real()
            esti_array[i,:]=sensor.update(yaw,vyaw,time)[:,0]
            i+=1
            lastT=time

    boat.stop()

    plt.title("bias vs time") # title
    plt.ylabel("bias") # y label
    plt.xlabel("time") # x label
    plt.plot(real_array[:,2],real_array[:,1],color=(255/255,100/255,100/255))
    plt.plot(esti_array[:,2],esti_array[:,1],'--',color=(100/255,100/255,255/255))
    plt.show()
    
    plt.title("yaw vs time") # title
    plt.ylabel("yaw") # y label
    plt.xlabel("time") # x label
    plt.plot(real_array[:,2],real_array[:,0],color=(255/255,100/255,100/255))
    plt.plot(esti_array[:,2],esti_array[:,0],'--',color=(100/255,100/255,255/255))
    plt.show()

    #print(real_array)
    #print(esti_array)

if __name__ == '__main__':
    run()
