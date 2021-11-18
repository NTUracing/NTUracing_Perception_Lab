import numpy as np

def find_common_axis_SVD(vec_pair_array):
    u, s, vh = np.linalg.svd(vec_pair_array, full_matrices=True)
    return vh[:,-1,:]/np.linalg.norm(vh[:,-1,:],axis=-1)[:,None]

def find_common_axis_crs(vec_pair_array):
    crs=np.cross(vec_pair_array[:,0,:],vec_pair_array[:,1,:],-1,-1)
    return crs/np.linalg.norm(crs,axis=-1)[:,None]

def get_ca_accuracy(vec_pair_array,common_axis_array):
    result=np.zeros((vec_pair_array.shape[0],2))
    result[:,0]=0.5*(np.diag(vec_pair_array[:,0,:].dot(common_axis_array.transpose()))/np.linalg.norm(vec_pair_array[:,0,:],axis=-1)+np.diag(vec_pair_array[:,1,:].dot(common_axis_array.transpose()))/np.linalg.norm(vec_pair_array[:,1,:],axis=-1))

    f= vec_pair_array[:,0,:]/np.linalg.norm(vec_pair_array[:,0,:],axis=-1)[:,None]
    g= vec_pair_array[:,1,:]/np.linalg.norm(vec_pair_array[:,1,:],axis=-1)[:,None]
    result[:,1]=np.diag(f.dot(g.transpose()))
    return result
