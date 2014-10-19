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

from numpy import asarray, array, float64, less, where
from math import sqrt, fabs
import utilsPUC
import numpy as np


__all__ = ["orthfilter", "qmf" , "dwt_sym"]

def qmf(filter):
	filter = array(filter)[::-1]
	filter[1::2] = -filter[1::2]
	return filter

def orthfilter(scaling_filter):
	assert len (scaling_filter) % 2 ==0
	
	scaling_filter = asarray(scaling_filter, dtype = float64)
	scaling_filter = scaling_filter/sum(scaling_filter)

	Lo_R = sqrt(2) * scaling_filter
	Hi_R = qmf(Lo_R)
	Hi_D = Hi_R[::-1]
	Lo_D = Lo_R[::-1]

	return (Lo_D, Hi_D, Lo_R, Hi_R)

############################################################################################
#######################   symmetric wavelet transform    ###################################

def dwt_sym(signal, lpd, hpd):
	
	len_lpfilt=int(len(lpd))
	len_data=int(len(signal))
	lf=len_lpfilt
	lx=len_data
	D=int(2)
	lenExt = int(lf -1)
	last = lx + lf - 1

	######################## signal extension symmetrically in point of the input vector ##################### 
	signal=utilsPUC.symm_ext(signal,lenExt)
	###########################################################################################################################
	
	cA_undec=np.real(utilsPUC.convfft(signal,lpd))
	cA_undec=cA_undec[lf:]
	cA_undec=cA_undec[:len(cA_undec)-lf+1]
	cA=utilsPUC.downsamp(cA_undec,D)


	cD_undec=np.real(utilsPUC.convfft(signal,hpd))
	cD_undec=cD_undec[lf:]
	cD_undec=cD_undec[:len(cD_undec)-lf+1]
	cD=utilsPUC.downsamp(cD_undec,D)

	return cA,cD

#############################  inverse  wavelet transform   ###############################
###########################################################################################

def idwt_sym(a,d,lpr,hpr):
	if len(a) > len(d):
		a=a[0:len(d)]

	len_lpfilt=int(len(lpr))
	len_hpfilt=int(len(hpr))		
	lf=len_lpfilt
	N= 2 * len(d)
	U=2

	cA_up=utilsPUC.upsamp(a,U)
	cA_up=cA_up[0:len(cA_up)-1]
	X_lp=np.real(utilsPUC.convfft(cA_up,lpr))

	cD_up=utilsPUC.upsamp(d,U)
	cD_up=cD_up[0:len(cD_up)-1]
	X_hp=np.real(utilsPUC.convfft(cD_up,hpr))
	
	X=X_lp+X_hp
	X=X[lf-2:]
	X=X[:len(X)-lf+2]
	
	return X

def softThresholding(levelCoefficients , Threshold):
	####################### function sign of decomposition vector #################################
	Con = 0
	vecCoefficients = []
	for var in levelCoefficients:
		vecCoefficients.append(utilsPUC.sign(levelCoefficients[Con]))
		Con+=1
	##########################################################################################
	################################ subtract threshold ######################################
	VecThreshold = map (abs, levelCoefficients)
	################################## coeficients menus vector ##########################################
	############################ abs(levelCoefficients) - Threshold) #####################################
	newVecThreshold = map(lambda VecThreshold: VecThreshold - Threshold, VecThreshold) 
	############################### multiplication point to point  *######################################
	###############################  coefficients new  ##########################################
	
	newCoefficients = np.multiply (vecCoefficients, newVecThreshold)
	newCoefficientsList = map(lambda newCoefficients: newCoefficients * 1, newCoefficients)
	
	######################################################################################################
	####################################### substrat coefficients of the  sinal ##########################
	
	coefficientsOut = less(VecThreshold, Threshold)
	newCoefficientsList =  where (coefficientsOut, 0, newCoefficientsList)
	newCoefficientsListEnd = map(lambda newCoefficientsList: newCoefficientsList * 1, newCoefficientsList)
	return newCoefficientsListEnd



