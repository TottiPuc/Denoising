#!user/bin/env python
# coding: utf-8

'''
################################################
#==============================================#
##### Christian Dayan Arcos Gordillo  ##########
#####       Reconhecimento de voz      #########
#####     christian@cetuc.puc-rio.br    ########
#######       CETUC - PUC - RIO       ##########
#==============================================#
################################################

'''
import sys
import numpy as np
from math import ceil

__all__= ["symm_ext","convfft", "upsamp", "downsamp"]



def symm_ext(x,a):
    
    for i in range(a):
        l=len(x)
        pre=x[1+i*2]
        post=x[l-(i+1)*2]
        x=np.append(x,post)
        x=np.append(pre,x)
    
    return x

def convfft(a,b):
    len_c = len(a)+len(b)-1
    a=np.array(a)
    b=np.array(b)
    az=np.zeros(len_c-len(a))
    bz=np.zeros(len_c-len(b))
    a=np.append(a,az)
    b=np.append(b,bz)
   
    x=np.fft.fft(a)
    y=np.fft.fft(b)
    z=x*y
    oup=np.fft.ifft(z)
    return oup

def upsamp(inp,M):
    x = np.array(inp)
    M=int(M)
    N = M * len(x)
    y=[]
   
    for i in range(N):
        if i%M == 0:
            y.append(x[i/M])
        else:
            y.append(0.0)
   
    return y


def downsamp(inp,M):
    x=np.array(inp)
    N = int(ceil(len(x) *1.0 / M))
    y=[]
   
    for i in range(N):
        y.append(x[i*M])
   
    return y



def sign(x):
    if x > 0:
        return 1
    elif x ==0:
        return 0
    else:
        return -1
    
def detcoef(coeff, longs, levels):
    nmax = len(longs)-2
    first = np.cumsum(longs) +1 
    first = first [-3::-1]
    longs = longs[-2:0:-1]
    last = first + longs -1
    nblev = 1
    
    tmp = [[0 for row in range(1)] for col in range(nblev)]
    for i in xrange(nblev):
        k= levels
        mm=first[k]
        mm1=last[k]
        mm2=last[k]+1 
        tmp[i] = coeff[first[k]: last[k] +1]
        
    return tmp

    
