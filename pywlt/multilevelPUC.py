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
import WaveletFiltersPUC
import functionPUC
import utilsPUC
from pywt import dwt, idwt, dwt_max_level



__all__ = ['wavedec', 'waverec']

def wavedec1(data, wavelet, mode ='sym', level =None ):

####################################################################################################impor######################
# multilevel 1D wavelet transform returns a list of coefficients according to the decomposition [cAn, cDn, cDn-1, ..., cD2, cD1]
###############################################################################################################################

#############################   checking levels of the transform    ##################################
######################################################################################################
	if level < 0:
		raise ValueError ( "valor do nivel %d esta fora da faixa. O  menor nivel e 0.  " % level)

###########  extracting orthogonal Daubechies Filters according to the degree of function ############
######################################################################################################
	
	(Lo_D, Hi_D) = WaveletFiltersPUC.NumberFilter(wavelet)
	

	(lpd, hpd) = WaveletFiltersPUC.FiltersList(wavelet)
######################################################################################################
##############################     perfect here   ####################################################
	
	lDes = [0]*(level+2)
	
	coeffs_list = []
	
	s = len (data)
	
	lDes[-1] = int(s) 
	
	for i in xrange (level): 
		data,d = functionPUC.dwt_sym(data, lpd, hpd)
		coeffs_list.extend(d)
		lDes [level - i]= int(len(d)) 
		

	lDes[0] = int(len(data))

	coeffs_list.extend(data)

	return coeffs_list, lDes

def waverec1 (coefficientsArray,  levelLimitArray, wavelet ):
	
	rmax = len(levelLimitArray)
	nmax = rmax -2
	
######## substract Daubachies ortogonal filters according to the degree of the function #############
######################################################################################################
	
	(Lo_R, Hi_R) = WaveletFiltersPUC.NumberFilter(wavelet)
	

	(lpr, hpr) = WaveletFiltersPUC.FiltersList(wavelet)

########################################################################################################

	a = coefficientsArray[0 : levelLimitArray[0]]
	
	p = range (0,nmax)
	for i in p [-1::-1]:
		d = utilsPUC.detcoef(coefficientsArray, levelLimitArray, i) #coefficients de detalles
		a = functionPUC.idwt_sym(a, d[0], lpr, hpr)
	return d
		
		

def waverec(coeffs, wavelet, mode='sym'):

		if not isinstance(coeffs, (list, tuple)):
			raise ValueError("Expected sequence of coefficient arrays.")

		if len(coeffs) < 2:
			raise ValueError( "Coefficient list too short (minimum 2 arrays required).")

		a, ds = coeffs[0], coeffs[1:]

		for d in ds:
			a = idwt(a, d, wavelet, mode, 1)

		return a


	
def wavedec(data, wavelet, mode='sym', level=None):

	if level is None:
		level = dwt_max_level(len(data), wavelet.dec_len)
	elif level < 0:
			raise ValueError( "Level value of %d is too low . Minimum level is 0." % level)

	coeffs_list = []

	a = data
	for i in xrange(level):
		a, d = dwt(a, wavelet, mode)
		coeffs_list.append(d)

	coeffs_list.append(a)
	coeffs_list.reverse()

	return coeffs_list
