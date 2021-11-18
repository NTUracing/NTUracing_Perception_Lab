import threading
import numpy as np
import math as m
import time
class plant:
    def __init__(self):
        self.bias=0
        self.yaw=0
        self.vyaw=0
        self.time=0
        self.bias_mu=0
        self.bias_sig=0.003
        self.flag=1

    def update(self,dt):
        self.yaw=self.yaw+self.vyaw*dt
        self.bias=self.bias+np.random.normal(self.bias_mu, self.bias_sig, 1)[0]
        self.time+=dt
        #print(dt)

    def get_rate(self):
        return [(self.vyaw+self.bias),self.time]

    def get_orient(self):
        return [self.yaw,self.time]

    def get_real(self):
        return np.array([self.yaw,self.vyaw,self.bias,self.time])

    def set_vyaw(self,vyaw):
        self.vyaw=vyaw

    def routine(self,per):
        while(self.flag):
            #self.set_vyaw(0.5*m.cos(0.5*self.time+0.3))
            self.set_vyaw(0.1)
            self.update(per)
            time.sleep(0.0001)

    def stop(self):
        self.flag=0

class observer:
    def __init__(self,newL):
        self.x=np.zeros((3,1))
        
        self.A=np.zeros((3,3))
        self.A[0,0]=1
        self.A[0,1]=0
        self.A[1,2]=-1
        self.A[2,2]=1

        self.B=np.array([[0],[1],[0]])
        self.C=np.array([1,0,0])
        self.L=newL

        self.lastT=0

    def update(self,yaw,vyaw,t):
        dt=t-self.lastT
        self.A[0,1]=dt
        self.x=self.A.dot(self.x)+self.B*vyaw
        self.x=self.x-self.L.dot(np.array([[yaw]])-self.C.dot(self.x))

        result=np.zeros((4,1))
        result[0:3,:]=self.x
        result[3,:]=t
        return result

def test():
    print("OK")
    i=0
    while(1):
        i+1

def run():
    boat=plant()
    L=np.array([[0.1],[0.1],[0.1]])
    sensor=observer(L)
    t = threading.Thread(target = boat.routine, args=(0.001,))
    #t = threading.Thread(target = test)
    t.start()
    #t.join()

    n=50
    real_array=np.zeros((n,4))
    esti_array=np.zeros((n,4))
    lastT=0;
    i=0
    while(i<n):
        time=boat.get_orient()[1]
        #print(time-lastT)
        if((time-lastT)>0.01):
            yaw=boat.get_orient()[0]
            vyaw=boat.get_rate()[0]
            real_array[i,:]=boat.get_real()
            esti_array[i,:]=sensor.update(yaw,vyaw,time)[:,0]
            i+=1
            lastT=time

    boat.stop()
    print(real_array)
    print(esti_array)

if __name__ == '__main__':
    run()
