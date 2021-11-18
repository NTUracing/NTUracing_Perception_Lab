import common_axis as ca
import numpy as np
import matplotlib.pyplot as plt

n=1000
'''
def generate_test_data(m):
    test_arr=np.zeros((m,2,3))
    v1=np.array([0,0,1])
    v2=np.array([0,1,0])
    for i in range(0,m):
        test_arr[i,0,:]=v1
        test_arr[i,1,:]=v2
    return test_arr
'''
def generate_test_data(m):
    test_arr=np.random.randn(m,2,3)
    return test_arr

def run():
    vec_pair_array=np.zeros((n,2,3))
    common_axis_array_SVD=np.zeros((n,3))
    common_axis_array_crs=np.zeros((n,3))
    acc_array_SVD=np.array((n,2))
    acc_array_crs=np.array((n,2))

    vec_pair_array=generate_test_data(n)
    #print(vec_pair_array)

    common_axis_array_SVD=ca.find_common_axis_SVD(vec_pair_array)
    common_axis_array_crs=ca.find_common_axis_crs(vec_pair_array)
    #print(common_axis_array_SVD)
    #print(common_axis_array_crs)

    acc_array_SVD=ca.get_ca_accuracy(vec_pair_array,common_axis_array_SVD)
    acc_array_crs=ca.get_ca_accuracy(vec_pair_array,common_axis_array_crs)

    array_svd=sorted(acc_array_SVD.tolist(), key=lambda t: t[1])
    array_crs=sorted(acc_array_crs.tolist(), key=lambda t: t[1])
    plt.title("Normal Vector Error vs Dot Product") # title
    plt.ylabel("Normal Vector Error") # y label
    plt.xlabel("Dot Product") # x label
    plt.plot(np.array(array_svd)[:,1],np.array(array_svd)[:,0],color=(255/255,100/255,100/255))
    plt.plot(np.array(array_crs)[:,1],np.array(array_crs)[:,0],'--',color=(100/255,100/255,255/255))
    plt.show()

if __name__ == '__main__': 
    run()
