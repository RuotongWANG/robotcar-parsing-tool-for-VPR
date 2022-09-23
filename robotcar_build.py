# -*- coding: utf-8 -*-
"""
Created on Sat Oct  9 08:57:46 2021

@author: 24379
"""
from os import walk
from os.path import join
import numpy as np

def quaternion_to_rotation_matrix(qvec):
    qvec = qvec / np.linalg.norm(qvec)
    w, x, y, z = qvec
    R = np.array([
        [1 - 2 * y * y - 2 * z * z, 2 * x * y - 2 * z * w, 2 * x * z + 2 * y * w],
        [2 * x * y + 2 * z * w, 1 - 2 * x * x - 2 * z * z, 2 * y * z - 2 * x * w],
        [2 * x * z - 2 * y * w, 2 * y * z + 2 * x * w, 1 - 2 * x * x - 2 * y * y]])
    return R

def camera_center_to_translation(c, qvec):
    R = quaternion_to_rotation_matrix(qvec)
    return (-1) * np.matmul(R, c)

def build_dataset():
    image_data = []
    with  open(nvm_path, 'r') as nvm_f:
        line = nvm_f.readline()
        while line == '\n' or line.startswith('NVM_V3'):
            line = nvm_f.readline()
        num_images = int(line)
        print('num_images: ', num_images)
        
        i = 0
        while i < num_images:
            line = nvm_f.readline()
            if line == '\n':
                continue
            data = line.strip('\n').split(' ')
            image_data.append(data)
            i += 1
    with open('database.txt', 'w') as f:
        for data in image_data:
            # Skip the focal length. Skip the distortion and terminal 0.
            name, _, qw, qx, qy, qz, cx, cy, cz, _, _ = data
            qvec = np.array([qw, qx, qy, qz], float)
            c = np.array([cx, cy, cz], float)
            t = camera_center_to_translation(c, qvec)
            
            line = list(map(str, [join('images',name[2:-3]+'jpg'), qw, qx, qy, qz]+list(t)))
            f.writelines(' '.join(line))
            f.write('\n') 

def build_query_test():
    queries = []
    conds = {}
    with open(qFile_test, 'r') as f:
        data = f.read()
        ims = data.split('\n')
        for im in ims:
            im = im.split('/')[-1][:-3]+'jpg'
            
            for root,dirs,files in walk('images/'):
                if im in files and root.split('/')[-1]=='rear':
                    queries.append(join('images', root.split('/')[-2], 'rear', im))
                    cond = root.split('/')[-2]
                    if cond in conds: 
                        conds[cond] += 1
                    else: conds[cond] = 1
                    
    with open('queries.txt', 'w') as f:
        for data in queries:
            f.writelines(data)
            f.write('\n') 
    print('Test: ', conds)
            
def build_query_train():
    queries = []
    conds = {}
    with open(qFile_train, 'r') as f:
        data = f.read()
        ims = data.strip('\n').split('\n')
        for im in ims:
            im = im.split(' ')[0]
            cond = im.split('/')[0]
            if cond in conds: 
                conds[cond] += 1
            else: conds[cond] = 1
            queries.append(join('images', im))
                    
    with open('train_queries.txt', 'w') as f:
        for data in queries:
            f.writelines(data)
            f.write('\n') 
    print('Train: ', conds)
            
if __name__ == '__main__':
    nvm_path = '3D-models/all-merged/all.nvm'
    qFile_test = 'robotcar_v2_test.txt'
    qFile_train = 'robotcar_v2_train.txt'
    build_query_test()
    build_query_train()
    
    
    
    
    
    
    
    
    
    
    
    
                
                
                        
                        
                        
                        
                        
                        
                        
                        
                        
                        